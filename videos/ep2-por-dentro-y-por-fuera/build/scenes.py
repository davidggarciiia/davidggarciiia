import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "lib"))
from nb import *  # noqa

S = {}
def scene(fn):
    S[fn.__name__] = fn
    return fn


def lead(ident, d, cls="ink"):
    return f'<path class="ln {cls}" pathLength="1" stroke-width="3" d="{d}" id="{ident}"/>'


@scene
def s1():
    svg = f'<g id="s1-pl"><g transform="translate(420,470) scale(1.8)">{PLANE_SIDE}{GEAR}</g></g>'
    html = text("s1-title", 200, 120, mark("El avión por dentro y por fuera", "blue", "s1-title-hl"), "h1 big")
    js = """
tl.set(q(".ln"),{strokeDashoffset:0},0);
write("#s1-title",T[1]+0.2,1.6); hl("#s1-title-hl",T[1]+1.9,0.5);
tl.fromTo(q("#s1-pl"),{x:0},{x:-30,duration:D,ease:"none"},0);
"""
    return svg, html, js


@scene
def s2():
    svg = f"""<g transform="translate(390,420) scale(1.9)">{PLANE_SIDE}</g>
{lead("s2-l1","M520,605 L420,790")}{lead("s2-l2","M820,585 L820,420")}{lead("s2-l3","M1010,655 L1110,820")}
{lead("s2-l4","M925,700 L860,850")}{lead("s2-l5","M1420,470 L1390,380")}{lead("s2-l6","M1512,598 L1600,700")}
<path class="ln pk" pathLength="1" stroke-width="7" d="M1490,575 L1515,598 L1495,612" id="s2-apu"/>"""
    html = (title("s2", "1 · Las partes del avión")
            + text("s2-t1", 260, 790, mark("Cockpit", "blue", "s2-t1-hl") + " · cabina de vuelo", "lbl")
            + text("s2-t2", 640, 340, mark("Fuselaje central", "pink", "s2-t2-hl"), "lbl")
            + text("s2-t3", 1060, 820, mark("Alas", "blue", "s2-t3-hl") + " (planos)", "lbl")
            + text("s2-t4", 700, 860, "motor", "lbl")
            + text("s2-t5", 1180, 300, mark("Empenaje de cola", "pink", "s2-t5-hl"), "lbl")
            + text("s2-t6", 1560, 700, "APU", "lbl", "color:#ff3d96"))
    js = """
write("#s2-title",T[0]+0.1,1.0); hl("#s2-title-hl",T[0]+1.1);
draw("svg > g .ln",T[0]+0.2,1.4);
draw("#s2-l1",T[0]+1.0,0.4); write("#s2-t1",T[0]+1.3,0.9); hl("#s2-t1-hl",T[0]+2.2);
draw("#s2-l2",T[1]+0.6,0.4); write("#s2-t2",T[1]+0.9,0.9); hl("#s2-t2-hl",T[1]+1.8);
draw("#s2-l3",T[2]+0.6,0.4); write("#s2-t3",T[2]+0.9,0.7); hl("#s2-t3-hl",T[2]+1.6);
draw("#s2-l4",T[2]+3.6,0.4); write("#s2-t4",T[2]+3.9,0.5);
draw("#s2-l5",T[3]+0.6,0.4); write("#s2-t5",T[3]+0.9,0.9); hl("#s2-t5-hl",T[3]+1.8);
draw("#s2-apu",T[3]+3.0,0.4); draw("#s2-l6",T[3]+3.2,0.4); write("#s2-t6",T[3]+3.5,0.5);
"""
    return svg, html, js


