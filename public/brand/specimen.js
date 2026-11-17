const sample = document.getElementById('sample')
const size = document.getElementById('size')
const preview = document.getElementById('type-preview')
const sizeValue = document.getElementById('size-value')
const ligature = document.getElementById('ligature')
const fontStyle = document.getElementById('font-style')
const styleValue = document.getElementById('style-value')
const theme = document.getElementById('theme')

function render() {
  preview.textContent = sample.value || 'Small tools. Clear purpose.'
  preview.style.fontSize = `${size.value}px`
  preview.style.fontWeight = fontStyle.value === 'bold' ? '700' : '400'
  preview.style.fontStyle = fontStyle.value === 'italic' ? 'italic' : 'normal'
  preview.style.fontFeatureSettings = `'dlig' ${ligature.checked ? 1 : 0}`
  sizeValue.value = `${size.value} px`
  styleValue.textContent = `${fontStyle.options[fontStyle.selectedIndex].textContent} / ${fontStyle.value === 'bold' ? 700 : 400}`
  document.querySelectorAll('.alphabet').forEach(alphabet => {
    alphabet.style.fontWeight = preview.style.fontWeight
    alphabet.style.fontStyle = preview.style.fontStyle
  })
}
sample.addEventListener('input', render)
size.addEventListener('input', render)
fontStyle.addEventListener('change', render)
ligature.addEventListener('change', render)
theme.addEventListener('click', () => {
  const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light'
  document.documentElement.dataset.theme = next
  try { localStorage.setItem('clyvora-theme', next) } catch { /* Appearance remains usable. */ }
  updateThemeLabel()
})
function updateThemeLabel() {
  const label = document.documentElement.dataset.theme === 'light' ? 'Switch to dark theme' : 'Switch to light theme'
  theme.setAttribute('aria-label', label)
  theme.setAttribute('title', label)
}
if (window.matchMedia('(max-width: 500px)').matches) size.value = '44'
render()
updateThemeLabel()
