"""Build Clyvora Display and its identity assets from original geometric outlines.

No installed font, traced bitmap, or third-party glyph outlines are used.
Coordinates are a 1000-unit em, with a 540-unit x-height and 140-unit stroke.
Run from any directory after installing requirements.txt.
"""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
import unicodedata

import pathops
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import parse_path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
BRAND = PUBLIC / "brand"
FONTS = PUBLIC / "fonts"
VERSION = "1.1.0"
FONT_REVISION = 1.1
COPYRIGHT = "Copyright (c) 2026 Clyvora contributors. All rights reserved."
INK, PAPER = "#151515", "#f4f3ed"


def path(data):
    p = pathops.Path()
    parse_path(data, p.getPen())
    return p


def rect(x, y, w, h, r=0):
    r = min(r, w / 2, h / 2)
    return path(f"M{x+r} {y}H{x+w-r}Q{x+w} {y} {x+w} {y+r}V{y+h-r}Q{x+w} {y+h} {x+w-r} {y+h}H{x+r}Q{x} {y+h} {x} {y+h-r}V{y+r}Q{x} {y} {x+r} {y}Z")


def oval(x, y, w, h):
    k, rx, ry = .55228475, w/2, h/2
    cx, cy = x+rx, y+ry
    return path(f"M{cx} {y}C{cx+k*rx} {y} {x+w} {cy-k*ry} {x+w} {cy}S{cx+k*rx} {y+h} {cx} {y+h}S{x} {cy+k*ry} {x} {cy}S{cx-k*rx} {y} {cx} {y}Z")


def union(*parts):
    result = pathops.Path()
    for part in parts:
        result = pathops.op(result, part, pathops.PathOp.UNION)
    return result


def minus(a, b):
    return pathops.op(a, b, pathops.PathOp.DIFFERENCE)


def shift(p, x=0, y=0, sx=1, sy=1):
    return p.transform(scaleX=sx, scaleY=sy, translateX=x, translateY=y)


def stroke(data, width=140, rounded=True):
    p = path(data)
    p.stroke(width, pathops.LineCap.ROUND_CAP if rounded else pathops.LineCap.BUTT_CAP,
             pathops.LineJoin.ROUND_JOIN, 4)
    p.convertConicsToQuads(.2)
    return p


def ring(x=30, y=-10, w=570, h=560, weight=140):
    return minus(oval(x, y, w, h), oval(x+weight, y+weight, w-2*weight, h-2*weight))


def poly(points):
    return path("M" + "L".join(f"{x} {y}" for x, y in points) + "Z")


