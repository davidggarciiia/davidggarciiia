import sys, pathlib, math
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "lib"))
from nb import *  # noqa

S = {}
def scene(fn):
    S[fn.__name__] = fn
    return fn

RED, BLU_T = "#e8364f", "#0a7fb8"


def ln(ident, d, cls="ink", w=4, fill="none", extra=""):
    return f'<path class="ln {cls}" pathLength="1" stroke-width="{w}" fill="{fill}" d="{d}" id="{ident}" {extra}/>'


def cloud(x, y, s=1.0, ident="", fill="rgba(255,255,255,.95)"):
    i = f' id="{ident}"' if ident else ""
    return (f'<g{i} transform="translate({x},{y}) scale({s})"><path fill="{fill}" stroke="#7d89b0" stroke-width="{4/s:.1f}" '
            f'd="M0,60 C-10,20 40,0 70,20 C90,-20 160,-10 170,30 C210,25 230,70 200,90 L10,90 C-20,90 -20,62 0,60 Z"/></g>')


def cb(x, y, s=1.0, ident=""):
    """cumulonimbus with anvil, base at (x,y)"""
    return (f'<g id="{ident}"><g transform="translate({x},{y}) scale({s})"><path fill="rgba(240,242,250,.95)" stroke="#23307a" stroke-width="{5/s:.1f}" '
            'd="M-160,0 C-200,-10 -190,-70 -140,-70 C-150,-140 -80,-170 -50,-130 C-60,-230 -20,-300 -40,-360 L-230,-380 C-260,-400 -230,-420 -200,-420 L230,-420 C260,-420 270,-395 240,-380 L50,-360 C30,-300 70,-230 60,-140 C100,-180 170,-140 150,-80 C200,-80 210,-10 160,0 Z"/></g></g>')


@scene
def s1():
    svg = ('<g id="s1-sun"><circle cx="420" cy="420" r="70" fill="rgba(255,214,90,.75)" stroke="#23307a" stroke-width="5"/>'
           + "".join(f'<path class="ink" stroke-width="5" d="M{420+95*math.cos(a):.0f},{420+95*math.sin(a):.0f} L{420+130*math.cos(a):.0f},{420+130*math.sin(a):.0f}"/>' for a in [k*math.pi/4 for k in range(8)]) + '</g>'
           + cloud(760, 330, 1.4, "s1-cl")
           + '<g id="s1-rain">' + "".join(f'<path class="bl" stroke-width="5" stroke-linecap="round" d="M{x},480 l-14,40"/>' for x in range(800, 1060, 40)) + '</g>'
           + '<path id="s1-bolt" fill="rgba(255,214,90,.9)" stroke="#23307a" stroke-width="4" d="M1380,300 L1320,450 L1370,450 L1330,580 L1450,410 L1395,410 L1440,300 Z"/>'
           + cloud(1250, 230, 1.2, "s1-cl2"))
    html = (text("s1-title", 0, 700, mark("Meteorología para volar", "blue", "s1-title-hl"), "h1 big", "width:1920px;text-align:center")
            + text("s1-def", 0, 860, "ciencia que estudia el comportamiento de la atmósfera", "lbl", "width:1920px;text-align:center"))
    js = """
tl.set(q("#s1-cl, #s1-rain, #s1-bolt, #s1-cl2"),{opacity:0},0);
show("#s1-cl",T[0]+1.4,0.4); show("#s1-rain",T[0]+2.6,0.3); show("#s1-cl2",T[0]+3.4,0.3); show("#s1-bolt",T[0]+4.0,0.1);
tl.fromTo(q("#s1-rain"),{y:0},{y:24,duration:0.3,repeat:Math.round((D-T[0]-2.6)/0.3),ease:"none"},T[0]+2.6);
tl.to(q("#s1-bolt"),{opacity:0.2,duration:0.08,yoyo:true,repeat:5},T[0]+4.2);
write("#s1-title",T[0]+0.6,1.4); hl("#s1-title-hl",T[0]+2.0,0.5);
write("#s1-def",T[1]+0.6,2.2);
"""
    return svg, html, js


