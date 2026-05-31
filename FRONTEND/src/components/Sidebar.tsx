import { NavLink } from 'react-router-dom'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard,
  Upload,
  FileText,
  MessageSquare,
  Shield,
  Scale,
  Building2,
  GraduationCap,
  Settings,
  User,
  ChevronLeft,
} from 'lucide-react'
import { useState } from 'react'

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/upload', icon: Upload, label: 'Upload Policy' },
  { to: '/policies', icon: FileText, label: 'Policy Library' },
  { to: '/claims', icon: Shield, label: 'Claims' },
  { to: '/mis-selling', icon: Scale, label: 'Mis-Selling Detector' },
  { to: '/companies', icon: Building2, label: 'Company Intelligence' },
  { to: '/learn', icon: GraduationCap, label: 'Learning Center' },
]

const bottomItems = [
  { to: '/settings', icon: Settings, label: 'Settings' },
  { to: '/profile', icon: User, label: 'Profile' },
]

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 h-screen bg-[#12121a]/90 backdrop-blur-xl border-r border-[#2a2a3e] flex flex-col transition-all duration-300 z-50',
        collapsed ? 'w-16' : 'w-60'
      )}
    >
      <div className="flex items-center justify-between p-4 border-b border-[#2a2a3e]">
        {!collapsed && (
          <span className="text-lg font-bold teal-gradient-text tracking-tight">
            Insurance Copilot
          </span>
        )}
        {collapsed && (
          <span className="text-lg font-bold teal-gradient-text mx-auto">IC</span>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="btn-ghost p-1.5"
        >
          <ChevronLeft className={cn('w-4 h-4 transition-transform', collapsed && 'rotate-180')} />
        </button>
      </div>

      <nav className="flex-1 p-3 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 text-sm',
                isActive
                  ? 'bg-[#1dd1a1]/10 text-[#1dd1a1] border border-[#1dd1a1]/20'
                  : 'text-[#9d9db0] hover:text-[#e8e8f0] hover:bg-[#1a1a2e]',
                collapsed && 'justify-center px-2'
              )
            }
          >
            <item.icon className="w-4 h-4 shrink-0" />
            {!collapsed && <span>{item.label}</span>}
          </NavLink>
        ))}
      </nav>

      <div className="p-3 border-t border-[#2a2a3e] space-y-1">
        {bottomItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 text-sm',
                isActive
                  ? 'bg-[#1dd1a1]/10 text-[#1dd1a1] border border-[#1dd1a1]/20'
                  : 'text-[#9d9db0] hover:text-[#e8e8f0] hover:bg-[#1a1a2e]',
                collapsed && 'justify-center px-2'
              )
            }
          >
            <item.icon className="w-4 h-4 shrink-0" />
            {!collapsed && <span>{item.label}</span>}
          </NavLink>
        ))}
      </div>
    </aside>
  )
}