def glyphs():
    g = {}
    def add(ch, p, advance):
        g[ch] = (p, advance)
    add("o", ring(), 630)
    add("c", path("M511 75Q526 88 512 104L448 172Q435 187 420 172C389 143 351 130 308 130C225 130 180 181 180 270S225 410 308 410C351 410 389 395 420 365Q435 350 449 364L515 430Q529 444 515 459C462 518 391 550 305 550C132 550 30 439 30 270S132-10 305-10C392-10 463 18 511 75Z"), 570)
    add("l", rect(40, -180, 145, 720, 46), 225)
    add("i", union(rect(40, 0, 145, 540, 40), rect(40, -185, 145, 125, 42)), 225)
    add("j", union(path("M116 0H228V507C228 638 164 700 50 700H8V563H40C88 563 102 545 102 497V16Q102 0 116 0Z"), rect(90,-185,145,125,42)), 270)
    add("v", path("M24 0H174L307 364 442 0H600L403 502Q387 544 341 544H276Q229 544 213 502L24 0Z"), 625)
    add("y", path("M70 0H165Q190 0 190 25V216Q190 322 268 322Q303 322 321 286L424 0H576L378 563Q337 690 203 690H145Q117 690 117 662V590Q117 566 142 566H196Q239 566 259 510L279 454C106 466 40 385 40 238V30Q40 0 70 0Z"), 605)
    add("u", path("M65 0H166Q190 0 190 24V298Q190 415 285 415T380 298V24Q380 0 404 0H505Q530 0 530 24V304Q530 550 285 550T40 304V24Q40 0 65 0Z"), 570)
    add("n", path("M40 540V0H173L182 60Q235-10 335-10Q535-10 535 227V540H385V241Q385 130 291 130Q190 130 190 249V540Z"), 575)
    add("h", union(g["n"][0], rect(40,-180,150,400,40)), 575)
    add("m", path("M40 540V0H174L182 58Q232-10 320-10Q423-10 470 73Q533-10 635-10Q820-10 820 216V540H670V234Q670 130 596 130Q514 130 514 241V540H364V234Q364 130 290 130Q190 130 190 249V540Z"), 860)
    add("a", union(ring(w=560),rect(450,0,140,540,24)), 625)
    add("b", union(ring(x=40,w=550),rect(40,-180,145,720,34)), 620)
    add("d", union(ring(x=30,w=550),rect(435,-180,145,720,34)), 620)
    add("p", union(ring(x=40,w=550),rect(40,0,145,730,26)), 620)
    add("q", union(ring(x=30,w=550),rect(435,0,145,730,26)), 620)
    add("g", union(ring(w=550),path("M435 0H580V487Q580 734 321 734Q185 734 89 673L155 553Q224 600 314 600Q435 600 435 483V0Z")), 620)
    # A continuous bowl and crossbar avoid the old right-edge ledge and lower notch.
    add("e", minus(path("M578 338H182C198 391 243 418 312 418C365 418 405 401 439 367Q452 354 465 367L524 423Q539 437 525 452C472 514 399 550 307 550C134 550 30 438 30 270C30 102 136-10 303-10C480-10 600 111 600 280V316Q600 338 578 338Z"),path("M181 238H445C434 164 383 124 305 124C239 124 194 163 181 238Z")), 620)
    add("r", path("M40 540V0H172L183 75Q245-10 348-10H382V140H333Q190 140 190 294V540Z"), 410)
    add("t", union(rect(150,-140,145,680,40),rect(35,0,380,130,30),path("M150 360H295V371Q295 419 343 419H403V540H322Q150 540 150 360Z")), 440)
    add("f", union(path("M130 540V37Q130-180 339-180H417V-47H367Q275-47 275 42V540Z"),rect(40,0,370,130,28)), 425)
    add("s", stroke("M458 89C399 54 317 41 255 58 158 82 139 167 240 201L377 247C549 306 529 459 378 481 266 499 171 481 101 435",135), 570)
    add("z", union(rect(40,0,480,130,28),rect(40,410,480,130,28),poly([(360,120),(520,120),(199,420),(40,420)])), 560)
    add("x", union(stroke("M98 68L471 472",140),stroke("M471 68L98 472",140)), 570)
    add("k", union(rect(40,-180,145,720,40),stroke("M438 65L184 283L455 473",140)), 560)
    add("w", path("M20 0H167L255 329 366 0H486L598 329 685 0H832L680 502Q666 544 619 544H580Q536 544 522 503L426 234 329 503Q315 544 271 544H233Q186 544 172 502L20 0Z"), 855)

    # Capitals share the lowercase's generous counters and softened terminals.
    add("O",ring(y=-190,w=640,h=740),700)
    # Capitals are drawn at cap proportions, not stretched lowercase outlines.
    add("C",path("M615-83Q628-67 613-51L545 18Q531 32 517 16C476-28 424-50 354-50C242-50 180 32 180 180C180 328 242 410 354 410C424 410 476 388 518 343Q532 329 547 343L615 411Q630 427 615 443C550 515 460 550 350 550C148 550 30 411 30 180C30-51 148-190 350-190C460-190 550-155 615-83Z"),680)
    add("G",path("M615-83Q628-67 613-51L545 18Q531 32 517 16C476-28 424-50 354-50C242-50 180 32 180 180C180 328 242 410 354 410C414 410 464 393 500 360V280H382Q358 280 358 256V172Q358 148 382 148H617Q641 148 641 172V417C571 503 467 550 350 550C148 550 30 411 30 180C30-51 148-190 350-190C460-190 550-155 615-83Z"),690)
    add("Q",union(g["O"][0],stroke("M422 369L643 563",125)),720)
    add("A",union(stroke("M92 475L298-116Q311-155 326-116L537 475",145),rect(180,228,280,125,20)),650)
    add("V",path("M26-180H188L337 345 487-180H650L430 487Q412 544 355 544H317Q260 544 242 487Z"),675)
    add("W",shift(g["w"][0],sy=720/540,y=-180),880)
    add("M",union(stroke("M110 470V-110L355 220L600-110V470",145)),710)
    add("N",stroke("M110 470V-110L571 470V-110",145),680)
    add("H",union(rect(40,-180,145,720,35),rect(470,-180,145,720,35),rect(130,108,430,140,24)),655)
    add("I",rect(40,-180,145,720,40),225)
    add("L",union(rect(40,-180,145,720,40),rect(110,395,407,145,32)),560)
    add("T",union(rect(28,-180,592,145,35),rect(251,-130,145,670,35)),650)
    add("E",path("M66-180H518Q542-180 542-156V-64Q542-40 518-40H185V105H465Q489 105 489 129V211Q489 235 465 235H185V400H518Q542 400 542 424V516Q542 540 518 540H66Q40 540 40 516V-156Q40-180 66-180Z"),580)
    add("F",union(rect(40,-180,145,720,32),rect(130,-180,405,140,30),rect(130,110,350,130,25)),570)
    add("B",union(rect(40,-180,145,720,35),minus(rect(70,-180,490,397,175),rect(185,-52,220,137,58)),minus(rect(70,110,515,430,185),rect(185,248,245,154,64))),625)
    add("P",union(rect(40,-180,145,720,35),minus(rect(70,-180,510,450,185),rect(185,-40,245,170,73))),620)
    add("R",union(g["P"][0],stroke("M322 212L534 472",143)),640)
    add("D",union(rect(40,-180,145,720,32),minus(rect(60,-180,570,720,280),rect(185,-40,290,440,140))),670)
    add("U",path("M40-180H190V250Q190 409 325 409T460 250V-180H610V253Q610 550 325 550T40 253Z"),650)
    add("J",stroke("M434-110V287Q434 480 257 480Q110 480 94 350",145),550)
    add("S",shift(g["s"][0],sy=720/540,y=-180,sx=1.07),620)
    add("Z",union(rect(40,-180,540,140,30),rect(40,400,540,140,30),poly([(395,-65),(580,-65),(225,425),(40,425)])),620)
    add("X",union(stroke("M112-110L530 470",145),stroke("M530-110L112 470",145)),650)
    add("K",union(rect(40,-180,145,720,40),stroke("M502-110L186 160L522 470",145)),640)
    add("Y",union(stroke("M103-110L320 183L537-110",145),rect(247,150,145,390,35)),650)

    # Figures are deliberately distinguishable: barred 1, open 4, oval 0.
    add("0",ring(x=35,y=-190,w=560,h=740),630)
    add("1",union(stroke("M90-42L260-125V468",140),rect(92,402,350,138,30)),500)
    add("2",union(stroke("M110-38C144-137 385-161 468-36C553 93 381 204 110 462",140),rect(65,402,475,138,30)),610)
    add("3",stroke("M111-83C244-170 496-142 496 40Q496 172 309 172M309 172Q516 172 516 349C516 520 266 546 112 451",140),620)
    add("4",union(stroke("M355-110L80 280H533",130),rect(339,-180,140,720,28)),605)
    add("5",union(rect(70,-180,450,135,28),rect(70,-150,140,300,25),stroke("M142 120C340 42 518 155 518 330C518 507 276 551 113 452",140)),620)
    add("6",union(ring(x=35,y=65,w=550,h=485,weight=133),stroke("M464-101C220-170 100-7 107 277",135)),620)
    add("7",union(rect(45,-180,510,140,28),poly([(391,-64),(555,-64),(295,540),(130,540)])),600)
    add("8",union(ring(x=65,y=-190,w=490,h=395,weight=125),ring(x=30,y=150,w=560,h=400,weight=130)),620)
    add("9",shift(g["6"][0],x=620,y=360,sx=-1,sy=-1),620)

    # Printable ASCII punctuation, plus common editorial and currency characters.
    add(" ",pathops.Path(),270)
    add(".",rect(40,388,150,152,46),230)
    add(",",union(rect(45,388,150,152,40),poly([(98,490),(193,490),(100,662),(28,662)])),235)
    add(":",union(g["."][0],shift(g["."][0],y=-315)),230)
    add(";",union(g[","][0],shift(g["."][0],y=-315)),235)
    add("-",rect(40,210,310,125,28),390)
    add("_",rect(20,600,540,110,24),580)
    add("!",union(rect(40,-180,140,455,40),g["."][0]),225)
    add("?",union(stroke("M105-60Q230-193 388-87Q515 29 342 146Q265 194 265 252",130),rect(194,388,145,152,44)),520)
    add("'",rect(50,-180,110,210,32),210)
    add('"',union(g["'"][0],shift(g["'"][0],x=190)),400)
    add("/",stroke("M392-168L85 590",105),485)
    add("\\",stroke("M85-168L392 590",105),485)
    add("(",stroke("M275-188Q35 160 275 635",110),360)
    add(")",shift(g["("][0],x=360,sx=-1),360)
    add("[",union(rect(65,-200,105,840,20),rect(65,-200,225,105,20),rect(65,535,225,105,20)),350)
    add("]",shift(g["["][0],x=350,sx=-1),350)
    add("{",stroke("M297-185Q170-185 170-30V60Q170 180 73 210Q170 240 170 360V450Q170 610 297 610",100),370)
    add("}",shift(g["{"][0],x=370,sx=-1),370)
    add("+",union(rect(210,10,120,460,25),rect(40,180,460,120,25)),550)
    add("=",union(rect(40,100,460,120,25),rect(40,310,460,120,25)),550)
    add("<",stroke("M425 28L100 248L425 468",105),540)
    add(">",shift(g["<"][0],x=540,sx=-1),540)
    add("|",rect(55,-210,100,870,25),210)
    add("~",stroke("M85 280Q185 140 285 260T485 240",90),570)
    add("`",poly([(60,-230),(190,-230),(280,-65),(190,-65)]),330)
    add("^",stroke("M85 75L255-140L425 75",100),510)
    add("*",union(stroke("M250-130V220",80),stroke("M98-42L402 132",80),stroke("M98 132L402-42",80)),500)
    add("#",union(stroke("M235-130L105 500",88),stroke("M460-130L330 500",88),rect(40,40,500,90,15),rect(15,290,500,90,15)),600)
    add("%",union(ring(28,-180,250,300,83),ring(332,240,250,300,83),stroke("M475-130L135 490",85)),620)
    add("&",union(stroke("M494 466L212 98Q100-72 258-118Q425-157 429-17Q429 71 223 215Q59 321 140 434Q260 582 507 235",110)),625)
    add("$",union(g["S"][0],rect(254,-263,78,880,20)),620)
    add("@",union(ring(20,-160,760,770,100),shift(g["a"][0],x=155,y=40,sx=.66,sy=.66),stroke("M590 65V303Q590 398 681 338",84)),820)
    add("£",union(stroke("M485-77Q249-235 191 7V452",130),rect(52,175,370,105,20),rect(50,405,500,135,28)),610)
    add("€",union(g["C"][0],rect(10,63,400,70,12),rect(10,239,370,70,12)),650)
    add("©",union(ring(20,-200,760,760,70),shift(g["c"][0],x=195,y=28,sx=.65,sy=.65)),800)
    add("®",union(ring(20,-200,760,760,70),shift(g["R"][0],x=200,y=60,sx=.58,sy=.58)),800)
    add("°",ring(30,-180,280,280,80),370)
    add("•",oval(40,150,180,180),260)
    add("×",union(stroke("M112 42L438 428",100),stroke("M438 42L112 428",100)),550)
    add("÷",union(rect(40,180,460,110,24),oval(216,-15,110,110),oval(216,375,110,110)),550)
    add("±",union(g["+"][0],rect(40,540,460,100,24)),550)
    add("–",rect(25,210,550,115,20),600)
    add("—",rect(25,210,820,115,20),870)
    add("…",union(g["."][0],shift(g["."][0],x=240),shift(g["."][0],x=480)),710)
    add("’",union(rect(55,-180,115,125,30),poly([(100,-100),(166,-100),(110,30),(35,30)])),220)
    add("‘",shift(g["’"][0],x=220,y=-150,sx=-1,sy=-1),220)
    add("“",union(g["‘"][0],shift(g["‘"][0],x=180)),400)
    add("”",union(g["’"][0],shift(g["’"][0],x=180)),400)
    add(" ",pathops.Path(),270)

    # Precomposed Latin accents use the same original base outlines.
    accents = {
        "\u0301":poly([(-110,-72),(-20,-72),(125,-220),(-10,-220)]),
        "\u0300":poly([(20,-72),(110,-72),(-10,-220),(-145,-220)]),
        "\u0302":stroke("M-125-95L0-205L125-95",70),
        "\u0303":stroke("M-140-110Q-70-205 0-140T140-165",63),
        "\u0308":union(oval(-145,-180,105,105),oval(40,-180,105,105)),
        "\u030a":ring(-100,-245,200,200,54),
        "\u0304":rect(-140,-167,280,65,18),
        "\u0306":stroke("M-132-190Q0-40 132-190",65),
        "\u030c":stroke("M-125-195L0-85L125-195",70),
        "\u0307":oval(-54,-180,108,108),
        "\u0327":stroke("M35 556L-30 616Q95 623 40 699Q0 738-70 704",60),
        "\u0328":stroke("M85 535Q-100 700 60 699",60),
    }
    for code in range(0xC0,0x180):
        ch=chr(code)
        parts=unicodedata.normalize("NFD",ch)
        if len(parts)==2 and parts[0] in g and parts[1] in accents:
            base, advance=g[parts[0]]
            if parts[0]=="i":
                base=minus(base,rect(-100,-260,500,260))
            mark=accents[parts[1]]
            top=-180 if parts[0].isupper() or parts[0] in "bdfhkl" else 0
            add(ch,union(base,shift(mark,x=advance/2,y=top if parts[1] not in "\u0327\u0328" else 0)),advance)
    add("ø",union(g["o"][0],stroke("M119 497L512 42",75)),630)
    add("Ø",union(g["O"][0],stroke("M113 472L594-118",78)),700)
    add("æ",union(shift(g["a"][0],sx=.88),shift(g["e"][0],x=420,sx=.88)),970)
    add("Æ",union(shift(g["A"][0],sx=.9),shift(g["E"][0],x=435,sx=.9)),1000)
    add("ß",path("M40 540V45Q40-190 258-190Q469-190 469 9Q469 113 369 169Q564 222 564 371Q564 550 354 550H277V419H334Q414 419 414 365Q414 296 277 278V142Q328 113 328 18Q328-52 258-52Q185-52 185 45V540Z"),610)
    add("ð",union(g["o"][0],stroke("M203-177Q528-123 522 193",110),stroke("M252-40L470-171",65)),630)
    add("Ð",union(g["D"][0],rect(0,115,330,105,20)),670)
    add("þ",union(g["p"][0],rect(40,-180,145,400,30)),620)
    add("Þ",shift(g["þ"][0],sy=1.05),650)
    add("ĳ",union(g["i"][0],shift(g["j"][0],x=225)),495)
    add("Ĳ",union(g["I"][0],shift(g["J"][0],x=225)),775)
    return g


