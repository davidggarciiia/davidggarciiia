import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "lib"))
from nb import *  # noqa

S = {}
def scene(fn):
    S[fn.__name__] = fn
    return fn

ORANGE = "#ff8a2a"


def ln(ident, d, cls="ink", w=4, fill="none"):
    return f'<path class="ln {cls}" pathLength="1" stroke-width="{w}" fill="{fill}" d="{d}" id="{ident}"/>'


@scene
def s1():
    mols = [(620, 590), (700, 600), (790, 588), (880, 602), (960, 590), (1050, 598), (1140, 588), (1230, 600), (1320, 592), (1400, 600)]
    svg = (f'<g transform="translate(420,460) scale(1.8)">{PLANE_SIDE}</g>'
           + "".join(f'<circle class="s1-o" cx="{x}" cy="{y}" r="15" fill="rgba(66,188,240,.65)"/>' for x, y in mols))
    html = (text("s1-o2", 1500, 420, "O₂", "lbl", "color:#0a7fb8;font-size:80px")
            + text("s1-title", 200, 110, mark("Oxígeno, comunicaciones y cajas negras", "blue", "s1-title-hl"), "h1"))
    js = """
tl.set(q("svg > g .ln"),{strokeDashoffset:0},0);
write("#s1-o2",T[0]+0.6,0.4);
tl.to(q(".s1-o"),{opacity:0,y:-40,duration:0.4,stagger:{each:0.35,from:"random"}},T[0]+2.6);
write("#s1-title",T[1]+0.8,1.6); hl("#s1-title-hl",T[1]+2.4,0.5);
tl.to(q(".s1-o"),{opacity:1,y:0,duration:0.4,stagger:0.08},T[1]+2.6);
"""
    return svg, html, js


@scene
def s2():
    svg = (ln("s2-ax", "M400,860 L1500,860 M400,860 L400,300", "ink", 5)
           + ln("s2-cur", "M440,340 C640,420 780,640 1000,740 C1150,800 1300,820 1460,830", "pk", 7)
           + arrow(1500, 860, 1540, 860, "ink", 5, 22, "s2-xh") + arrow(400, 300, 400, 260, "ink", 5, 22, "s2-yh"))
    html = (title("s2", "1 · Tiempo útil de consciencia")
            + text("s2-y", 200, 250, "tiempo", "sm") + text("s2-x", 1380, 890, "altitud", "sm")
            + text("s2-a", 1000, 330, mark("TUC", "pink", "s2-ah") + " · actuar con normalidad", "lbl")
            + text("s2-b", 1000, 400, "sin oxígeno", "sm")
            + text("s2-c", 1000, 560, "+ altura → − tiempo", "lbl"))
    js = """
write("#s2-title",T[0]+0.1,1.1); hl("#s2-title-hl",T[0]+1.2);
draw("#s2-ax",T[0]+0.8,0.8); draw("#s2-xh path, #s2-yh path",T[0]+1.5,0.3); write("#s2-y, #s2-x",T[0]+1.6,0.5);
write("#s2-b",T[0]+2.4,0.8);
write("#s2-a",T[1]+0.2,1.2); hl("#s2-ah",T[1]+1.4);
draw("#s2-cur",T[2]+0.3,1.8); write("#s2-c",T[2]+1.6,1.0);
"""
    return svg, html, js


