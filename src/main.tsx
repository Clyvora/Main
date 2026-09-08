import { useEffect, useRef, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { Analytics } from '@vercel/analytics/react'
import { ArrowUpRight, Moon, Sun } from 'lucide-react'
import './styles.css'

const apps = [
  { name: 'Lens', description: 'Explore JSON & CSV.', image: '/apps/lens.webp', href: 'https://www.lens.clyvora.tech/' },
  { name: 'Convert', description: 'Convert audio & video.', image: '/apps/convert.webp', href: 'https://www.convert.clyvora.tech/' },
] as const

function AppCard({ app }: { app: typeof apps[number] }) {
  const card = useRef<HTMLElement>(null)
  useEffect(() => {
    const element = card.current!
    const motion = window.matchMedia('(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)')
    let frame = 0
    const reset = () => {
      cancelAnimationFrame(frame)
      for (const property of ['--tilt-x', '--tilt-y', '--art-x', '--art-y']) element.style.removeProperty(property)
    }
    const move = (event: PointerEvent) => {
      if (!motion.matches || event.pointerType === 'touch') return
      const bounds = element.getBoundingClientRect()
      const x = (event.clientX - bounds.left) / bounds.width - .5
      const y = (event.clientY - bounds.top) / bounds.height - .5
      cancelAnimationFrame(frame)
      frame = requestAnimationFrame(() => {
        element.style.setProperty('--tilt-x', `${-y * 5}deg`)
        element.style.setProperty('--tilt-y', `${x * 5}deg`)
        element.style.setProperty('--art-x', `${x * 15}px`)
        element.style.setProperty('--art-y', `${y * 12}px`)
      })
    }
    element.addEventListener('pointermove', move)
    element.addEventListener('pointerleave', reset)
    motion.addEventListener('change', reset)
    return () => {
      reset()
      element.removeEventListener('pointermove', move)
      element.removeEventListener('pointerleave', reset)
      motion.removeEventListener('change', reset)
    }
  }, [])
  return <article ref={card} className={`app-card app-${app.name.toLowerCase()}`} aria-labelledby={`${app.name}-title`}>
    <div className="card-surface">
      <div className="app-art" aria-hidden="true"><div className="art-parallax"><img src={app.image} alt="" width="420" height="420" fetchPriority="high" /></div></div>
      <div className="app-details">
        <h2 id={`${app.name}-title`}>{app.name}</h2>
        <p>{app.description}</p>
        <a className="open-app" href={app.href} target="_blank" rel="noreferrer">
          <span>Open {app.name}</span><ArrowUpRight size={19} strokeWidth={1.65} aria-hidden="true" />
          <span className="sr-only"> (opens in a new tab)</span>
        </a>
      </div>
    </div>
  </article>
}

function App() {
  const [theme, setTheme] = useState(() => document.documentElement.dataset.theme === 'light' ? 'light' : 'dark')
  useEffect(() => {
    document.documentElement.dataset.theme = theme
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#151515' : '#fafafa')
    try { localStorage.setItem('clyvora-theme', theme) } catch { /* Theme remains usable without storage. */ }
  }, [theme])
  return <div className="site-shell">
    <a href="#apps" className="skip-link">Skip to apps</a>
    <header className="site-header">
      <div className="brand">
        <svg className="brand-mark" width="46" height="46" viewBox="0 0 48 48" fill="none" aria-hidden="true">
          <path d="M37.5 10.5A19 19 0 1 0 37.5 37.5" stroke="currentColor" strokeWidth="8" strokeLinecap="round" />
          <path d="M30 19a8 8 0 1 0 0 10" stroke="currentColor" strokeWidth="5" strokeLinecap="round" />
        </svg>
        <h1>Clyvora</h1>
      </div>
      <button className="theme-toggle" type="button" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}>
        {theme === 'dark' ? <Sun size={19} strokeWidth={1.6} /> : <Moon size={19} strokeWidth={1.6} />}
      </button>
    </header>
    <main id="apps" className="app-gallery" aria-label="Clyvora apps">{apps.map(app => <AppCard key={app.name} app={app} />)}</main>
    <footer className="site-footer">
      <span>© {new Date().getFullYear()} Clyvora</span>
      <nav aria-label="More about Clyvora"><a href="/about/">About</a><a href="https://github.com/Clyvora" target="_blank" rel="noreferrer">GitHub <span className="sr-only">(opens in a new tab)</span></a></nav>
    </footer>
  </div>
}
createRoot(document.getElementById('root')!).render(<><App /><Analytics /></>)