def svg_path(p):
    pen=SVGPathPen(None,ntos=lambda n: f"{n:.3f}".rstrip("0").rstrip(".") if n else "0")
    p.draw(pen)
    return pen.getCommands()


def svg(p, viewbox, color="currentColor", title="Clyvora", background=None, radius=0):
    x,y,w,h=viewbox
    bg=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{background}"/>' if background else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" role="img" aria-label="{html.escape(title)}">{bg}<path fill="{color}" d="{svg_path(p)}"/></svg>\n'


def inset_shape(shape, amount):
    """Thin a filled outline evenly without redrawing its letter skeleton."""
    if not amount or not shape.contours:
        return shape
    base = pathops.Path()
    base.addPath(shape)
    base.convertConicsToQuads(.2)
    edge = pathops.Path()
    edge.addPath(base)
    edge.stroke(amount * 2, pathops.LineCap.BUTT_CAP, pathops.LineJoin.ROUND_JOIN, 4)
    edge.convertConicsToQuads(.2)
    return pathops.op(base, edge, pathops.PathOp.DIFFERENCE)


def build_font(g, *, style, weight, suffix, inset=0, slant=0):
    names={ch: f"uni{ord(ch):04X}" for ch in g}
    source={ch:(inset_shape(shape,inset),advance) for ch,(shape,advance) in g.items()}
    ligature=union(source["y"][0],shift(source["v"][0],x=490))
    # A small top incision makes the shared shoulder intentional and readable.
    ligature=minus(ligature,poly([(559,-1),(584,-1),(565,58)]))
    all_glyphs={names[ch]:(p,adv) for ch,(p,adv) in source.items()}
    all_glyphs["y_v"]=(ligature,1115)
    all_glyphs[".notdef"]=(minus(rect(50,-150,500,690,25),rect(170,-30,260,450,10)),600)
    order=[".notdef"]+[names[ch] for ch in g]+["y_v"]
    fb=FontBuilder(1000,isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({**{ord(ch):name for ch,name in names.items()},0xE000:"y_v"})
    contours,metrics={},{}
    for name,(p,advance) in all_glyphs.items():
        p=pathops.simplify(p)
        p.convertConicsToQuads(.2)
        pen=TTGlyphPen(None)
        target=Cu2QuPen(pen,.65,reverse_direction=True)
        # Source outlines use downward-increasing Y. Anchor the shear at the
        # baseline so a negative source-space slant makes the tops lean right.
        p.draw(TransformPen(target,(1,0,slant,-1,-slant*540,540)))
        glyph=pen.glyph()
        glyph.recalcBounds(None)
        contours[name]=glyph
        if slant:
            # Preserve the original rhythm; expand only when the slant would
            # otherwise push the right edge into the next glyph.
            farthest=slant*(p.bounds[1]-540) if slant<0 else slant*(p.bounds[3]-540)
            advance += max(0,round(p.bounds[2] + farthest - advance - 32))
        metrics[name]=(advance,glyph.xMin if glyph.numberOfContours else 0)
    fb.setupGlyf(contours)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=1020,descent=-260,lineGap=0)
    full_name=f"Clyvora Display {style}"
    selection={"Regular":0x40,"Italic":0x01,"Bold":0xA0}[style]
    fb.setupNameTable({"familyName":"Clyvora Display","styleName":style,"uniqueFontIdentifier":f"ClyvoraDisplay-{suffix}-{VERSION}","fullName":full_name,"psName":f"ClyvoraDisplay-{suffix}","version":f"Version {VERSION}","copyright":COPYRIGHT,"manufacturer":"Clyvora","designer":"Clyvora","description":"Original rounded display lettering for Clyvora. Optional y-v ligature. Latin display coverage.","licenseDescription":"Proprietary. See the Clyvora brand license distributed with this font.","licenseInfoURL":"https://www.clyvora.tech/brand/"})
    fb.setupOS2(version=4,sTypoAscender=1020,sTypoDescender=-260,sTypoLineGap=0,usWinAscent=1020,usWinDescent=260,sxHeight=540,sCapHeight=720,usWeightClass=weight,usWidthClass=5,fsSelection=selection,fsType=0)
    fb.setupPost(keepGlyphNames=True)
    fb.setupMaxp()
    fb.font["head"].macStyle=(1 if weight>=700 else 0)|(2 if slant else 0)
    if slant:
        fb.font["post"].italicAngle=-9
    fb.font["head"].fontRevision=FONT_REVISION
    # Stable OpenType timestamps make releases reproducible byte for byte.
    fb.font["head"].created=fb.font["head"].modified=3877632000
    features=["languagesystem DFLT dflt; languagesystem latn dflt;",f"feature dlig {{ sub {names['y']} {names['v']} by y_v; }} dlig;", "feature kern {"]
    pairs={"cl":-4,"ly":-10,"vo":-14,"or":-10,"ra":-14,"ov":-12,"va":-18,"yo":-12,"To":-40,"Ta":-36,"Te":-32,"AV":-40,"VA":-35,"WA":-22,"Yo":-35,"LT":-22,"Fo":-25,"Pa":-20}
    for pair,value in pairs.items():
        features.append(f"pos {names[pair[0]]} {names[pair[1]]} {value};")
    features.extend([f"pos {names['l']} y_v -10;",f"pos y_v {names['o']} -14;","} kern;"])
    addOpenTypeFeaturesFromString(fb.font,"\n".join(features))
    fb.font.recalcTimestamp=False
    ttf=FONTS/f"ClyvoraDisplay-{suffix}.ttf"
    fb.save(ttf)
    fb.font.flavor="woff2"
    fb.font.save(FONTS/f"ClyvoraDisplay-{suffix}.woff2")
    return ligature,names


