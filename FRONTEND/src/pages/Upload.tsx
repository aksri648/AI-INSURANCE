import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useUploadPolicy } from '@/hooks/usePolicy'
import { GlassCard } from '@/components/GlassCard'
import { Upload as UploadIcon, File, X, ChevronRight } from 'lucide-react'

export function Upload() {
  const navigate = useNavigate()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [file, setFile] = useState<File | null>(null)
  const [title, setTitle] = useState('')
  const [insurer, setInsurer] = useState('')
  const [policyNumber, setPolicyNumber] = useState('')
  const [policyType, setPolicyType] = useState('general')
  const uploadMutation = useUploadPolicy()

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile && isValidFile(droppedFile)) {
      setFile(droppedFile)
      if (!title) setTitle(droppedFile.name.replace(/\.[^/.]+$/, ''))
    }
  }

  const isValidFile = (f: File) => {
    const valid = ['application/pdf', 'image/png', 'image/jpeg']
    return valid.includes(f.type)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file || !title) return

    const formData = new FormData()
    formData.append('file', file)
    formData.append('title', title)
    if (insurer) formData.append('insurer', insurer)
    if (policyNumber) formData.append('policy_number', policyNumber)
    formData.append('policy_type', policyType)

    try {
      const result = await uploadMutation.mutateAsync(formData)
      navigate(`/policies/${result.id}`)
    } catch (err) {
      console.error('Upload failed:', err)
    }
  }

  const policyTypes = [
    { value: 'health', label: 'Health Insurance' },
    { value: 'life', label: 'Life Insurance' },
    { value: 'motor', label: 'Motor Insurance' },
    { value: 'home', label: 'Home Insurance' },
    { value: 'travel', label: 'Travel Insurance' },
    { value: 'term', label: 'Term Insurance' },
    { value: 'general', label: 'General Insurance' },
  ]

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Upload Policy</h1>
        <p className="text-[#9d9db0] text-sm mt-1">
          Upload your insurance policy document to get a complete analysis
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          onClick={() => fileInputRef.current?.click()}
          className="glass-card p-12 text-center cursor-pointer hover:border-[#1dd1a1]/30 transition-all"
        >
          {file ? (
            <div className="flex items-center justify-center gap-4">
              <File className="w-8 h-8 text-[#1dd1a1]" />
              <div className="text-left">
                <p className="font-medium">{file.name}</p>
                <p className="text-sm text-[#9d9db0]">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
              <button
                type="button"
                onClick={(e) => { e.stopPropagation(); setFile(null) }}
                className="p-1 hover:bg-[#2a2a3e] rounded"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <>
              <UploadIcon className="w-12 h-12 text-[#2a2a3e] mx-auto mb-4" />
              <p className="text-[#9d9db0] mb-2">
                Drop your policy document here or click to browse
              </p>
              <p className="text-xs text-[#5a5a6e]">
                Supports PDF, PNG, JPG (max 50 MB)
              </p>
            </>
          )}
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.png,.jpg,.jpeg"
            className="hidden"
            onChange={(e) => {
              const f = e.target.files?.[0]
              if (f) {
                setFile(f)
                if (!title) setTitle(f.name.replace(/\.[^/.]+$/, ''))
              }
            }}
          />
        </div>

        <GlassCard>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Policy Title *</label>
              <input
                className="input-field"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g., My Health Insurance Policy"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Insurer</label>
                <input
                  className="input-field"
                  value={insurer}
                  onChange={(e) => setInsurer(e.target.value)}
                  placeholder="e.g., ICICI Lombard"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Policy Number</label>
                <input
                  className="input-field"
                  value={policyNumber}
                  onChange={(e) => setPolicyNumber(e.target.value)}
                  placeholder="Optional"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Policy Type</label>
              <select
                className="input-field"
                value={policyType}
                onChange={(e) => setPolicyType(e.target.value)}
              >
                {policyTypes.map((t) => (
                  <option key={t.value} value={t.value}>{t.label}</option>
                ))}
              </select>
            </div>
          </div>
        </GlassCard>

        <button
          type="submit"
          disabled={!file || !title || uploadMutation.isPending}
          className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {uploadMutation.isPending ? (
            'Processing...'
          ) : (
            <>
              Upload & Analyze
              <ChevronRight className="w-4 h-4" />
            </>
          )}
        </button>
      </form>
    </div>
  )
}