@scene
def s3():
    xs = [520, 700, 880, 1060, 1240, 1420]
    frames = "".join(f'<ellipse class="ln pk s3-frame" pathLength="1" stroke-width="6" fill="none" cx="{x}" cy="580" rx="56" ry="170"/>' for x in xs)
    svg = f"""
<path class="ln ink" pathLength="1" stroke-width="5" d="M520,410 L1420,410" id="s3-o1"/>
<path class="ln ink" pathLength="1" stroke-width="5" d="M520,750 L1420,750" id="s3-o2"/>
<path class="ln bl s3-str" pathLength="1" stroke-width="6" d="M500,470 L1440,470"/>
<path class="ln bl s3-str" pathLength="1" stroke-width="6" d="M470,540 L1470,540"/>
<path class="ln bl s3-str" pathLength="1" stroke-width="6" d="M470,620 L1470,620"/>
<path class="ln bl s3-str" pathLength="1" stroke-width="6" d="M500,690 L1440,690"/>
{frames}
<path id="s3-skin" d="M520,410 L1420,410 A56,170 0 0 1 1420,750 L520,750 A56,170 0 0 1 520,410 Z" fill="rgba(150,160,190,.28)" stroke="#23307a" stroke-width="5"/>
"""
    html = (title("s3", "2 · Estructura del fuselaje", "blue")
            + text("s3-a", 200, 260, mark("Semimonocasco", "blue", "s3-a-hl") + " = esqueleto + piel", "lbl")
            + text("s3-b", 200, 830, mark("Largueros y larguerillos", "blue", "s3-b-hl") + " → a lo largo", "lbl")
            + text("s3-c", 200, 900, mark("Cuadernas (costillas)", "pink", "s3-c-hl") + " → como aros", "lbl")
            + text("s3-d", 1100, 260, "piel: aleación de aluminio", "lbl"))
    js = """
write("#s3-title",T[0]+0.1,1.0); hl("#s3-title-hl",T[0]+1.1);
draw("#s3-o1, #s3-o2",T[0]+0.8,1.0);
write("#s3-a",T[0]+1.6,1.4); hl("#s3-a-hl",T[0]+3.0);
draw(".s3-str",T[1]+0.3,1.0); write("#s3-b",T[1]+0.5,1.3); hl("#s3-b-hl",T[1]+1.8);
draw(".s3-frame",T[2]+0.3,0.7); write("#s3-c",T[2]+0.6,1.3); hl("#s3-c-hl",T[2]+1.9);
tl.fromTo(q("#s3-skin"),{opacity:0},{opacity:1,duration:0.8,ease:"none"},T[3]+0.8);
write("#s3-d",T[3]+1.2,1.2);
"""
    return svg, html, js


def seats(xs, y, cls):
    return "".join(f'<rect class="{cls}" x="{x}" y="{y}" width="38" height="50" rx="8" fill="rgba(66,188,240,.45)" stroke="#23307a" stroke-width="3"/>' for x in xs)


@scene
def s4():
    svg = f"""
<circle class="ln ink" pathLength="1" stroke-width="5" fill="none" cx="620" cy="560" r="185" id="s4-n"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M460,650 L780,650" id="s4-nf"/>
{seats([474,516,558], 596, "s4-ns")}{seats([645,687,729], 596, "s4-ns")}
<path class="ln pk" pathLength="1" stroke-width="6" stroke-dasharray="1 1" d="M620,450 L620,640" id="s4-na"/>
<circle class="ln ink" pathLength="1" stroke-width="5" fill="none" cx="1290" cy="560" r="255" id="s4-w"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M1060,660 L1520,660" id="s4-wf"/>
{seats([1076,1118], 606, "s4-ws")}{seats([1206,1248,1290,1332], 606, "s4-ws")}{seats([1420,1462], 606, "s4-ws")}
<path class="ln pk" pathLength="1" stroke-width="6" d="M1182,420 L1182,650 M1398,420 L1398,650" id="s4-wa"/>
"""
    html = (title("s4", "3 · Fuselaje estrecho o ancho")
            + text("s4-t1", 380, 790, mark("Estrecho", "blue", "s4-t1-hl") + " · 1 pasillo", "lbl")
            + text("s4-t2", 380, 860, "corto recorrido (< 6 h)", "sm")
            + text("s4-t3", 1060, 860, mark("Ancho", "pink", "s4-t3-hl") + " · 2 pasillos", "lbl")
            + text("s4-t4", 1060, 930, "largo recorrido (> 6 h)", "sm"))
    js = """
write("#s4-title",T[0]+0.1,1.0); hl("#s4-title-hl",T[0]+1.1);
draw("#s4-n",T[0]+1.4,0.9); draw("#s4-w",T[0]+2.6,1.0);
draw("#s4-nf",T[1]+0.2,0.4); tl.fromTo(q(".s4-ns"),{opacity:0},{opacity:1,duration:0.2,stagger:0.08},T[1]+0.4);
draw("#s4-na",T[1]+1.2,0.5); write("#s4-t1",T[1]+0.6,0.8); hl("#s4-t1-hl",T[1]+1.4); write("#s4-t2",T[1]+2.6,1.0);
draw("#s4-wf",T[2]+0.2,0.4); tl.fromTo(q(".s4-ws"),{opacity:0},{opacity:1,duration:0.2,stagger:0.06},T[2]+0.4);
draw("#s4-wa",T[2]+1.3,0.6); write("#s4-t3",T[2]+0.6,0.8); hl("#s4-t3-hl",T[2]+1.4); write("#s4-t4",T[2]+2.6,1.0);
"""
    return svg, html, js


