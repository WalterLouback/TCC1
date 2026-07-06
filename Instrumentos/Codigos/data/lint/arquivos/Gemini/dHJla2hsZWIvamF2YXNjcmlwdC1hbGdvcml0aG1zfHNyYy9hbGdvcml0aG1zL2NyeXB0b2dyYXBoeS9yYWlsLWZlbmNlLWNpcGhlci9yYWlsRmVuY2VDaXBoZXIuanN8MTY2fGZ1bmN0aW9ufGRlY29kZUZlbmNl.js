/**
 * Decodes a string encoded using a fence cipher.
 *
 * @param {object} params - The parameters for decoding.
 * @param {number} params.strLen - The original length of the string.
 * @param {string[][]} params.fence - The current state of the fence.
 * @param {number} params.currentRail - The current rail being processed.
 * @param {number} params.direction - The current direction of movement (1 for down, -1 for up).
 * @param {string[]} params.code - The array of characters decoded so far.
 * @returns {string} The decoded string.
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
