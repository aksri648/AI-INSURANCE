import { useAuth as useClerkAuth, useUser } from '@clerk/clerk-react'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import type { AuthUser } from '@/lib/clerk'

export function useAuth() {
  const { isSignedIn, isLoaded, getToken } = useClerkAuth()
  const { user: clerkUser } = useUser()
  const [user, setUser] = useState<AuthUser | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadUser() {
      if (!isSignedIn || !isLoaded) {
        setLoading(false)
        return
      }

      try {
        const token = await getToken()
        if (token) {
          api.setToken(token)
          const response = await api.get<AuthUser>('/auth/me')
          setUser(response)
        }
      } catch (err) {
        console.error('Failed to load user:', err)
      } finally {
        setLoading(false)
      }
    }

    loadUser()
  }, [isSignedIn, isLoaded, getToken])

  return {
    isSignedIn,
    isLoaded,
    user,
    clerkUser,
    loading,
    getToken,
  }
}
