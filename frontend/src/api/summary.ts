import type { SummaryOut } from '../types'
import client from './client'

/**
 * Fetch aggregated dashboard statistics for a given tax year.
 *
 * Combines expenses, reimbursements, contributions, IRS limits, and the
 * latest balance snapshot into a single response. Omitting year defaults
 * to the current calendar year on the backend.
 */
export async function getSummary(year?: number): Promise<SummaryOut> {
  const { data } = await client.get<SummaryOut>('/summary/', {
    params: year != null ? { year } : {},
  })
  return data
}
