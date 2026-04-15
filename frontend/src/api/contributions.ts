import type {
  ContributionCreate,
  ContributionOut,
  ContributionUpdate,
  PaginatedContributions,
} from '../types'
import client from './client'

/**
 * Fetch all contributions for a tax year, including IRS limit data and remaining headroom.
 * Omitting tax_year defaults to the current calendar year on the backend.
 */
export async function getContributions(tax_year?: number): Promise<PaginatedContributions> {
  const { data } = await client.get<PaginatedContributions>('/contributions/', {
    params: tax_year != null ? { tax_year } : {},
  })
  return data
}

/** Record a new HSA contribution. */
export async function createContribution(body: ContributionCreate): Promise<ContributionOut> {
  const { data } = await client.post<ContributionOut>('/contributions/', body)
  return data
}

/** Partially update a contribution record. */
export async function updateContribution(
  id: string,
  body: ContributionUpdate,
): Promise<ContributionOut> {
  const { data } = await client.patch<ContributionOut>(`/contributions/${id}`, body)
  return data
}

/** Delete a contribution record. */
export async function deleteContribution(id: string): Promise<void> {
  await client.delete(`/contributions/${id}`)
}

/** Fetch distinct tax years present in the contributions table, newest first. */
export async function getContributionYears(): Promise<number[]> {
  const { data } = await client.get<number[]>('/contributions/years')
  return data
}
