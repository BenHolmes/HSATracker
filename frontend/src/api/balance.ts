import type { BalanceCreate, BalanceList, BalanceOut } from '../types'
import client from './client'

/**
 * Fetch all balance snapshots ordered by date DESC, with the latest pre-extracted.
 * Returns { items: BalanceOut[], latest: BalanceOut | null }.
 */
export async function getBalance(): Promise<BalanceList> {
  const { data } = await client.get<BalanceList>('/balance/')
  return data
}

/**
 * Record a new account balance snapshot.
 * Balances are user-entered (not computed) because investment returns and
 * fees from the HSA custodian cannot be tracked automatically.
 */
export async function createBalance(body: BalanceCreate): Promise<BalanceOut> {
  const { data } = await client.post<BalanceOut>('/balance/', body)
  return data
}

/** Delete a balance snapshot. */
export async function deleteBalance(id: string): Promise<void> {
  await client.delete(`/balance/${id}`)
}
