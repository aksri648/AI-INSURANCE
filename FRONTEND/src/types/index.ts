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

export interface ChatResponse {
  reply: string
  sources: { title: string; content: string }[]
  confidence: string
  suggested_questions: string[]
}

export interface CompanyInfo {
  id: string | null
  name: string
  irda_id: string | null
  website: string | null
  description: string | null
  claim_settlement_ratio: number | null
  solvency_ratio: number | null
  market_share: number | null
  trust_score: number | null
  confidence: string
  sources: string[]
}

export interface EducationResult {
  topic: string
  explanation: string
  key_takeaways: string[]
  related_topics: string[]
  confidence: string
}

export interface MisSellingResult {
  findings: {
    type: string
    severity: string
    title: string
    description: string
    evidence: string
  }[]
  severity: string
  summary: string
  recommendations: string[]
  confidence: string
}
