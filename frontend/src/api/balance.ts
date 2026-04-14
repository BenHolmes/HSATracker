import type { BalanceCreate, BalanceList, BalanceOut } from '../types'
import client from './client'

export async function getBalance(): Promise<BalanceList> {
  const { data } = await client.get<BalanceList>('/balance/')
  return data
}

export async function createBalance(body: BalanceCreate): Promise<BalanceOut> {
  const { data } = await client.post<BalanceOut>('/balance/', body)
  return data
}

export async function deleteBalance(id: string): Promise<void> {
  await client.delete(`/balance/${id}`)
}
