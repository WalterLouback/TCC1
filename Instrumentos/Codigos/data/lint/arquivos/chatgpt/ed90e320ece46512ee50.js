/**
 * Calculates basic descriptive statistics for a numeric array.
 *
 * For non-empty arrays, it computes the median (using the sorted values),
 * minimum, maximum, mean (rounded), standard deviation (rounded),
 * and coefficient of variation in percent (rounded).
 *
 * @param {number[]} arr - Input array of numbers.
 * @returns {null | {median: number, min: number, max: number, mean: number, stddev: number, cv: number}} 
 * Returns null when the input array is empty; otherwise returns an object with the computed statistics.
 */
function calcStats(arr) {
  if (arr.length === 0) return null

  const sorted = [...arr].sort((a, b) => a - b)
  const mid = Math.floor(sorted.length / 2)
  const median =
    sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2
  const min = sorted[0]
  const max = sorted[sorted.length - 1]
  const mean = arr.reduce((a, b) => a + b, 0) / arr.length
  const variance =
    arr.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / arr.length
  const stddev = Math.sqrt(variance)
  const cv = mean > 0 ? (stddev / mean) * 100 : 0 // coefficient of variation as %

  return {
    median,
    min,
    max,
    mean: Math.round(mean),
    stddev: Math.round(stddev),
    cv: Math.round(cv),
  }
}