@scene
def s3():
    masks = ""
    for i, x in enumerate([780, 960, 1140]):
        masks += (f'<g class="s3-m" id="s3-m{i}"><path class="ink" fill="none" stroke-width="3" d="M{x},330 C{x+10},420 {x-10},480 {x},560"/>'
                  f'<path class="ink" fill="rgba(255,214,90,.55)" stroke-width="4" d="M{x-34},560 L{x+34},560 L{x+26},610 Q{x},632 {x-26},610 Z"/></g>')
    svg = (ln("s3-ceil", "M600,320 L1320,320", "ink", 6)
           + masks
           + '<rect id="s3-gen" x="1400" y="250" width="180" height="70" rx="10" fill="rgba(255,92,168,.3)" stroke="#23307a" stroke-width="4"/>'
           + ln("s3-clock", "M420,760 m0,-110 a110,110 0 1 1 -0.1,0", "bl", 10)
           + '<path id="s3-hand" class="ink" fill="none" stroke-width="6" d="M420,760 L420,680"/>')
    html = (title("s3", "2 · Máscaras de pasajeros", "blue")
            + text("s3-a", 200, 260, "sistema " + mark("fijo", "blue", "s3-ah"), "lbl")
            + text("s3-g", 1380, 340, "generador químico", "sm")
            + text("s3-mix", 1380, 420, "O₂ + aire de cabina", "lbl")
            + text("s3-t", 580, 700, mark("≈ 15 min", "pink", "s3-th"), "lbl")
            + text("s3-t2", 580, 770, "hasta bajar a una altura", "sm") + text("s3-t3", 580, 820, "donde se respira bien", "sm"))
    js = """
write("#s3-title",T[0]+0.1,0.9); hl("#s3-title-hl",T[0]+1.0);
draw("#s3-ceil",T[0]+0.4,0.6); write("#s3-a",T[0]+0.6,0.8); hl("#s3-ah",T[0]+1.4);
tl.set(q(".s3-m"),{opacity:0},0);
tl.fromTo(q(".s3-m"),{opacity:1,y:-220},{opacity:1,y:0,duration:0.7,ease:"bounce.out",stagger:0.15},T[0]+3.0);
tl.fromTo(q("#s3-gen"),{opacity:0},{opacity:1,duration:0.3},T[1]+1.4); write("#s3-g",T[1]+1.5,0.8);
write("#s3-mix",T[1]+3.0,1.0);
draw("#s3-clock",T[2]+0.4,1.4); tl.fromTo(q("#s3-hand"),{rotation:0,svgOrigin:"420 760"},{rotation:360,svgOrigin:"420 760",duration:3,ease:"none"},T[2]+0.4);
write("#s3-t",T[2]+0.6,0.7); hl("#s3-th",T[2]+1.3); write("#s3-t2",T[2]+3.2,0.9); write("#s3-t3",T[2]+4.2,0.9);
"""
    return svg, html, js


@scene
def s4():
    smoke = "".join(f'<path class="s4-sm" fill="none" stroke="#9aa0b8" stroke-width="5" d="M{x},{y} c20,-20 -20,-40 0,-60 c20,-20 -20,-40 0,-60"/>' for x, y in [(240, 760), (280, 790), (520, 770)])
    svg = (smoke
           + ln("s4-hood", "M260,700 C260,520 320,440 400,440 C480,440 540,520 540,700 L520,780 L280,780 Z", "ink", 5, "rgba(255,214,90,.35)")
           + ln("s4-vis", "M320,560 L480,560 L480,640 L320,640 Z", "bl", 5, "rgba(66,188,240,.25)")
           + ln("s4-bot", "M860,500 C860,470 880,460 900,460 L960,460 C980,460 1000,470 1000,500 L1000,780 L860,780 Z", "ink", 5, "rgba(66,188,240,.3)")
           + ln("s4-valve", "M905,460 L905,420 L955,420 L955,460 M955,430 C1040,430 1060,520 1040,600", "ink", 4)
           + ln("s4-mask", "M1010,600 L1070,600 L1060,650 Q1040,665 1020,650 Z", "ink", 4, "rgba(255,214,90,.55)")
           + ln("s4-head", "M1480,780 C1480,640 1430,600 1430,540 C1430,450 1500,420 1560,420 C1630,420 1680,470 1680,540 C1680,620 1640,650 1640,780", "ink", 5)
           + ln("s4-qd", "M1400,560 L1470,540 L1500,620 L1420,640 Z M1470,560 C1530,520 1600,500 1660,500", "pk", 5, "rgba(255,92,168,.3)"))
    html = (title("s4", "3 · Oxígeno portátil y de cabina")
            + text("s4-a", 200, 820, mark("PBE", "blue", "s4-ah") + " · tripulantes", "lbl")
            + text("s4-a2", 200, 890, "protege de humo y tóxicos", "sm")
            + text("s4-b", 780, 820, mark("Terapéutico", "pink", "s4-bh"), "lbl")
            + text("s4-b2", 780, 890, "limitado · 20–60 min", "sm")
            + text("s4-c", 1340, 820, mark("Cabina de vuelo", "blue", "s4-ch"), "lbl")
            + text("s4-c2", 1340, 890, "O₂ puro a presión · ≈ 2 h", "sm"))
    js = """
write("#s4-title",T[0]+0.1,1.1); hl("#s4-title-hl",T[0]+1.2);
draw("#s4-hood",T[0]+0.8,1.2); draw("#s4-vis",T[0]+1.8,0.5); write("#s4-a",T[0]+2.0,0.8); hl("#s4-ah",T[0]+2.8);
tl.fromTo(q(".s4-sm"),{opacity:0},{opacity:0.8,duration:0.5,stagger:0.2},T[1]+0.6);
tl.to(q(".s4-sm"),{y:-20,x:-10,duration:1.2,yoyo:true,repeat:3,ease:"sine.inOut"},T[1]+0.8);
write("#s4-a2",T[1]+1.2,1.2);
draw("#s4-bot",T[2]+0.3,0.9); draw("#s4-valve",T[2]+1.1,0.5); draw("#s4-mask",T[2]+1.5,0.4); write("#s4-b",T[2]+2.0,0.8); hl("#s4-bh",T[2]+2.8);
write("#s4-b2",T[3]+0.6,1.6);
draw("#s4-head",T[4]+0.3,1.0); draw("#s4-qd",T[4]+1.2,0.8); write("#s4-c",T[4]+1.4,0.9); hl("#s4-ch",T[4]+2.3);
write("#s4-c2",T[5]+0.4,1.6);
"""
    return svg, html, js