def build_art(g,mark):
    parts=[]
    x=0
    for ch in ("c","l","yv","o","r","a"):
        p,advance=(mark,1115) if ch=="yv" else g[ch]
        parts.append(shift(p,x=x))
        x+=advance-({"c":4,"l":10,"yv":14,"o":10,"r":14}.get(ch,0))
    word=union(*parts)
    vb=(0,-200,x,940)
    markvb=(0,-10,1120,750)
    for name,p,box in [("wordmark",word,vb),("monogram",mark,markvb)]:
        for suffix,color in [("", "currentColor"),("-black",INK),("-white",PAPER)]:
            (BRAND/f"clyvora-{name}{suffix}.svg").write_text(svg(p,box,color,f"Clyvora {name}"),encoding="utf-8")
    # The favicon and app tiles are produced from the exact same ligature.
    tilemark=shift(mark,x=13,y=20,sx=38/1120,sy=38/1120)
    (PUBLIC/"brand-mark.svg").write_text(svg(tilemark,(0,0,64,64),PAPER,"Clyvora",INK,15),encoding="utf-8")
    (BRAND/"clyvora-icon.svg").write_text(svg(tilemark,(0,0,64,64),PAPER,"Clyvora",INK,15),encoding="utf-8")
    return word,vb,markvb


