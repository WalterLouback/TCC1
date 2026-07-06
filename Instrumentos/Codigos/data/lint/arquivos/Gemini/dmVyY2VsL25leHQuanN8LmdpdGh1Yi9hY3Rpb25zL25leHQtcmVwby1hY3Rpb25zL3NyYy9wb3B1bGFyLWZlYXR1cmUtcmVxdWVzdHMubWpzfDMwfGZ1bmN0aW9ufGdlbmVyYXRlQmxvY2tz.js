/**
 * Generates a list of blocks for a Slack message, displaying feature requests.
 *
 * @param {Array<Object>} items - An array of feature request objects. Each object is expected to have properties like `html_url`, `number`, `upvoteCount`, `created_at`, and `title`.
 * @returns {Array<Object>} An array of block objects suitable for a Slack message.
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
