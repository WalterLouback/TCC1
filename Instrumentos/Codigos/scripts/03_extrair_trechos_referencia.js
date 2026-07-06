const fs = require("fs");
const path = require("path");
const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;

const BASE = path.resolve(__dirname, "..");
const REPOS_FILE = path.join(BASE, "data", "repos", "repos_encontrados.json");
const CLONES_DIR = path.join(BASE, "data", "repos", "clones");
const OUT_FILE = path.join(BASE, "data", "dataset", "trechos_com_referencia.json");

fs.mkdirSync(path.dirname(OUT_FILE), { recursive: true });

const repos = JSON.parse(fs.readFileSync(REPOS_FILE, "utf8"));
const repoMap = new Map(
  repos.map((r) => [r.full_name.replace("/", "__"), r])
);

const SKIP_DIRS = new Set([
  "node_modules", ".git", "dist", "build", "coverage", "vendor", "docs", "doc", "storybook-static"
]);

function walk(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name)) continue;
      walk(full, files);
    } else if (
      /\.(js|cjs|mjs|jsx)$/.test(entry.name) &&
      !entry.name.endsWith(".min.js") &&
      !entry.name.endsWith(".bundle.js") &&
      !entry.name.endsWith(".spec.js") &&
      !entry.name.endsWith(".test.js")
    ) {
      files.push(full);
    }
  }
  return files;
}

function parseCode(code) {
  return parser.parse(code, {
    sourceType: "unambiguous",
    allowReturnOutsideFunction: true,
    errorRecovery: true,
    attachComment: true,
    plugins: [
      "jsx",
      "classProperties",
      "classPrivateProperties",
      "classPrivateMethods",
      "optionalChaining",
      "nullishCoalescingOperator",
      "objectRestSpread",
      "dynamicImport",
      "topLevelAwait"
    ]
  });
}

function getAdjacentJsDoc(commentHolderNode, declNode, code) {
  const comments = commentHolderNode.leadingComments || [];
  if (!comments.length) return null;

  const c = comments[comments.length - 1];
  const raw = code.slice(c.start, c.end);

  if (c.type !== "CommentBlock") return null;
  if (!raw.startsWith("/**")) return null;

  const between = code.slice(c.end, declNode.start);
  if (!/^\s*$/.test(between)) return null;

  return {
    raw,
    start: c.start,
    end: c.end,
    startLine: c.loc?.start?.line || null,
    endLine: c.loc?.end?.line || null
  };
}

function cleanName(name) {
  return (name || "").trim();
}

function codeLoc(code) {
  return code.split(/\r?\n/).filter((l) => l.trim()).length;
}

function hasUsefulJsDoc(doc) {
  if (!doc) return false;
  const hasParam = /@param\b/.test(doc);
  const hasReturns = /@returns?\b/.test(doc);
  const hasDesc = /\/\*\*[\s\S]*?[A-Za-zÀ-ÿ]{4,}/.test(doc);
  return hasDesc && (hasParam || hasReturns);
}

function buildId(repoName, relFile, line, type, name) {
  const base = `${repoName}|${relFile}|${line}|${type}|${name}`;
  return Buffer.from(base).toString("base64").replace(/=+$/g, "");
}

function pushRecord(out, ctx, code) {
  const {
    repoMeta, repoDirName, filePath, nodeForCode, nodeForName, jsdocHolder, type
  } = ctx;

  const jsdoc = getAdjacentJsDoc(jsdocHolder, nodeForCode, code);
  if (!jsdoc) return;
  if (!hasUsefulJsDoc(jsdoc.raw)) return;

  const snippetCode = code.slice(nodeForCode.start, nodeForCode.end);
  const loc = codeLoc(snippetCode);
  if (loc < 3 || loc > 80) return;

  let name = "";
  if (type === "class") {
    name = cleanName(nodeForName.id?.name);
  } else if (nodeForName.id?.name) {
    name = cleanName(nodeForName.id.name);
  } else if (nodeForName.key?.name) {
    name = cleanName(nodeForName.key.name);
  } else if (nodeForName.name) {
    name = cleanName(nodeForName.name);
  }

  if (!name) return;

  const relFile = path.relative(path.join(CLONES_DIR, repoDirName), filePath).replace(/\\/g, "/");
  const id = buildId(repoMeta.full_name, relFile, nodeForCode.loc.start.line, type, name);

  out.push({
    id_trecho: id,
    repo: repoMeta.full_name,
    repo_dir: repoDirName,
    stars: repoMeta.stargazers_count,
    arquivo: relFile,
    tipo: type,
    nome: name,
    linha_inicio: nodeForCode.loc.start.line,
    linha_fim: nodeForCode.loc.end.line,
    loc,
    codigo: snippetCode,
    documentacao_referencia: jsdoc.raw,
    repo_created_at: repoMeta.created_at,
    repo_pushed_at: repoMeta.pushed_at
  });
}