def raster(g,wordvb,markvb):
    fontpath=str(FONTS/"ClyvoraDisplay-Bold.ttf")
    def font(size): return ImageFont.truetype(fontpath,size)
    def text_image(text,size,color,ligature=False):
        f=font(size)
        # Private-use access is useful in design apps without discretionary ligatures.
        text=text.replace("yv","\ue000") if ligature else text
        bounds=f.getbbox(text)
        im=Image.new("RGBA",(bounds[2]-bounds[0]+8,bounds[3]-bounds[1]+8))
        ImageDraw.Draw(im).text((4-bounds[0],4-bounds[1]),text,font=f,fill=color)
        return im
    for filename,size in [("favicon.png",64),("apple-touch-icon.png",180),("icon-192.png",192),("icon-512.png",512)]:
        big=Image.new("RGB",(size*4,size*4),INK)
        # The same glyph is used, with fixed 20% minimum clear space.
        mark=text_image("yv",round(size*4*.67),PAPER,True)
        mark.thumbnail((round(size*4*.62),round(size*4*.62)),Image.Resampling.LANCZOS)
        big.paste(mark,((size*4-mark.width)//2,(size*4-mark.height)//2),mark)
        big.resize((size,size),Image.Resampling.LANCZOS).save(PUBLIC/filename)
    for filename,color in [("dark-logo.png",PAPER),("light-logo.png",INK)]:
        im=Image.new("RGBA",(400,400))
        mark=text_image("yv",540,color,True)
        mark.thumbnail((260,260),Image.Resampling.LANCZOS)
        im.paste(mark,((400-mark.width)//2,(400-mark.height)//2),mark)
        im.save(PUBLIC/filename)
    for filename in ["social-card.png","og.png"]:
        im=Image.new("RGB",(1200,630),INK)
        word=text_image("clyvora",240,PAPER,True)
        word.thumbnail((880,260),Image.Resampling.LANCZOS)
        im.paste(word,((1200-word.width)//2,152),word)
        # Supporting copy uses our own original font as well.
        draw=ImageDraw.Draw(im)
        draw.text((600,450),"Small tools. Clear purpose.",font=font(35),anchor="mm",fill="#aaa9a4")
        im.save(PUBLIC/filename)
    proof=Image.new("RGB",(1600,1160),PAPER)
    draw=ImageDraw.Draw(proof)
    draw.text((76,58),"Clyvora Display / Bold",font=font(36),fill=INK)
    brand=text_image("clyvora",330,INK,True)
    brand.thumbnail((1448,310),Image.Resampling.LANCZOS)
    proof.paste(brand,((1600-brand.width)//2,160),brand)
    for row,(sample,size) in enumerate([("abcdefghijklmnopqrstuvwxyz",64),("ABCDEFGHIJKLMNOPQRSTUVWXYZ",60),("0123456789  !?&@",70),("IJsselmeer. Eén idee, veel plezier.",54)]):
        draw.text((76,540+row*112),sample,font=font(size),fill=INK)
    draw.line((76,1000,1524,1000),fill="#cbc9c1",width=2)
    mark=text_image("yv",145,INK,True)
    proof.paste(mark,(76,1030),mark)
    draw.text((340,1044),f"Original lettering / v{VERSION}",font=font(30),fill=INK)
    proof.save(BRAND/"clyvora-display-specimen.png")


def main():
    BRAND.mkdir(parents=True,exist_ok=True)
    FONTS.mkdir(parents=True,exist_ok=True)
    g=glyphs()
    mark,names=build_font(g,style="Bold",weight=700,suffix="Bold")
    build_font(g,style="Regular",weight=400,suffix="Regular",inset=20)
    build_font(g,style="Italic",weight=400,suffix="Italic",inset=20,slant=-.1584)
    _,vb,markvb=build_art(g,mark)
    raster(g,vb,markvb)
    # Emit a shared source module: React and exported assets use identical paths.
    (ROOT/"src"/"brand.ts").write_text("// Generated by scripts/brand/build.py. Edit the original outlines there.\n"+
        f"export const brandMarkPath = {json.dumps(svg_path(mark))}\n"+
        f"export const brandMarkViewBox = {json.dumps(' '.join(map(str,markvb)))}\n",encoding="utf-8")
    manifest={"name":"Clyvora Display","version":VERSION,"styles":{"Regular":{"weight":400,"italic":False},"Italic":{"weight":400,"italic":True},"Bold":{"weight":700,"italic":False}},"unitsPerEm":1000,"xHeight":540,"capHeight":720,"characters":"".join(g),"encodedCharacters":len(g)+1,"glyphs":len(g)+2,"monogramCodepoint":"U+E000","features":{"kern":"Optical pair spacing","dlig":"Optional joined y-v brand ligature"},"copyright":COPYRIGHT,"source":"scripts/brand/build.py","files":{}}
    for f in sorted([*FONTS.glob("ClyvoraDisplay-*"),*BRAND.glob("clyvora-*")]):
        if f.suffix==".zip":
            continue
        manifest["files"][f.relative_to(PUBLIC).as_posix()]={"bytes":f.stat().st_size,"sha256":hashlib.sha256(f.read_bytes()).hexdigest()}
    (BRAND/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Built Clyvora Display {VERSION}: {len(g)+1} encoded characters, TTF + WOFF2, brand vectors and raster exports.")


if __name__=="__main__": main()