@scene
def s2():
    bands = [("tropo", 780, 140, "rgba(66,188,240,.45)"), ("strato", 640, 140, "rgba(66,188,240,.32)"), ("meso", 520, 120, "rgba(90,63,176,.22)"),
             ("termo", 400, 120, "rgba(255,92,168,.22)"), ("exo", 300, 100, "rgba(255,92,168,.12)")]
    svg = '<path id="s2-earth" fill="rgba(120,160,110,.45)" stroke="#23307a" stroke-width="5" d="M560,920 L1240,920 L1240,960 L560,960 Z"/>'
    for name, y, h, c in bands:
        svg += f'<rect class="s2-b" id="s2-{name}" x="600" y="{y}" width="600" height="{h}" fill="{c}" stroke="#23307a" stroke-width="3"/>'
    svg += (f'<g id="s2-pl"><g transform="translate(760,840) scale(0.35)">{PLANE_SIDE}</g></g>'
            + f'<g id="s2-cc"><g transform="translate(820,690) scale(0.28)">{PLANE_SIDE}</g></g>'
            + '<path id="s2-mag" fill="none" stroke="#5a3fb0" stroke-width="5" stroke-dasharray="14 12" d="M540,940 C440,520 620,240 900,230 C1180,240 1360,520 1260,940"/>')
    html = (title("s2", "1 · Capas de la atmósfera")
            + text("s2-t1", 1260, 820, mark("Troposfera", "blue", "s2-t1h") + " · tiempo y aviones", "lbl")
            + text("s2-t2", 1260, 680, "Estratosfera · Concorde", "lbl")
            + text("s2-t3", 1260, 550, "Mesosfera", "lbl") + text("s2-t4", 1260, 430, "Termosfera / Ionosfera", "lbl")
            + text("s2-t5", 1260, 320, "Exosfera", "lbl") + text("s2-t6", 200, 300, "Magnetosfera", "lbl", "color:#5a3fb0"))
    js = """
write("#s2-title",T[0]+0.1,1.0); hl("#s2-title-hl",T[0]+1.1);
tl.set(q(".s2-b, #s2-pl, #s2-cc, #s2-mag"),{opacity:0},0); tl.set(q("svg .ln"),{strokeDashoffset:0},0);
tl.to(q(".s2-b"),{opacity:1,duration:0.3,stagger:0.25},T[0]+2.6);
write("#s2-t1",T[1]+0.4,1.1); hl("#s2-t1h",T[1]+1.5); show("#s2-pl",T[1]+5.4,0.4);
tl.fromTo(q("#s2-pl"),{x:-60},{x:120,duration:D-T[1]-5,ease:"none"},T[1]+5.4);
write("#s2-t2",T[2]+0.3,1.2); show("#s2-cc",T[2]+3.4,0.4);
write("#s2-t3",T[3]+0.4,0.6); write("#s2-t4",T[3]+1.6,1.0); write("#s2-t5",T[3]+3.6,0.6);
show("#s2-mag",T[3]+5.0,0.6); write("#s2-t6",T[3]+5.4,0.9);
"""
    return svg, html, js