function processFile(repoMeta, repoDirName, filePath, out, seen) {
  const code = fs.readFileSync(filePath, "utf8");
  let ast;

  try {
    ast = parseCode(code);
  } catch {
    return;
  }

  function register(key, fn) {
    if (seen.has(key)) return;
    seen.add(key);
    fn();
  }

  traverse(ast, {
    noScope: true,

    FunctionDeclaration(pathRef) {
      const node = pathRef.node;
      const key = `${filePath}:${node.start}:function`;
      register(key, () => {
        pushRecord(out, {
          repoMeta, repoDirName, filePath,
          nodeForCode: node,
          nodeForName: node,
          jsdocHolder: node,
          type: "function"
        }, code);
      });
    },

    ClassDeclaration(pathRef) {
      const node = pathRef.node;
      const key = `${filePath}:${node.start}:class`;
      register(key, () => {
        pushRecord(out, {
          repoMeta, repoDirName, filePath,
          nodeForCode: node,
          nodeForName: node,
          jsdocHolder: node,
          type: "class"
        }, code);
      });
    },

    VariableDeclaration(pathRef) {
      const declNode = pathRef.node;
      const holder = declNode;

      for (const d of declNode.declarations || []) {
        const initType = d.init?.type;
        const isFunctionExpr = initType === "ArrowFunctionExpression" || initType === "FunctionExpression";
        if (!isFunctionExpr) continue;

        const key = `${filePath}:${declNode.start}:function:${d.id?.name || ""}`;
        register(key, () => {
          pushRecord(out, {
            repoMeta, repoDirName, filePath,
            nodeForCode: declNode,
            nodeForName: d,
            jsdocHolder: holder,
            type: "function"
          }, code);
        });
      }
    },

    ExportNamedDeclaration(pathRef) {
      const exportNode = pathRef.node;
      const decl = exportNode.declaration;
      if (!decl) return;

      if (decl.type === "FunctionDeclaration") {
        const key = `${filePath}:${exportNode.start}:function:export`;
        register(key, () => {
          pushRecord(out, {
            repoMeta, repoDirName, filePath,
            nodeForCode: exportNode,
            nodeForName: decl,
            jsdocHolder: exportNode,
            type: "function"
          }, code);
        });
      }

      if (decl.type === "ClassDeclaration") {
        const key = `${filePath}:${exportNode.start}:class:export`;
        register(key, () => {
          pushRecord(out, {
            repoMeta, repoDirName, filePath,
            nodeForCode: exportNode,
            nodeForName: decl,
            jsdocHolder: exportNode,
            type: "class"
          }, code);
        });
      }

      if (decl.type === "VariableDeclaration") {
        for (const d of decl.declarations || []) {
          const initType = d.init?.type;
          const isFunctionExpr = initType === "ArrowFunctionExpression" || initType === "FunctionExpression";
          if (!isFunctionExpr) continue;

          const key = `${filePath}:${exportNode.start}:function:${d.id?.name || ""}:export`;
          register(key, () => {
            pushRecord(out, {
              repoMeta, repoDirName, filePath,
              nodeForCode: exportNode,
              nodeForName: d,
              jsdocHolder: exportNode,
              type: "function"
            }, code);
          });
        }
      }
    }
  });
}

const out = [];
const seen = new Set();

for (const repoDirName of fs.readdirSync(CLONES_DIR)) {
  const repoPath = path.join(CLONES_DIR, repoDirName);
  if (!fs.statSync(repoPath).isDirectory()) continue;

  const repoMeta = repoMap.get(repoDirName);
  if (!repoMeta) continue;

  const files = walk(repoPath);
  for (const filePath of files) {
    processFile(repoMeta, repoDirName, filePath, out, seen);
  }
}

fs.writeFileSync(OUT_FILE, JSON.stringify(out, null, 2), "utf8");
console.log(`${out.length} trechos salvos em ${OUT_FILE}`);