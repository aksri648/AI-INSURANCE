import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { useAuth } from './useAuth'

export interface Policy {
  id: string
  title: string
  insurer: string | null
  policy_number: string | null
  policy_type: string
  status: string
  file_type: string | null
  file_size_bytes: number | null
  summary: string | null
  page_count: number | null
  created_at: string
  updated_at: string
  benefits: Benefit[]
  structured_data: Record<string, unknown>
}

export interface Benefit {
  id?: string
  name: string
  description: string | null
  coverage_amount: string | null
  currency: string
  waiting_period: string | null
  exclusions: string | null
  conditions: string | null
  claim_limit: string | null
  deductible: string | null
  copay: string | null
  is_sub_limit: boolean
  parent_benefit: string | null
  confidence: string
}

export function usePolicies() {
  const { getToken } = useAuth()

  return useQuery({
    queryKey: ['policies'],
    queryFn: async () => {
      const token = await getToken()
      if (token) api.setToken(token)
      return api.get<Policy[]>('/policies/')
    },
  })
}

export function usePolicy(id: string | undefined) {
  const { getToken } = useAuth()

  return useQuery({
    queryKey: ['policy', id],
    queryFn: async () => {
      const token = await getToken()
      if (token) api.setToken(token)
      return api.get<Policy>(`/policies/${id}`)
    },
    enabled: !!id,
  })
}

export function useUploadPolicy() {
  const queryClient = useQueryClient()
  const { getToken } = useAuth()

  return useMutation({
    mutationFn: async (formData: FormData) => {
      const token = await getToken()
      if (token) api.setToken(token)
      return api.post<Policy>('/policies/upload', formData)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policies'] })
    },
  })
}

export function useAnalyzePolicy() {
  const queryClient = useQueryClient()
  const { getToken } = useAuth()

  return useMutation({
    mutationFn: async (policyId: string) => {
      const token = await getToken()
      if (token) api.setToken(token)
      return api.post(`/policies/${policyId}/analyze`)
    },
    onSuccess: (_data, policyId) => {
      queryClient.invalidateQueries({ queryKey: ['policy', policyId] })
      queryClient.invalidateQueries({ queryKey: ['policies'] })
    },
  })
}

export function useDeletePolicy() {
  const queryClient = useQueryClient()
  const { getToken } = useAuth()

  return useMutation({
    mutationFn: async (policyId: string) => {
      const token = await getToken()
      if (token) api.setToken(token)
      return api.delete(`/policies/${policyId}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['policies'] })
    },
  })
}
