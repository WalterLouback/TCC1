/**
 * Creates attributes for code and pre elements based on metadata and code highlighter.
 *
 * @param {object} metadata - An object containing metadata for the code.
 * @param {string} metadata.languageName - The name of the programming language.
 * @param {string} [metadata.title] - An optional title for the code block.
 * @param {string} [metadata.languageStringLiteral] - An optional string literal representing the language.
 * @param {object} codeHighlighter - An object representing the code highlighter.
 * @param {string} codeHighlighter.name - The name of the code highlighter.
 * @returns {object} An object containing attributes for pre and code elements.
 * @returns {object} return.preAttributes - Attributes for the pre element.
 * @returns {object} return.codeAttributes - Attributes for the code element.
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
