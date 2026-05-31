import { useParams, Link } from 'react-router-dom'
import { usePolicy, useAnalyzePolicy } from '@/hooks/usePolicy'
import { GlassCard } from '@/components/GlassCard'
import { StatCard } from '@/components/StatCard'
import { Shield, MessageSquare, AlertTriangle, CheckCircle, Clock, ArrowLeft, Zap } from 'lucide-react'

export function PolicyAnalysis() {
  const { id } = useParams<{ id: string }>()
  const { data: policy, isLoading } = usePolicy(id)
  const analyzeMutation = useAnalyzePolicy()

  if (isLoading) {
    return <div className="animate-pulse text-[#1dd1a1]">Loading policy...</div>
  }

  if (!policy) {
    return <div className="text-[#ff6b6b]">Policy not found</div>
  }

  const analyzed = policy.status === 'analyzed'

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to="/policies" className="btn-ghost p-2">
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold">{policy.title}</h1>
            <p className="text-[#9d9db0] text-sm">
              {policy.insurer || 'Unknown Insurer'} · <span className="capitalize">{policy.policy_type}</span>
              {policy.policy_number && ` · Policy #${policy.policy_number}`}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Link to={`/policies/${id}/chat`} className="btn-secondary flex items-center gap-2">
            <MessageSquare className="w-4 h-4" />
            Chat
          </Link>
          {!analyzed && (
            <button
              onClick={() => analyzeMutation.mutate(id!)}
              disabled={analyzeMutation.isPending}
              className="btn-primary flex items-center gap-2"
            >
              <Zap className="w-4 h-4" />
              {analyzeMutation.isPending ? 'Analyzing...' : 'Analyze Policy'}
            </button>
          )}
        </div>
      </div>

      {!analyzed ? (
        <GlassCard className="text-center py-12">
          <Clock className="w-12 h-12 text-[#feca57] mx-auto mb-4" />
          <h2 className="text-lg font-semibold mb-2">Policy Not Yet Analyzed</h2>
          <p className="text-[#9d9db0] mb-4">Click "Analyze Policy" to extract all benefits, coverage, and terms</p>
        </GlassCard>
      ) : (
        <>
          <div className="grid grid-cols-4 gap-4">
            <StatCard label="Total Benefits" value={policy.benefits?.length || 0} icon="🎯" />
            <StatCard label="Coverage Amount" value="View Below" icon="💰" />
            <StatCard label="Status" value="Analyzed" icon="✅" />
            <StatCard label="Confidence" value="Verified" icon="🟢" />
          </div>

          <GlassCard>
            <h2 className="section-title">Benefits & Coverage</h2>
            {policy.benefits && policy.benefits.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="text-left text-sm text-[#9d9db0] border-b border-[#2a2a3e]">
                      <th className="pb-3 font-medium">Benefit</th>
                      <th className="pb-3 font-medium">Coverage Amount</th>
                      <th className="pb-3 font-medium">Waiting Period</th>
                      <th className="pb-3 font-medium">Deductible</th>
                      <th className="pb-3 font-medium">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {policy.benefits.map((b) => (
                      <tr key={b.id || b.name} className="border-b border-[#1a1a2e] text-sm">
                        <td className="py-3">
                          <div>
                            <p className="font-medium">{b.name}</p>
                            {b.description && (
                              <p className="text-xs text-[#9d9db0] mt-0.5">{b.description}</p>
                            )}
                          </div>
                        </td>
                        <td className="py-3 text-[#1dd1a1] font-medium">
                          {b.coverage_amount || 'N/A'}
                        </td>
                        <td className="py-3 text-[#9d9db0]">{b.waiting_period || 'None'}</td>
                        <td className="py-3 text-[#9d9db0]">{b.deductible || 'None'}</td>
                        <td className="py-3">
                          <span className={b.confidence === 'verified' ? 'badge-verified' : 'badge-review'}>
                            {b.confidence === 'verified' ? '🟢 Verified' : '🟡 Needs Review'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-[#9d9db0]">No benefits extracted yet</p>
            )}
          </GlassCard>

          {policy.structured_data?.exclusions && (
            <GlassCard>
              <h2 className="section-title flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-[#feca57]" />
                Exclusions
              </h2>
              <ul className="space-y-2">
                {(policy.structured_data.exclusions as string[]).map((e, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-[#9d9db0]">
                    <span className="text-[#ff6b6b] mt-1">•</span>
                    {e}
                  </li>
                ))}
              </ul>
            </GlassCard>
          )}

          <GlassCard>
            <h2 className="section-title">Summary</h2>
            <p className="text-[#9d9db0] text-sm leading-relaxed">
              {policy.summary || 'No summary available.'}
            </p>
          </GlassCard>
        </>
      )}
    </div>
  )
}
