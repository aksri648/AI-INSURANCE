import { cn } from '@/lib/utils'

interface StatCardProps {
  label: string
  value: string | number
  icon?: string
  trend?: 'up' | 'down' | 'neutral'
  className?: string
}

export function StatCard({ label, value, icon, trend, className }: StatCardProps) {
  const trendColors = {
    up: 'text-[#1dd1a1]',
    down: 'text-[#ff6b6b]',
    neutral: 'text-[#feca57]',
  }

  return (
    <div className={cn('glass-card p-5 text-center', className)}>
      {icon && <div className="text-2xl mb-2">{icon}</div>}
      <div className="stat-value">{value}</div>
      <div className="text-sm text-[#9d9db0] mt-1">{label}</div>
      {trend && (
        <div className={cn('text-xs mt-1 font-medium', trendColors[trend])}>
          {trend === 'up' && '↑ '}
          {trend === 'down' && '↓ '}
          {trend === 'neutral' && '→ '}
          {label}
        </div>
      )}
    </div>
  )
}
