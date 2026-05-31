import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { usePolicies } from '@/hooks/usePolicy'
import { useClaims } from '@/hooks/useClaims'
import { getUserStats } from '@/lib/clerk'
import { GlassCard } from '@/components/GlassCard'
import { StatCard } from '@/components/StatCard'
import { Upload, FileText, Shield, TrendingUp, ArrowRight, Zap } from 'lucide-react'

export function Dashboard() {
  const { user, getToken } = useAuth()
  const { data: policies } = usePolicies()
  const { data: claims } = useClaims()
  const [stats, setStats] = useState({ total_policies: 0, total_claims: 0, total_reports: 0 })

  useEffect(() => {
    async function load() {
      const token = await getToken()
      if (token) {
        const s = await getUserStats(token)
        setStats(s)
      }
    }
    load()
  }, [getToken])

  const recentPolicies = (policies || []).slice(0, 5)

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Welcome, {user?.name || 'User'}</h1>
          <p className="text-[#9d9db0] text-sm mt-1">Your insurance intelligence dashboard</p>
        </div>
        <Link to="/upload" className="btn-primary flex items-center gap-2">
          <Upload className="w-4 h-4" />
          Upload Policy
        </Link>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="grid grid-cols-4 gap-4"
      >
        <StatCard label="Total Policies" value={stats.total_policies} icon="📋" />
        <StatCard label="Claims Assessed" value={stats.total_claims} icon="🛡️" />
        <StatCard label="Reports Generated" value={stats.total_reports} icon="📊" />
        <StatCard label="Coverage Score" value="--" icon="🎯" />
      </motion.div>

      <div className="grid grid-cols-3 gap-6">
        <GlassCard className="col-span-2">
          <h2 className="section-title">Recent Policies</h2>
          {recentPolicies.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="w-12 h-12 text-[#2a2a3e] mx-auto mb-4" />
              <p className="text-[#9d9db0] mb-4">No policies uploaded yet</p>
              <Link to="/upload" className="btn-primary inline-flex items-center gap-2">
                <Upload className="w-4 h-4" />
                Upload Your First Policy
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {recentPolicies.map((policy) => (
                <Link
                  key={policy.id}
                  to={`/policies/${policy.id}`}
                  className="flex items-center justify-between p-3 rounded-lg bg-[#12121a] hover:bg-[#1a1a2e] transition-colors group"
                >
                  <div className="flex items-center gap-3">
                    <FileText className="w-4 h-4 text-[#4facfe]" />
                    <div>
                      <p className="text-sm font-medium">{policy.title}</p>
                      <p className="text-xs text-[#9d9db0]">
                        {policy.insurer || 'Unknown'} · {policy.policy_type}
                      </p>
                    </div>
                  </div>
                  <ArrowRight className="w-4 h-4 text-[#2a2a3e] group-hover:text-[#1dd1a1] transition-colors" />
                </Link>
              ))}
              <Link
                to="/policies"
                className="block text-center text-sm text-[#1dd1a1] hover:text-[#4facfe] transition-colors pt-2"
              >
                View all policies →
              </Link>
            </div>
          )}
        </GlassCard>

        <div className="space-y-4">
          <GlassCard>
            <h2 className="section-title">Quick Actions</h2>
            <div className="space-y-2">
              <Link to="/upload" className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#12121a] transition-colors group">
                <Upload className="w-4 h-4 text-[#1dd1a1]" />
                <span className="text-sm group-hover:text-[#1dd1a1] transition-colors">Upload Policy</span>
              </Link>
              <Link to="/claims" className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#12121a] transition-colors group">
                <Shield className="w-4 h-4 text-[#4facfe]" />
                <span className="text-sm group-hover:text-[#4facfe] transition-colors">Assess Claim</span>
              </Link>
              <Link to="/mis-selling" className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#12121a] transition-colors group">
                <Zap className="w-4 h-4 text-[#feca57]" />
                <span className="text-sm group-hover:text-[#feca57] transition-colors">Check Mis-Selling</span>
              </Link>
              <Link to="/health-check" className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#12121a] transition-colors group">
                <TrendingUp className="w-4 h-4 text-[#a855f7]" />
                <span className="text-sm group-hover:text-[#a855f7] transition-colors">Health Check</span>
              </Link>
            </div>
          </GlassCard>

          <GlassCard>
            <h2 className="section-title">Recent Claims</h2>
            {(claims || []).length === 0 ? (
              <p className="text-sm text-[#9d9db0] text-center py-4">No claims assessed yet</p>
            ) : (
              <div className="space-y-2">
                {(claims || []).slice(0, 3).map((claim) => (
                  <div key={claim.id} className="flex items-center justify-between p-2 rounded">
                    <div>
                      <p className="text-xs font-medium">{claim.claim_type}</p>
                      <p className="text-xs text-[#9d9db0]">{claim.estimated_payout || 'Pending'}</p>
                    </div>
                    <span className="text-xs text-[#1dd1a1]">{claim.eligibility_score}%</span>
                  </div>
                ))}
              </div>
            )}
          </GlassCard>
        </div>
      </div>
    </div>
  )
}
