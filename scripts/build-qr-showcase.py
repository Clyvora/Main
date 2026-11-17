"""Compose original 3D card materials with an exact, editable QR matrix."""
import base64
from pathlib import Path
import sys
import qrcode

root = Path(__file__).resolve().parents[1]
source = root / 'public/apps/showcase/qr-studio-card.webp'
destination = root / 'public/apps/showcase/qr-studio.svg'
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=4)
qr.add_data('https://clyvora.tech/')
qr.make(fit=True)
matrix = qr.get_matrix()
n = len(matrix) - 8
cells = []
finders = [(4,4),(4+n-7,4),(4,4+n-7)]
for y,row in enumerate(matrix):
    for x,dark in enumerate(row):
        if dark and not any(a <= x < a+7 and b <= y < b+7 for a,b in finders):
            cells.append(f'M{x} {y}h1v1h-1z')
finder_shapes = ''.join(f'<rect x="{x+.5}" y="{y+.5}" width="6" height="6" rx="1.1" fill="none" stroke="url(#ink)" stroke-width="1"/><rect x="{x+2}" y="{y+2}" width="3" height="3" rx=".45" fill="url(#ink)"/>' for x,y in finders)
background = base64.b64encode(source.read_bytes()).decode('ascii')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="960" viewBox="0 0 1280 1280" fill="none" role="img" aria-labelledby="title desc">
<title id="title">Clyvora QR Studio</title><desc id="desc">An ivory QR card with aqua glass and a cyan swatch. Scan the card to visit https://clyvora.tech/.</desc>
<defs><linearGradient id="ink" x1="4" y1="4" x2="27" y2="27" gradientUnits="userSpaceOnUse"><stop stop-color="#266963"/><stop offset=".5" stop-color="#1e625d"/><stop offset="1" stop-color="#19534e"/></linearGradient></defs>
<image width="1280" height="1280" href="data:image/webp;base64,{background}"/>
<g transform="matrix(1 -.06 -.08 1.1 180 270)"><g transform="scale(20)"><path fill="url(#ink)" d="{''.join(cells)}"/>{finder_shapes}</g></g>
</svg>
'''
destination.write_text(svg, encoding='utf-8', newline='\n')
print(destination, destination.stat().st_size, 'bytes')