@scene
def s5():
    waves = lambda cx, cy, ident: "".join(f'<path class="{ident}" fill="none" stroke="#1ea7e4" stroke-width="5" d="M{cx+r*0.7:.0f},{cy-r*0.7:.0f} A{r},{r} 0 0 1 {cx+r*0.7:.0f},{cy+r*0.7:.0f}"/>' for r in (40, 75, 110))
    svg = (f'<g transform="translate(300,300) scale(0.9)">{PLANE_SIDE}</g>'
           + f'<g transform="translate(1260,250) scale(0.6)">{PLANE_SIDE}</g>'
           + ln("s5-tower", "M560,880 L600,620 L640,880 M570,620 L630,620 L630,580 L570,580 Z", "ink", 5)
           + ln("s5-g", "M200,880 L1720,880", "ink", 4)
           + ln("s5-at", "M560,420 L600,580", "bl", 5) + ln("s5-aa", "M860,380 L1260,320", "bl", 5)
           + '<g id="s5-spk"><path class="ink" fill="rgba(255,92,168,.35)" stroke-width="5" d="M1150,600 L1190,600 L1240,560 L1240,720 L1190,680 L1150,680 Z"/>'
           + waves(1250, 640, "s5-w") + '</g>'
           + ln("s5-phone", "M1520,600 C1500,640 1500,700 1520,740 L1560,740 L1560,700 L1540,700 C1535,680 1535,660 1540,640 L1560,640 L1560,600 Z", "ink", 5, "rgba(66,188,240,.3)"))
    html = (title("s5", "4 · Comunicaciones", "blue")
            + text("s5-a", 380, 520, "aire-tierra", "sm", "color:#0a7fb8") + text("s5-b", 940, 260, "aire-aire", "sm", "color:#0a7fb8")
            + text("s5-pa", 1100, 760, mark("PA", "pink", "s5-pah") + " · megafonía", "lbl")
            + text("s5-ip", 1480, 760, "interfonos", "lbl")
            + text("s5-ob", 1100, 900, "obligatorio · más de 19 asientos", "sm"))
    js = """
write("#s5-title",T[0]+0.1,0.9); hl("#s5-title-hl",T[0]+1.0);
tl.set(q("svg > g:not(#s5-spk) .ln"),{strokeDashoffset:0},0);
tl.set(q("#s5-spk, #s5-pa, #s5-ip"),{opacity:0},0);
draw("#s5-g",T[0]+0.6,0.5); draw("#s5-tower",T[0]+3.2,0.8); draw("#s5-at",T[0]+4.0,0.5); write("#s5-a",T[0]+4.2,0.6);
draw("#s5-aa",T[0]+5.8,0.6); write("#s5-b",T[0]+6.0,0.6);
show("#s5-spk",T[1]+3.0,0.3); tl.set(q("#s5-pa"),{opacity:1},T[1]+3.0); write("#s5-pa",T[1]+3.0,0.8); hl("#s5-pah",T[1]+3.8);
tl.fromTo(q(".s5-w"),{opacity:0},{opacity:1,duration:0.2,stagger:0.2,yoyo:true,repeat:5},T[1]+3.4);
draw("#s5-phone",T[1]+6.0,0.7); tl.set(q("#s5-ip"),{opacity:1},T[1]+6.2); write("#s5-ip",T[1]+6.2,0.6);
write("#s5-ob",T[2]+0.6,1.6);
"""
    return svg, html, js


