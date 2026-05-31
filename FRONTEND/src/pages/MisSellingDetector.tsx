import { useState } from 'react'
import { usePolicies } from '@/hooks/usePolicy'
import { GlassCard } from '@/components/GlassCard'
import { api } from '@/lib/api'
import { useAuth } from '@/hooks/useAuth'
import { Scale, AlertTriangle, CheckCircle, Search, FileText } from 'lucide-react'

export function MisSellingDetector() {
  const { data: policies } = usePolicies()
  const { getToken } = useAuth()
  const [selectedPolicy, setSelectedPolicy] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Record<string, unknown> | null>(null)

  const checkMisSelling = async () => {
    if (!selectedPolicy) return
    setLoading(true)
    try {
      const token = await getToken()
      if (token) api.setToken(token)
      const res = await api.post('/education/mis-selling-check', { policy_id: selectedPolicy })
      setResult(res as Record<string, unknown>)
    } catch (err) {
      console.error('Mis-selling check failed:', err)
    } finally {
      setLoading(false)
    }
  }

  const severityColor = (s: string) => {
    switch (s) {
      case 'critical': return 'text-[#ff6b6b] border-[#ff6b6b]/30 bg-[#ff6b6b]/10'
      case 'high': return 'text-[#ff6b6b] border-[#ff6b6b]/30 bg-[#ff6b6b]/10'
      case 'medium': return 'text-[#feca57] border-[#feca57]/30 bg-[#feca57]/10'
      case 'low': return 'text-[#4facfe] border-[#4facfe]/30 bg-[#4facfe]/10'
      default: return 'text-[#9d9db0] border-[#2a2a3e] bg-[#12121a]'
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Mis-Selling Detector</h1>
        <p className="text-[#9d9db0] text-sm mt-1">
          Detect misleading statements, hidden clauses, and unfair terms in your policies
        </p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <GlassCard>
          <h2 className="section-title flex items-center gap-2">
            <Search className="w-4 h-4 text-[#feca57]" />
            Check a Policy
          </h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Select Policy</label>
              <select className="input-field" value={selectedPolicy} onChange={(e) => setSelectedPolicy(e.target.value)}>
                <option value="">Choose a policy to check</option>
                {(policies || []).map((p) => (
                  <option key={p.id} value={p.id}>{p.title}</option>
                ))}
              </select>
            </div>
            <button onClick={checkMisSelling} disabled={!selectedPolicy || loading} className="btn-primary w-full flex items-center justify-center gap-2">
              <Scale className="w-4 h-4" />
              {loading ? 'Analyzing...' : 'Check for Mis-Selling'}
            </button>
          </div>
        </GlassCard>

        {result && (
          <GlassCard>
            <h2 className="section-title flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-[#feca57]" />
              Findings
            </h2>
            <div className="mb-4">
              <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium border ${severityColor(result.severity as string)}`}>
                {(result.severity as string || 'unknown').toUpperCase()} SEVERITY
              </span>
            </div>
            {result.summary && (
              <p className="text-sm text-[#9d9db0] mb-4">{String(result.summary)}</p>
            )}
            {(result.findings as Record<string, unknown>[] || []).map((f, i) => (
              <div key={i} className={`p-3 rounded-lg mb-2 border ${severityColor(f.severity as string)}`}>
                <p className="text-sm font-medium mb-1">{String(f.title)}</p>
                <p className="text-xs text-[#9d9db0]">{String(f.description)}</p>
                {f.evidence && <p className="text-xs text-[#5a5a6e] mt-1 italic">Evidence: {String(f.evidence).slice(0, 200)}</p>}
              </div>
            ))}
            {(result.recommendations as string[] || []).length > 0 && (
              <div className="mt-4">
                <p className="text-sm font-medium mb-2">Recommended Actions</p>
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
          </GlassCard>
        )}
      </div>
    </div>
  )
}
