import { cn } from '@/lib/utils'
import { ReactNode } from 'react'

interface GlassCardProps {
  children: ReactNode
  className?: string
  hover?: boolean
  glow?: boolean
}

export function GlassCard({ children, className, hover = false, glow = false }: GlassCardProps) {
  return (
    <div
      className={cn(
        'glass-card p-6 transition-all duration-300',
        hover && 'hover:border-[#1dd1a1]/30 hover:shadow-glow',
        glow && 'glow-border',
        className
      )}
    >
      {children}
    </div>
  )
}