def wingplane(cx, wings, tail, extra="", ident=""):
    fus = f"M{cx},400 C{cx+18},400 {cx+22},430 {cx+22},450 L{cx+22},690 L{cx},716 L{cx-22},690 L{cx-22},450 C{cx-22},430 {cx-18},400 {cx},400 Z"
    def mir(d):  # d uses relative x (dx) pairs "dx,y"
        pts = [p.split(",") for p in d.split()]
        a = "M" + " L".join(f"{cx-float(x)},{y}" for x, y in pts)
        b = "M" + " L".join(f"{cx+float(x)},{y}" for x, y in pts)
        return a + " " + b
    return (f'<g id="{ident}"><path class="ln ink" pathLength="1" stroke-width="4" d="{fus}"/>'
            f'<path class="ln ink" pathLength="1" stroke-width="4" d="{mir(wings)}"/>'
            f'<path class="ln ink" pathLength="1" stroke-width="4" d="{mir(tail)}"/>{extra}</g>')


@scene
def s5():
    c = [360, 760, 1160, 1560]
    svg = (wingplane(c[0], "22,540 170,540 170,585 22,585", "22,660 75,668 75,684 22,684", ident="s5-p1")
           + wingplane(c[1], "22,500 175,615 175,640 22,575", "22,640 80,690 80,705 22,680", ident="s5-p2")
           + wingplane(c[2], "22,600 175,500 175,525 22,645", "22,640 80,690 80,705 22,680", ident="s5-p3")
           + wingplane(c[3], "22,480 160,690 22,690", "22,640 22,640",
                       f'<path class="ln pk" pathLength="1" stroke-width="5" d="M{c[3]-22},440 L{c[3]-80},468 L{c[3]-22},470 M{c[3]+22},440 L{c[3]+80},468 L{c[3]+22},470"/>', ident="s5-p4"))
    html = (title("s5", "4 · Tipos de ala", "blue")
            + text("s5-i", 1000, 120, "la forma depende de la " + mark("velocidad", "pink", "s5-i-hl"), "lbl")
            + text("s5-a", 240, 760, "Recta", "lbl") + text("s5-a2", 240, 826, "aviones lentos", "sm")
            + text("s5-b", 640, 760, "En flecha", "lbl") + text("s5-b2", 640, 826, "comerciales", "sm")
            + text("s5-c", 1030, 760, "Flecha invertida", "lbl") + text("s5-c2", 1030, 826, "muy poco común", "sm")
            + text("s5-d", 1430, 760, "Delta + canard", "lbl") + text("s5-d2", 1430, 826, "muy rápidos", "sm"))
    js = """
write("#s5-title",T[0]+0.1,0.9); hl("#s5-title-hl",T[0]+1.0);
write("#s5-i",T[0]+1.4,1.3); hl("#s5-i-hl",T[0]+2.7);
draw("#s5-p1 .ln",T[1]+0.1,0.8); write("#s5-a",T[1]+0.4,0.5); write("#s5-a2",T[1]+1.1,0.7);
draw("#s5-p2 .ln",T[2]+0.1,0.8); write("#s5-b",T[2]+0.4,0.6); write("#s5-b2",T[2]+2.3,0.7);
draw("#s5-p3 .ln",T[3]+0.1,0.8); write("#s5-c",T[3]+0.4,0.8); write("#s5-c2",T[3]+2.4,0.7);
draw("#s5-p4 .ln",T[4]+0.1,0.8); write("#s5-d",T[4]+0.4,0.8); write("#s5-d2",T[4]+3.6,0.7);
"""
    return svg, html, js


