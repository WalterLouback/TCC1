/**
 * Builds attribute objects for a code block based on provided metadata and a code highlighter.
 *
 * Creates:
 * - `codeAttributes` with Prism-compatible language classes and translation disabled.
 * - `preAttributes` optionally containing language string literal, title, and a preview flag for Prism.
 *
 * @param {Object} metadata
 * @param {string} metadata.languageName - Language name used to build the `language-<name>` CSS class.
 * @param {string} [metadata.title] - Optional title to be set as `data-code-title`.
 * @param {string} [metadata.languageStringLiteral] - Optional language string literal to be set as `data-code-language`.
 * @param {Function|Object} codeHighlighter - Highlighter reference; its `name` is used to detect Prism.
 * @returns {{ preAttributes: Object, codeAttributes: Object }} An object containing `preAttributes` and `codeAttributes`.
 */
const createAttributes = (metadata, codeHighlighter) => {
  const { languageName, title, languageStringLiteral } = metadata;

  // Note: While something classless, such as `[data-code-grammar=languageName]`
  // would be nicer to look at, Prism uses the same language-X classes to target
  // nested styles. This is also the HTML5 spec suggestion for higlighting code.
  // By using a class for this plugin, consistence and compliance are ensured.
  const codeAttributes = {
    class: `language-${languageName} notranslate`,
    translate: `no`,
  };
  const preAttributes = {};

  if (languageStringLiteral)
    preAttributes[`data-code-language`] = languageStringLiteral;

  if (title) preAttributes[`data-code-title`] = title;

  if (codeHighlighter.name === 'prism')
    preAttributes[`data-code-preview`] = true;

  return { preAttributes, codeAttributes };
};
