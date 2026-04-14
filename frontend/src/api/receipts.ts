import type { ReceiptOut } from '../types'
import client from './client'

export async function getReceipts(expenseId: string): Promise<ReceiptOut[]> {
  const { data } = await client.get<ReceiptOut[]>(`/expenses/${expenseId}/receipts/`)
  return data
}

export async function uploadReceipt(expenseId: string, file: File): Promise<ReceiptOut> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await client.post<ReceiptOut>(`/expenses/${expenseId}/receipts/`, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function deleteReceipt(id: string): Promise<void> {
  await client.delete(`/receipts/${id}`)
}

/** Returns the URL to stream a receipt file inline in the browser. */
export function getReceiptFileUrl(id: string): string {
  return `/api/v1/receipts/${id}/file`
}
