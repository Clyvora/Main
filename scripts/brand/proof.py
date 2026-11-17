"""Compare the installed output outlines at display and heading sizes.

Usage: python scripts/brand/proof.py previous.ttf output.png
The system font is used for proof-sheet labels only, never for font outlines.
"""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

root=Path(__file__).resolve().parents[2]
if len(sys.argv)!=3:
    raise SystemExit("Supply the previous font path and the destination PNG.")
before=Path(sys.argv[1])
after=root/"public"/"fonts"/"ClyvoraDisplay-Bold.ttf"
destination=Path(sys.argv[2])
destination.parent.mkdir(parents=True,exist_ok=True)
image=Image.new("RGB",(1600,1000),"#151515")
draw=ImageDraw.Draw(image)
label_path=Path("C:/Windows/Fonts/segoeui.ttf")
def labels(size):
    return ImageFont.truetype(str(label_path),size) if label_path.exists() else ImageFont.load_default(size=size)
label=labels(26)
small=labels(21)
draw.text((64,38),"Clyvora Display / letter refinements",font=label,fill="#f4f3ed")
draw.line((64,100,1536,100),fill="#393a36",width=2)
for x,name,file in [(64,"Before",before),(850,"After",after)]:
    draw.text((x,126),name,font=label,fill="#acada6")
    for text,size,baseline in [("Cc  Ee  Gg",152,365),("Clear purpose.",90,535),("Good things. Eén idee.",54,690),("cl\ue000ora",74,840)]:
        font=ImageFont.truetype(str(file),size)
        draw.text((x,baseline),text,font=font,fill="#f4f3ed",anchor="ls")
draw.line((800,130,800,890),fill="#393a36",width=2)
draw.text((64,930),"Broader C proportions / continuous e bowl / cleaner G crossbar",font=small,fill="#acada6")
image.save(destination)
print(destination.resolve())
