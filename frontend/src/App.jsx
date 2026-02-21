import { useState, useCallback } from 'react'
import './App.css'

const API_BASE = '/api'

function App() {
  const [pdfFile, setPdfFile] = useState(null)
  const [imageFile, setImageFile] = useState(null)
  const [qualidade, setQualidade] = useState(40)
  const [status, setStatus] = useState({ type: null, message: '' })
  const [loading, setLoading] = useState(false)

  const clearStatus = useCallback(() => {
    setStatus({ type: null, message: '' })
  }, [])

  const handlePdfChange = (e) => {
    const file = e.target.files?.[0]
    setPdfFile(file || null)
    clearStatus()
  }

  const handleImageChange = (e) => {
    const file = e.target.files?.[0]
    setImageFile(file || null)
    clearStatus()
  }

  const downloadBlob = (blob, filename) => {
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  const compressPdf = async () => {
    if (!pdfFile) {
      setStatus({ type: 'error', message: 'Selecione um arquivo PDF.' })
      return
    }
    setLoading(true)
    setStatus({ type: 'info', message: 'Comprimindo PDF...' })
    try {
      const form = new FormData()
      form.append('file', pdfFile)
      const res = await fetch(`${API_BASE}/compress/pdf`, {
        method: 'POST',
        body: form,
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.error || data.detail || `Erro ${res.status}`)
      }
      const blob = await res.blob()
      const name = res.headers.get('Content-Disposition')?.match(/filename="?([^";]+)"?/)?.[1]
        || pdfFile.name.replace('.pdf', '_comprimido.pdf')
      downloadBlob(blob, name)
      setStatus({ type: 'success', message: 'PDF comprimido! O download foi iniciado.' })
      setPdfFile(null)
    } catch (err) {
      setStatus({ type: 'error', message: err.message || 'Erro ao comprimir PDF.' })
    } finally {
      setLoading(false)
    }
  }

  const compressImage = async () => {
    if (!imageFile) {
      setStatus({ type: 'error', message: 'Selecione uma imagem (JPG ou PNG).' })
      return
    }
    setLoading(true)
    setStatus({ type: 'info', message: 'Comprimindo imagem...' })
    try {
      const form = new FormData()
      form.append('file', imageFile)
      form.append('qualidade', String(qualidade))
      const res = await fetch(`${API_BASE}/compress/image`, {
        method: 'POST',
        body: form,
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.error || data.detail || `Erro ${res.status}`)
      }
      const blob = await res.blob()
      const name = res.headers.get('Content-Disposition')?.match(/filename="?([^";]+)"?/)?.[1]
        || imageFile.name.replace(/(\.[^.]+)$/, '_comprimido$1')
      downloadBlob(blob, name)
      setStatus({ type: 'success', message: 'Imagem comprimida! O download foi iniciado.' })
      setImageFile(null)
    } catch (err) {
      setStatus({ type: 'error', message: err.message || 'Erro ao comprimir imagem.' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Compressor de Arquivos</h1>
        <p>Reduza o tamanho de PDFs e imagens (JPG/PNG) antes de enviar.</p>
      </header>

      <main className="main">
        <section className="card">
          <h2>Comprimir PDF</h2>
          <p className="card-desc">Ghostscript reduz o tamanho do arquivo.</p>
          <div className="upload-zone">
            <input
              type="file"
              id="pdf-input"
              accept=".pdf"
              onChange={handlePdfChange}
              disabled={loading}
            />
            <label htmlFor="pdf-input" className="upload-label">
              {pdfFile ? pdfFile.name : 'Clique ou arraste um PDF'}
            </label>
          </div>
          <button
            type="button"
            className="btn btn-primary"
            onClick={compressPdf}
            disabled={!pdfFile || loading}
          >
            {loading ? 'Comprimindo…' : 'Comprimir PDF'}
          </button>
        </section>

        <section className="card">
          <h2>Comprimir Imagem</h2>
          <p className="card-desc">JPG e PNG. Ajuste a qualidade para JPG.</p>
          <div className="upload-zone">
            <input
              type="file"
              id="image-input"
              accept=".jpg,.jpeg,.png"
              onChange={handleImageChange}
              disabled={loading}
            />
            <label htmlFor="image-input" className="upload-label">
              {imageFile ? imageFile.name : 'Clique ou arraste uma imagem'}
            </label>
          </div>
          <div className="qualidade-row">
            <label htmlFor="qualidade">Qualidade JPG (1–100):</label>
            <input
              id="qualidade"
              type="range"
              min="1"
              max="100"
              value={qualidade}
              onChange={(e) => setQualidade(Number(e.target.value))}
              disabled={loading}
            />
            <span className="qualidade-value">{qualidade}</span>
          </div>
          <button
            type="button"
            className="btn btn-primary"
            onClick={compressImage}
            disabled={!imageFile || loading}
          >
            {loading ? 'Comprimindo…' : 'Comprimir Imagem'}
          </button>
        </section>
      </main>

      {status.message && (
        <div className={`toast toast-${status.type}`} role="alert">
          {status.message}
        </div>
      )}
    </div>
  )
}

export default App
