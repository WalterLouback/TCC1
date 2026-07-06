/**
 * Finalizes ESM resolution by validating the resolved specifier, converting it to a
 * filesystem path, attempting to resolve an existing file, and throwing an error
 * when the module cannot be found.
 *
 * @param {string} resolved - The resolved ESM specifier/path to validate and convert.
 * @param {string} parentPath - The parent path used for error context.
 * @param {string} pkgPath - The package path used to create the "not found" error.
 * @returns {*} The resolved file path/value returned by {@link tryFile} when found.
 * @throws {ERR_INVALID_MODULE_SPECIFIER} If {@link resolved} contains encoded "/" or "\\" characters.
 * @throws {*} Throws the error created by {@link createEsmNotFoundErr} when the file cannot be resolved.
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
