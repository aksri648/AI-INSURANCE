import { api } from './api'

export interface AuthUser {
  id: string
  clerk_id: string
  email: string
  name: string | null
  avatar_url: string | null
  preferences: Record<string, unknown>
  created_at: string
}

export interface UserStats {
  total_policies: number
  total_claims: number
  total_reports: number
}

export async function getCurrentUser(token: string): Promise<AuthUser> {
  api.setToken(token)
  return api.get<AuthUser>('/auth/me')
}

export async function getUserStats(token: string): Promise<UserStats> {
  api.setToken(token)
  return api.get<UserStats>('/auth/stats')
}

export async function updateProfile(token: string, data: Partial<AuthUser>): Promise<AuthUser> {
  api.setToken(token)
  return api.put<AuthUser>('/auth/profile', data)
}
