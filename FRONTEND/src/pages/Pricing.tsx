import { Link } from 'react-router-dom'
import { CheckCircle } from 'lucide-react'

export function Pricing() {
  const plans = [
    {
      name: 'Free',
      price: '₹0',
      desc: 'Get started with basic insurance intelligence',
      features: [
        '1 policy upload per month',
        'Basic policy analysis',
        'AI chat with policy',
        'Limited education content',
        'Standard report format',
      ],
      cta: 'Start Free',
      featured: false,
    },
    {
      name: 'Pro',
      price: '₹499',
      period: '/month',
      desc: 'For individuals who want full coverage intelligence',
      features: [
        '25 policy uploads per month',
        'Full policy analysis with benefits table',
        'Claims assessment & estimation',
        'Mis-selling detection',
        'Company intelligence reports',
        'Full education library',
        '25-section comprehensive report',
        'Priority support',
      ],
      cta: 'Start Free Trial',
      featured: true,
    },
    {
      name: 'Family',
      price: '₹999',
      period: '/month',
      desc: 'For families managing multiple policies',
      features: [
        '100 policy uploads per month',
        'Everything in Pro',
        'Family coverage dashboard',
        'Multi-policy comparison',
        'Recommendation engine',
        'Coverage health check',
        'Premium support',
      ],
      cta: 'Start Free Trial',
      featured: false,
    },
  ]

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0f]/80 backdrop-blur-xl border-b border-[#2a2a3e]">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold teal-gradient-text">Insurance Copilot</Link>
          <div className="flex items-center gap-4">
            <Link to="/features" className="text-[#9d9db0] hover:text-[#e8e8f0] text-sm">Features</Link>
            <Link to="/pricing" className="text-[#1dd1a1] text-sm">Pricing</Link>
            <Link to="/about" className="text-[#9d9db0] hover:text-[#e8e8f0] text-sm">About</Link>
            <Link to="/sign-in" className="btn-secondary text-sm">Sign In</Link>
            <Link to="/sign-up" className="btn-primary text-sm">Get Started</Link>
          </div>
        </div>
      </nav>

      <section className="pt-24 pb-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold text-center mb-4">Simple, Transparent Pricing</h1>
          <p className="text-[#9d9db0] text-center mb-12 max-w-2xl mx-auto">
            No hidden fees. No surprises. Just the tools you need to understand your insurance.
          </p>

          <div className="grid md:grid-cols-3 gap-6">
            {plans.map((plan) => (
              <div
                key={plan.name}
                className={`glass-card p-8 relative ${
                  plan.featured
                    ? 'border-[#1dd1a1]/40 shadow-glow'
                    : ''
                }`}
              >
                {plan.featured && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 bg-[#1dd1a1] text-[#0a0a0f] text-xs font-bold rounded-full">
                    MOST POPULAR
                  </div>
                )}
                <h2 className="text-xl font-bold mb-2">{plan.name}</h2>
                <div className="mb-4">
                  <span className="text-3xl font-bold">{plan.price}</span>
                  {plan.period && <span className="text-[#9d9db0] text-sm">{plan.period}</span>}
                </div>
                <p className="text-[#9d9db0] text-sm mb-6">{plan.desc}</p>
                <Link
                  to="/sign-up"
                  className={`block text-center py-2.5 rounded-lg font-medium transition-all mb-6 ${
                    plan.featured
                      ? 'btn-primary'
                      : 'btn-secondary'
                  }`}
                >
                  {plan.cta}
                </Link>
                <ul className="space-y-3">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-start gap-2 text-sm text-[#9d9db0]">
                      <CheckCircle className="w-4 h-4 text-[#1dd1a1] mt-0.5 shrink-0" />
                      {f}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