@scene
def s6():
    svg = (ln("s6-rad", "M300,880 L360,760 L420,880 M360,760 L360,700 M310,700 C340,640 380,640 410,700", "ink", 5)
           + '<path id="s6-sweep" fill="rgba(66,188,240,.25)" d="M360,690 L760,560 A420,420 0 0 1 700,880 Z"/>'
           + f'<g transform="translate(560,380) scale(0.8)">{PLANE_SIDE}</g>'
           + ln("s6-tag", "M1060,430 L1100,400 L1560,400 L1560,620 L1100,620 L1100,460 Z", "ink", 4, "rgba(255,255,255,.6)")
           + ln("s6-box", "M1000,720 L1560,720 L1560,880 L1000,880 Z", "ink", 5, "#fdfdff"))
    html = (title("s6", "5 · Transpondedor (squawk)")
            + text("s6-t1", 1130, 420, "posición", "sm") + text("s6-t2", 1130, 470, "rumbo", "sm")
            + text("s6-t3", 1130, 520, "altitud", "sm") + text("s6-t4", 1130, 570, "velocidad", "sm")
            + text("s6-c0", 1040, 730, "2 0 4 6", "big", "font-size:120px;letter-spacing:10px")
            + text("s6-c1", 1040, 730, "7 7 0 0", "big", "font-size:120px;letter-spacing:10px;color:#ff3d96")
            + text("s6-c2", 1040, 730, "7 6 0 0", "big", "font-size:120px;letter-spacing:10px;color:#ff3d96")
            + text("s6-c3", 1040, 730, "7 5 0 0", "big", "font-size:120px;letter-spacing:10px;color:#ff3d96")
            + text("s6-sq", 1000, 650, mark("squawk", "blue", "s6-sqh") + " · 4 cifras", "sm")
            + text("s6-m1", 200, 920, "7700 · emergencia general", "lbl", "color:#ff3d96")
            + text("s6-m2", 200, 920, "7600 · fallo de radio", "lbl", "color:#ff3d96")
            + text("s6-m3", 200, 920, "7500 · interferencia ilícita", "lbl", "color:#ff3d96"))
    js = """
write("#s6-title",T[0]+0.1,1.0); hl("#s6-title-hl",T[0]+1.1);
draw("#s6-rad",T[0]+0.4,0.7);
tl.fromTo(q("#s6-sweep"),{rotation:-30,svgOrigin:"360 690",opacity:0},{opacity:1,duration:0.3},T[0]+1.0);
tl.to(q("#s6-sweep"),{rotation:20,svgOrigin:"360 690",duration:1.6,yoyo:true,repeat:Math.round((D-T[0]-1.3)/1.6),ease:"sine.inOut"},T[0]+1.3);
tl.set(q("svg > g .ln"),{strokeDashoffset:0},0);
draw("#s6-tag",T[0]+2.2,0.6);
write("#s6-t1",T[0]+3.0,0.4); write("#s6-t2",T[0]+3.8,0.4); write("#s6-t3",T[0]+4.4,0.4); write("#s6-t4",T[0]+5.0,0.5);
draw("#s6-box",T[1]+0.6,0.6); write("#s6-sq",T[1]+1.0,0.8); hl("#s6-sqh",T[1]+1.8);
tl.set(q("#s6-c1, #s6-c2, #s6-c3, #s6-m1, #s6-m2, #s6-m3"),{opacity:0},0);
write("#s6-c0",T[1]+2.0,0.6);
tl.set(q("#s6-c0"),{opacity:0},T[2]+1.8); tl.set(q("#s6-c1"),{opacity:1},T[2]+1.8); write("#s6-c1",T[2]+1.8,0.5);
tl.set(q("#s6-m1"),{opacity:1},T[2]+2.6); write("#s6-m1",T[2]+2.6,1.0);
tl.set(q("#s6-c1, #s6-m1"),{opacity:0},T[3]); tl.set(q("#s6-c2, #s6-m2"),{opacity:1},T[3]); write("#s6-c2",T[3],0.5); write("#s6-m2",T[3]+0.6,0.9);
tl.set(q("#s6-c2, #s6-m2"),{opacity:0},T[4]); tl.set(q("#s6-c3, #s6-m3"),{opacity:1},T[4]); write("#s6-c3",T[4],0.5); write("#s6-m3",T[4]+0.6,1.0);
"""
    return svg, html, js


