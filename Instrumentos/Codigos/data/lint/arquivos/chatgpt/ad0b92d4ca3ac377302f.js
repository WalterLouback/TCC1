/**
 * Merges an array of CodePathSegment objects by repeatedly combining the first half
 * with the second half until the number of segments is reduced to `context.count`.
 *
 * At each iteration, it creates a new array where each element is produced by
 * `CodePathSegment.newNext(nextId, [leftSegment, rightSegment])`, using a fresh id
 * from `context.idGenerator.next()`.
 *
 * @param {Object} context - Execution context containing the target segment count and an id generator.
 * @param {number} context.count - Target number of segments to stop merging at.
 * @param {Object} context.idGenerator - Id generator used to create ids for merged segments.
 * @param {Function} context.idGenerator.next - Returns the next id value.
 * @param {Array<any>} segments - Initial list of segments to be merged.
 * @returns {Array<any>} The merged segments array with length equal to `context.count` (or less if input is not compatible).
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
