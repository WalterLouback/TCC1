/**
 * Decodes a string by traversing a set of rails (fence) and accumulating characters
 * until the target length is reached.
 *
 * The function is recursive: at each step it appends the current rail's first character
 * to the output, advances the rail index/direction using `getNextDirection`, updates
 * the current rail by removing the consumed character, and continues until
 * `code.length === strLen`.
 *
 * @param {Object} params - Input parameters for the decoder.
 * @param {number} params.strLen - Target length of the decoded output.
 * @param {Array<Array<string>>} params.fence - Rail fence structure; each rail is an array of characters.
 * @param {number} params.currentRail - Index of the currently active rail.
 * @param {*} params.direction - Current traversal direction (type depends on `getNextDirection`).
 * @param {Array<string>} params.code - Accumulated decoded characters so far.
 * @returns {string} The decoded string once `code` reaches `strLen`.
 */
const decodeFence = (params) => {
  const {
    strLen,
    fence,
    currentRail,
    direction,
    code,
  } = params;

  if (code.length === strLen) {
    return code.join('');
  }

  const railCount = fence.length;

  const [currentChar, ...nextRail] = fence[currentRail];
  const nextDirection = getNextDirection(
    { railCount, currentRail, direction },
  );

  return decodeFence({
    railCount,
    strLen,
    currentRail: currentRail + nextDirection,
    direction: nextDirection,
    code: [...code, currentChar],
    fence: fence.map((rail, idx) => (idx === currentRail ? nextRail : rail)),
  });
};
