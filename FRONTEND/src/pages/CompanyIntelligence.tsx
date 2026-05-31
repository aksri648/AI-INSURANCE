import { useState } from 'react'
import { GlassCard } from '@/components/GlassCard'
import { api } from '@/lib/api'
import { useAuth } from '@/hooks/useAuth'
import { Building2, Search, BarChart3, TrendingUp, Shield } from 'lucide-react'

export function CompanyIntelligence() {
  const { getToken } = useAuth()
  const [companyName, setCompanyName] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const [compareMode, setCompareMode] = useState(false)
  const [companies, setCompanies] = useState<string[]>(['', ''])

  const searchCompany = async () => {
    if (!companyName) return
    setLoading(true)
    try {
      const token = await getToken()
      if (token) api.setToken(token)
      const res = await api.post('/companies/search', { company_name: companyName })
      setResult(res as Record<string, unknown>)
    } catch (err) {
      console.error('Company search failed:', err)
    } finally {
      setLoading(false)
    }
  }

  const compareCompanies = async () => {
    const valid = companies.filter(Boolean)
    if (valid.length < 2) return
    setLoading(true)
    try {
      const token = await getToken()
      if (token) api.setToken(token)
      const res = await api.post('/companies/compare', { company_names: valid })
      setResult(res as Record<string, unknown>)
    } catch (err) {
      console.error('Comparison failed:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Company Intelligence</h1>
          <p className="text-[#9d9db0] text-sm mt-1">Research insurance companies' performance and trustworthiness</p>
        </div>
        <button onClick={() => { setCompareMode(!compareMode); setResult(null) }} className="btn-secondary text-sm">
          {compareMode ? 'Single Search' : 'Compare Companies'}
        </button>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <GlassCard>
          <h2 className="section-title flex items-center gap-2">
            <Search className="w-4 h-4 text-[#4facfe]" />
            {compareMode ? 'Compare Companies' : 'Search Company'}
          </h2>

          {compareMode ? (
            <div className="space-y-3">
              {companies.map((_, i) => (
                <input key={i} className="input-field" value={companies[i]} onChange={(e) => { const c = [...companies]; c[i] = e.target.value; setCompanies(c) }} placeholder={`Company ${i + 1} name`} />
              ))}
              <button onClick={compareCompanies} disabled={loading || companies.filter(Boolean).length < 2} className="btn-primary w-full">
                {loading ? 'Comparing...' : 'Compare'}
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              <input className="input-field" value={companyName} onChange={(e) => setCompanyName(e.target.value)} placeholder="e.g., ICICI Lombard" onKeyDown={(e) => e.key === 'Enter' && searchCompany()} />
              <button onClick={searchCompany} disabled={loading || !companyName} className="btn-primary w-full flex items-center justify-center gap-2">
                <Building2 className="w-4 h-4" />
                {loading ? 'Searching...' : 'Search'}
              </button>
            </div>
          )}
        </GlassCard>

        {result && (
          <GlassCard>
            <h2 className="section-title flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-[#1dd1a1]" />
              {result.name as string || 'Results'}
            </h2>
            <div className="grid grid-cols-2 gap-3 mb-4">
              {result.claim_settlement_ratio && (
                <div className="glass-card p-3 text-center">
                  <div className="text-lg font-bold text-[#1dd1a1]">{result.claim_settlement_ratio as number}%</div>
                  <div className="text-xs text-[#9d9db0]">Claim Settlement Ratio</div>
                </div>
              )}
              {result.solvency_ratio && (
                <div className="glass-card p-3 text-center">
                  <div className="text-lg font-bold text-[#4facfe]">{result.solvency_ratio as number}%</div>
                  <div className="text-xs text-[#9d9db0]">Solvency Ratio</div>
                </div>
              )}
              {result.trust_score && (
                <div className="glass-card p-3 text-center">
                  <div className="text-lg font-bold text-[#feca57]">{result.trust_score as number}/100</div>
                  <div className="text-xs text-[#9d9db0]">Trust Score</div>
                </div>
              )}
              {result.market_share && (
                <div className="glass-card p-3 text-center">
                  <div className="text-lg font-bold text-[#a855f7]">{result.market_share as number}%</div>
                  <div className="text-xs text-[#9d9db0]">Market Share</div>
                </div>
              )}
            </div>
            {result.summary && <p className="text-sm text-[#9d9db0]">{result.summary as string}</p>}
            {(result.strengths as string[] || []).length > 0 && (
              <div className="mt-3">
                <p className="text-xs font-medium text-[#1dd1a1] mb-1">Strengths</p>
                <ul className="space-y-1">{(result.strengths as string[]).map((s, i) => <li key={i} className="text-xs text-[#9d9db0]">• {s}</li>)}</ul>
              </div>
            )}
            {(result.weaknesses as string[] || []).length > 0 && (
              <div className="mt-3">
                <p className="text-xs font-medium text-[#ff6b6b] mb-1">Weaknesses</p>
                <ul className="space-y-1">{(result.weaknesses as string[]).map((w, i) => <li key={i} className="text-xs text-[#9d9db0]">• {w}</li>)}</ul>
              </div>
            )}
          </GlassCard>
        )}
      </div>
    </div>
  )
}
