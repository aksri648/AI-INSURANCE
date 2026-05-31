import { useState } from 'react'
import { usePolicies } from '@/hooks/usePolicy'
import { useAssessClaim, useClaims } from '@/hooks/useClaims'
import { GlassCard } from '@/components/GlassCard'
import { StatCard } from '@/components/StatCard'
import { Shield, CheckCircle, AlertTriangle, FileText, Clock } from 'lucide-react'

export function Claims() {
  const { data: policies } = usePolicies()
  const { data: claims } = useClaims()
  const assessClaim = useAssessClaim()
  const [selectedPolicy, setSelectedPolicy] = useState('')
  const [claimType, setClaimType] = useState('')
  const [claimAmount, setClaimAmount] = useState('')
  const [description, setDescription] = useState('')
  const [result, setResult] = useState<any>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedPolicy || !claimType || !description) return

    try {
      const res = await assessClaim.mutateAsync({
        policy_id: selectedPolicy,
        claim_type: claimType,
        claim_amount: claimAmount ? parseFloat(claimAmount) : undefined,
        description,
      })
      setResult(res as any)
    } catch (err) {
      console.error('Claim assessment failed:', err)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Claim Assessment</h1>
        <p className="text-[#9d9db0] text-sm mt-1">
          Check your claim eligibility and estimated payout before filing
        </p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <GlassCard>
          <h2 className="section-title flex items-center gap-2">
            <Shield className="w-4 h-4 text-[#4facfe]" />
            Assess New Claim
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Policy</label>
              <select className="input-field" value={selectedPolicy} onChange={(e) => setSelectedPolicy(e.target.value)} required>
                <option value="">Select a policy</option>
                {(policies || []).map((p) => (
                  <option key={p.id} value={p.id}>{p.title}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Claim Type</label>
              <input className="input-field" value={claimType} onChange={(e) => setClaimType(e.target.value)} placeholder="e.g., Hospitalization, Accidental Damage" required />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Claim Amount (optional)</label>
              <input className="input-field" type="number" value={claimAmount} onChange={(e) => setClaimAmount(e.target.value)} placeholder="e.g., 50000" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Description</label>
              <textarea className="input-field min-h-[100px]" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Describe your claim situation..." required />
            </div>
            <button type="submit" disabled={assessClaim.isPending} className="btn-primary w-full">
              {assessClaim.isPending ? 'Assessing...' : 'Assess Claim'}
            </button>
          </form>
        </GlassCard>

        {result && (
          <GlassCard>
            <h2 className="section-title flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-[#1dd1a1]" />
              Assessment Result
            </h2>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="glass-card p-4 text-center">
                  <div className="text-2xl font-bold text-[#1dd1a1]">{String(result.eligibility_score ?? 'N/A')}%</div>
                  <div className="text-xs text-[#9d9db0]">Eligibility Score</div>
                </div>
                <div className="glass-card p-4 text-center">
                  <div className="text-2xl font-bold text-[#4facfe]">{String(result.estimated_payout || 'N/A')}</div>
                  <div className="text-xs text-[#9d9db0]">Estimated Payout</div>
                </div>
              </div>
              {result.summary && (
                <div className="p-3 rounded-lg bg-[#12121a] text-sm text-[#9d9db0]">
                  {String(result.summary)}
                </div>
              )}
              {(result.recommendations as string[] || []).length > 0 && (
                <div>
                  <p className="text-sm font-medium mb-2">Recommendations</p>
                  <ul className="space-y-1">
                    {(result.recommendations as string[]).map((r, i) => (
                      <li key={i} className="text-sm text-[#9d9db0] flex items-start gap-2">
                        <CheckCircle className="w-3 h-3 text-[#1dd1a1] mt-1 shrink-0" />
                        {r}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </GlassCard>
        )}
      </div>

      {(claims || []).length > 0 && (
        <GlassCard>
          <h2 className="section-title flex items-center gap-2">
            <Clock className="w-4 h-4 text-[#9d9db0]" />
            Claim History
          </h2>
          <div className="space-y-2">
            {(claims || []).map((c) => (
              <div key={c.id} className="flex items-center justify-between p-3 rounded-lg bg-[#12121a]">
                <div>
                  <p className="text-sm font-medium">{c.claim_type}</p>
                  <p className="text-xs text-[#9d9db0]">{c.policy_title}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-[#1dd1a1]">{c.eligibility_score ?? 'N/A'}%</p>
                  <p className="text-xs text-[#9d9db0]">{c.estimated_payout || 'N/A'}</p>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      )}
    </div>
  )
}