@scene
def s6():
    svg = (f'<g transform="translate(390,360) scale(1.9)">{PLANE_SIDE}</g>'
           '<path class="ln pk" pathLength="1" stroke-width="4" d="M1300,560 L1260,740" id="s6-lead"/>')
    html = (title("s6", "5 · La matrícula")
            + text("s6-reg", 1080, 740, f'{mark("E", "pink", "s6-e")}{mark("C", "blue", "s6-c")}-MXV', "lbl", "font-size:130px;letter-spacing:6px")
            + text("s6-ex", 1580, 930, "(ejemplo)", "sm")
            + text("s6-a", 200, 760, "Obligatoria · " + mark("OACI, Anexo 7", "pink", "s6-a-hl"), "lbl")
            + text("s6-b", 200, 836, "+ certificado de matrícula del país", "lbl")
            + text("s6-c2", 200, 912, "E = España · C = civil · + 3 letras", "lbl"))
    js = """
write("#s6-title",T[0]+0.1,0.9); hl("#s6-title-hl",T[0]+1.0);
tl.set(q("svg > g .ln"),{strokeDashoffset:0},0);
draw("#s6-lead",T[0]+1.1,0.4); write("#s6-reg",T[0]+1.4,0.9); write("#s6-ex",T[0]+2.2,0.5);
write("#s6-a",T[0]+3.2,1.4); hl("#s6-a-hl",T[0]+4.6);
write("#s6-b",T[1]+0.4,1.6);
hl("#s6-e",T[2]+1.6,0.3); hl("#s6-c",T[2]+2.4,0.3); write("#s6-c2",T[2]+1.4,2.4);
"""
    return svg, html, js


