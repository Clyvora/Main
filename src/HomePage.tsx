import { useEffect, useRef, useState } from 'react'
import { ArrowUp, ArrowUpRight, Check, Copy, Moon, Sun } from 'lucide-react'
import { TextMorph } from 'torph/react'
import { brandMarkPath, brandMarkViewBox } from './brand'

const apps = [
  { id: 'lens', name: 'Lens', description: 'Your data. In focus.', detail: 'Open JSON and CSV files, find what matters, and export them the way you need. All in your browser, with your files staying on your device.', icon: '/apps/lens.svg', art: '/apps/showcase/lens.webp', href: 'https://www.lens.clyvora.tech/' },
  { id: 'mewvi', name: 'mewvi', description: 'Download. Convert. Keep.', detail: 'Download supported public media or convert your own audio and video. Local conversion stays on your device; public links use our media service.', icon: '/apps/convert-cat.webp', art: '/apps/showcase/mewvi.webp', href: 'https://mewvi.xyz/', beta: true },
  { id: 'liveopweg', name: 'Live op Weg', description: 'The railway, in motion.', detail: 'Follow live train locations on the map and see where they are as they travel. A little closer to the journey, wherever you are.', icon: '/apps/liveopweg.svg', art: '/apps/showcase/liveopweg.webp', href: 'https://liveopweg.nl/' },
  { id: 'qr-studio', name: 'QR Studio', description: 'A code of your own.', detail: 'Create QR codes for links, Wi-Fi, contacts, and more. Make them yours with colours and styles, then export as PNG, SVG, or PDF. Your QR content stays on your device.', icon: '/apps/qr-studio.svg', art: '/apps/showcase/qr-studio.svg', href: 'https://qr.clyvora.tech/' },
] as const

function Morph({ children }: { children: string }) {
  const supported = typeof Element.prototype.animate === 'function' && typeof Element.prototype.getAnimations === 'function'
  return supported ? <TextMorph as="span" duration={420} respectReducedMotion>{children}</TextMorph> : <span>{children}</span>
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
  const step = (delta: number) => choose((selected + delta + apps.length) % apps.length)
  const app = apps[selected]

  return <section id="apps" className="gallery" aria-label="Explore Clyvora apps" aria-roledescription="carousel" data-app={app.id} data-running={running} data-reduced={reduced}
    onPointerEnter={event => { if (event.pointerType === 'mouse') setHovered(true) }}
    onPointerLeave={() => { setHovered(false); artwork.current?.style.removeProperty('transform') }}
    onPointerMove={event => {
      if (reduced || event.pointerType !== 'mouse' || !artwork.current) return
      const bounds = event.currentTarget.getBoundingClientRect()
      const x = (event.clientX - bounds.left) / bounds.width - .5
      const y = (event.clientY - bounds.top) / bounds.height - .5
      artwork.current.style.transform = `translate3d(${x * 10}px, ${y * 8}px, 0)`
    }}
    onFocusCapture={() => setFocused(true)} onBlurCapture={event => { if (!event.currentTarget.contains(event.relatedTarget)) setFocused(false) }}>
    <div className="gallery-panel">
      <div className="gallery-stage" aria-live={running ? 'off' : 'polite'} aria-atomic="true">
        <article className="gallery-slide" aria-labelledby={`${app.id}-title`} aria-roledescription="slide">
          <div className="art-stage" aria-hidden="true"><div className="art-glow" /><div ref={artwork} className="app-art"><img key={app.id} src={app.art} width="960" height="960" alt="" fetchPriority={selected === 0 ? 'high' : 'auto'} draggable="false" /></div></div>
          <div className="app-details">
            <div className="app-heading"><span className={`app-logo app-logo-${app.id}`} aria-hidden="true"><img src={app.icon} width="34" height="34" alt="" /></span><h2 id={`${app.id}-title`}><Morph>{app.name}</Morph></h2>{'beta' in app && <span className="beta-label">Beta</span>}</div>
            <p className="app-tagline"><Morph>{app.description}</Morph></p>
            <p key={app.id} className="app-description">{app.detail}</p>
            <div className="app-actions"><a className="open-app" href={app.href} target="_blank" rel="noreferrer"><span>Open {app.name}</span><ArrowUpRight size={19} strokeWidth={1.65} aria-hidden="true" /><span className="sr-only"> (opens in a new tab)</span></a><ShareButton key={app.id} href={app.href} /></div>
          </div>
        </article>
      </div>
    </div>
    <div className="gallery-selectors" role="group" aria-label="Choose an app" onKeyDown={event => {
      const buttons = Array.from(event.currentTarget.querySelectorAll('button'))
      const index = buttons.indexOf(document.activeElement as HTMLButtonElement)
      if (index < 0) return
      const next = event.key === 'ArrowRight' ? (index + 1) % apps.length : event.key === 'ArrowLeft' ? (index + apps.length - 1) % apps.length : event.key === 'Home' ? 0 : event.key === 'End' ? apps.length - 1 : null
      if (next !== null) { event.preventDefault(); choose(next); buttons[next].focus() }
    }}>
      {apps.map((item, index) => <button key={item.id} type="button" className={`app-selector app-selector-${item.id}`} aria-label={`Show ${item.name}`} aria-pressed={selected === index} onClick={() => choose(index)}><span className="selector-icon">{selected === index && <svg key={cycle} className="selector-timer" viewBox="0 0 64 64" aria-hidden="true"><rect x="1" y="1" width="62" height="62" rx="18" pathLength="100" onAnimationEnd={() => { if (running) step(1) }} /></svg>}<img src={item.icon} width="38" height="38" alt="" /></span><span className="selector-name">{item.name}</span></button>)}
    </div>
  </section>
}

