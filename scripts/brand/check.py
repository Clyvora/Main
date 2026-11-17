"""Verify the release's encoding, shaping, metrics, vector identity, and exports."""
import hashlib
import json
from pathlib import Path
import unicodedata
import xml.etree.ElementTree as ET

from fontTools.ttLib import TTFont
from PIL import Image
import uharfbuzz as hb

ROOT=Path(__file__).resolve().parents[2]
PUBLIC=ROOT/"public"
BRAND=PUBLIC/"brand"
font_path=PUBLIC/"fonts"/"ClyvoraDisplay-Bold.ttf"
font=TTFont(font_path)
variants={
    "Regular":(400,0x40),
    "Italic":(400,0x01),
    "Bold":(700,0xA0),
}
fonts={style:TTFont(PUBLIC/"fonts"/f"ClyvoraDisplay-{style}.ttf") for style in variants}
webfonts={style:TTFont(PUBLIC/"fonts"/f"ClyvoraDisplay-{style}.woff2") for style in variants}
cmap=font.getBestCmap()
for style,(weight,selection) in variants.items():
    instance=fonts[style]
    webfont=webfonts[style]
    assert cmap==instance.getBestCmap()==webfont.getBestCmap(),(style,"font encodings differ")
    assert instance["OS/2"].usWeightClass==weight,(style,"wrong weight metadata")
    assert instance["OS/2"].fsSelection==selection,(style,"wrong style metadata")
    assert instance["name"].getDebugName(1)=="Clyvora Display"
    assert instance["name"].getDebugName(2)==style
    assert instance["name"].getDebugName(5)==f"Version {json.loads((BRAND/'manifest.json').read_text(encoding='utf-8'))['version']}"
    assert instance.getGlyphOrder()==font.getGlyphOrder(),(style,"glyph order differs")
    assert webfont["name"].getDebugName(5)==instance["name"].getDebugName(5)
    assert {"kern","dlig"}.issubset({record.FeatureTag for table in ("GSUB","GPOS") for record in instance[table].table.FeatureList.FeatureRecord}),(style,"missing OpenType feature")
    assert len(instance.getGlyphOrder())==len(set(instance.getGlyphOrder()))
    for name in instance.getGlyphOrder():
        glyph=instance["glyf"][name]
        if glyph.numberOfContours:
            assert glyph.yMax<=instance["hhea"].ascent,(style,name,"ascender clipping")
            assert glyph.yMin>=instance["hhea"].descent,(style,name,"descender clipping")
            assert instance["hmtx"][name][1]==glyph.xMin,(style,name,"inconsistent sidebearing")
assert fonts["Regular"]["glyf"]["uni0069"].xMax-fonts["Regular"]["glyf"]["uni0069"].xMin < fonts["Bold"]["glyf"]["uni0069"].xMax-fonts["Bold"]["glyf"]["uni0069"].xMin
assert fonts["Italic"]["post"].italicAngle==-9
assert fonts["Italic"]["glyf"]["uni0069"].yMax==fonts["Regular"]["glyf"]["uni0069"].yMax,"Oblique changed vertical letter proportions"
assert all(code in cmap for code in range(32,127)),"Missing printable ASCII"
assert all(ord(ch) in cmap for ch in "éëïöüÉËÏÖÜĳĲ€£“”’–—…"),"Missing Dutch/editorial coverage"
assert font["name"].getDebugName(1)=="Clyvora Display"
assert {"kern","dlig"}.issubset({r.FeatureTag for table in ("GSUB","GPOS") for r in font[table].table.FeatureList.FeatureRecord})
assert font["OS/2"].fsType==0
assert len(font.getGlyphOrder())==len(set(font.getGlyphOrder()))
face=hb.Face(font_path.read_bytes())
hbfont=hb.Font(face)
def shape(text,ligature=False):
    buf=hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbfont,buf,{"dlig":ligature,"kern":True})
    assert all(item.codepoint!=0 for item in buf.glyph_infos),(text,".notdef in shaped text")
    return buf
plain=shape("clyvora")
joined=shape("clyvora",True)
assert len(plain.glyph_infos)==7 and len(joined.glyph_infos)==6
assert any(font.getGlyphName(item.codepoint)=="y_v" for item in joined.glyph_infos)
assert sum(pos.x_advance for pos in joined.glyph_positions)<sum(pos.x_advance for pos in plain.glyph_positions)
for text in ["IJsselmeer. Eén idee, veel plezier.","Clyvora Technologies / 0123456789",unicodedata.normalize("NFD","één naïef idee")]:
    shape(text)
assert font.getGlyphName(shape("\ue000").glyph_infos[0].codepoint)=="y_v"

manifest=json.loads((BRAND/"manifest.json").read_text(encoding="utf-8"))
assert manifest["styles"]=={"Regular":{"weight":400,"italic":False},"Italic":{"weight":400,"italic":True},"Bold":{"weight":700,"italic":False}}
assert font["name"].getDebugName(5)==f"Version {manifest['version']}","Font and release versions differ"
assert webfont["name"].getDebugName(5)==font["name"].getDebugName(5)
assert manifest["encodedCharacters"]==len(cmap)
for relative,record in manifest["files"].items():
    assert not relative.endswith(".zip"),"The release cannot recursively hash itself"
    data=(PUBLIC/relative).read_bytes()
    assert len(data)==record["bytes"],relative
    assert hashlib.sha256(data).hexdigest()==record["sha256"],relative
for filename,size in [("favicon.png",64),("apple-touch-icon.png",180),("icon-192.png",192),("icon-512.png",512)]:
    with Image.open(PUBLIC/filename) as im:
        assert im.size==(size,size),filename
        assert im.getextrema()[0][0]!=im.getextrema()[0][1],(filename,"blank artwork")
for filename in ["social-card.png","og.png"]:
    with Image.open(PUBLIC/filename) as im: assert im.size==(1200,630)
for filename in ["dark-logo.png","light-logo.png"]:
    with Image.open(PUBLIC/filename) as im: assert im.size==(400,400) and im.mode=="RGBA"
ns={"s":"http://www.w3.org/2000/svg"}
mark=ET.parse(BRAND/"clyvora-monogram.svg").getroot().find("s:path",ns).attrib["d"]
shared=(ROOT/"src"/"brand.ts").read_text(encoding="utf-8")
assert json.dumps(mark) in shared,"Site monogram differs from the exported monogram"
for filename in ["clyvora-wordmark-black.svg","clyvora-wordmark-white.svg","clyvora-icon.svg"]:
    root=ET.parse(BRAND/filename).getroot()
    assert root.find("s:path",ns) is not None
    assert root.find("s:text",ns) is None,"Logo must use outlines, not an installed font"
print(f"Passed: {len(cmap)} encoded characters; TTF/WOFF2; readable/shaped text; optional yv; metrics; hashes; SVG/PNG exports.")
