import { useEffect, useRef, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { Analytics } from '@vercel/analytics/react'
import { ArrowLeft, ArrowRight, ArrowUpRight, Moon, Sun } from 'lucide-react'
import { TextMorph } from 'torph/react'
import './styles.css'

const apps = [
  { id: 'lens', name: 'Lens', description: 'Explore JSON & CSV.', detail: 'Open your data, find what matters, and export it in the format you need. All in your browser.', image: '/apps/lens.webp', href: 'https://www.lens.clyvora.tech/' },
  { id: 'convert', name: 'Convert', description: 'Convert audio & video.', detail: 'Choose a file or paste a SoundCloud link. Pick your format, adjust the quality, and download the result.', image: '/apps/convert.webp', href: 'https://www.convert.clyvora.tech/' },
  { id: 'liveopweg', name: 'Live op Weg', translation: 'Live on the Go', description: 'See live train locations.', detail: 'Follow trains on the map and see where they are as they travel. A live view of the railway, at a glance.', image: '/apps/liveopweg.svg', href: 'https://liveopweg.nl/' },
] as const

function Morph({ children, className, scale = true, spring = false }: { children: string; className?: string; scale?: boolean; spring?: boolean }) {
  const supported = typeof Element.prototype.animate === 'function' && typeof Element.prototype.getAnimations === 'function'
  return supported ? <TextMorph as="span" className={className} duration={550} ease={spring ? { stiffness: 180, damping: 12, mass: 0.8 } : undefined} scale={scale} respectReducedMotion>{children}</TextMorph> : <span className={className}>{children}</span>
}

function AppGallery() {
  const artwork = useRef<HTMLDivElement>(null)
  const [selected, setSelected] = useState(0)
  const [hovered, setHovered] = useState(false)
  const [focused, setFocused] = useState(false)
  const [hidden, setHidden] = useState(() => document.hidden)
  const [reduced, setReduced] = useState(() => window.matchMedia('(prefers-reduced-motion: reduce)').matches)
  const [cycle, setCycle] = useState(0)
  useEffect(() => {
    const motion = window.matchMedia('(prefers-reduced-motion: reduce)')
    const updateMotion = () => setReduced(motion.matches)
    const updateVisibility = () => setHidden(document.hidden)
    motion.addEventListener('change', updateMotion)
    document.addEventListener('visibilitychange', updateVisibility)
    return () => {
      motion.removeEventListener('change', updateMotion)
      document.removeEventListener('visibilitychange', updateVisibility)
    }
  }, [])
  const running = !hovered && !focused && !hidden && !reduced
  const choose = (index: number) => { setSelected(index); setCycle(value => value + 1) }
  const app = apps[selected]
  const step = (delta: number) => choose((selected + delta + apps.length) % apps.length)
  return <section className="gallery" aria-label="Explore Clyvora apps" aria-roledescription="carousel" data-running={running} data-reduced={reduced}
    onPointerEnter={event => { if (event.pointerType === 'mouse') setHovered(true) }} onPointerLeave={() => { setHovered(false); artwork.current?.style.removeProperty('transform') }}
    onPointerMove={event => {
      if (reduced || event.pointerType !== 'mouse' || !artwork.current) return
      const bounds = event.currentTarget.getBoundingClientRect()
      const x = (event.clientX - bounds.left) / bounds.width - .5
      const y = (event.clientY - bounds.top) / bounds.height - .5
      artwork.current.style.transform = `translate3d(${x * 18}px, ${y * 14}px, 0)`
    }}
    onFocusCapture={() => setFocused(true)} onBlurCapture={event => { if (!event.currentTarget.contains(event.relatedTarget)) setFocused(false) }}>
    <div className="gallery-stage" aria-live={running ? "off" : "polite"} aria-atomic="true">
      <article className="gallery-slide" aria-labelledby={`${app.id}-title`} aria-roledescription="slide">
        <div ref={artwork} className="app-art" aria-hidden="true"><img key={app.id} src={app.image} alt="" width="420" height="420" fetchPriority="high" /></div>
        <div className="app-details">
          <h2 id={`${app.id}-title`}><Morph>{app.name}</Morph><span className="app-translation"><Morph>{'translation' in app ? `(${app.translation})` : ''}</Morph></span></h2>
          <p className="app-tagline"><Morph>{app.description}</Morph></p>
          <p key={app.id} className="app-description">{app.detail}</p>
          <a className="open-app" href={app.href} target="_blank" rel="noreferrer">
            <Morph>{`Open ${app.name}`}</Morph><ArrowUpRight size={20} strokeWidth={1.65} aria-hidden="true" />
            <span className="sr-only"> (opens in a new tab)</span>
          </a>
        </div>
      </article>
    </div>
    <button type="button" className="gallery-arrow gallery-prev" aria-label="Previous app" onClick={() => step(-1)}><ArrowLeft size={20} aria-hidden="true" /></button>
    <button type="button" className="gallery-arrow gallery-next" aria-label="Next app" onClick={() => step(1)}><ArrowRight size={20} aria-hidden="true" /></button>
    <div className="gallery-selectors" role="group" aria-label="Choose an app" onKeyDown={event => {
      const buttons = Array.from(event.currentTarget.querySelectorAll('button'))
      const index = buttons.indexOf(document.activeElement as HTMLButtonElement)
      const next = event.key === 'ArrowRight' ? (index + 1) % apps.length : event.key === 'ArrowLeft' ? (index + apps.length - 1) % apps.length : event.key === 'Home' ? 0 : event.key === 'End' ? apps.length - 1 : null
      if (next !== null) { event.preventDefault(); choose(next); buttons[next].focus() }
    }}>
      {apps.map((item, index) => <button key={item.id} type="button" className="app-selector" aria-label={`Show ${item.name}`} aria-pressed={selected === index} onClick={() => choose(index)}>
        {selected === index && <svg key={cycle} className="selector-timer" viewBox="0 0 76 76" preserveAspectRatio="none" aria-hidden="true"><rect x="1" y="1" width="74" height="74" rx="15" pathLength="100" onAnimationEnd={() => { if (running) step(1) }} /></svg>}
        <img src={item.image} width="48" height="48" alt="" />
      </button>)}
    </div>
  </section>
}

function About() {
  const section = useRef<HTMLElement>(null)
  useEffect(() => {
    const element = section.current
    if (!element || !('IntersectionObserver' in window)) return
    const motion = window.matchMedia('(prefers-reduced-motion: reduce)')
    if (motion.matches) return
    element.dataset.reveal = 'waiting'
    const reveal = () => { element.dataset.reveal = 'visible'; observer.disconnect() }
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) reveal()
    }, { threshold: .12 })
    observer.observe(element)
    motion.addEventListener('change', reveal)
    return () => { observer.disconnect(); motion.removeEventListener('change', reveal) }
  }, [])
  return <section ref={section} id="about" className="about-section" aria-labelledby="about-title" tabIndex={-1}>
    <div className="about-art" aria-hidden="true">
      <svg viewBox="0 0 48 48" fill="none"><path d="M37.5 10.5A19 19 0 1 0 37.5 37.5" stroke="currentColor" strokeWidth="8" strokeLinecap="round" /><path d="M30 19a8 8 0 1 0 0 10" stroke="currentColor" strokeWidth="5" strokeLinecap="round" /></svg>
    </div>
    <div className="about-copy">
      <h2 id="about-title">We’re Clyvora.</h2>
      <p>We make small tools for things we think should be easier.</p>
      <p>Clyvora started with simple ideas: viewing a file without fighting with it, converting media without digging through menus, or seeing where a train actually is.</p>
      <p>We build the kind of software we’d want to use ourselves: quick to open, clear about what it does, and without much getting in the way.</p>
      <p>Some projects stay small. Others keep growing. If an idea is useful enough to keep coming back to, it’s probably worth building.</p>
    </div>
  </section>
}

