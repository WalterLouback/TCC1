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