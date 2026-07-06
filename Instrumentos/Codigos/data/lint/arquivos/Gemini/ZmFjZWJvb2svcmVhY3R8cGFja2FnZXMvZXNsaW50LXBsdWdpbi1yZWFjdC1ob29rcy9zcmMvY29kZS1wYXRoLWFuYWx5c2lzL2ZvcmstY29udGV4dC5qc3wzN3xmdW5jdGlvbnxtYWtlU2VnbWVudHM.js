/**
 * Generates a list of segments based on provided context and range.
 *
 * @param {object} context - The context object containing segmentsList, count, idGenerator, and id.
 * @param {Array<Array<any>>} context.segmentsList - A list of existing segments.
 * @param {number} context.count - The number of segments to create.
 * @param {object} context.idGenerator - An object with a next() method to generate IDs.
 * @param {string} context.id - The ID of the context.
 * @param {number} begin - The starting index for segment selection. Can be negative to count from the end.
 * @param {number} end - The ending index for segment selection. Can be negative to count from the end.
 * @param {function(string, Array<any>): any} create - A function to create new segments. It receives a generated ID and an array of previous segments.
 * @returns {Array<any>} An array of newly created segments.
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
