# Clyvora identity — version 1.1.0

Canonical identity files for Clyvora, established 16 November 2026. This is the
repository's source of truth for the adopted custom-wordmark direction. Earlier
files in `docs/brand-exploration/` are historical proposals, not alternate logos.
Publication is a separate deployment step; this document does not assert that
the files have already reached the public website or every project.

## Identity

- Written name: **Clyvora**. Legal text, page titles, metadata, and prose keep this spelling.
- Primary logo: the supplied lowercase **clyvora** wordmark, with its joined y/v.
- Compact logo: the **yv monogram**, extracted from the same wordmark outlines.
- Font family: **Clyvora Display**, version 1.1.0; Regular 400, Italic 400, and Bold 700.
- Palette: ink `#151515`; paper `#f4f3ed`. The main site keeps its existing theme surfaces.
- Existing individual project brands, including mewvi's cat, remain their own identities.

Use the full wordmark when the name needs to be read. Use the monogram at small
sizes and for app tiles, favicons, avatars, and supporting artwork. Do not place
the monogram immediately beside the full wordmark: it repeats the same gesture.
The primary wordmark is fixed; it does not rotate between alternate company names.

## Logo use

Use the outlined files in `public/brand/`. They do not require a font installation.
Choose the `-black` or `-white` version for image placement. The unsuffixed SVG uses
`currentColor` for inline embedding; an `<img>` cannot inherit a parent's color.

Clear space: at least half the lowercase x-height around the visible wordmark.
Minimum digital wordmark width: 112 CSS pixels. Minimum monogram width: 20 CSS
pixels; use the complete app tile at 16 px. Never stretch, tilt, add outlines or
shadows, crop, or rebuild the logo with a substitute font. Use a plain contrasting
background. Social assets and raster icons are generated from the same font.

## Typeface

Install the TTF files in `public/fonts/` in a desktop font manager, or host the
matching WOFF2 files for the web. Each is a genuine OpenType font in the
`Clyvora Display` family. The Regular and Italic styles use weight `400`; Bold
uses weight `700`. A web setup:

```css
@font-face {
  font-family: 'Clyvora Display';
  src: url('/fonts/ClyvoraDisplay-Regular.woff2?v=1.1.0') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: 'Clyvora Display';
  src: url('/fonts/ClyvoraDisplay-Italic.woff2?v=1.1.0') format('woff2');
  font-weight: 400;
  font-style: italic;
  font-display: swap;
}
@font-face {
  font-family: 'Clyvora Display';
  src: url('/fonts/ClyvoraDisplay-Bold.woff2?v=1.1.0') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}
.display { font-family: 'Clyvora Display', sans-serif; font-weight: 400; }
.display-italic { font-family: 'Clyvora Display', sans-serif; font-weight: 400; font-style: italic; }
.display-bold { font-family: 'Clyvora Display', sans-serif; font-weight: 700; }
.wordmark { font-feature-settings: 'dlig' 1; }
```

Use for names, titles, and short headlines, preferably at 28 px or larger. The
Italic style is an oblique cut of the same Regular outlines; it is not connected
script. Keep paragraphs and interface controls in the existing system sans serif.
Uppercase/lowercase Latin, numbers,
printable ASCII punctuation, common editorial/currency signs, and many
precomposed Latin accents are included. The exact encoded set is in
`public/brand/manifest.json`; this is not a pan-Unicode or variable font.

The joined y/v is an optional OpenType discretionary ligature (`dlig`). Leave it
off for ordinary text. The monogram is also mapped to private-use U+E000 for
design tools without discretionary-ligature controls. Use accessible text
“Clyvora” for logo images or controls, not a spoken private-use character.
Pair spacing is provided by the `kern` feature. Screen readers receive the
normal name on the site; the stylized lettering is decorative within that label.

## Files and build

- `scripts/brand/build.py`: original editable geometric outlines and export pipeline.
- `src/brand.ts`: generated shared monogram path used by React.
- `public/fonts/`: installable TTF and self-hosted WOFF2.
- `public/brand/`: outlined wordmarks/monograms, icon, specimen, license, manifest, kit.
- `public/brand/index.html`: browser specimen and asset download page at `/brand/`.
- `public/{brand-mark.svg,favicon.png,apple-touch-icon.png,icon-192.png,icon-512.png}`: app icons.
- `public/{social-card.png,og.png,dark-logo.png,light-logo.png}`: updated compatibility assets.

The outlines are original vector geometry. The approved generated image was a
visual reference, not a bitmap trace, a font source, or the final production file.
No existing font was renamed or modified. FontTools, skia-pathops, Pillow, and
HarfBuzz are build/validation tools, not browser dependencies.

Install the pinned Python dependencies in a dedicated environment, then run:

```text
python -m pip install -r scripts/brand/requirements.txt
python scripts/brand/build.py
python scripts/brand/check.py
python scripts/brand/package.py
pnpm build
```

The font's version and timestamps are fixed for reproducible exports. The release
manifest records asset hashes. Change source geometry, rebuild and check before
publishing an updated release. Keep the kit, wordmark, font, and monogram together.

## Ownership

The existing repository license applies to the font and brand assets; see
`public/brand/LICENSE.txt`. Public download does not grant a general reuse license.
This is a brand identity release, not a claim of trademark registration.

## Typeface revision — 17 November 2026

Version 1.0.1 redrew C/c, E/e, and G. The capital C uses its own wider cap-height
proportions. The lowercase c has softened terminals; the e has one continuous
bowl/crossbar without the former ledge and notch. Capital E has a unified outline,
and G has a clean crossbar and lower bowl. Related accented forms, the euro and
copyright symbols, and outlined wordmarks are regenerated from the same source.
The y/v ligature and monogram are retained. Web font URLs carry the new version
so browsers request the corrected outlines. Version 1.0.0's archive remains a
historical release; version 1.1.0 adds matching Regular and Italic styles while
keeping the Bold wordmark unchanged.

## Typeface family — 17 November 2026

Version 1.1.0 adds a Regular cut by evenly reducing each outline from its edges,
and an Italic cut by slanting that same Regular geometry. It does not redraw the
letters or create connected cursive. Bold remains the source of the official
wordmark, monogram, and existing site headings. The brand specimen lets visitors
preview all three styles; the download kit includes TTF and WOFF2 files for each.
