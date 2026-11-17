"""Package the canonical font, logos, usage guide, and rebuildable source."""
from pathlib import Path
import json
import zipfile

ROOT=Path(__file__).resolve().parents[2]
PUBLIC=ROOT/"public"
BRAND=PUBLIC/"brand"
version=json.loads((BRAND/"manifest.json").read_text(encoding="utf-8"))["version"]
kit=BRAND/f"clyvora-brand-kit-{version}.zip"
entries={}
for file in sorted((PUBLIC/"fonts").glob("ClyvoraDisplay-*")):
    entries[f"fonts/{file.name}"]=file
for file in sorted(BRAND.glob("clyvora-*")):
    if file.suffix!=".zip": entries[f"identity/{file.name}"]=file
for name in ["brand-mark.svg","favicon.png","apple-touch-icon.png","icon-192.png","icon-512.png","social-card.png","og.png"]:
    entries[f"exports/{name}"]=PUBLIC/name
for file in sorted((ROOT/"scripts"/"brand").glob("*")):
    if file.is_file(): entries[f"source/scripts/brand/{file.name}"]=file
entries["source/docs/BRAND.md"]=ROOT/"docs"/"BRAND.md"
entries["source/public/brand/LICENSE.txt"]=BRAND/"LICENSE.txt"
entries["BRAND.md"]=ROOT/"docs"/"BRAND.md"
entries["LICENSE.txt"]=BRAND/"LICENSE.txt"
entries["manifest.json"]=BRAND/"manifest.json"
with zipfile.ZipFile(kit,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
    for name,file in sorted(entries.items()):
        info=zipfile.ZipInfo(f"clyvora-brand-{version}/{name}",date_time=(2026,11,17,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        archive.writestr(info,file.read_bytes())
with zipfile.ZipFile(kit) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist())==len(entries)
print(f"Packaged {len(entries)} files: {kit} ({kit.stat().st_size:,} bytes)")
