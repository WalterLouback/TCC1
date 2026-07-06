/**
 * Recursively fills the encode fence with characters.
 *
 * @param {Array<Array<string>>} fence - The current state of the fence.
 * @param {number} currentRail - The index of the current rail being filled.
 * @param {number} direction - The current direction of movement (1 for down, -1 for up).
 * @param {Array<string>} chars - The remaining characters to be placed.
 * @returns {Array<Array<string>>} The completed fence.
 */
const fillEncodeFence = ({
  fence,
  currentRail,
  direction,
  chars,
}) => {
  if (chars.length === 0) {
    // All chars have been placed on a fence.
    return fence;
  }

  const railCount = fence.length;

  // Getting the next character to place on a fence.
  const [letter, ...nextChars] = chars;
  const nextDirection = getNextDirection({
    railCount,
    currentRail,
    direction,
  });

  return fillEncodeFence({
    fence: fence.map(addCharToRail(currentRail, letter)),
    currentRail: currentRail + nextDirection,
    direction: nextDirection,
    chars: nextChars,
  });
};
