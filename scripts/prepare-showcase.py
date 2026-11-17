"""Export transparent product illustrations to compact, same-sized web assets.

Usage: python scripts/prepare-showcase.py qr-studio source.png
This only resizes/encodes generated assets; it does not alter their artwork.
"""
from pathlib import Path
import sys
from PIL import Image

destination=Path(__file__).resolve().parents[1]/"public"/"apps"/"showcase"
destination.mkdir(parents=True,exist_ok=True)
arguments=sys.argv[1:]
if not arguments or len(arguments)%2 or not set(arguments[::2]).issubset({"lens","mewvi","liveopweg","qr-studio"}) or len(set(arguments[::2]))!=len(arguments[::2]):
    raise SystemExit("Supply unique supported app names and PNG source paths in name/path pairs.")
for name,source in zip(arguments[::2],arguments[1::2]):
    with Image.open(source) as original:
        image=original.convert("RGBA")
        image.thumbnail((960,960),Image.Resampling.LANCZOS)
        assert image.getchannel("A").getextrema()[0]==0,"Transparent artwork required"
        target=destination/f"{name}.webp"
        image.save(target,"WEBP",quality=87,method=6,alpha_quality=100)
        print(f"{name}: {image.width} x {image.height}, {target.stat().st_size:,} bytes")
