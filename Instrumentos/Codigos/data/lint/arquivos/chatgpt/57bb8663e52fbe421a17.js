/**
 * Creates a metadata extractor function for a given set of languages.
 *
 * The returned function derives language-related metadata from a node by:
 * - Resolving the language name from the node.
 * - Parsing node.meta (or an empty string) into a metadata structure.
 * - Extracting the "title" meta value (or returning null if missing).
 * - Looking up a language string literal from the provided languages map.
 * - Collecting meta ranges for highlighted, inserted, and deleted sections.
 * - Collecting foldable section boundaries for collapsed sections.
 *
 * @param {Object<string, string>} languages - Map from language name to a language string literal.
 * @returns {(node: any) => {
 *   languageName: any,
 *   title: (string|null),
 *   languageStringLiteral: string,
 *   highlightedLines: any,
 *   insertedLines: any,
 *   deletedLines: any,
 *   foldedSections: any
 * }} A function that extracts metadata from a node.
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
