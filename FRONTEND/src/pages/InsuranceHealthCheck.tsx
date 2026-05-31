import { usePolicies } from '@/hooks/usePolicy'
import { GlassCard } from '@/components/GlassCard'
import { StatCard } from '@/components/StatCard'
import { Activity, Shield, AlertTriangle, CheckCircle, TrendingUp } from 'lucide-react'

export function InsuranceHealthCheck() {
  const { data: policies } = usePolicies()

  const totalCoverage = policies?.reduce((sum, p) => {
    return sum + (p.benefits?.reduce((s, b) => {
      const amt = parseFloat(String(b.coverage_amount || '0').replace(/[^0-9.]/g, ''))
      return s + (isNaN(amt) ? 0 : amt)
    }, 0) || 0)
  }, 0) || 0

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Insurance Health Check</h1>
        <p className="text-[#9d9db0] text-sm mt-1">Comprehensive analysis of your insurance coverage adequacy</p>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <StatCard label="Total Policies" value={policies?.length || 0} icon="📋" />
        <StatCard label="Total Coverage" value={totalCoverage > 0 ? `₹${(totalCoverage / 100000).toFixed(1)}L` : 'N/A'} icon="💰" />
        <StatCard label="Health Score" value="--/10" icon="🎯" />
        <StatCard label="Gaps Found" value="--" icon="⚠️" />
      </div>

      <div className="grid grid-cols-2 gap-6">
        <GlassCard>
          <h2 className="section-title flex items-center gap-2">
            <Activity className="w-4 h-4 text-[#1dd1a1]" />
            Coverage Overview
          </h2>
          {(!policies || policies.length === 0) ? (
            <div className="text-center py-8">
              <Shield className="w-12 h-12 text-[#2a2a3e] mx-auto mb-3" />
              <p className="text-sm text-[#9d9db0]">Upload policies to see your coverage overview</p>
            </div>
          ) : (
            <div className="space-y-3">
              {policies.map((p) => (
                <div key={p.id} className="flex items-center justify-between p-3 rounded-lg bg-[#12121a]">
                  <div>
                    <p className="text-sm font-medium">{p.title}</p>
                    <p className="text-xs text-[#9d9db0]">{p.insurer || 'Unknown'}</p>
                  </div>
                  <span className={`text-xs ${p.status === 'analyzed' ? 'text-[#1dd1a1]' : 'text-[#feca57]'}`}>
                    {p.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </GlassCard>

        <GlassCard>
          <h2 className="section-title flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-[#1dd1a1]" />
            Recommendations
          </h2>
          {(!policies || policies.length === 0) ? (
            <div className="text-center py-8">
              <TrendingUp className="w-12 h-12 text-[#2a2a3e] mx-auto mb-3" />
              <p className="text-sm text-[#9d9db0]">Upload and analyze policies for personalized recommendations</p>
            </div>
          ) : (
            <div className="space-y-3">
              {policies.length === 0 && (
                <div className="flex items-start gap-2 p-3 rounded-lg bg-[#feca57]/5 border border-[#feca57]/20">
                  <AlertTriangle className="w-4 h-4 text-[#feca57] mt-0.5 shrink-0" />
                  <div>
                    <p className="text-sm font-medium">No Policies Found</p>
                    <p className="text-xs text-[#9d9db0]">Upload at least one policy to get started</p>
                  </div>
                </div>
              )}
            </div>
          )}
        </GlassCard>
      </div>
    </div>
  )
}
