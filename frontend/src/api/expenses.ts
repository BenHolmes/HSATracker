import type { ExpenseCreate, ExpenseOut, ExpenseUpdate, PaginatedExpenses } from '../types'
import client from './client'

export interface ExpenseFilters {
  year?: number
  category?: string
  payment_method?: string
  page?: number
  size?: number
}

export async function getExpenses(filters: ExpenseFilters = {}): Promise<PaginatedExpenses> {
  const { data } = await client.get<PaginatedExpenses>('/expenses/', { params: filters })
  return data
}

export async function getExpense(id: string): Promise<ExpenseOut> {
  const { data } = await client.get<ExpenseOut>(`/expenses/${id}`)
  return data
}

export async function createExpense(body: ExpenseCreate): Promise<ExpenseOut> {
  const { data } = await client.post<ExpenseOut>('/expenses/', body)
  return data
}

export async function updateExpense(id: string, body: ExpenseUpdate): Promise<ExpenseOut> {
  const { data } = await client.patch<ExpenseOut>(`/expenses/${id}`, body)
  return data
}

export async function deleteExpense(id: string): Promise<void> {
  await client.delete(`/expenses/${id}`)
}