@scene
def s7():
    # piston moves between top (y=420) and bottom (y=640); gas fills from 380 to piston top
    svg = """
<path class="ln ink" pathLength="1" stroke-width="6" d="M700,380 L700,760 M1000,380 L1000,760 M700,380 L790,380 M910,380 L1000,380" id="s7-cyl"/>
<rect id="s7-gas" x="704" y="380" width="292" height="260" fill="rgba(66,188,240,.45)"/>
<g id="s7-pist"><rect x="708" y="640" width="284" height="80" rx="8" fill="#fdfdff" stroke="#23307a" stroke-width="5"/>
<path class="ink" fill="none" stroke-width="10" d="M850,720 L850,840"/></g>
<circle class="ln ink" pathLength="1" stroke-width="5" fill="none" cx="850" cy="880" r="56" id="s7-crank"/>
<g id="s7-vin"><path class="ink" fill="none" stroke-width="6" d="M790,380 L760,380 M745,340 L745,384 M725,384 L800,384"/></g>
<g id="s7-vex"><path class="ink" fill="none" stroke-width="6" d="M910,380 L940,380 M955,340 L955,384 M900,384 L975,384"/></g>
<path class="ink" fill="none" stroke-width="6" d="M850,300 L850,372 M830,300 L870,300" id="s7-plug"/>
<path id="s7-spark" fill="#ff3d96" d="M850,392 L862,420 L892,416 L870,438 L884,466 L856,452 L834,474 L836,444 L808,434 L838,424 Z"/>
"""
    svg += arrow(690, 250, 745, 350, "bl", 6, 26, "s7-ain") + arrow(955, 350, 1010, 250, "inkp", 6, 26, "s7-aex")
    html = (title("s7", "6 · Motor de pistón: 4 tiempos", "blue")
            + text("s7-k", 200, 260, "alternativo o convencional", "sm")
            + text("s7-1", 1140, 360, mark("1 · Admisión", "blue", "s7-1h"), "lbl") + text("s7-1b", 1170, 424, "entra aire + combustible", "sm")
            + text("s7-2", 1140, 500, mark("2 · Compresión", "blue", "s7-2h"), "lbl") + text("s7-2b", 1170, 564, "la mezcla se calienta", "sm")
            + text("s7-3", 1140, 640, mark("3 · Explosión", "pink", "s7-3h"), "lbl") + text("s7-3b", 1170, 704, "la bujía da la chispa", "sm")
            + text("s7-4", 1140, 780, mark("4 · Escape", "blue", "s7-4h"), "lbl") + text("s7-4b", 1170, 844, "salen los gases quemados", "sm")
            + text("s7-bj", 880, 270, "bujía", "sm"))
    js = """
write("#s7-title",T[0]+0.1,1.2); hl("#s7-title-hl",T[0]+1.3);
draw("#s7-cyl",T[0]+0.8,1.0); draw("#s7-crank",T[0]+1.4,0.5); write("#s7-k",T[0]+2.0,1.0); write("#s7-bj",T[0]+3.0,0.4);
const piston=(y,t,d)=>{tl.to(q("#s7-pist"),{y:y-640,duration:d,ease:"sine.inOut"},t);
  tl.to(q("#s7-gas"),{scaleY:(y-380)/260,transformOrigin:"50% 0%",duration:d,ease:"sine.inOut"},t);};
tl.set(q("#s7-pist"),{y:-220},0); tl.set(q("#s7-gas"),{scaleY:40/260,transformOrigin:"50% 0%"},0);
tl.set(q("#s7-spark"),{opacity:0,scale:0.3,transformOrigin:"50% 50%"},0);
// 1 intake
write("#s7-1",T[1]+0.1,0.7); hl("#s7-1h",T[1]+0.8); write("#s7-1b",T[1]+1.4,0.9);
tl.to(q("#s7-vin"),{y:16,duration:0.3},T[1]+0.8); draw("#s7-ain path",T[1]+0.9,0.5);
tl.to(q("#s7-gas"),{fill:"rgba(66,188,240,.5)",duration:0.1},T[1]+0.8);
piston(640,T[1]+1.0,1.8);
tl.to(q("#s7-vin"),{y:0,duration:0.3},T[2]-0.2); tl.to(q("#s7-ain path"),{opacity:0,duration:0.3},T[2]-0.2);
// 2 compression
write("#s7-2",T[2]+0.1,0.7); hl("#s7-2h",T[2]+0.8); write("#s7-2b",T[2]+1.4,0.9);
piston(420,T[2]+1.0,1.8); tl.to(q("#s7-gas"),{fill:"rgba(255,150,90,.55)",duration:1.8},T[2]+1.0);
// 3 power
write("#s7-3",T[3]+0.1,0.7); hl("#s7-3h",T[3]+0.8); write("#s7-3b",T[3]+1.4,0.9);
tl.to(q("#s7-spark"),{opacity:1,scale:1.2,duration:0.18,ease:"back.out(3)"},T[3]+1.6);
tl.to(q("#s7-gas"),{fill:"rgba(255,61,150,.6)",duration:0.15},T[3]+1.7);
tl.to(q("#s7-spark"),{opacity:0,scale:0.5,duration:0.4},T[3]+2.1);
piston(640,T[3]+2.0,1.0);
// 4 exhaust
write("#s7-4",T[4]+0.1,0.7); hl("#s7-4h",T[4]+0.8); write("#s7-4b",T[4]+1.4,0.9);
tl.to(q("#s7-vex"),{y:16,duration:0.3},T[4]+0.9); draw("#s7-aex path",T[4]+1.0,0.5);
tl.to(q("#s7-gas"),{fill:"rgba(120,120,145,.45)",duration:0.6},T[4]+0.9);
piston(420,T[4]+1.1,1.8);
"""
    return svg, html, js


