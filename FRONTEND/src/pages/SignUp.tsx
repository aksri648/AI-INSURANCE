import { SignUp as ClerkSignUp } from '@clerk/clerk-react'
import { Link } from 'react-router-dom'

export function SignUp() {
  return (
    <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center p-6">
      <div className="glass-card p-8 max-w-md w-full">
        <div className="text-center mb-6">
          <Link to="/" className="text-xl font-bold teal-gradient-text">Insurance Copilot</Link>
          <p className="text-[#9d9db0] text-sm mt-2">Create your account</p>
        </div>
        <ClerkSignUp
          appearance={{
            elements: {
              rootBox: 'w-full',
              card: 'bg-transparent shadow-none',
              headerTitle: 'text-[#e8e8f0]',
              headerSubtitle: 'text-[#9d9db0]',
              formFieldLabel: 'text-[#e8e8f0]',
              formFieldInput: 'input-field',
              formButtonPrimary: 'btn-primary w-full',
              footerActionLink: 'text-[#1dd1a1]',
              dividerLine: 'bg-[#2a2a3e]',
              dividerText: 'text-[#5a5a6e]',
              socialButtonsBlockButton: 'btn-secondary w-full',
            },
          }}
        />
      </div>
    </div>
  )
}
