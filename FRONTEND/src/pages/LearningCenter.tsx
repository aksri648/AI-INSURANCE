import { useState } from 'react'
import { GlassCard } from '@/components/GlassCard'
import { api } from '@/lib/api'
import { useAuth } from '@/hooks/useAuth'
import { GraduationCap, Search, BookOpen, Lightbulb, ChevronRight } from 'lucide-react'

const commonTopics = [
  'What is a deductible?',
  'What is a waiting period?',
  'What is a copay?',
  'What is claim settlement ratio?',
  'What is no-claim bonus?',
  'What is a premium?',
  'What is sum insured?',
  'What are policy exclusions?',
  'What is portability?',
  'What is a rider?',
]

export function LearningCenter() {
  const { getToken } = useAuth()
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Record<string, unknown> | null>(null)

  const learn = async (q: string) => {
    setQuery(q)
    setLoading(true)
    try {
      const token = await getToken()
      if (token) api.setToken(token)
      const res = await api.post('/education/explain', { query: q, difficulty: 'beginner' })
      setResult(res as Record<string, unknown>)
    } catch (err) {
      console.error('Education query failed:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Learning Center</h1>
        <p className="text-[#9d9db0] text-sm mt-1">Understand insurance concepts in simple language</p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 space-y-6">
          <GlassCard>
            <div className="flex gap-3">
              <input
                className="input-field flex-1"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask any insurance question..."
                onKeyDown={(e) => e.key === 'Enter' && learn(query)}
              />
              <button onClick={() => learn(query)} disabled={loading || !query} className="btn-primary">
                {loading ? '...' : <Search className="w-4 h-4" />}
              </button>
            </div>
          </GlassCard>

          {result && (
            <GlassCard>
              <div className="flex items-center gap-2 mb-4">
                <BookOpen className="w-5 h-5 text-[#1dd1a1]" />
                <h2 className="text-lg font-semibold">{result.topic as string}</h2>
              </div>
              <div className="text-sm text-[#9d9db0] leading-relaxed whitespace-pre-wrap mb-6">
                {result.explanation as string}
              </div>
              {(result.key_takeaways as string[] || []).length > 0 && (
                <div className="mb-4">
                  <h3 className="text-sm font-medium text-[#1dd1a1] mb-2">Key Takeaways</h3>
                  <ul className="space-y-1">
                    {(result.key_takeaways as string[]).map((t, i) => (
                      <li key={i} className="text-sm text-[#9d9db0] flex items-start gap-2">
                        <Lightbulb className="w-3 h-3 text-[#feca57] mt-1 shrink-0" />
                        {t}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {(result.related_topics as string[] || []).length > 0 && (
                <div>
                  <h3 className="text-sm font-medium text-[#4facfe] mb-2">Related Topics</h3>
                  <div className="flex flex-wrap gap-2">
                    {(result.related_topics as string[]).map((t, i) => (
                      <button key={i} onClick={() => learn(t)} className="text-xs px-3 py-1.5 rounded-full bg-[#12121a] border border-[#2a2a3e] text-[#9d9db0] hover:border-[#4facfe]/30 hover:text-[#4facfe] transition-colors">
                        {t}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </GlassCard>
          )}
        </div>

        <div className="space-y-4">
          <GlassCard>
            <h2 className="section-title flex items-center gap-2">
              <GraduationCap className="w-4 h-4 text-[#1dd1a1]" />
              Common Topics
            </h2>
            <div className="space-y-1">
              {commonTopics.map((topic) => (
                <button
                  key={topic}
                  onClick={() => learn(topic)}
                  className="w-full flex items-center justify-between p-2 rounded text-sm text-[#9d9db0] hover:text-[#e8e8f0] hover:bg-[#12121a] transition-colors text-left"
                >
                  {topic}
                  <ChevronRight className="w-3 h-3" />
                </button>
              ))}
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  )
}
