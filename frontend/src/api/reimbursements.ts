import type {
  PaginatedReimbursements,
  ReimbursementCreate,
  ReimbursementOut,
  ReimbursementUpdate,
} from '../types'
import client from './client'

export interface ReimbursementFilters {
  status?: string
  year?: number
}

export async function getReimbursements(
  filters: ReimbursementFilters = {},
): Promise<PaginatedReimbursements> {
  const { data } = await client.get<PaginatedReimbursements>('/reimbursements/', {
    params: filters,
  })
  return data
}

export async function createReimbursement(
  body: ReimbursementCreate,
): Promise<ReimbursementOut> {
  const { data } = await client.post<ReimbursementOut>('/reimbursements/', body)
  return data
}

export async function updateReimbursement(
  id: string,
  body: ReimbursementUpdate,
): Promise<ReimbursementOut> {
  const { data } = await client.patch<ReimbursementOut>(`/reimbursements/${id}`, body)
  return data
}

export async function deleteReimbursement(id: string): Promise<void> {
  await client.delete(`/reimbursements/${id}`)
}
