/**
 * Builds an array of segment objects by collecting per-index items from a
 * 2D-like structure in `context.segmentsList` across a normalized range,
 * then passing them to a provided factory function.
 *
 * The `begin` and `end` parameters are normalized: if a value is negative,
 * it is treated as an offset from `context.segmentsList.length`.
 *
 * For each index `i` from `0` to `context.count - 1`, it collects
 * `list[j][i]` for all `j` in the inclusive range `[normalizedBegin, normalizedEnd]`,
 * and calls `create(context.idGenerator.next(), allPrevSegments)`.
 *
 * @param {Object} context
 * @param {Array} context.segmentsList A list where each element is indexable by `i` (i.e., `list[j][i]`).
 * @param {number} context.count Number of segments to create (drives the outer loop).
 * @param {Object} context.idGenerator An object with a `next()` method used to generate an id for each created segment.
 * @param {number} begin Start index for the inclusive range; negative values are offsets from `segmentsList.length`.
 * @param {number} end End index for the inclusive range; negative values are offsets from `segmentsList.length`.
 * @param {Function} create Factory function invoked as `create(id, allPrevSegments)`.
 * @returns {Array} An array of created segments, one per `i` in `[0, context.count)`.
 */
function makeSegments(context, begin, end, create) {
  const list = context.segmentsList;

  const normalizedBegin = begin >= 0 ? begin : list.length + begin;
  const normalizedEnd = end >= 0 ? end : list.length + end;

  const segments = [];

  for (let i = 0; i < context.count; ++i) {
    const allPrevSegments = [];

    for (let j = normalizedBegin; j <= normalizedEnd; ++j) {
      allPrevSegments.push(list[j][i]);
    }

    segments.push(create(context.idGenerator.next(), allPrevSegments));
  }

  return segments;
}
