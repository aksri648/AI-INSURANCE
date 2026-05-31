import { Link } from 'react-router-dom'

export function About() {
  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0f]/80 backdrop-blur-xl border-b border-[#2a2a3e]">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold teal-gradient-text">Insurance Copilot</Link>
          <div className="flex items-center gap-4">
            <Link to="/features" className="text-[#9d9db0] hover:text-[#e8e8f0] text-sm">Features</Link>
            <Link to="/pricing" className="text-[#9d9db0] hover:text-[#e8e8f0] text-sm">Pricing</Link>
            <Link to="/about" className="text-[#1dd1a1] text-sm">About</Link>
            <Link to="/sign-in" className="btn-secondary text-sm">Sign In</Link>
          </div>
        </div>
      </nav>
      <section className="pt-24 pb-16 px-6 max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold mb-6">About Insurance Copilot</h1>
        <div className="space-y-4 text-[#9d9db0] leading-relaxed">
          <p>Insurance Copilot is an evidence-based insurance intelligence platform designed to help consumers understand their insurance policies completely.</p>
          <p>Insurance policies are complex legal documents filled with jargon, hidden clauses, and fine print. Most people sign up without fully understanding what they're covered for — or what they're not.</p>
          <p>We built Insurance Copilot to change that. Our AI-powered system reads your policy documents, extracts every benefit, coverage, exclusion, and condition, and presents them in simple, understandable language.</p>
          <p>Every fact is backed by evidence from your documents. We never hallucinate insurance details. If we can't find the information, we tell you honestly.</p>
        </div>
      </section>
    </div>
  )
}