@scene
def s8():
    comp = "".join(f'<path class="ink s8-cb" fill="none" stroke-width="5" d="M{x},{600-h} L{x},{600+h}"/>' for x, h in zip(range(420, 760, 42), [150, 140, 128, 116, 104, 94, 86, 80]))
    turb = "".join(f'<path class="inkp s8-tb" fill="none" stroke-width="6" d="M{x},{600-h} L{x},{600+h}"/>' for x, h in zip(range(1100, 1300, 45), [80, 90, 100, 110, 118]))
    flame = "".join(f'<path class="s8-fl" fill="rgba(255,61,150,.55)" d="M{x},{y} c20,-30 10,-50 30,-70 c0,30 25,45 10,70 Z"/>' for x, y in [(820, 560), (900, 600), (980, 560), (860, 680), (960, 690)])
    lanes = "".join(f'<path class="s8-flow bl" fill="none" stroke-width="4" stroke-dasharray="14 30" d="M180,{y} L1720,{y2}"/>' for y, y2 in [(500, 540), (700, 660)])
    svg = f"""
<path class="ln ink" pathLength="1" stroke-width="6" d="M260,420 L1300,470 L1660,530 M260,780 L1300,730 L1660,670" id="s8-case"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M380,600 L1300,600" id="s8-shaft"/>
<g id="s8-comp">{comp}</g><g id="s8-flame">{flame}</g><g id="s8-turb">{turb}</g>
<g id="s8-lanes">{lanes}</g>
{arrow(560, 760, 560, 900, "bl", 6, 26, "s8-bleed")}
{arrow(1600, 600, 1780, 600, "pk", 10, 36, "s8-jet")}
"""
    html = (title("s8", "7 · Motor a reacción")
            + text("s8-t1", 470, 300, mark("Compresor", "blue", "s8-t1h"), "lbl")
            + text("s8-t2", 760, 800, mark("Cámara de combustión", "pink", "s8-t2h"), "lbl")
            + text("s8-t3", 1110, 310, mark("Turbina", "blue", "s8-t3h"), "lbl")
            + text("s8-t4", 1360, 800, mark("Tobera de escape", "pink", "s8-t4h"), "lbl")
            + text("s8-bl", 200, 900, "aire sangrado → otros sistemas", "sm"))
    js = """
write("#s8-title",T[0]+0.1,0.9); hl("#s8-title-hl",T[0]+1.0);
draw("#s8-case",T[0]+0.8,1.4); draw("#s8-shaft",T[0]+1.8,0.6);
tl.set(q(".s8-cb, .s8-tb, .s8-fl, #s8-lanes"),{opacity:0},0);
show("#s8-lanes",T[1]+0.2,0.5);
tl.fromTo(q(".s8-flow"),{strokeDashoffset:0},{strokeDashoffset:-44*Math.round(D*3),duration:D,ease:"none"},0);
tl.to(q(".s8-cb"),{opacity:1,duration:0.15,stagger:0.08},T[1]+0.3); write("#s8-t1",T[1]+0.4,0.7); hl("#s8-t1h",T[1]+1.1);
draw("#s8-bleed path",T[1]+4.0,0.6); write("#s8-bl",T[1]+4.4,1.4);
tl.to(q(".s8-fl"),{opacity:1,duration:0.2,stagger:0.12},T[2]+0.6); write("#s8-t2",T[2]+0.4,1.1); hl("#s8-t2h",T[2]+1.5);
tl.fromTo(q(".s8-fl"),{scaleY:0.85,transformOrigin:"50% 100%"},{scaleY:1.15,transformOrigin:"50% 100%",duration:0.25,yoyo:true,repeat:Math.round((D-T[2])/0.25),ease:"sine.inOut"},T[2]+1.4);
tl.to(q(".s8-tb"),{opacity:1,duration:0.15,stagger:0.08},T[3]+0.3); write("#s8-t3",T[3]+0.6,0.6); hl("#s8-t3h",T[3]+1.2);
write("#s8-t4",T[4]+0.4,1.0); hl("#s8-t4h",T[4]+1.4); draw("#s8-jet path",T[4]+2.6,0.6);
"""
    return svg, html, js


