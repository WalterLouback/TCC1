/**
 * Merges extra segments into a context until the number of segments is less than or equal to the context count.
 *
 * @param {object} context - The context object containing idGenerator and count.
 * @param {object} context.idGenerator - An object with a next() method to generate IDs.
 * @param {number} context.count - The maximum number of segments allowed.
 * @param {Array<object>} segments - An array of segments to be merged.
 * @returns {Array<object>} The array of merged segments.
 */
function mergeExtraSegments(context, segments) {
  let currentSegments = segments;

  while (currentSegments.length > context.count) {
    const merged = [];

    for (
      let i = 0, length = (currentSegments.length / 2) | 0;
      i < length;
      ++i
    ) {
      merged.push(
        CodePathSegment.newNext(context.idGenerator.next(), [
          currentSegments[i],
          currentSegments[i + length],
        ]),
      );
    }
    currentSegments = merged;
  }
  return currentSegments;
}
