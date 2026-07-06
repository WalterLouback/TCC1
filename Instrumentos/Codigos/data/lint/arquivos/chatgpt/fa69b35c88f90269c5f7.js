/**
 * Builds an array of Slack Block Kit blocks that summarizes the top feature requests.
 * The output includes a header section, a divider, and a final section containing a
 * numbered list derived from the provided items.
 *
 * @param {Array<Object>} items - List of feature request items. Each item is expected to include:
 * @param {string} items[].html_url - URL to the item on GitHub.
 * @param {number} items[].number - Item number used for display.
 * @param {number} items[].upvoteCount - Upvote count used for display.
 * @param {string} items[].created_at - Creation date string passed to `formattedDate`.
 * @returns {Array<Object>} An array of block objects suitable for Slack Block Kit.
 */
function generateBlocks(items) {
  const blocks = [
    {
      type: 'section',
      text: {
        type: 'mrkdwn',
        text: '*A list of the top 15 feature requests sorted by upvotes over the last 90 days.*\n_Note: This :github2: <https://github.com/vercel/next.js/blob/canary/.github/workflows/popular.yml|workflow> → <https://github.com/vercel/next.js/blob/canary/.github/actions/next-repo-actions/src/popular-feature-requests.mjs|action> will run every Monday at 10AM UTC (6AM EST)._',
      },
    },
    {
      type: 'divider',
    },
  ]

  let text = ''

  items.forEach((item, i) => {
    text += `${i + 1}. [<${item.html_url}|#${item.number}>, ↑ ${
      item.upvoteCount
    }, ${formattedDate(item.created_at)}]: ${item.title}\n`
  })

  blocks.push({
    type: 'section',
    text: {
      type: 'mrkdwn',
      text: text,
    },
  })

  return blocks
}