@scene
def s3():
    iso = ""
    for i, (rx, ry) in enumerate([(110, 70), (190, 130), (270, 190)]):
        iso += f'<ellipse class="s3-iA" cx="760" cy="640" rx="{rx}" ry="{ry}" fill="none" stroke="#1ea7e4" stroke-width="4"/>'
        iso += f'<ellipse class="s3-iB" cx="1320" cy="640" rx="{rx-10}" ry="{ry}" fill="none" stroke="#ff3d96" stroke-width="4"/>'
    svg = (iso
           + '<g id="s3-drops">' + "".join(f'<path fill="rgba(66,188,240,.7)" stroke="#23307a" stroke-width="3" d="M{x},{y} c-14,22 -14,36 0,36 c14,0 14,-14 0,-36 Z"/>' for x, y in [(1500, 220), (1560, 260), (1620, 215)]) + '</g>'
           + arrow(760, 500, 760, 600, "bl", 6, 24, "s3-dn") + arrow(1320, 600, 1320, 500, "pk", 6, 24, "s3-up")
           + '<circle id="s3-dana" cx="1580" cy="380" r="40" fill="rgba(255,92,168,.25)" stroke="#23307a" stroke-width="4"/>')
    html = (title("s3", "2 · Humedad y presión", "blue")
            + text("s3-h", 200, 240, mark("Humedad", "blue", "s3-hh") + " = vapor de agua en el aire", "lbl")
            + text("s3-h2", 200, 306, "baja la temperatura → " + mark("rocío", "pink", "s3-h2h"), "sm")
            + text("s3-is", 960, 880, mark("isobaras", "blue", "s3-ish") + " · igual presión", "lbl")
            + text("s3-A", 730, 610, "A", "big", f"color:{BLU_T}") + text("s3-B", 1290, 610, "B", "big", "color:#ff3d96")
            + text("s3-a2", 200, 880, mark("Anticiclón", "blue", "s3-a2h"), "lbl") + text("s3-a3", 200, 946, "aire frío que baja · estable", "sm")
            + text("s3-b2", 1480, 760, mark("Borrasca", "pink", "s3-b2h"), "lbl") + text("s3-b3", 1480, 826, "aire cálido que sube", "sm")
            + text("s3-d", 1480, 440, "DANA · niveles altos", "sm"))
    js = """
write("#s3-title",T[0]+0.1,0.9); hl("#s3-title-hl",T[0]+1.0);
write("#s3-h",T[0]+0.8,1.4); hl("#s3-hh",T[0]+2.2);
tl.set(q("#s3-drops, .s3-iA, .s3-iB, #s3-dana"),{opacity:0},0);
show("#s3-drops",T[0]+5.4,0.4); write("#s3-h2",T[0]+6.2,1.4); hl("#s3-h2h",T[0]+7.6);
tl.to(q(".s3-iA, .s3-iB"),{opacity:1,duration:0.3,stagger:0.12},T[1]+0.4); write("#s3-is",T[1]+1.0,0.9); hl("#s3-ish",T[1]+1.9);
write("#s3-A",T[2]+0.3,0.3); write("#s3-a2",T[2]+0.6,0.7); hl("#s3-a2h",T[2]+1.3); draw("#s3-dn path",T[2]+1.8,0.5); write("#s3-a3",T[2]+2.4,1.2);
write("#s3-B",T[3]+0.3,0.3); write("#s3-b2",T[3]+0.6,0.7); hl("#s3-b2h",T[3]+1.3); draw("#s3-up path",T[3]+1.8,0.5); write("#s3-b3",T[3]+2.2,1.0);
show("#s3-dana",T[4]+0.4,0.3); write("#s3-d",T[4]+0.6,1.0);
"""
    return svg, html, js