@scene
def s7():
    rings = "".join(f'<circle class="s7-ring" cx="1500" cy="800" r="{r}" fill="none" stroke="#1ea7e4" stroke-width="4"/>' for r in (30, 60, 90))
    svg = (f'<g transform="translate(240,300) scale(1.25)">{PLANE_SIDE}</g>'
           + f'<rect id="s7-bx" x="860" y="370" width="46" height="34" rx="6" fill="{ORANGE}" stroke="#23307a" stroke-width="3"/>'
           + f'<g id="s7-cvr"><rect x="300" y="560" width="300" height="200" rx="18" fill="{ORANGE}" stroke="#23307a" stroke-width="5"/>'
           + '<path class="ink" fill="none" stroke-width="6" d="M430,600 L430,670 Q450,700 470,670 L470,600 Q450,575 430,600 Z M410,660 Q450,730 490,660 M450,700 L450,730"/></g>'
           + f'<g id="s7-fdr"><rect x="700" y="560" width="300" height="200" rx="18" fill="{ORANGE}" stroke="#23307a" stroke-width="5"/>'
           + '<path class="ink" fill="none" stroke-width="6" d="M730,690 L780,640 L820,700 L860,610 L900,680 L960,630"/></g>'
           + '<path id="s7-sea" fill="rgba(66,188,240,.22)" d="M1240,620 C1300,600 1360,640 1420,620 C1480,600 1540,640 1600,620 C1660,600 1700,630 1720,620 L1720,960 L1240,960 Z"/>'
           + f'<rect id="s7-ulb" x="1470" y="780" width="60" height="40" rx="6" fill="{ORANGE}" stroke="#23307a" stroke-width="3"/>' + rings)
    html = (title("s7", "6 · Las cajas negras")
            + text("s7-or", 980, 250, "…que son " + mark("naranjas", "pink", "s7-orh"), "lbl")
            + text("s7-a", 300, 780, mark("CVR", "blue", "s7-ah") + " · voces", "lbl")
            + text("s7-b", 700, 780, mark("FDR", "blue", "s7-bh") + " · datos", "lbl")
            + text("s7-a2", 300, 850, "cabina de vuelo", "sm") + text("s7-b2", 700, 850, "en tiempo real", "sm")
            + text("s7-c", 1100, 420, "lejos del combustible", "sm")
            + text("s7-d", 1260, 520, mark("radiobaliza submarina", "pink", "s7-dh"), "lbl", "font-size:48px"))
    js = """
write("#s7-title",T[0]+0.1,0.9); hl("#s7-title-hl",T[0]+1.0);
tl.set(q("svg > g:first-child .ln"),{strokeDashoffset:0},0);
tl.set(q("#s7-cvr, #s7-fdr, #s7-sea, #s7-ulb, .s7-ring"),{opacity:0},0);
tl.fromTo(q("#s7-bx"),{opacity:0,scale:0.2,transformOrigin:"50% 50%"},{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"},T[0]+2.0);
write("#s7-or",T[0]+4.2,1.1); hl("#s7-orh",T[0]+5.3);
tl.fromTo(q("#s7-cvr"),{opacity:0,y:30},{opacity:1,y:0,duration:0.5},T[1]+0.3); write("#s7-a",T[1]+0.5,0.6); hl("#s7-ah",T[1]+1.1); write("#s7-a2",T[1]+3.6,0.8);
tl.fromTo(q("#s7-fdr"),{opacity:0,y:30},{opacity:1,y:0,duration:0.5},T[2]+0.3); write("#s7-b",T[2]+0.5,0.6); hl("#s7-bh",T[2]+1.1); write("#s7-b2",T[2]+3.0,0.8);
write("#s7-c",T[3]+0.6,1.2);
show("#s7-sea",T[3]+3.6,0.5); show("#s7-ulb",T[3]+4.0,0.3); write("#s7-d",T[3]+4.0,1.0); hl("#s7-dh",T[3]+5.0);
tl.fromTo(q(".s7-ring"),{opacity:0,scale:0.4,transformOrigin:"50% 50%"},{opacity:1,scale:1.3,duration:0.9,stagger:0.3,repeat:Math.max(1,Math.round((D-T[3]-4.4)/1.2)),ease:"sine.out"},T[3]+4.4);
"""
    return svg, html, js