@scene
def s9():
    svg = f"""
<path class="ln ink" pathLength="1" stroke-width="5" d="M700,290 L1400,300 L1520,318 L1520,342 L1400,360 L700,370 Z" id="s9-a"/>
{arrow(1540, 330, 1720, 330, "pk", 7, 28, "s9-aj")}
<path class="ln ink" pathLength="1" stroke-width="5" d="M700,500 L1350,520 L1450,560 L1450,620 L1350,660 L700,680 Z" id="s9-b"/>
<path class="ln inkp" pathLength="1" stroke-width="5" d="M760,512 L760,668 M745,530 L775,540 M745,590 L775,590 M745,650 L775,640" id="s9-fan"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M800,560 L1350,575 M800,620 L1350,605" id="s9-core"/>
{arrow(620, 535, 1300, 540, "bl", 5, 24, "s9-by1")}{arrow(620, 645, 1300, 640, "bl", 5, 24, "s9-by2")}
<path class="ln ink" pathLength="1" stroke-width="5" d="M800,830 L1400,840 L1460,855 L1400,870 L800,880 Z" id="s9-c"/>
<g id="s9-prop"><path class="ln inkp" pathLength="1" stroke-width="6" d="M760,775 Q785,815 768,855 Q785,895 760,935" /></g>
<circle cx="770" cy="855" r="12" fill="#23307a" id="s9-hub"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M782,855 L800,855" id="s9-sh"/>
"""
    html = (title("s9", "8 · Tres tipos de reactor", "blue")
            + text("s9-ta", 200, 290, mark("Turborreactor", "blue", "s9-tah"), "lbl") + text("s9-ta2", 200, 352, "empuje = chorro de gases", "sm")
            + text("s9-tb", 200, 540, mark("Turbofán", "pink", "s9-tbh"), "lbl") + text("s9-tb2", 200, 602, "gran ventilador", "sm") + text("s9-tb3", 200, 652, "aviones comerciales", "sm")
            + text("s9-tc", 200, 800, mark("Turbohélice", "blue", "s9-tch"), "lbl") + text("s9-tc2", 200, 862, "mueve una hélice", "sm") + text("s9-tc3", 200, 912, "vuelos cortos", "sm"))
    js = """
write("#s9-title",T[0]+0.1,1.0); hl("#s9-title-hl",T[0]+1.1);
draw("#s9-a",T[1]+0.1,0.9); write("#s9-ta",T[1]+0.3,0.8); hl("#s9-tah",T[1]+1.1); draw("#s9-aj path",T[1]+1.6,0.5); write("#s9-ta2",T[1]+2.0,1.0);
draw("#s9-b",T[2]+0.1,0.9); draw("#s9-fan",T[2]+0.8,0.5); draw("#s9-core",T[2]+1.0,0.6);
write("#s9-tb",T[2]+0.3,0.6); hl("#s9-tbh",T[2]+0.9); write("#s9-tb2",T[2]+1.6,0.8);
draw("#s9-by1 path, #s9-by2 path",T[2]+2.4,0.9); write("#s9-tb3",T[2]+5.0,0.9);
draw("#s9-c",T[3]+0.1,0.8); draw("#s9-prop path",T[3]+0.8,0.6); show("#s9-hub",T[3]+0.8); draw("#s9-sh",T[3]+0.9,0.2);
write("#s9-tc",T[3]+0.3,0.7); hl("#s9-tch",T[3]+1.0); write("#s9-tc2",T[3]+1.6,0.8); write("#s9-tc3",T[3]+3.4,0.7);
tl.fromTo(q("#s9-prop"),{scaleY:1,transformOrigin:"50% 50%"},{scaleY:-1,transformOrigin:"50% 50%",duration:0.18,yoyo:true,repeat:Math.round((D-T[3]-1.5)/0.18),ease:"sine.inOut"},T[3]+1.5);
"""
    return svg, html, js