@scene
def s4():
    semis = "".join(f'<path fill="{RED}" d="M{x},540 a26,26 0 0 1 52,0 Z"/>' for x in range(260, 820, 110))
    tris = "".join(f'<path fill="#1e6fe4" d="M{x},540 L{x+26},494 L{x+52},540 Z"/>' for x in range(1100, 1660, 110))
    svg = (ln("s4-wl", "M240,540 L860,540", "", 7, extra=f'style="stroke:{RED}"') + f'<g id="s4-semi">{semis}</g>'
           + ln("s4-cl", "M1080,540 L1700,540", "", 7, extra='style="stroke:#1e6fe4"') + f'<g id="s4-tri">{tris}</g>'
           + '<path id="s4-st" fill="rgba(200,205,225,.8)" stroke="#23307a" stroke-width="4" d="M220,720 C260,690 840,690 880,720 C900,750 860,770 820,770 L280,770 C230,770 200,750 220,720 Z"/>'
           + cb(1520, 960, 0.6, "s4-cb"))
    html = (title("s4", "3 · Frentes")
            + text("s4-w", 240, 400, mark("Frente cálido", "pink", "s4-wh"), "lbl") + text("s4-w2", 240, 790, "estratos · nubes bajas y extendidas", "sm")
            + text("s4-c", 1080, 400, mark("Frente frío", "blue", "s4-ch"), "lbl") + text("s4-c2", 1080, 630, "cumulonimbos", "sm")
            + text("s4-c3", 1080, 680, "desarrollo vertical", "sm"))
    js = """
write("#s4-title",T[0]+0.1,0.6); hl("#s4-title-hl",T[0]+0.7);
tl.set(q("#s4-semi path, #s4-tri path, #s4-st, #s4-cb"),{opacity:0},0);
draw("#s4-wl",T[1]+0.4,0.8); tl.to(q("#s4-semi path"),{opacity:1,duration:0.15,stagger:0.12},T[1]+1.0);
write("#s4-w",T[1]+0.2,0.7); hl("#s4-wh",T[1]+0.9);
tl.fromTo(q("#s4-st"),{opacity:0,scaleX:0.3,transformOrigin:"50% 50%"},{opacity:1,scaleX:1,duration:0.8},T[1]+3.4); write("#s4-w2",T[1]+3.8,1.4);
draw("#s4-cl",T[2]+0.4,0.8); tl.to(q("#s4-tri path"),{opacity:1,duration:0.15,stagger:0.12},T[2]+1.0);
write("#s4-c",T[2]+0.2,0.7); hl("#s4-ch",T[2]+0.9);
tl.fromTo(q("#s4-cb"),{opacity:0,scaleY:0.2,transformOrigin:"50% 100%"},{opacity:1,scaleY:1,duration:1.2,ease:"power2.out"},T[2]+3.4);
write("#s4-c2",T[2]+3.6,0.8); write("#s4-c3",T[2]+4.6,0.9);
"""
    return svg, html, js