function ShareButton({ href }: { href: string }) {
  const [status, setStatus] = useState<'idle' | 'copied' | 'error'>('idle')
  const timer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined)
  useEffect(() => () => clearTimeout(timer.current), [])
  const copyLink = async () => {
    try { await navigator.clipboard.writeText(href); setStatus('copied') } catch { setStatus('error') }
    clearTimeout(timer.current)
    timer.current = setTimeout(() => setStatus('idle'), 2200)
  }
  return <><button className="copy-link" type="button" onClick={copyLink} aria-label={status === 'copied' ? 'App link copied' : 'Copy app link'}>{status === 'copied' ? <Check size={17} aria-hidden="true" /> : <Copy size={17} aria-hidden="true" />}</button><span className="sr-only" role="status">{status === 'copied' ? 'App link copied.' : status === 'error' ? 'Could not copy the link. Use the app link beside this button.' : ''}</span></>
}

function About({ onLogoClick }: { onLogoClick: () => void }) {
  return <section id="about" className="about-section" aria-labelledby="about-title">
    <div className="about-intro"><div className="about-eyebrow"><button type="button" className="about-mark" onClick={onLogoClick} aria-label="Clyvora monogram"><svg viewBox={brandMarkViewBox} aria-hidden="true"><path d={brandMarkPath} fill="currentColor" /></svg></button><span>A little about Clyvora</span></div><h2 id="about-title">Small tools.<br />Clear purpose.</h2></div>
    <div className="about-copy"><p>We make tools for opening data, working with media, creating QR codes, and following the railway. A few useful things, made to be easy to use.</p><p>Some projects stay small. Others keep growing. We keep working on the ones we want to use ourselves.</p><a className="about-link" href="/brand/">Brand &amp; type<ArrowUpRight size={17} strokeWidth={1.6} aria-hidden="true" /></a></div>
  </section>
}

function BackToTop() {
  const [visible, setVisible] = useState(false)
  useEffect(() => {
    const update = () => setVisible(window.scrollY > window.innerHeight / 2)
    update()
    window.addEventListener('scroll', update, { passive: true })
    window.addEventListener('resize', update)
    return () => { window.removeEventListener('scroll', update); window.removeEventListener('resize', update) }
  }, [])
  if (!visible) return null
  return <button className="back-to-top" type="button" aria-label="Back to top" onClick={() => window.scrollTo({top:0,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'})}><ArrowUp size={18} strokeWidth={1.7} aria-hidden="true" /></button>
}

export function HomePage() {
  const [theme, setTheme] = useState(() => document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light')
  const [easterEgg, setEasterEgg] = useState<'header' | 'about' | null>(null)
  const logoClicks = useRef(0)
  const logoTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined)
  useEffect(() => () => clearTimeout(logoTimer.current), [])
  const handleLogoClick = (source: 'header' | 'about') => {
    logoClicks.current += 1
    clearTimeout(logoTimer.current)
    if (logoClicks.current >= 5) {
      logoClicks.current = 0
      setEasterEgg(source)
      logoTimer.current = setTimeout(() => setEasterEgg(null), 1100)
    } else { logoTimer.current = setTimeout(() => { logoClicks.current = 0 }, 1400) }
  }
  useEffect(() => {
    document.documentElement.dataset.theme = theme
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#171816' : '#fbfaf7')
    try { localStorage.setItem('clyvora-theme', theme) } catch { /* Theme works without storage. */ }
  }, [theme])
  return <div className={`site-shell${easterEgg ? ` easter-egg-${easterEgg}` : ''}`}>
    <a href="#apps" className="skip-link">Skip to apps</a>
    <header className="site-header"><h1 className="brand-name" aria-label="Clyvora"><button className="brand-wordmark-button" type="button" aria-label="Clyvora logo" onClick={() => handleLogoClick('header')}><span aria-hidden="true">clyvora</span></button></h1><nav className="main-nav" aria-label="Main navigation"><a href="#apps">Apps</a><a href="#about">About</a><a className="nav-github" href="https://github.com/Clyvora" target="_blank" rel="noreferrer">GitHub<ArrowUpRight size={13} aria-hidden="true" /></a></nav><button className="theme-toggle" type="button" onClick={() => setTheme(value => value === 'dark' ? 'light' : 'dark')} aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}>{theme === 'dark' ? <Sun size={18} strokeWidth={1.6} aria-hidden="true" /> : <Moon size={18} strokeWidth={1.6} aria-hidden="true" />}</button></header>
    <main><AppGallery /><About onLogoClick={() => handleLogoClick('about')} /></main>
    <footer className="site-footer"><span>© {new Date().getFullYear()} Clyvora</span><a href="https://github.com/Clyvora" target="_blank" rel="noreferrer">Find us on GitHub<ArrowUpRight size={14} aria-hidden="true" /></a></footer>
    <BackToTop />
  </div>
}
