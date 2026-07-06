/**
 * Asserts that the provided body is a valid BufferSource or a string if allowed.
 *
 * @param {any} body The value to assert.
 * @param {boolean} allowString Whether to allow strings as valid input.
 * @param {string} hookName The name of the hook where the assertion is performed.
 * @throws {ERR_INVALID_RETURN_PROPERTY_VALUE} If the body is not a valid BufferSource or string (if allowed).
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
