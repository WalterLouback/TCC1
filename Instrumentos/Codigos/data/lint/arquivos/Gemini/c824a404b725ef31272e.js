/**
 * Finalizes the ESM resolution process.
 * Checks for encoded path separators in the resolved path and attempts to resolve the file.
 *
 * @param {string} resolved The resolved module specifier.
 * @param {string} parentPath The parent path of the module.
 * @param {string} pkgPath The package path.
 * @returns {string} The resolved file path if found.
 * @throws {ERR_INVALID_MODULE_SPECIFIER} If the resolved path includes encoded '/' or '\' characters.
 * @throws {Error} If the module cannot be found.
 */
function finalizeEsmResolution(resolved, parentPath, pkgPath) {
  const { encodedSepRegEx } = require('internal/modules/esm/resolve');
  if (RegExpPrototypeExec(encodedSepRegEx, resolved) !== null) {
    throw new ERR_INVALID_MODULE_SPECIFIER(
      resolved, 'must not include encoded "/" or "\\" characters', parentPath);
  }
  const filename = fileURLToPath(resolved);
  const actual = tryFile(filename);
  if (actual) {
    return actual;
  }
  throw createEsmNotFoundErr(filename, pkgPath);
}
