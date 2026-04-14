import type {
  ContributionCreate,
  ContributionOut,
  ContributionUpdate,
  PaginatedContributions,
} from '../types'
import client from './client'

export async function getContributions(tax_year?: number): Promise<PaginatedContributions> {
  const { data } = await client.get<PaginatedContributions>('/contributions/', {
    params: tax_year != null ? { tax_year } : {},
  })
  return data
}

export async function createContribution(body: ContributionCreate): Promise<ContributionOut> {
  const { data } = await client.post<ContributionOut>('/contributions/', body)
  return data
}

export async function updateContribution(
  id: string,
  body: ContributionUpdate,
): Promise<ContributionOut> {
  const { data } = await client.patch<ContributionOut>(`/contributions/${id}`, body)
  return data
}

export async function deleteContribution(id: string): Promise<void> {
  await client.delete(`/contributions/${id}`)
}
