/**
 * Validates that a return value is a valid buffer-like source.
 * Accepts either a string (only when `allowString` is true) or an ArrayBuffer/typed array.
 * Throws an error when `body` is not a supported type.
 *
 * @param {*} body - The value to validate as the `source` return property.
 * @param {boolean} allowString - Whether a string value is allowed.
 * @param {string} hookName - Name of the hook used to construct the error context.
 * @throws {ERR_INVALID_RETURN_PROPERTY_VALUE} If `body` is not an allowed string (when enabled) and not an ArrayBuffer or typed array.
 */
function assertBufferSource(body, allowString, hookName) {
  if (allowString && typeof body === 'string') {
    return;
  }
  const { isArrayBufferView, isAnyArrayBuffer } = lazyTypes();
  if (isArrayBufferView(body) || isAnyArrayBuffer(body)) {
    return;
  }
  throw new ERR_INVALID_RETURN_PROPERTY_VALUE(
    `${allowString ? 'string, ' : ''}array buffer, or typed array`,
    hookName,
    'source',
    body,
  );
}
