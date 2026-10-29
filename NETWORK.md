# Network boundary

The Clyvora website loads its interface and cookie-free Vercel page analytics from its own origin. It does not load third-party fonts or advertising and it never receives selected file contents from Lens, mewvi, or Resize.

Outbound product links are followed only when a visitor selects them. mewvi at https://mewvi.xyz/ converts selected local files on-device, while public-link inspection, downloads, and collection discovery contact Clyvora infrastructure and source platforms. Live op Weg uses online railway data. The existing Fetch service also contacts ClyvoraAPI and supported source platforms. Each product documents its own network behavior; the main website does not submit media links or files on a visitor's behalf.

The homepage stores the selected appearance locally under `clyvora-theme`. This preference is not sent to an endpoint. App artwork is served from the site's own origin.
