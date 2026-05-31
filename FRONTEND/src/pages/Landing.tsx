import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Shield, FileSearch, BarChart3, Scale, GraduationCap, Building2 } from 'lucide-react'

export function Landing() {
  const features = [
    {
      icon: <FileSearch className="w-6 h-6 text-[#1dd1a1]" />,
      title: 'Policy Analysis',
      desc: 'Upload any insurance policy and get a complete breakdown of benefits, coverage, exclusions, and hidden clauses.',
    },
    {
      icon: <Scale className="w-6 h-6 text-[#4facfe]" />,
      title: 'Mis-Selling Detection',
      desc: 'AI-powered detection of misleading statements, hidden clauses, and unfair terms in your policies.',
    },
    {
      icon: <Shield className="w-6 h-6 text-[#feca57]" />,
      title: 'Claim Assessment',
      desc: 'Know your claim eligibility, estimated payout, and required documentation before filing.',
    },
    {
      icon: <BarChart3 className="w-6 h-6 text-[#a855f7]" />,
      title: 'Company Intelligence',
      desc: 'Research insurer claim settlement ratios, solvency, complaints, and trust scores.',
    },
    {
      icon: <GraduationCap className="w-6 h-6 text-[#1dd1a1]" />,
      title: 'Insurance Education',
      desc: 'Learn insurance concepts in simple language. No jargon, no confusion.',
    },
    {
      icon: <Building2 className="w-6 h-6 text-[#4facfe]" />,
      title: 'Coverage Health Check',
      desc: 'Determine if your coverage is adequate and get personalized recommendations.',
    },
  ]

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0f]/80 backdrop-blur-xl border-b border-[#2a2a3e]">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <span className="text-xl font-bold teal-gradient-text">Insurance Copilot</span>
          <div className="flex items-center gap-4">
            <Link to="/features" className="text-[#9d9db0] hover:text-[#e8e8f0] transition-colors text-sm">Features</Link>
            <Link to="/pricing" className="text-[#9d9db0] hover:text-[#e8e8f0] transition-colors text-sm">Pricing</Link>
            <Link to="/about" className="text-[#9d9db0] hover:text-[#e8e8f0] transition-colors text-sm">About</Link>
            <Link to="/sign-in" className="btn-secondary text-sm">Sign In</Link>
            <Link to="/sign-up" className="btn-primary text-sm">Get Started</Link>
          </div>
        </div>
      </nav>

      <section className="pt-32 pb-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold leading-tight mb-6">
              Your Insurance.{' '}
              <span className="teal-gradient-text">Explained.</span>
            </h1>
            <p className="text-xl text-[#9d9db0] max-w-2xl mx-auto mb-10 leading-relaxed">
              The evidence-based insurance intelligence platform that helps you understand every benefit, 
              coverage, exclusion, and clause in your insurance policies — in simple language.
            </p>
            <div className="flex items-center justify-center gap-4">
              <Link to="/sign-up" className="btn-primary text-lg px-8 py-3">
                Start Free
              </Link>
              <Link to="/features" className="btn-secondary text-lg px-8 py-3">
                See Features
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="py-20 px-6 border-t border-[#2a2a3e]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">Everything You Need</h2>
          <p className="text-[#9d9db0] text-center mb-12 max-w-2xl mx-auto">
            From policy analysis to claim assessment — make informed insurance decisions with AI-powered intelligence.
          </p>
          <div className="grid md:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: i * 0.1 }}
                className="glass-card p-6 hover:border-[#1dd1a1]/30 hover:shadow-glow transition-all duration-300"
              >
                <div className="mb-4">{f.icon}</div>
                <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
                <p className="text-[#9d9db0] text-sm leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 px-6 border-t border-[#2a2a3e]">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Evidence-Based. Always.</h2>
          <p className="text-[#9d9db0] text-lg mb-8">
            Every fact comes from your documents. Every statement is backed by evidence. 
            We never hallucinate policy details.
          </p>
          <div className="flex justify-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#1dd1a1]" />
              <span className="text-[#9d9db0]">Verified</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#feca57]" />
              <span className="text-[#9d9db0]">Needs Review</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#ff6b6b]" />
              <span className="text-[#9d9db0]">Not Found</span>
            </div>
          </div>
        </div>
      </section>

      <footer className="border-t border-[#2a2a3e] py-8 px-6">
        <div className="max-w-6xl mx-auto flex items-center justify-between text-sm text-[#5a5a6e]">
          <span>&copy; 2026 Insurance Copilot. All rights reserved.</span>
          <div className="flex gap-6">
            <Link to="/about" className="hover:text-[#9d9db0] transition-colors">About</Link>
            <Link to="/contact" className="hover:text-[#9d9db0] transition-colors">Contact</Link>
            <Link to="/pricing" className="hover:text-[#9d9db0] transition-colors">Pricing</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