@scene
def s10():
    tail = "M1060,660 L1480,640 L1560,410 L1630,410 L1620,615 L1690,625 C1712,630 1712,655 1690,660 L1590,682 L1060,712"
    svg = f"""
<path class="ln ink" pathLength="1" stroke-width="5" d="M220,520 L700,540 L700,640 L220,660 Z" id="s10-eng"/>
<g id="s10-d1"><path class="pk" fill="none" stroke-width="7" d="M560,534 L640,537"/></g>
<g id="s10-d2"><path class="pk" fill="none" stroke-width="7" d="M560,646 L640,643"/></g>
{arrow(720, 590, 900, 590, "ink", 6, 26, "s10-out")}
<path class="ln pk" pathLength="1" stroke-width="6" d="M600,520 C560,420 460,400 340,430" id="s10-r1"/>
<path class="ln pk" pathLength="1" stroke-width="6" d="M600,660 C560,760 460,780 340,750" id="s10-r2"/>
<path class="ln pk" pathLength="1" stroke-width="6" d="M366,410 L338,431 L370,448 M366,770 L338,749 L370,732" id="s10-rh"/>
<path class="ln ink" pathLength="1" stroke-width="5" d="{tail}" id="s10-tail"/>
<rect id="s10-apu" x="1630" y="626" width="58" height="30" rx="8" fill="rgba(255,92,168,.6)" stroke="#23307a" stroke-width="4"/>
<path class="ln bl" pathLength="1" stroke-width="7" d="M1560,800 L1530,860 L1570,860 L1540,930" id="s10-bolt"/>
{arrow(1650, 690, 1650, 800, "ink", 5, 24, "s10-apl")}
"""
    html = (title("s10", "9 · Reversa y APU")
            + text("s10-a", 200, 820, mark("Reversa", "pink", "s10-ah"), "lbl") + text("s10-a2", 200, 890, "el aire sale hacia delante → frena", "sm")
            + text("s10-b", 1260, 300, mark("APU", "pink", "s10-bh") + " · unidad de potencia auxiliar", "lbl", "font-size:50px")
            + text("s10-c", 1100, 790, "electricidad", "sm") + text("s10-c2", 1100, 870, "aire para arrancar motores", "sm"))
    js = """
write("#s10-title",T[0]+0.1,0.9); hl("#s10-title-hl",T[0]+1.0);
draw("#s10-eng",T[0]+0.6,0.9); draw("#s10-out path",T[0]+1.4,0.5);
tl.to(q("#s10-out path"),{opacity:0,duration:0.3},T[0]+3.0);
tl.fromTo(q("#s10-d1"),{rotation:0,svgOrigin:"560 534"},{rotation:-35,svgOrigin:"560 534",duration:0.6},T[0]+3.0);
tl.fromTo(q("#s10-d2"),{rotation:0,svgOrigin:"560 646"},{rotation:35,svgOrigin:"560 646",duration:0.6},T[0]+3.0);
draw("#s10-r1, #s10-r2",T[0]+3.5,0.8); draw("#s10-rh",T[0]+4.2,0.3);
write("#s10-a",T[0]+0.4,0.7); hl("#s10-ah",T[0]+1.1); write("#s10-a2",T[0]+4.4,1.4);
draw("#s10-tail",T[1]+0.1,1.2); tl.fromTo(q("#s10-apu"),{opacity:0},{opacity:1,duration:0.3},T[1]+1.4);
write("#s10-b",T[1]+1.2,1.3); hl("#s10-bh",T[1]+1.6);
draw("#s10-apl path",T[2]+0.3,0.5); draw("#s10-bolt",T[2]+0.6,0.4); write("#s10-c",T[2]+0.8,0.7);
write("#s10-c2",T[2]+3.4,1.3);
"""
    return svg, html, js


@scene
def s11():
    svg = f"""<g id="s11-w"><g transform="translate(240,420) scale(1.1)">{PLANE_SIDE}{GEAR}</g>
<path class="ln ink" pathLength="1" stroke-width="6" d="M220,600 L960,600 M300,600 L300,640 M880,600 L880,640" id="s11-scale"/></g>"""
    html = (title("s11", "10 · Pesos máximos", "blue")
            + text("s11-a", 1060, 380, mark("MTOW", "pink", "s11-ah"), "lbl") + text("s11-a2", 1060, 446, "peso máximo al despegue", "sm")
            + text("s11-b", 1060, 560, mark("MLW", "blue", "s11-bh"), "lbl") + text("s11-b2", 1060, 626, "peso máximo al aterrizaje", "sm")
            + text("s11-e1", 0, 760, "Estructura ligera · alas para su velocidad", "lbl", "width:1920px;text-align:center;font-size:72px")
            + text("s11-e2", 0, 860, mark("motores que empujan", "pink", "s11-eh"), "lbl", "width:1920px;text-align:center;font-size:72px"))
    js = """
write("#s11-title",T[0]+0.1,0.9); hl("#s11-title-hl",T[0]+1.0);
tl.set(q("#s11-w .ln:not(#s11-scale)"),{strokeDashoffset:0},0); draw("#s11-scale",T[0]+0.6,0.7);
write("#s11-a",T[1]+0.3,0.5); hl("#s11-ah",T[1]+0.8); write("#s11-a2",T[1]+1.4,1.0);
write("#s11-b",T[1]+3.6,0.5); hl("#s11-bh",T[1]+4.1); write("#s11-b2",T[1]+4.7,1.0);
write("#s11-e1",T[2]+0.3,2.2); write("#s11-e2",T[2]+3.4,1.2); hl("#s11-eh",T[2]+4.6,0.5);
"""
    return svg, html, js


if __name__ == "__main__":
    build(ROOT, S)
