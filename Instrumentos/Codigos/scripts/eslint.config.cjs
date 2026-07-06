const jsdoc = require("eslint-plugin-jsdoc");

module.exports = [
  {
    files: ["data/lint/arquivos/**/*.js"],
    plugins: {
      jsdoc
    },
    rules: {
      "jsdoc/check-alignment": "error",
      "jsdoc/check-indentation": "error",
      "jsdoc/check-param-names": "error",
      "jsdoc/check-tag-names": "error",
      "jsdoc/require-description": "error",
      "jsdoc/require-param": "error",
      "jsdoc/require-param-description": "error",
      "jsdoc/require-returns": "error",
      "jsdoc/require-returns-description": "error"
    }
  }
];