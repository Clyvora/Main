import { readFileSync } from 'node:fs'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const productionHeaders = Object.fromEntries(JSON.parse(readFileSync(new URL('./vercel.json', import.meta.url), 'utf8')).headers[0].headers.map((header: { key: string; value: string }) => [header.key, header.value]))

const compactHtml = {
	name: 'compact-html',
	transformIndexHtml(html: string) {
		return html.replace(/\n\s*/g, '').trim()
	},
}

export default defineConfig({ preview: { headers: productionHeaders }, plugins: [react(), compactHtml] })
