# Homepage design — 16 November 2026

The user approved a MacPaw-informed refresh while preserving Clyvora's spacious,
short homepage. This change continues the custom-wordmark identity; the project
apps keep their existing logos and public destinations.

## Result

- Small left-aligned wordmark, Apps/About navigation, GitHub link, and theme control.
- Warm light default for first visits, with a user's saved dark/light preference preserved.
- One large, softly tinted product stage: lavender data sheets and lens; peach audio/video objects; mint railway map.
- Original product icons remain visible beside app names and in the three-item selector.
- Useful descriptions, clear app links, a separate copy action, and a visible beta label for mewvi. The local/public-link distinction is retained.
- Compact previous/next and play/pause controls. Ten-second rotation pauses on mouse hover, keyboard focus, hidden tabs, manual pause, and reduced motion.
- A short About section, using Clyvora Display for the headline. Brand & type remains beneath the About copy.
- A simple back-to-top arrow appears only after scrolling. No floating brand monogram.

## Artwork

The three illustrations were generated with the built-in image-generation tool,
then resized and encoded as transparent WebP assets by `scripts/prepare-showcase.py`.
The prompts are in `homepage-art-prompts.json`. Final, project-owned assets are:

- `public/apps/showcase/lens.webp` — 64,620 bytes
- `public/apps/showcase/mewvi.webp` — 57,042 bytes
- `public/apps/showcase/liveopweg.webp` — 63,008 bytes

The images are decorative physical metaphors, not product screenshots, new app
logos, actual geography, or current train data. Existing app artwork is preserved.

## Scope

Homepage source, the theme initializer, and supporting design documentation.
Existing brand assets, font source, font kit, product sites, backend services,
and privacy boundaries are retained. Deployment is a separate step; local edits
do not imply that clyvora.tech has changed.

## Verification

- Production TypeScript/Vite build passed; no new npm dependency was added.
- All three optimized artwork URLs returned HTTP 200 and loaded in the browser.
- The three product panels had equal measured heights at desktop and 320 px;
  neither viewport had horizontal overflow.
- Product selection, keyboard wraparound, manual play/pause, timed rotation,
  and clipboard copying were exercised successfully.
- Light and dark themes were inspected. New-visitor, saved preference, invalid
  preference, and unavailable-storage theme initialization passed direct checks.
- The narrow About heading occupied two lines. Brand & type remained inside
  About, and the footer link did not overlap the back-to-top arrow.
- Browser error/warning logs were empty. Reduced-motion guards and listener/timer
  cleanup were reviewed in source; OS-level reduced motion was not emulated.
- The live local preview is `http://localhost:4190/`. A full-page light screenshot
  is saved at `../output/homepage-redesign/desktop-light.jpg`, relative to the Main
  repository root. Original generated PNGs are under the adjacent `source-art/`.

The pre-existing, uncommitted font/brand work is retained. These homepage changes
are also local and uncommitted; no public deployment was made.
