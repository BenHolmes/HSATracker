import type {
  PaginatedReimbursements,
  ReimbursementCreate,
  ReimbursementOut,
  ReimbursementUpdate,
} from '../types'
import client from './client'

/** Filters accepted by the list endpoint. */
export interface ReimbursementFilters {
  status?: string  // 'pending' | 'reimbursed'
  year?: number    // filters by the linked expense's date year
}

/**
 * Fetch all reimbursements with aggregate totals.
 * Response always includes pending_amount and reimbursed_amount_ytd
 * regardless of which filters are applied.
 */
export async function getReimbursements(
  filters: ReimbursementFilters = {},
): Promise<PaginatedReimbursements> {
  const { data } = await client.get<PaginatedReimbursements>('/reimbursements/', {
    params: filters,
  })
  return data
}

/**
 * Start tracking an out-of-pocket expense for reimbursement.
 * The backend validates that the expense exists, is out-of-pocket,
 * and doesn't already have a reimbursement record.
 */
export async function createReimbursement(
  body: ReimbursementCreate,
): Promise<ReimbursementOut> {
  const { data } = await client.post<ReimbursementOut>('/reimbursements/', body)
  return data
}

/**
 * Update a reimbursement record.
 * Typical usage: set status='reimbursed' with reimbursed_date and reimbursed_amount
 * once the HSA custodian has transferred funds back.
 */
export async function updateReimbursement(
  id: string,
  body: ReimbursementUpdate,
): Promise<ReimbursementOut> {
  const { data } = await client.patch<ReimbursementOut>(`/reimbursements/${id}`, body)
  return data
}

/** Delete a reimbursement record. The linked expense is not affected. */
export async function deleteReimbursement(id: string): Promise<void> {
  await client.delete(`/reimbursements/${id}`)
}
