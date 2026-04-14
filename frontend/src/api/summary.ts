import type { SummaryOut } from '../types'
import client from './client'

export async function getSummary(year?: number): Promise<SummaryOut> {
  const { data } = await client.get<SummaryOut>('/summary/', {
    params: year != null ? { year } : {},
  })
  return data
}
