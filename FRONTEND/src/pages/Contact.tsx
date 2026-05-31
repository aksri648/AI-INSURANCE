import { Link } from 'react-router-dom'

export function Contact() {
  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0f]/80 backdrop-blur-xl border-b border-[#2a2a3e]">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold teal-gradient-text">Insurance Copilot</Link>
          <div className="flex items-center gap-4">
            <Link to="/features" className="text-[#9d9db0] hover:text-[#e8e8f0] text-sm">Features</Link>
            <Link to="/pricing" className="text-[#9d9db0] hover:text-[#e8e8f0] text-sm">Pricing</Link>
            <Link to="/about" className="text-[#9d9db0] hover:text-[#e8e8f0] text-sm">About</Link>
            <Link to="/sign-in" className="btn-secondary text-sm">Sign In</Link>
          </div>
        </div>
      </nav>
      <section className="pt-24 pb-16 px-6 max-w-2xl mx-auto">
        <h1 className="text-4xl font-bold mb-6">Contact Us</h1>
        <p className="text-[#9d9db0] mb-8">Have questions or feedback? We'd love to hear from you.</p>
        <div className="glass-card p-8">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <input type="email" className="input-field" placeholder="your@email.com" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Message</label>
              <textarea className="input-field min-h-[120px]" placeholder="How can we help?" />
            </div>
            <button className="btn-primary w-full">Send Message</button>
          </div>
        </div>
      </section>
    </div>
  )
}
