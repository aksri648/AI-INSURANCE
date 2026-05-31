import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { useAuth } from './useAuth'

export interface ClaimAssessment {
  id: string
  policy_id: string
  policy_title?: string
  claim_type: string
  claim_amount: string | null
  description: string | null
  eligibility_score: number | null
  estimated_payout: string | null
  assessment_result: Record<string, unknown>
  confidence: string
  summary: string
  recommendations: string[]
  evidence_refs: Record<string, unknown>[]
  created_at?: string
}

export function useClaims() {
  const { getToken } = useAuth()

  return useQuery({
    queryKey: ['claims'],
    queryFn: async () => {
      const token = await getToken()
      if (token) api.setToken(token)
      return api.get<ClaimAssessment[]>('/claims/history')
    },
  })
}

export function useClaimDetail(id: string | undefined) {
  const { getToken } = useAuth()

  return useQuery({
    queryKey: ['claim', id],
    queryFn: async () => {
      const token = await getToken()
      if (token) api.setToken(token)
      return api.get<ClaimAssessment>(`/claims/${id}`)
    },
    enabled: !!id,
  })
}

export function useAssessClaim() {
  const queryClient = useQueryClient()
  const { getToken } = useAuth()

  return useMutation({
    mutationFn: async (data: {
      policy_id: string
      claim_type: string
      claim_amount?: number
      description: string
    }) => {
      const token = await getToken()
      if (token) api.setToken(token)
      return api.post<ClaimAssessment>('/claims/assess', data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['claims'] })
    },
  })
}
