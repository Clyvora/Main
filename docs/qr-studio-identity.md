# Clyvora QR Studio

Added to the Main catalogue on 17 November 2026 at the user's request. The user
supplied `https://qr.clyvora.tech/`; features were checked against the sibling
QRCODE repository README. This records local work, not publication.

The app is listed as QR Studio in the picker and headline. The small category
labels above all app titles were removed at the user's request. Its SVG icon uses three rounded QR finder squares and four modules on
an aqua tile. It matches the existing app icons' rounded forms, soft dimensional
colour, and light highlights. The mark is decorative, not a scannable code.

- Editable app icon: `public/apps/qr-studio.svg` (128-unit viewBox).
- Homepage artwork: `public/apps/showcase/qr-studio.svg` (transparent, 1280-unit viewBox).
- Card materials: `public/apps/showcase/qr-studio-card.webp`, embedded into the SVG.
- QR payload in the showcase: `https://clyvora.tech/`.
- Rebuild: `python scripts/build-qr-showcase.py` with `qrcode==8.2` installed.
- Homepage destination: `https://qr.clyvora.tech/`.
- Showcase colour: light `#e9f3f3`, dark `#233234`.

The showcase combines the original soft 3D design with an exact vector QR
matrix. The original generated illustration was edited with the image tool to
remove the decorative pattern, preserving the ivory card, aqua glass, and cyan
swatch. Its transparent WebP is embedded in the SVG, and the rounded finder
marks and exact QR cells are placed on the face in its perspective. The matrix
keeps a four-module quiet zone and links to Clyvora's main website. The restored
mobile homepage screenshot was decoded with jsQR 1.4.0 to verify the payload.
The original generated WebP remains a historical artwork asset; its initial
prompt is recorded in `homepage-art-prompts.json`. The small app icon remains a
decorative brand mark.

Main's homepage, static About catalogue, metadata, and README include the new
project. QR Studio's own repository has not been changed.
