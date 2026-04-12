const fs = require("fs");
const path = require("path");
const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;

const BASE_DIR = path.resolve(__dirname, "..");
const REPOS_DIR = path.join(BASE_DIR, "data", "repos");
const OUT_DIR = path.join(BASE_DIR, "data", "trechos");

if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

const EXTENSOES = new Set([".js", ".jsx", ".mjs", ".cjs"]);
const IGNORAR_DIRS = new Set([
  "node_modules", ".git", "dist", "build", "coverage",
  ".next", ".nuxt", "vendor", "tmp", "temp"
]);

function ignorarCaminho(filePath) {
  const partes = filePath.split(path.sep);
  if (partes.some(p => IGNORAR_DIRS.has(p))) return true;
  if (filePath.endsWith(".min.js")) return true;
  return false;
}

function listarArquivos(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (ignorarCaminho(full)) continue;

    if (entry.isDirectory()) {
      listarArquivos(full, files);
    } else {
      const ext = path.extname(entry.name).toLowerCase();
      if (EXTENSOES.has(ext)) files.push(full);
    }
  }
  return files;
}

function parseSeguro(code) {
  try {
    return parser.parse(code, {
      sourceType: "unambiguous",
      plugins: [
        "jsx",
        "classProperties",
        "objectRestSpread",
        "optionalChaining",
        "dynamicImport"
      ]
    });
  } catch {
    return null;
  }
}

function criarTrecho(repoName, relativePath, tipo, nome, node, code) {
  if (!node || !node.loc) return null;

  return {
    repo: repoName,
    arquivo: relativePath,
    tipo,
    nome: nome || "Anonymous",
    linha_inicio: node.loc.start.line,
    linha_fim: node.loc.end.line,
    loc: node.loc.end.line - node.loc.start.line + 1,
    codigo: code.slice(node.start, node.end)
  };
}

function extrairDeArquivo(repoName, repoRoot, filePath) {
  const code = fs.readFileSync(filePath, "utf8");
  const ast = parseSeguro(code);
  if (!ast) return [];

  const relativePath = path.relative(repoRoot, filePath).replaceAll("\\", "/");
  const trechos = [];
  const vistos = new Set();

  function adicionar(item) {
    if (!item) return;
    const chave = `${item.arquivo}::${item.tipo}::${item.nome}::${item.linha_inicio}`;
    if (vistos.has(chave)) return;
    vistos.add(chave);
    trechos.push(item);
  }

  traverse(ast, {
    FunctionDeclaration(p) {
      const n = p.node;
      adicionar(criarTrecho(repoName, relativePath, "function", n.id?.name, n, code));
    },

    ClassDeclaration(p) {
      const n = p.node;
      adicionar(criarTrecho(repoName, relativePath, "class", n.id?.name, n, code));
    },

    VariableDeclarator(p) {
      const n = p.node;
      if (!n.id || !n.init || !n.loc) return;

      if (
        n.init.type === "ArrowFunctionExpression" ||
        n.init.type === "FunctionExpression"
      ) {
        adicionar(criarTrecho(repoName, relativePath, "function", n.id.name, n, code));
      }

      if (n.init.type === "ClassExpression") {
        adicionar(criarTrecho(repoName, relativePath, "class", n.id.name, n, code));
      }
    },

    ExportDefaultDeclaration(p) {
      const decl = p.node.declaration;
      if (!decl) return;

      if (decl.type === "ClassDeclaration" || decl.type === "ClassExpression") {
        adicionar(
          criarTrecho(
            repoName,
            relativePath,
            "class",
            decl.id?.name || "DefaultExportClass",
            decl,
            code
          )
        );
      }

      if (decl.type === "FunctionDeclaration" || decl.type === "FunctionExpression") {
        adicionar(
          criarTrecho(
            repoName,
            relativePath,
            "function",
            decl.id?.name || "DefaultExportFunction",
            decl,
            code
          )
        );
      }
    }
  });

  return trechos;
}

function main() {
  const repos = fs.readdirSync(REPOS_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);

  const todos = [];

  for (const repo of repos) {
    const repoRoot = path.join(REPOS_DIR, repo);
    const arquivos = listarArquivos(repoRoot);
    const trechosRepo = [];

    for (const arquivo of arquivos) {
      try {
        const extraidos = extrairDeArquivo(repo, repoRoot, arquivo);
        trechosRepo.push(...extraidos);
      } catch (err) {
        console.error(`[ERRO] ${repo} :: ${arquivo} :: ${err.message}`);
      }
    }

    const arquivoSaida = path.join(OUT_DIR, `${repo}.json`);
    fs.writeFileSync(arquivoSaida, JSON.stringify(trechosRepo, null, 2), "utf8");
    todos.push(...trechosRepo);
    console.log(`[OK] ${repo}: ${trechosRepo.length} trechos`);
  }

  fs.writeFileSync(
    path.join(OUT_DIR, "todos_os_trechos.json"),
    JSON.stringify(todos, null, 2),
    "utf8"
  );

  console.log(`[TOTAL] ${todos.length} trechos extraídos`);
}

main();