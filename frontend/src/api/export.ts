/**
 * Export download helpers.
 *
 * Both functions construct the API URL and trigger a browser download via a
 * temporary anchor click. This keeps the file in the browser's download tray
 * without navigating away from the page or loading the blob into JS memory.
 */

function triggerDownload(url: string) {
  const a = document.createElement('a')
  a.href = url
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

/** Download all expenses (or a single year) as a CSV file. */
export function downloadExpensesCsv(year?: number) {
  const params = year ? `?year=${year}` : ''
  triggerDownload(`/api/v1/export/expenses.csv${params}`)
}

/** Download a ZIP archive containing expenses.csv and all renamed receipt files. */
export function downloadFullZip(year?: number) {
  const params = year ? `?year=${year}` : ''
  triggerDownload(`/api/v1/export/full.zip${params}`)
}