@scene
def s5():
    svg = (cb(960, 860, 1.1, "s5-cb")
           + '<path id="s5-bolt" fill="rgba(255,214,90,.95)" stroke="#23307a" stroke-width="4" d="M940,720 L900,820 L935,820 L905,920 L990,790 L950,790 L980,720 Z"/>'
           + '<g id="s5-rain">' + "".join(f'<path class="bl" stroke-width="5" stroke-linecap="round" d="M{x},880 l-12,36"/>' for x in range(820, 1120, 36)) + '</g>'
           + arrow(1220, 640, 1420, 600, "inkp", 6, 24, "s5-wind")
           + ln("s5-detour", "M300,700 C420,700 520,940 760,960 C1100,990 1400,960 1640,700", "pk", 5, extra='stroke-dasharray="1 1"')
           + f'<g id="s5-pl"><g transform="translate(160,660) scale(0.3)">{PLANE_SIDE}</g></g>')
    html = (title("s5", "4 · Tormentas", "blue")
            + text("s5-l1", 200, 280, "aparato eléctrico", "sm") + text("s5-l2", 200, 340, "precipitaciones", "sm")
            + text("s5-l3", 200, 400, "vientos muy fuertes", "sm") + text("s5-l4", 200, 460, "turbulencia", "sm") + text("s5-l5", 200, 520, "engelamiento", "sm")
            + text("s5-r", 1340, 300, mark("los aviones las rodean", "pink", "s5-rh"), "lbl")
            + text("s5-h", 1340, 400, "huracanes y tornados", "sm") + text("s5-h2", 1340, 450, "→ aún más violentos", "sm"))
    js = """
write("#s5-title",T[0]+0.1,0.8); hl("#s5-title-hl",T[0]+0.9);
tl.set(q("#s5-bolt, #s5-rain, #s5-pl"),{opacity:0},0); tl.set(q("#s5-pl .ln"),{strokeDashoffset:0},0);
tl.fromTo(q("#s5-cb"),{opacity:0,scaleY:0.3,transformOrigin:"50% 100%"},{opacity:1,scaleY:1,duration:1.2,ease:"power2.out"},T[0]+0.6);
write("#s5-l1",T[1]+0.2,0.6); tl.to(q("#s5-bolt"),{opacity:1,duration:0.06,yoyo:true,repeat:5},T[1]+0.3);
write("#s5-l2",T[1]+1.4,0.6); show("#s5-rain",T[1]+1.4,0.3);
tl.fromTo(q("#s5-rain"),{y:0},{y:20,duration:0.3,repeat:Math.round((D-T[1]-1.4)/0.3),ease:"none"},T[1]+1.4);
write("#s5-l3",T[1]+2.6,0.6); draw("#s5-wind path",T[1]+2.8,0.5);
write("#s5-l4",T[1]+3.8,0.5); write("#s5-l5",T[1]+4.6,0.6);
draw("#s5-detour",T[1]+5.8,1.4); show("#s5-pl",T[1]+5.8,0.3); write("#s5-r",T[1]+6.0,1.0); hl("#s5-rh",T[1]+7.0);
tl.to(q("#s5-pl"),{x:1350,y:-20,duration:2.6,ease:"none"},T[1]+6.0);
write("#s5-h",T[2]+0.3,1.0); write("#s5-h2",T[2]+1.6,1.0);
"""
    return svg, html, js


@scene
def s6():
    svg = (f'<g transform="translate(520,500)"><path class="ln ink" pathLength="1" stroke-width="5" fill="#fdfdff" d="M0,80 C0,30 110,0 280,0 C460,0 650,50 760,90 C650,92 460,108 280,112 C110,114 0,108 0,80 Z" id="s6-af"/></g>'
           + '<path id="s6-clear" fill="rgba(150,215,255,.55)" stroke="#1ea7e4" stroke-width="3" d="M528,540 C520,500 560,480 620,478 L640,494 C590,496 556,512 548,546 C546,570 560,590 600,600 L590,618 C540,606 530,580 528,540 Z"/>'
           + '<g id="s6-rime">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" stroke="#7d89b0" stroke-width="2"/>' for x, y, r in
                                          [(512, 560, 14), (520, 530, 12), (540, 505, 13), (566, 488, 11), (596, 480, 12), (506, 590, 12), (522, 612, 11)]) + '</g>'
           + '<path class="ln ink" pathLength="1" stroke-width="5" fill="none" d="M1560,300 L1560,600 M1600,300 L1600,600 M1560,300 Q1580,270 1600,300" id="s6-th"/>'
           + '<circle cx="1580" cy="640" r="40" fill="rgba(66,188,240,.7)" stroke="#23307a" stroke-width="5" id="s6-bulb"/>'
           + '<g id="s6-drops">' + "".join(f'<path fill="rgba(66,188,240,.7)" stroke="#23307a" stroke-width="3" d="M{x},{y} c-14,22 -14,36 0,36 c14,0 14,-14 0,-36 Z"/>' for x, y in [(300, 420), (360, 470), (290, 520)]) + '</g>')
    html = (title("s6", "5 · Engelamiento")
            + text("s6-a", 200, 260, "humedad visible + " + mark("≤ 0 °C", "blue", "s6-ah"), "lbl")
            + text("s6-t", 1640, 560, "0 °C", "lbl")
            + text("s6-c", 300, 760, mark("Clear ice", "blue", "s6-ch"), "lbl") + text("s6-c2", 300, 830, "transparente y duro", "sm")
            + text("s6-r", 1000, 760, mark("Granular (rime)", "pink", "s6-rh"), "lbl") + text("s6-r2", 1000, 830, "blanco y opaco", "sm"))
    js = """
write("#s6-title",T[0]+0.1,0.8); hl("#s6-title-hl",T[0]+0.9);
draw("#s6-af",T[0]+0.6,1.0);
tl.set(q("#s6-clear, #s6-rime, #s6-drops, #s6-bulb"),{opacity:0},0);
show("#s6-drops",T[0]+4.4,0.4); write("#s6-a",T[0]+4.4,1.4); hl("#s6-ah",T[0]+5.8);
draw("#s6-th",T[0]+6.0,0.6); show("#s6-bulb",T[0]+6.4,0.3); write("#s6-t",T[0]+6.6,0.4);
show("#s6-clear",T[1]+0.6,0.6); write("#s6-c",T[1]+0.4,0.6); hl("#s6-ch",T[1]+1.0); write("#s6-c2",T[1]+2.0,1.0);
tl.to(q("#s6-clear"),{opacity:0,duration:0.4},T[2]-0.2);
tl.to(q("#s6-rime circle"),{opacity:1,duration:0.15,stagger:0.1},T[2]+0.4); tl.set(q("#s6-rime"),{opacity:1},T[2]+0.4);
write("#s6-r",T[2]+0.4,0.8); hl("#s6-rh",T[2]+1.2); write("#s6-r2",T[2]+1.5,0.8);
"""
    return svg, html, js


