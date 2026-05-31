import { useParams, Link } from 'react-router-dom'
import { useState } from 'react'
import { usePolicy } from '@/hooks/usePolicy'
import { GlassCard } from '@/components/GlassCard'
import { api } from '@/lib/api'
import { useAuth } from '@/hooks/useAuth'
import { ArrowLeft, Send, Bot, User as UserIcon, AlertCircle } from 'lucide-react'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export function PolicyChat() {
  const { id } = useParams<{ id: string }>()
  const { data: policy } = usePolicy(id)
  const { getToken } = useAuth()
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: `Hello! I'm your policy assistant. I can help you understand ${policy?.title || 'your policy'}. Ask me anything about benefits, coverage, exclusions, or claim process.`,
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMsg: ChatMessage = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const token = await getToken()
      if (token) api.setToken(token)

      const response = await api.post<{ reply: string; sources: unknown[]; confidence: string }>(
        `/chat/policy/${id}`,
        {
          message: input,
          conversation_history: messages.map((m) => ({ role: m.role, content: m.content })),
        }
      )

      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: response.reply },
      ])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)]">
      <div className="flex items-center gap-4 mb-4">
        <Link to={`/policies/${id}`} className="btn-ghost p-2">
          <ArrowLeft className="w-4 h-4" />
        </Link>
        <div>
          <h1 className="text-lg font-bold">Chat with Policy</h1>
          <p className="text-xs text-[#9d9db0]">{policy?.title}</p>
        </div>
      </div>

      <GlassCard className="flex-1 flex flex-col overflow-hidden">
        <div className="flex-1 overflow-y-auto space-y-4 p-4">
          {messages.map((msg, i) => (
            <div key={i} className={`flex items-start gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`p-2 rounded-full ${msg.role === 'user' ? 'bg-[#1dd1a1]/10' : 'bg-[#4facfe]/10'}`}>
                {msg.role === 'user' ? (
                  <UserIcon className="w-4 h-4 text-[#1dd1a1]" />
                ) : (
                  <Bot className="w-4 h-4 text-[#4facfe]" />
                )}
              </div>
              <div
                className={`max-w-[80%] p-3 rounded-lg text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-[#1dd1a1]/10 border border-[#1dd1a1]/20'
                    : 'glass-card'
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex items-center gap-2 text-sm text-[#9d9db0]">
              <div className="animate-pulse">Thinking</div>
              <span className="animate-pulse">...</span>
            </div>
          )}
        </div>

        <div className="border-t border-[#2a2a3e] p-4">
          <form
            onSubmit={(e) => { e.preventDefault(); sendMessage() }}
            className="flex gap-2"
          >
            <input
              className="input-field flex-1"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about your policy..."
              disabled={loading}
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="btn-primary p-2.5"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </GlassCard>
    </div>
  )
}
