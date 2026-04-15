import type { ExpenseCreate, ExpenseOut, ExpenseUpdate, PaginatedExpenses } from '../types'
import client from './client'

/** Filters accepted by the list endpoint. All fields are optional and ANDed together. */
export interface ExpenseFilters {
  year?: number
  category?: string
  payment_method?: string
  page?: number
  size?: number
}

/** Fetch a paginated, optionally filtered list of expenses. */
export async function getExpenses(filters: ExpenseFilters = {}): Promise<PaginatedExpenses> {
  const { data } = await client.get<PaginatedExpenses>('/expenses/', { params: filters })
  return data
}

/** Fetch a single expense by ID, including its nested reimbursement and receipts. */
export async function getExpense(id: string): Promise<ExpenseOut> {
  const { data } = await client.get<ExpenseOut>(`/expenses/${id}`)
  return data
}

/** Create a new expense. Returns the created record with empty receipts and no reimbursement. */
export async function createExpense(body: ExpenseCreate): Promise<ExpenseOut> {
  const { data } = await client.post<ExpenseOut>('/expenses/', body)
  return data
}

/** Partially update an expense. Only fields included in body are changed. */
export async function updateExpense(id: string, body: ExpenseUpdate): Promise<ExpenseOut> {
  const { data } = await client.patch<ExpenseOut>(`/expenses/${id}`, body)
  return data
}

/** Delete an expense and cascade-delete its reimbursement and receipts. */
export async function deleteExpense(id: string): Promise<void> {
  await client.delete(`/expenses/${id}`)
}
