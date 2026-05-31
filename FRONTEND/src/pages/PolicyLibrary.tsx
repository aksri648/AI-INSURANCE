import { Link } from 'react-router-dom'
import { usePolicies, useDeletePolicy } from '@/hooks/usePolicy'
import { GlassCard } from '@/components/GlassCard'
import { FileText, Plus, Trash2, MessageSquare, ChevronRight, Clock } from 'lucide-react'
import { formatDate } from '@/lib/utils'

export function PolicyLibrary() {
  const { data: policies, isLoading } = usePolicies()
  const deletePolicy = useDeletePolicy()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-pulse text-[#1dd1a1]">Loading policies...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Policy Library</h1>
          <p className="text-[#9d9db0] text-sm mt-1">
            {policies?.length || 0} policy{policies?.length !== 1 ? 'ies' : ''} uploaded
          </p>
        </div>
        <Link to="/upload" className="btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" />
          Upload New
        </Link>
      </div>

      {(!policies || policies.length === 0) ? (
        <GlassCard className="text-center py-16">
          <FileText className="w-16 h-16 text-[#2a2a3e] mx-auto mb-4" />
          <h2 className="text-lg font-semibold mb-2">No policies yet</h2>
          <p className="text-[#9d9db0] mb-6">Upload your first insurance policy to get started</p>
          <Link to="/upload" className="btn-primary inline-flex items-center gap-2">
            <Plus className="w-4 h-4" />
            Upload Policy
          </Link>
        </GlassCard>
      ) : (
        <div className="space-y-3">
          {policies.map((policy) => (
            <GlassCard key={policy.id} hover>
              <div className="flex items-center justify-between">
                <div className="flex items-start gap-4 flex-1">
                  <div className="p-2 rounded-lg bg-[#1dd1a1]/10">
                    <FileText className="w-5 h-5 text-[#1dd1a1]" />
                  </div>
                  <div className="flex-1">
                    <Link
                      to={`/policies/${policy.id}`}
                      className="text-lg font-semibold hover:text-[#1dd1a1] transition-colors"
                    >
                      {policy.title}
                    </Link>
                    <div className="flex items-center gap-4 mt-1 text-sm text-[#9d9db0]">
                      <span>{policy.insurer || 'Unknown Insurer'}</span>
                      <span className="capitalize">{policy.policy_type}</span>
                      <span className={`inline-flex items-center gap-1 ${
                        policy.status === 'analyzed' ? 'text-[#1dd1a1]' : 'text-[#feca57]'
                      }`}>
                        <span className={`w-1.5 h-1.5 rounded-full ${
                          policy.status === 'analyzed' ? 'bg-[#1dd1a1]' : 'bg-[#feca57]'
                        }`} />
                        {policy.status}
                      </span>
                    </div>
                    {policy.benefits && policy.benefits.length > 0 && (
                      <div className="flex items-center gap-2 mt-2">
                        {policy.benefits.slice(0, 4).map((b) => (
                          <span key={b.id || b.name} className="text-xs px-2 py-0.5 rounded bg-[#12121a] text-[#9d9db0]">
                            {b.name}
                          </span>
                        ))}
                        {policy.benefits.length > 4 && (
                          <span className="text-xs text-[#5a5a6e]">+{policy.benefits.length - 4} more</span>
                        )}
                      </div>
                    )}
                    <div className="flex items-center gap-4 mt-2 text-xs text-[#5a5a6e]">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {formatDate(policy.created_at)}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Link
                    to={`/policies/${policy.id}/chat`}
                    className="btn-ghost p-2"
                    title="Chat with policy"
                  >
                    <MessageSquare className="w-4 h-4" />
                  </Link>
                  <button
                    onClick={() => {
                      if (confirm('Delete this policy?')) deletePolicy.mutate(policy.id)
                    }}
                    className="btn-ghost p-2 text-[#ff6b6b] hover:bg-[#ff6b6b]/10"
                    title="Delete policy"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                  <Link
                    to={`/policies/${policy.id}`}
                    className="btn-ghost p-2"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            </GlassCard>
          ))}
        </div>
      )}
    </div>
  )
}
