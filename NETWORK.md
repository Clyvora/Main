# Network boundary

The Clyvora website loads its interface and cookie-free Vercel page analytics from its own origin. It does not load third-party fonts or advertising and it never receives selected file contents from Lens, Convert, or Resize.

Outbound product links are followed only when a visitor selects them. Fetch is the only networked processing product: its submitted public URL is sent to ClyvoraAPI and the supported source platform, as documented in Fetch's own network policy.

The homepage stores the selected appearance locally under `clyvora-theme`. This preference is not sent to an endpoint. App artwork is served from the site's own origin.
