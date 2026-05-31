import { Link } from 'react-router-dom'
import { Shield, Search, FileText, MessageSquare, BarChart3, Scale, Building2, GraduationCap, CheckCircle, AlertTriangle, Zap } from 'lucide-react'

export function Features() {
  const features = [
    {
      category: 'Policy Analysis',
      icon: <Search className="w-5 h-5 text-[#1dd1a1]" />,
      items: [
        'Upload PDF or image-based insurance policies',
        'AI extracts every benefit, coverage, and exclusion',
        'Structured coverage tables with amounts and conditions',
        'Waiting periods and hidden clause identification',
        'Simple language explanations for every term',
      ],
    },
    {
      category: 'Claim Assessment',
      icon: <Shield className="w-5 h-5 text-[#4facfe]" />,
      items: [
        'Check claim eligibility before filing',
        'Estimate possible claim payout amounts',
        'Identify required documentation',
        'Understand claim conditions and limits',
        'Get claim readiness score',
      ],
    },
    {
      category: 'Mis-Selling Detection',
      icon: <AlertTriangle className="w-5 h-5 text-[#feca57]" />,
      items: [
        'Detect misleading statements in policies',
        'Identify hidden clauses and unfair terms',
        'Flag exaggerated benefit claims',
        'Compare promised vs actual coverage',
        'Get actionable recommendations',
      ],
    },
    {
      category: 'Company Intelligence',
      icon: <Building2 className="w-5 h-5 text-[#a855f7]" />,
      items: [
        'Research insurer claim settlement ratios',
        'View solvency ratios and financial health',
        'Check complaint data and customer reviews',
        'Compare multiple insurance companies',
        'IRDAI compliance status',
      ],
    },
    {
      category: 'Insurance Education',
      icon: <GraduationCap className="w-5 h-5 text-[#1dd1a1]" />,
      items: [
        'Learn insurance concepts at 8th-grade level',
        'Interactive explanations with examples',
        'No jargon without explanation',
        'Related topic recommendations',
        'Build insurance literacy over time',
      ],
    },
    {
      category: 'Reports & Insights',
      icon: <BarChart3 className="w-5 h-5 text-[#4facfe]" />,
      items: [
        '25-section comprehensive report',
        'Coverage adequacy assessment',
        'Personalized recommendations',
        'Example claim scenarios with estimates',
        'Final verdict with pros and cons',
      ],
    },
  ]

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0f]/80 backdrop-blur-xl border-b border-[#2a2a3e]">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold teal-gradient-text">Insurance Copilot</Link>
          <div className="flex items-center gap-4">
            <Link to="/features" className="text-[#1dd1a1] text-sm">Features</Link>
            <Link to="/pricing" className="text-[#9d9db0] hover:text-[#e8e8f0] text-sm">Pricing</Link>
            <Link to="/about" className="text-[#9d9db0] hover:text-[#e8e8f0] text-sm">About</Link>
            <Link to="/sign-in" className="btn-secondary text-sm">Sign In</Link>
            <Link to="/sign-up" className="btn-primary text-sm">Get Started</Link>
          </div>
        </div>
      </nav>

      <section className="pt-24 pb-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold text-center mb-4">All Features</h1>
          <p className="text-[#9d9db0] text-center mb-16 max-w-2xl mx-auto">
            Everything you need to understand, analyze, and optimize your insurance coverage.
          </p>

          <div className="space-y-8">
            {features.map((f) => (
              <div key={f.category} className="glass-card p-8">
                <div className="flex items-center gap-3 mb-6">
                  {f.icon}
                  <h2 className="text-xl font-semibold">{f.category}</h2>
                </div>
                <div className="grid md:grid-cols-2 gap-3">
                  {f.items.map((item) => (
                    <div key={item} className="flex items-start gap-2 text-[#9d9db0]">
                      <CheckCircle className="w-4 h-4 text-[#1dd1a1] mt-0.5 shrink-0" />
                      <span>{item}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link to="/sign-up" className="btn-primary text-lg px-8 py-3">
              Get Started Free
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
