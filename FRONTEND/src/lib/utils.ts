import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatCurrency(amount: string | number, currency = 'INR'): string {
  const num = typeof amount === 'string' ? parseFloat(amount.replace(/[^0-9.]/g, '')) : amount
  if (isNaN(num)) return String(amount)
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency, maximumFractionDigits: 0 }).format(num)
}

export function formatDate(date: string | Date): string {
  return new Intl.DateTimeFormat('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(new Date(date))
}

export function truncate(str: string, length = 100): string {
  if (str.length <= length) return str
  return str.slice(0, length) + '...'
}

export function getConfidenceBadge(confidence: string): { label: string; className: string } {
  switch (confidence) {
    case 'verified':
      return { label: '🟢 Verified', className: 'badge-verified' }
    case 'needs_review':
      return { label: '🟡 Needs Review', className: 'badge-review' }
    default:
      return { label: '🔴 Not Found', className: 'badge-notfound' }
  }
}

export function getSeverityColor(severity: string): string {
  switch (severity) {
    case 'critical': return '#ff6b6b'
    case 'high': return '#ff6b6b'
    case 'medium': return '#feca57'
    case 'low': return '#4facfe'
    default: return '#9d9db0'
  }
}
