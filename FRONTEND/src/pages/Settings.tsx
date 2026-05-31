import { useAuth } from '@/hooks/useAuth'
import { GlassCard } from '@/components/GlassCard'
import { Settings as SettingsIcon, User, Bell, Shield, Palette, ChevronRight } from 'lucide-react'

export function Settings() {
  const { user } = useAuth()

  const sections = [
    { icon: <User className="w-4 h-4" />, title: 'Profile', desc: 'Manage your personal information' },
    { icon: <Bell className="w-4 h-4" />, title: 'Notifications', desc: 'Configure notification preferences' },
    { icon: <Shield className="w-4 h-4" />, title: 'Privacy & Security', desc: 'Manage your data and privacy settings' },
    { icon: <Palette className="w-4 h-4" />, title: 'Appearance', desc: 'Customize the interface theme' },
  ]

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-[#9d9db0] text-sm mt-1">Manage your account and preferences</p>
      </div>

      <GlassCard>
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 rounded-full bg-[#1dd1a1]/10 flex items-center justify-center text-2xl">
            {user?.name?.[0] || 'U'}
          </div>
          <div>
            <h2 className="text-lg font-semibold">{user?.name || 'User'}</h2>
            <p className="text-sm text-[#9d9db0]">{user?.email}</p>
          </div>
        </div>
      </GlassCard>

      <div className="space-y-2">
        {sections.map((s) => (
          <GlassCard key={s.title} hover>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-[#1a1a2e]">{s.icon}</div>
                <div>
                  <p className="text-sm font-medium">{s.title}</p>
                  <p className="text-xs text-[#9d9db0]">{s.desc}</p>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-[#5a5a6e]" />
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  )
}
