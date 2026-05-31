import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ClerkProvider } from '@clerk/clerk-react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { Layout } from '@/components/Layout'

import { Landing } from '@/pages/Landing'
import { Features } from '@/pages/Features'
import { Pricing } from '@/pages/Pricing'
import { About } from '@/pages/About'
import { Contact } from '@/pages/Contact'
import { SignIn } from '@/pages/SignIn'
import { SignUp } from '@/pages/SignUp'
import { Dashboard } from '@/pages/Dashboard'
import { Upload } from '@/pages/Upload'
import { PolicyLibrary } from '@/pages/PolicyLibrary'
import { PolicyAnalysis } from '@/pages/PolicyAnalysis'
import { PolicyChat } from '@/pages/PolicyChat'
import { Claims } from '@/pages/Claims'
import { MisSellingDetector } from '@/pages/MisSellingDetector'
import { CompanyIntelligence } from '@/pages/CompanyIntelligence'
import { LearningCenter } from '@/pages/LearningCenter'
import { Settings } from '@/pages/Settings'
import { InsuranceHealthCheck } from '@/pages/InsuranceHealthCheck'

const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

if (!clerkPubKey) {
  console.error('VITE_CLERK_PUBLISHABLE_KEY is not set in .env file')
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 30000,
    },
  },
})

export default function App() {
  if (!clerkPubKey) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center p-6">
        <div className="glass-card p-8 max-w-md w-full text-center">
          <h1 className="text-xl font-bold text-[#ff6b6b] mb-4">Configuration Error</h1>
          <p className="text-[#9d9db0] mb-4">
            VITE_CLERK_PUBLISHABLE_KEY is not configured.
          </p>
          <p className="text-sm text-[#5a5a6e]">
            Please add your Clerk Publishable Key to the .env file in the FRONTEND directory.
            You can get it from <a href="https://dashboard.clerk.com" className="text-[#1dd1a1]">https://dashboard.clerk.com</a>
          </p>
        </div>
      </div>
    )
  }

  return (
    <ClerkProvider publishableKey={clerkPubKey}>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/features" element={<Features />} />
            <Route path="/pricing" element={<Pricing />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/sign-in" element={<SignIn />} />
            <Route path="/sign-up" element={<SignUp />} />

            <Route element={<ProtectedRoute />}>
              <Route element={<Layout />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/upload" element={<Upload />} />
                <Route path="/policies" element={<PolicyLibrary />} />
                <Route path="/policies/:id" element={<PolicyAnalysis />} />
                <Route path="/policies/:id/chat" element={<PolicyChat />} />
                <Route path="/claims" element={<Claims />} />
                <Route path="/mis-selling" element={<MisSellingDetector />} />
                <Route path="/companies" element={<CompanyIntelligence />} />
                <Route path="/learn" element={<LearningCenter />} />
                <Route path="/health-check" element={<InsuranceHealthCheck />} />
                <Route path="/settings" element={<Settings />} />
              </Route>
            </Route>

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </ClerkProvider>
  )
}
