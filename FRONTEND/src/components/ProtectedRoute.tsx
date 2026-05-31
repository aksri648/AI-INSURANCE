import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '@clerk/clerk-react'

export function ProtectedRoute() {
  const { isSignedIn, isLoaded } = useAuth()

  if (!isLoaded) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#0a0a0f]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border border-[#1dd1a1] border-t-transparent mx-auto mb-4"></div>
          <div className="text-[#1dd1a1] text-lg">Loading authentication...</div>
        </div>
      </div>
    )
  }

  if (!isSignedIn) {
    return <Navigate to="/sign-in" replace />
  }

  return <Outlet />
}