@scene
def s7():
    def wave(x, amp, ident):
        pts = " ".join(f"L{x + i*20},{560 + amp*math.sin(i*1.3):.0f}" for i in range(1, 15))
        return f'<path id="{ident}" class="ln ink" pathLength="1" stroke-width="5" fill="none" d="M{x},560 {pts}"/>'
    svg = (wave(220, 8, "s7-w1") + wave(560, 22, "s7-w2") + wave(900, 40, "s7-w3") + wave(1240, 62, "s7-w4")
           + '<g id="s7-jet">' + "".join(arrow(260 + i * 300, 860, 460 + i * 300, 860, "pk", 6, 24, f"s7-j{i}") for i in range(5)) + '</g>'
           + '<path id="s7-cat" fill="none" stroke="#5a3fb0" stroke-width="4" stroke-dasharray="10 12" d="M500,815 C560,790 620,840 680,815 C740,790 800,840 860,815 C920,790 980,840 1040,815 C1100,790 1160,840 1220,815"/>')
    html = (title("s7", "6 · Turbulencia", "blue")
            + text("s7-l1", 200, 650, "ligera", "lbl") + text("s7-l1b", 200, 716, "5–15 kt", "sm")
            + text("s7-l2", 540, 650, "moderada", "lbl") + text("s7-l2b", 540, 716, "15–25 kt", "sm")
            + text("s7-l3", 880, 650, "fuerte", "lbl") + text("s7-l3b", 880, 716, "+ 25 kt", "sm")
            + text("s7-l4", 1220, 650, mark("severa", "pink", "s7-l4h"), "lbl")
            + text("s7-c", 200, 900, mark("CAT", "pink", "s7-ch") + " · turbulencia en aire claro: no se ve", "lbl")
            + text("s7-jt", 1400, 760, "jet stream", "sm", "color:#ff3d96"))
    js = """
write("#s7-title",T[0]+0.1,0.8); hl("#s7-title-hl",T[0]+0.9);
tl.set(q("#s7-cat"),{opacity:0},0);
draw("#s7-w1",T[1]+0.3,0.6); write("#s7-l1",T[1]+0.3,0.5); write("#s7-l1b",T[1]+1.3,0.6);
draw("#s7-w2",T[1]+2.6,0.6); write("#s7-l2",T[1]+2.6,0.6); write("#s7-l2b",T[1]+3.4,0.6);
draw("#s7-w3",T[1]+5.0,0.6); write("#s7-l3",T[1]+5.0,0.5); write("#s7-l3b",T[1]+5.8,0.6);
draw("#s7-w4",T[1]+7.6,0.6); write("#s7-l4",T[1]+7.6,0.6); hl("#s7-l4h",T[1]+8.2);
tl.fromTo(q("#s7-w4"),{y:0},{y:8,duration:0.15,yoyo:true,repeat:Math.round((D-T[1]-8.4)/0.15)},T[1]+8.4);
draw("#s7-jet path",T[2]+0.6,0.8); write("#s7-jt",T[2]+1.0,0.6);
show("#s7-cat",T[2]+2.4,0.6); write("#s7-c",T[2]+2.6,1.6); hl("#s7-ch",T[2]+4.2);
"""
    return svg, html, js


