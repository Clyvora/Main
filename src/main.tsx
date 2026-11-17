import { createRoot } from 'react-dom/client'
import { Analytics } from '@vercel/analytics/react'
import { HomePage } from './HomePage'
import './styles.css'

createRoot(document.getElementById('root')!).render(<><HomePage /><Analytics /></>)
