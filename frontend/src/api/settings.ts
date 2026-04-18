import type { AppSettings, AppSettingsUpdate } from '../types'
import client from './client'

export async function getSettings(): Promise<AppSettings> {
  const { data } = await client.get<AppSettings>('/settings/')
  return data
}

export async function updateSettings(patch: AppSettingsUpdate): Promise<AppSettings> {
  const { data } = await client.patch<AppSettings>('/settings/', patch)
  return data
}