function BrandName() {
  const [index, setIndex] = useState(0)
  useEffect(() => {
    const motion = window.matchMedia('(prefers-reduced-motion: reduce)')
    let timer: ReturnType<typeof setInterval> | undefined
    const sync = () => {
      clearInterval(timer)
      if (motion.matches) { setIndex(0); return }
      if (!document.hidden) timer = setInterval(() => setIndex(value => (value + 1) % 3), 4500)
    }
    sync()
    motion.addEventListener('change', sync)
    document.addEventListener('visibilitychange', sync)
    return () => {
      clearInterval(timer)
      motion.removeEventListener('change', sync)
      document.removeEventListener('visibilitychange', sync)
    }
  }, [])
  return <h1 className="brand-name" aria-label="Clyvora"><Morph className="brand-word" scale={false} spring>{['Clyvora', 'ClyvoraTech', 'Clyvora\nTechnologies'][index]}</Morph></h1>
}

function ScrollSignal() {
  const [progress, setProgress] = useState(0)
  useEffect(() => {
    const update = () => {
      const range = document.documentElement.scrollHeight - window.innerHeight
      setProgress(range > 0 ? window.scrollY / range : 0)
    }
    update()
    window.addEventListener('scroll', update, { passive: true })
    window.addEventListener('resize', update)
    return () => {
      window.removeEventListener('scroll', update)
      window.removeEventListener('resize', update)
    }
  }, [])
  return <button className="scroll-signal" type="button" aria-label="Back to top" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
    <svg viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <path className="scroll-signal-track" d="M37.5 10.5A19 19 0 1 0 37.5 37.5" />
      <path className="scroll-signal-progress" d="M37.5 10.5A19 19 0 1 0 37.5 37.5" pathLength="1" style={{ strokeDashoffset: 1 - progress }} />
      <path d="M30 19a8 8 0 1 0 0 10" />
    </svg>
  </button>
}

function App() {
  const [theme, setTheme] = useState(() => document.documentElement.dataset.theme === 'light' ? 'light' : 'dark')
  useEffect(() => {
    document.documentElement.dataset.theme = theme
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#151515' : '#fafafa')
    try { localStorage.setItem('clyvora-theme', theme) } catch { /* Theme remains usable without storage. */ }
  }, [theme])
  return <div className="site-shell">
    <ScrollSignal />
    <a href="#apps" className="skip-link">Skip to apps</a>
    <header className="site-header">
      <div className="brand">
        <svg className="brand-mark" width="46" height="46" viewBox="0 0 48 48" fill="none" aria-hidden="true">
          <path d="M37.5 10.5A19 19 0 1 0 37.5 37.5" stroke="currentColor" strokeWidth="8" strokeLinecap="round" />
          <path d="M30 19a8 8 0 1 0 0 10" stroke="currentColor" strokeWidth="5" strokeLinecap="round" />
        </svg>
        <BrandName />
      </div>
      <button className="theme-toggle" type="button" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}>
        {theme === 'dark' ? <Sun size={19} strokeWidth={1.6} /> : <Moon size={19} strokeWidth={1.6} />}
      </button>
    </header>
    <main id="apps" tabIndex={-1}><AppGallery /><About /></main>
    <footer className="site-footer">
      <span>© {new Date().getFullYear()} Clyvora</span>
    </footer>
  </div>
}
createRoot(document.getElementById('root')!).render(<><App /><Analytics /></>)