@scene
def s8():
    svg = ('<path id="s8-band" fill="rgba(255,92,168,.2)" d="M200,330 C600,280 1200,400 1720,330 L1720,450 C1200,520 600,400 200,450 Z"/>'
           + "".join(arrow(260 + i * 290, 390, 420 + i * 290, 390 + (i % 2) * 10, "pk", 6, 24, f"s8-a{i}") for i in range(5))
           + f'<g id="s8-pl"><g transform="translate(300,380) scale(0.4) scale(-1,1) translate(-600,0)">{PLANE_SIDE}</g></g>'
           + ln("s8-rw", "M1000,900 L1720,900", "ink", 6)
           + f'<g id="s8-pl2"><g transform="translate(700,700) rotate(8) scale(0.45) scale(-1,1) translate(-600,0)">{PLANE_SIDE}</g></g>'
           + arrow(900, 640, 1060, 640, "bl", 6, 24, "s8-w1") + arrow(1160, 640, 1060, 760, "pk", 6, 24, "s8-w2") + arrow(1300, 760, 1180, 760, "inkp", 6, 24, "s8-w3"))
    html = (title("s8", "7 · Jet stream y cizalladura")
            + text("s8-j", 1180, 220, mark("Jet stream", "pink", "s8-jh") + " · fuerte y estrecho", "lbl")
            + text("s8-j2", 200, 500, "a favor → + velocidad", "lbl")
            + text("s8-s", 200, 820, mark("Wind shear", "blue", "s8-sh"), "lbl") + text("s8-s2", 200, 890, "cambio brusco de dirección o velocidad", "sm")
            + text("s8-s3", 1300, 930, "peligrosa cerca del suelo", "sm"))
    js = """
write("#s8-title",T[0]+0.1,1.0); hl("#s8-title-hl",T[0]+1.1);
tl.set(q("#s8-band, #s8-pl, #s8-pl2"),{opacity:0},0); tl.set(q("#s8-pl .ln, #s8-pl2 .ln"),{strokeDashoffset:0},0);
show("#s8-band",T[0]+0.8,0.6); draw("[id^=s8-a] path",T[0]+1.4,0.8); write("#s8-j",T[0]+1.2,1.1); hl("#s8-jh",T[0]+2.3);
show("#s8-pl",T[1]+0.2,0.3); tl.fromTo(q("#s8-pl"),{x:0},{x:1100,duration:2.4,ease:"power2.in"},T[1]+0.4); write("#s8-j2",T[1]+0.6,1.2);
draw("#s8-rw",T[2]+0.4,0.5); show("#s8-pl2",T[2]+0.6,0.3);
draw("#s8-w1 path",T[2]+1.4,0.4); draw("#s8-w2 path",T[2]+2.0,0.4); draw("#s8-w3 path",T[2]+2.6,0.4);
tl.fromTo(q("#s8-pl2"),{y:0,rotation:0,svgOrigin:"840 740"},{y:30,rotation:-6,svgOrigin:"840 740",duration:0.4,yoyo:true,repeat:5,ease:"sine.inOut"},T[2]+3.0);
write("#s8-s",T[2]+0.6,0.8); hl("#s8-sh",T[2]+1.4); write("#s8-s2",T[2]+3.4,1.6); write("#s8-s3",T[2]+8.0,1.2);
"""
    return svg, html, js


