/**
 * Recursively fills an encoding "fence" by placing characters onto rails.
 * If there are no remaining characters, returns the current fence.
 *
 * @param {Object} params
 * @param {Array<Array<string>>} params.fence - The current fence structure (array of rails).
 * @param {number} params.currentRail - The index of the rail where the next character will be placed.
 * @param {number} params.direction - The current direction used to determine the next rail.
 * @param {Array<string>} params.chars - The remaining characters to place.
 * @returns {Array<Array<string>>} The updated fence after all characters have been placed.
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
