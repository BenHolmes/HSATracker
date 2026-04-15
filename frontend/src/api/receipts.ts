import type { ReceiptOut } from '../types'
import client from './client'

/** Fetch all receipt metadata for an expense, ordered by upload time. */
export async function getReceipts(expenseId: string): Promise<ReceiptOut[]> {
  const { data } = await client.get<ReceiptOut[]>(`/expenses/${expenseId}/receipts/`)
  return data
}

/**
 * Upload a receipt file and attach it to an expense.
 * Accepts image/jpeg, image/png, and application/pdf up to MAX_UPLOAD_SIZE_MB (default 10 MB).
 * The backend validates MIME type, magic bytes, and file size before writing to disk.
 */
export async function uploadReceipt(expenseId: string, file: File): Promise<ReceiptOut> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await client.post<ReceiptOut>(`/expenses/${expenseId}/receipts/`, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

/** Delete a receipt record and its file from disk. */
export async function deleteReceipt(id: string): Promise<void> {
  await client.delete(`/receipts/${id}`)
}

/** Returns the URL to stream a receipt file inline in the browser (images and PDFs render directly). */
export function getReceiptFileUrl(id: string): string {
  return `/api/v1/receipts/${id}/file`
}