@scene
def s9():
    X = lambda m: 560 + m / 5000 * 1100
    ticks = "".join(f'M{X(m):.0f},860 L{X(m):.0f},880 ' for m in range(0, 5001, 1000))
    rows = [("niebla", 0, 1000, "rgba(120,130,160,.55)", 330), ("neblina", 1000, 3000, "rgba(160,170,200,.45)", 450),
            ("bruma", 0, 2000, "rgba(66,188,240,.45)", 570), ("calima", 2000, 5000, "rgba(220,170,90,.5)", 690)]
    svg = ln("s9-ax", f"M{X(0)},870 L{X(5000)},870", "ink", 5) + ln("s9-tk", ticks, "ink", 4)
    html = title("s9", "8 · Niebla y visibilidad", "blue")
    for i, (n, a, b, c, y) in enumerate(rows):
        svg += f'<rect class="s9-r" id="s9-r{i}" x="{X(a):.0f}" y="{y}" width="{X(b)-X(a):.0f}" height="70" rx="10" fill="{c}" stroke="#23307a" stroke-width="3"/>'
        html += text(f"s9-n{i}", 200, y + 4, n.capitalize(), "lbl")
    html += "".join(text(f"s9-m{m}", X(m) - 60, 890, f"{m} m", "sm", "width:120px;text-align:center") for m in range(0, 5001, 1000))
    html += (text("s9-d0", 900, 336, "nube baja · < 1000 m", "sm") + text("s9-d1", 1580, 456, "más tenue", "sm")
             + text("s9-d2", 1020, 576, "partículas + humedad · < 2000 m", "sm") + text("s9-d3", 1020, 696, "polvo", "sm")
             + text("s9-s", 200, 960, mark("Smog", "pink", "s9-sh") + " = humo + niebla · " + mark("Humo", "pink", "s9-hh") + " = contaminación (industria, ciudades)", "sm"))
    js = """
write("#s9-title",T[0]+0.1,1.0); hl("#s9-title-hl",T[0]+1.1);
draw("#s9-ax",T[0]+0.8,0.6); draw("#s9-tk",T[0]+1.2,0.4);
tl.fromTo(q("[id^=s9-m]"),{opacity:0},{opacity:1,duration:0.2,stagger:0.08},T[0]+1.3);
const bar=(i,t)=>{tl.fromTo(q("#s9-r"+i),{scaleX:0,transformOrigin:"0% 50%"},{scaleX:1,duration:0.8,ease:"power2.out"},t); write("#s9-n"+i,t,0.5); write("#s9-d"+i,t+0.9,0.8);};
bar(0,T[0]+2.6); bar(1,T[1]+0.3); bar(2,T[2]+0.3); bar(3,T[3]+0.3);
write("#s9-s",T[4]+0.3,3.2); hl("#s9-sh",T[4]+0.6,0.3); hl("#s9-hh",T[4]+2.4,0.3);
"""
    return svg, html, js


@scene
def s10():
    html = (text("s10-a", 0, 380, "Presión · frentes · hielo", "big", "width:1920px;text-align:center")
            + text("s10-b", 0, 520, "viento · visibilidad", "big", "width:1920px;text-align:center")
            + text("s10-c", 0, 700, mark("leer el cielo es volar seguro", "pink", "s10-ch"), "big", "width:1920px;text-align:center"))
    js = """
write("#s10-a",T[0]+0.1,1.4); write("#s10-b",T[0]+1.6,1.2); write("#s10-c",T[0]+3.2,1.4); hl("#s10-ch",T[0]+4.6,0.5);
"""
    return "", html, js


if __name__ == "__main__":
    build(ROOT, S)