@scene
def s8():
    svg = (ln("s8-sat", "M1500,300 L1580,300 L1580,360 L1500,360 Z M1420,310 L1500,320 M1580,320 L1660,310 M1420,350 L1500,340 M1580,340 L1660,350", "ink", 5)
           + ln("s8-beam", "M1540,370 L1540,560", "bl", 5))
    html = (title("s8", "7 · Frecuencias de emergencia", "blue")
            + text("s8-a", 240, 340, mark("121,5", "blue", "s8-ah") + " MHz · civil", "big", "font-size:100px")
            + text("s8-b", 240, 520, mark("243", "pink", "s8-bh") + " MHz · militar", "big", "font-size:100px")
            + text("s8-c", 240, 700, mark("406", "blue", "s8-ch") + " MHz · satélite", "big", "font-size:100px"))
    js = """
write("#s8-title",T[0]+0.1,1.1); hl("#s8-title-hl",T[0]+1.2);
write("#s8-a",T[1]+0.1,1.4); hl("#s8-ah",T[1]+1.5);
write("#s8-b",T[2]+0.1,1.3); hl("#s8-bh",T[2]+1.4);
write("#s8-c",T[3]+0.1,1.3); hl("#s8-ch",T[3]+1.4); draw("#s8-sat",T[3]+1.2,0.8); draw("#s8-beam",T[3]+1.8,0.4);
"""
    return svg, html, js


@scene
def s9():
    html = (text("s9-a", 0, 330, "Oxígeno para " + mark("respirar", "blue", "s9-ah"), "big", "width:1920px;text-align:center")
            + text("s9-b", 0, 490, "radios para " + mark("hablar", "blue", "s9-bh"), "big", "width:1920px;text-align:center")
            + text("s9-c", 0, 650, "cajas negras para " + mark("aprender", "pink", "s9-ch"), "big", "width:1920px;text-align:center"))
    js = """
write("#s9-a",T[0]+0.1,1.2); hl("#s9-ah",T[0]+1.3,0.3);
write("#s9-b",T[0]+1.8,1.0); hl("#s9-bh",T[0]+2.8,0.3);
write("#s9-c",T[0]+3.3,1.2); hl("#s9-ch",T[0]+4.5,0.4);
"""
    return "", html, js


if __name__ == "__main__":
    build(ROOT, S)
