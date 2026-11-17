try {
  document.documentElement.dataset.theme = localStorage.getItem('clyvora-theme') === 'dark' ? 'dark' : 'light';
} catch {
  document.documentElement.dataset.theme = 'light';
}
