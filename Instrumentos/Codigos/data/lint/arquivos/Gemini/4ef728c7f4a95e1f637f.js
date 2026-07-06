/**
 * Creates a metadata extractor function for a given set of languages.
 *
 * @param {object} languages - An object mapping language names to their string literals.
 * @param {function(object): string} languages.languageName - The name of the language.
 * @param {function(object): object} node - The node to extract metadata from.
 * @returns {object} An object containing extracted metadata.
 * @returns {string} return.languageName - The name of the language of the node.
 * @returns {string|null} return.title - The title of the node, or null if not found.
 * @returns {string} return.languageStringLiteral - The string literal for the node's language.
 * @returns {Array<object>} return.highlightedLines - An array of objects representing highlighted lines.
 * @returns {Array<object>} return.insertedLines - An array of objects representing inserted lines.
 * @returns {Array<object>} return.deletedLines - An array of objects representing deleted lines.
 * @returns {Array<object>} return.foldedSections - An array of objects representing folded sections.
 */
const createMetadataExtractor = languages => node => {
  const languageName = getLanguageName(node);
  const meta = parseMeta(node.meta || '');
  const title = getMetaString(meta, 'title')?.value || null;
  const languageStringLiteral = languages[languageName] || '';
  const highlightedLines = getMetaRanges(meta, null);
  const insertedLines = getMetaRanges(meta, 'ins');
  const deletedLines = getMetaRanges(meta, 'del');
  const foldedSections = getMetaRangeBoundaries(meta, 'collapse');

  return {
    languageName,
    title,
    languageStringLiteral,
    highlightedLines,
    insertedLines,
    deletedLines,
    foldedSections,
  };
};
