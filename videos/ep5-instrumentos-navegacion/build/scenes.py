import sys, pathlib, math
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "lib"))
from nb import *  # noqa

S = {}
def scene(fn):
    S[fn.__name__] = fn
    return fn

BLUE_T = "#0a7fb8"


def ln(ident, d, cls="ink", w=4, fill="none"):
    return f'<path class="ln {cls}" pathLength="1" stroke-width="{w}" fill="{fill}" d="{d}" id="{ident}"/>'


def dial(ident, cx, cy, r, n=12, needle_id=None, label=""):
    ticks = "".join(
        f'M{cx + (r-6)*math.cos(a):.1f},{cy + (r-6)*math.sin(a):.1f} L{cx + (r-24)*math.cos(a):.1f},{cy + (r-24)*math.sin(a):.1f} '
        for a in [2 * math.pi * i / n for i in range(n)])
    nid = needle_id or f"{ident}-n"
    return (f'<g id="{ident}"><circle class="ln ink" pathLength="1" cx="{cx}" cy="{cy}" r="{r}" fill="#fdfdff" stroke-width="6"/>'
            f'<path class="ink" fill="none" stroke-width="4" d="{ticks}"/>'
            f'<path id="{nid}" class="pk" fill="none" stroke-width="8" stroke-linecap="round" d="M{cx},{cy} L{cx},{cy - r + 34}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="10" fill="#23307a"/></g>')


def cloud(x, y, s=1.0, ident=""):
    i = f' id="{ident}"' if ident else ""
    return (f'<path{i} class="cl" fill="rgba(255,255,255,.9)" stroke="#9aa6c8" stroke-width="4" transform="translate({x},{y}) scale({s})" '
            f'd="M0,60 C-10,20 40,0 70,20 C90,-20 160,-10 170,30 C210,25 230,70 200,90 L10,90 C-20,90 -20,62 0,60 Z"/>')


@scene
def s1():
    svg = ('<g id="s1-cl">' + cloud(240, 300, 1.4) + cloud(1300, 260, 1.6) + cloud(700, 720, 1.2) + cloud(1450, 700, 1.1) + '</g>'
           + f'<g id="s1-pl"><g transform="translate(640,440) scale(1.1)">{PLANE_SIDE}</g></g>' + '<g id="s1-cf">' + cloud(1100, 470, 1.3) + '</g>')
    html = (text("s1-q1", 220, 160, "¿velocidad?", "lbl") + text("s1-q2", 820, 200, "¿altura?", "lbl") + text("s1-q3", 1360, 160, "¿rumbo?", "lbl")
            + text("s1-title", 0, 880, mark("Instrumentos y navegación", "blue", "s1-title-hl"), "h1 big", "width:1920px;text-align:center"))
    js = """
tl.set(q("svg .ln"),{strokeDashoffset:0},0);
tl.fromTo(q("#s1-cl"),{x:0},{x:-120,duration:D,ease:"none"},0); tl.fromTo(q("#s1-cf"),{x:0},{x:-260,duration:D,ease:"none"},0);
tl.fromTo(q("#s1-pl"),{y:0},{y:-14,duration:1.6,yoyo:true,repeat:Math.round(D/1.6),ease:"sine.inOut"},0);
write("#s1-q1",T[0]+3.6,0.6); write("#s1-q2",T[0]+4.8,0.5); write("#s1-q3",T[0]+6.2,0.5);
write("#s1-title",T[1]+0.4,1.4); hl("#s1-title-hl",T[1]+1.8,0.5);
"""
    return svg, html, js


@scene
def s2():
    svg = (f'<g transform="translate(-120,260) scale(3.2)">{PLANE_SIDE}</g>'
           + ln("s2-pitot", "M120,560 L20,560 M120,560 L120,590", "pk", 9)
           + f'<circle id="s2-static" cx="560" cy="610" r="14" fill="#fdfdff" stroke="#ff3d96" stroke-width="7"/>'
           + "".join(arrow(-200 + 0, 560 + dy, 0, 560 + dy, "bl", 5, 20, f"s2-w{i}") for i, dy in enumerate([-30, 0, 30])))
    html = (title("s2", "1 · Tomas de aire")
            + text("s2-s", 480, 700, mark("Tomas estáticas", "blue", "s2-sh"), "lbl")
            + text("s2-s2", 480, 770, "presión ambiental exterior", "sm")
            + text("s2-p", 200, 380, mark("Tubo pitot", "pink", "s2-ph"), "lbl")
            + text("s2-p2", 200, 450, "presión de impacto", "sm"))
    js = """
write("#s2-title",T[0]+0.1,0.8); hl("#s2-title-hl",T[0]+0.9);
draw("svg > g:first-child .ln",T[0]+0.3,1.6);
tl.fromTo(q("#s2-static"),{opacity:0,scale:0.2,transformOrigin:"50% 50%"},{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"},T[1]+0.8);
write("#s2-s",T[1]+0.6,0.9); hl("#s2-sh",T[1]+1.5); write("#s2-s2",T[1]+2.4,1.0);
draw("#s2-pitot",T[2]+0.6,0.6); write("#s2-p",T[2]+0.8,0.7); hl("#s2-ph",T[2]+1.5);
tl.set(q("#s2-w0, #s2-w1, #s2-w2"),{x:0},0);
tl.fromTo(q("[id^=s2-w] path"),{strokeDashoffset:1},{strokeDashoffset:0,duration:0.5,stagger:0.1},T[2]+2.6);
tl.fromTo(q("[id^=s2-w]"),{x:0},{x:120,duration:1.0,ease:"power1.in"},T[2]+2.8);
write("#s2-p2",T[2]+3.0,0.9);
"""
    return svg, html, js


@scene
def s3():
    svg = (dial("s3-asi", 760, 600, 260)
           + ln("s3-pp", "M300,880 L300,720 L520,720", "pk", 6) + ln("s3-sp", "M300,940 L560,940 L620,840", "bl", 6))
    html = (title("s3", "2 · Anemómetro", "blue")
            + text("s3-a", 200, 270, "air speed indicator → " + mark("velocidad", "pink", "s3-ah"), "lbl")
            + text("s3-pt", 200, 640, "pitot", "sm", "color:#ff3d96") + text("s3-st", 200, 860, "estáticas", "sm", f"color:{BLUE_T}")
            + text("s3-k1", 1140, 440, mark("1 nudo (kt)", "blue", "s3-k1h") + " = 1 NM/h", "lbl")
            + text("s3-k2", 1140, 560, mark("1 milla náutica", "pink", "s3-k2h"), "lbl")
            + text("s3-k3", 1160, 630, "= 1,852 km", "lbl"))
    js = """
write("#s3-title",T[0]+0.1,0.8); hl("#s3-title-hl",T[0]+0.9);
draw("#s3-asi .ln",T[0]+0.4,0.8); tl.fromTo(q("#s3-asi"),{opacity:0},{opacity:1,duration:0.3},T[0]+0.4);
write("#s3-a",T[0]+1.4,1.2); hl("#s3-ah",T[0]+2.6);
tl.fromTo(q("#s3-asi-n"),{rotation:-120,svgOrigin:"760 600"},{rotation:60,svgOrigin:"760 600",duration:3,ease:"power2.inOut"},T[0]+3.0);
draw("#s3-pp",T[0]+4.4,0.6); write("#s3-pt",T[0]+4.6,0.4); draw("#s3-sp",T[0]+5.4,0.6); write("#s3-st",T[0]+5.6,0.5);
write("#s3-k1",T[1]+0.6,1.4); hl("#s3-k1h",T[1]+2.0);
write("#s3-k2",T[1]+3.4,0.9); hl("#s3-k2h",T[1]+4.3); write("#s3-k3",T[1]+5.4,0.9);
"""
    return svg, html, js


@scene
def s4():
    dots = "".join(f'<circle class="s4-d" cx="{x}" cy="{y}" r="7" fill="rgba(66,188,240,.7)"/>' for x, y in
                   [(240 + 40 * (i % 9), 900 - 30 * (i // 9) - (i % 3) * 6) for i in range(54) if (i // 9) < 6 and (i % (1 + i // 9)) == 0])
    svg = (dots + f'<g id="s4-pl"><g transform="translate(260,820) scale(0.5)">{PLANE_SIDE}</g></g>'
           + dial("s4-alt", 960, 560, 200) + dial("s4-vsi", 1460, 560, 200))
    html = (title("s4", "3 · Altímetro y variómetro")
            + text("s4-a", 800, 790, mark("Altímetro", "blue", "s4-ah"), "lbl") + text("s4-a2", 760, 860, "solo tomas estáticas", "sm")
            + text("s4-p", 200, 260, "+ altura → − presión", "lbl")
            + text("s4-m", 780, 930, mark("1 m = 3,28 ft", "pink", "s4-mh"), "lbl")
            + text("s4-v", 1300, 790, mark("Variómetro", "blue", "s4-vh"), "lbl") + text("s4-v2", 1300, 860, "velocidad vertical", "sm")
            + text("s4-v3", 1300, 920, "pies por minuto", "sm"))
    js = """
write("#s4-title",T[0]+0.1,1.0); hl("#s4-title-hl",T[0]+1.1);
tl.set(q("#s4-pl .ln"),{strokeDashoffset:0},0);
tl.fromTo(q("#s4-alt"),{opacity:0},{opacity:1,duration:0.4},T[0]+0.6); draw("#s4-alt .ln",T[0]+0.6,0.6);
write("#s4-a",T[0]+0.8,0.6); hl("#s4-ah",T[0]+1.4); write("#s4-a2",T[0]+2.4,0.9);
tl.fromTo(q("#s4-pl"),{x:0,y:0},{x:120,y:-400,duration:3.2,ease:"power1.inOut"},T[0]+3.4);
tl.fromTo(q("#s4-alt-n"),{rotation:0,svgOrigin:"960 560"},{rotation:300,svgOrigin:"960 560",duration:3.2,ease:"power1.inOut"},T[0]+3.4);
write("#s4-p",T[0]+3.8,1.2);
write("#s4-m",T[1]+1.4,1.2); hl("#s4-mh",T[1]+2.6);
tl.fromTo(q("#s4-vsi"),{opacity:0},{opacity:1,duration:0.4},T[2]+0.2); draw("#s4-vsi .ln",T[2]+0.2,0.6);
write("#s4-v",T[2]+0.4,0.7); hl("#s4-vh",T[2]+1.1); write("#s4-v2",T[2]+2.6,0.9); write("#s4-v3",T[2]+5.4,0.9);
tl.fromTo(q("#s4-vsi-n"),{rotation:-90,svgOrigin:"1460 560"},{rotation:-40,svgOrigin:"1460 560",duration:0.8,yoyo:true,repeat:3,ease:"sine.inOut"},T[2]+3.4);
"""
    return svg, html, js


@scene
def s5():
    ai = """<g id="s5-ai"><clipPath id="s5-clip"><circle cx="420" cy="560" r="170"/></clipPath>
<g clip-path="url(#s5-clip)"><g id="s5-hz"><rect x="120" y="300" width="600" height="260" fill="rgba(66,188,240,.55)"/><rect x="120" y="560" width="600" height="300" fill="rgba(176,120,70,.55)"/>
<path class="ink" fill="none" stroke-width="5" d="M120,560 L720,560"/></g></g>
<circle cx="420" cy="560" r="170" fill="none" stroke="#23307a" stroke-width="7"/>
<path fill="none" stroke="#ff3d96" stroke-width="9" stroke-linecap="round" d="M330,560 L390,560 L420,585 L450,560 L510,560"/></g>"""
    rose = "".join(f'<path class="ink" fill="none" stroke-width="{5 if i % 3 == 0 else 3}" d="M{960 + 170*math.sin(a):.1f},{560 - 170*math.cos(a):.1f} L{960 + (140 if i % 3 == 0 else 152)*math.sin(a):.1f},{560 - (140 if i % 3 == 0 else 152)*math.cos(a):.1f}"/>' for i, a in enumerate([2*math.pi*k/36 for k in range(36)]))
    hdg = (f'<g id="s5-hd"><circle cx="960" cy="560" r="180" fill="#fdfdff" stroke="#23307a" stroke-width="7"/><g id="s5-rose">{rose}'
           '<text x="960" y="440" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="56" fill="#23307a">N</text></g>'
           '<path fill="none" stroke="#ff3d96" stroke-width="8" stroke-linecap="round" d="M960,500 L960,620 M920,540 L1000,540 M940,600 L980,600"/></g>')
    tc = ('<g id="s5-tc"><circle cx="1500" cy="560" r="170" fill="#fdfdff" stroke="#23307a" stroke-width="7"/>'
          '<g id="s5-tcp"><path fill="none" stroke="#ff3d96" stroke-width="9" stroke-linecap="round" d="M1380,560 L1620,560 M1500,560 L1500,520 M1470,600 L1530,600"/></g>'
          '<path class="ink" fill="none" stroke-width="4" d="M1380,630 L1404,620 M1620,630 L1596,620"/></g>')
    efis = ln("s5-efis", "M560,300 L1360,300 L1360,820 L560,820 Z", "ink", 8, "rgba(35,48,122,.92)")
    svg = ai + hdg + tc + efis + '<g id="s5-efc"><rect x="640" y="380" width="300" height="360" fill="rgba(66,188,240,.7)"/><rect x="640" y="560" width="300" height="180" fill="rgba(176,120,70,.7)"/><path stroke="#20d080" stroke-width="5" fill="none" d="M1000,400 L1000,720 M1100,400 L1100,720 M1180,560 A80,80 0 1 1 1180,559"/></g>'
    html = (title("s5", "4 · Giróscopos", "blue")
            + text("s5-a", 250, 760, mark("Horizonte artificial", "blue", "s5-ah"), "lbl")
            + text("s5-b", 830, 760, mark("Giro direccional", "pink", "s5-bh"), "lbl") + text("s5-b2", 870, 830, "rumbo", "sm")
            + text("s5-c", 1330, 760, mark("Coordinador de giro", "blue", "s5-ch"), "lbl")
            + text("s5-e", 760, 860, mark("Pantallas EFIS", "pink", "s5-eh") + " · todo junto", "lbl"))
    js = """
write("#s5-title",T[0]+0.1,0.8); hl("#s5-title-hl",T[0]+0.9);
tl.set(q("#s5-ai, #s5-hd, #s5-tc, #s5-efc"),{opacity:0},0);
show("#s5-ai",T[1]+0.3,0.4); write("#s5-a",T[1]+0.5,0.9); hl("#s5-ah",T[1]+1.4);
tl.fromTo(q("#s5-hz"),{rotation:0,y:0,svgOrigin:"420 560"},{rotation:18,y:-30,svgOrigin:"420 560",duration:1.4,yoyo:true,repeat:3,ease:"sine.inOut"},T[1]+1.6);
show("#s5-hd",T[2]+0.2,0.4); write("#s5-b",T[2]+0.4,0.8); hl("#s5-bh",T[2]+1.2); write("#s5-b2",T[2]+1.6,0.4);
tl.fromTo(q("#s5-rose"),{rotation:0,svgOrigin:"960 560"},{rotation:-70,svgOrigin:"960 560",duration:2.4,ease:"sine.inOut"},T[2]+0.8);
show("#s5-tc",T[3]+0.3,0.4); write("#s5-c",T[3]+0.5,0.9); hl("#s5-ch",T[3]+1.4);
tl.fromTo(q("#s5-tcp"),{rotation:0,svgOrigin:"1500 560"},{rotation:-18,svgOrigin:"1500 560",duration:1.0,yoyo:true,repeat:3,ease:"sine.inOut"},T[3]+1.6);
tl.to(q("#s5-ai, #s5-hd, #s5-tc, #s5-a, #s5-b, #s5-b2, #s5-c"),{opacity:0,duration:0.4},T[4]-0.1);
draw("#s5-efis",T[4]+0.3,0.8); show("#s5-efc",T[4]+0.9,0.5); write("#s5-e",T[4]+1.2,1.0); hl("#s5-eh",T[4]+2.2);
"""
    return svg, html, js


@scene
def s6():
    vors = [(700, 520), (1200, 360), (1300, 760)]
    hexa = lambda cx, cy, i: f'<path id="s6-v{i}" class="ln ink" pathLength="1" stroke-width="5" fill="rgba(66,188,240,.35)" d="M{cx-30},{cy} L{cx-15},{cy-26} L{cx+15},{cy-26} L{cx+30},{cy} L{cx+15},{cy+26} L{cx-15},{cy+26} Z"/>'
    rays = "".join(f'<path fill="none" stroke="#1ea7e4" stroke-width="4" d="M700,520 L{700 + 240*math.cos(a):.0f},{520 + 240*math.sin(a):.0f}"/>' for a in [k * math.pi / 6 for k in range(12)])
    svg = (f'<g id="s6-ndb"><circle cx="300" cy="420" r="16" fill="#23307a"/><circle cx="300" cy="420" r="44" fill="none" stroke="#23307a" stroke-width="3" stroke-dasharray="6 8"/></g>'
           + f'<g id="s6-rays">{rays}</g>' + "".join(hexa(x, y, i) for i, (x, y) in enumerate(vors))
           + ln("s6-aw", "M700,520 L1200,360 M700,520 L1300,760 M1200,360 L1300,760", "pk", 6)
           + f'<g id="s6-pl"><g transform="translate(860,420) scale(0.35)">{PLANE_SIDE}</g></g>'
           + arrow(940, 470, 735, 515, "inkp", 5, 22, "s6-dme")
           + ln("s6-rw", "M1500,880 L1720,880 M1500,900 L1720,900", "ink", 6)
           + ln("s6-gs", "M1500,890 L1180,700 M1500,890 L1220,640", "bl", 4))
    html = (title("s6", "5 · Radioayudas")
            + text("s6-n", 200, 480, "NDB", "lbl") + text("s6-n2", 200, 540, "la primera", "sm")
            + text("s6-v", 520, 640, mark("VOR", "blue", "s6-vh") + " · como un faro", "lbl")
            + text("s6-v2", 520, 710, "≈ 200 km · morse · equipo NAV", "sm")
            + text("s6-aw2", 1300, 520, "aerovías", "lbl", "color:#ff3d96")
            + text("s6-d", 900, 260, mark("DME", "pink", "s6-dh") + " · distancia", "lbl")
            + text("s6-i", 1420, 940, mark("ILS", "blue", "s6-ih") + " · hasta la pista", "lbl"))
    js = """
write("#s6-title",T[0]+0.1,0.8); hl("#s6-title-hl",T[0]+0.9);
tl.set(q("#s6-ndb, #s6-rays, #s6-pl"),{opacity:0},0); tl.set(q("#s6-pl .ln"),{strokeDashoffset:0},0);
show("#s6-ndb",T[1]+0.3,0.3); write("#s6-n",T[1]+0.3,0.5); write("#s6-n2",T[1]+2.6,0.6);
draw("#s6-v0",T[2]+0.2,0.5); write("#s6-v",T[2]+0.4,0.9); hl("#s6-vh",T[2]+1.3);
show("#s6-rays",T[2]+1.0,0.3); tl.fromTo(q("#s6-rays"),{rotation:0,svgOrigin:"700 520"},{rotation:180,svgOrigin:"700 520",duration:D-T[2]-1,ease:"none"},T[2]+1.0);
tl.to(q("#s6-rays"),{opacity:0.35,duration:0.5},T[2]+3.0);
write("#s6-v2",T[2]+2.2,2.4);
draw("#s6-v1, #s6-v2",T[2]+6.6,0.4); draw("#s6-aw",T[2]+7.0,1.2); write("#s6-aw2",T[2]+7.6,0.6);
show("#s6-pl",T[3]+0.2,0.3); draw("#s6-dme path",T[3]+0.6,0.5); write("#s6-d",T[3]+0.4,0.7); hl("#s6-dh",T[3]+1.1);
draw("#s6-rw",T[4]+0.4,0.5); draw("#s6-gs",T[4]+1.2,0.8); write("#s6-i",T[4]+0.6,0.8); hl("#s6-ih",T[4]+1.4);
"""
    return svg, html, js


@scene
def s7():
    svg = (f'<g transform="translate(560,600) rotate(90) scale(0.4)">{PLANE_TOP}</g>'
           + '<circle id="s7-ring" cx="560" cy="600" r="210" fill="none" stroke="#1ea7e4" stroke-width="5" stroke-dasharray="14 12"/>'
           + f'<g id="s7-oth"><g transform="translate(700,330) rotate(200) scale(0.3)">{PLANE_TOP}</g></g>'
           + '<path id="s7-mt" fill="rgba(120,140,110,.35)" stroke="#23307a" stroke-width="5" d="M1300,880 L1500,520 L1600,660 L1680,560 L1760,880 Z"/>'
           + f'<g id="s7-gp"><g transform="translate(1040,560) rotate(10) scale(0.45)">{PLANE_SIDE}</g></g>')
    html = (title("s7", "6 · Evitar accidentes", "blue")
            + text("s7-t", 200, 860, mark("TCAS", "blue", "s7-th") + " · otros aviones", "lbl")
            + text("s7-g", 1100, 860, mark("GPWS", "pink", "s7-gh") + " · el terreno", "lbl")
            + text("s7-w", 1180, 360, "TERRAIN!", "lbl", "color:#ff3d96"))
    js = """
write("#s7-title",T[0]+0.1,1.0); hl("#s7-title-hl",T[0]+1.1);
tl.set(q("svg .ln"),{strokeDashoffset:0},0);
tl.set(q("svg > g, #s7-ring, #s7-mt"),{opacity:0},0);
tl.to(q("svg > g:first-child"),{opacity:1,duration:0.3},T[1]); show("#s7-ring",T[1]+0.4,0.3);
show("#s7-oth",T[1]+1.0,0.3); tl.fromTo(q("#s7-oth"),{x:0,y:0},{x:-60,y:60,duration:2,ease:"none"},T[1]+1.0);
tl.to(q("#s7-oth .ln"),{stroke:"#e8364f",duration:0.2},T[1]+2.0);
write("#s7-t",T[1]+0.6,0.8); hl("#s7-th",T[1]+1.4);
show("#s7-mt",T[2]+0.2,0.4); show("#s7-gp",T[2]+0.4,0.3);
tl.fromTo(q("#s7-gp"),{x:0,y:0},{x:80,y:30,duration:2,ease:"none"},T[2]+0.4);
write("#s7-g",T[2]+0.4,0.8); hl("#s7-gh",T[2]+1.2);
tl.fromTo(q("#s7-w"),{opacity:0},{opacity:1,duration:0.1,yoyo:true,repeat:7},T[2]+2.4);
"""
    return svg, html, js


@scene
def s8():
    cx, cy, r = 700, 630, 270
    pars = "".join(f'<ellipse class="s8-par" cx="{cx}" cy="{cy + r*math.sin(a):.0f}" rx="{r*math.cos(a):.0f}" ry="{max(6, 30*math.cos(a)):.0f}" fill="none" stroke="#1ea7e4" stroke-width="3"/>' for a in [-1.0, -0.5, 0.5, 1.0])
    mers = "".join(f'<ellipse class="s8-mer" cx="{cx}" cy="{cy}" rx="{rx}" ry="{r}" fill="none" stroke="#5a3fb0" stroke-width="3"/>' for rx in (100, 200))
    svg = (f'<circle class="ln ink" pathLength="1" id="s8-globe" cx="{cx}" cy="{cy}" r="{r}" fill="#fdfdff" stroke-width="6"/>'
           + pars + mers
           + f'<ellipse id="s8-eq" cx="{cx}" cy="{cy}" rx="{r}" ry="34" fill="none" stroke="#ff3d96" stroke-width="7"/>'
           + f'<path id="s8-gw" fill="none" stroke="#ff3d96" stroke-width="7" d="M{cx},{cy-r} L{cx},{cy+r}"/>'
           + f'<circle id="s8-pt" cx="{cx+100}" cy="{cy - r*math.sin(0.5):.0f}" r="14" fill="#ff3d96"/>')
    html = (title("s8", "7 · Coordenadas")
            + text("s8-g", 200, 236, mark("Geoide", "blue", "s8-gh") + " · la forma de la Tierra", "lbl")
            + text("s8-eqt", 1060, 300, mark("Paralelos", "blue", "s8-eqh") + " → latitud", "lbl") + text("s8-eq2", 1080, 370, "0–90° · Norte / Sur", "sm")
            + text("s8-mt", 1060, 480, mark("Meridianos", "pink", "s8-mh") + " → longitud", "lbl") + text("s8-mt2", 1080, 550, "Greenwich = 0° · 0–180° E / O", "sm")
            + text("s8-c", 1060, 680, "cruce = " + mark("coordenada", "pink", "s8-ch"), "lbl")
            + text("s8-c2", 1080, 760, "decimal: 40,42° N · 3,70° O", "sm") + text("s8-c3", 1080, 815, "sexagesimal: 40° 25′ N · 3° 42′ O", "sm")
            + text("s8-c4", 1080, 870, "(ejemplo: Madrid)", "sm"))
    js = """
write("#s8-title",T[0]+0.1,0.8); hl("#s8-title-hl",T[0]+0.9);
draw("#s8-globe",T[0]+0.4,1.0); write("#s8-g",T[0]+4.0,1.2); hl("#s8-gh",T[0]+5.2);
tl.set(q(".s8-par, .s8-mer, #s8-eq, #s8-gw, #s8-pt"),{opacity:0},0);
show("#s8-eq",T[1]+1.2,0.3); tl.to(q(".s8-par"),{opacity:1,duration:0.2,stagger:0.15},T[1]+1.6);
write("#s8-eqt",T[1]+0.6,0.9); hl("#s8-eqh",T[1]+1.5); write("#s8-eq2",T[1]+3.6,1.0);
tl.to(q(".s8-mer"),{opacity:1,duration:0.2,stagger:0.15},T[2]+0.8); show("#s8-gw",T[2]+2.0,0.3);
write("#s8-mt",T[2]+0.6,0.9); hl("#s8-mh",T[2]+1.5); write("#s8-mt2",T[2]+3.4,1.4);
show("#s8-pt",T[3]+1.0,0.2); tl.fromTo(q("#s8-pt"),{scale:2.2,transformOrigin:"50% 50%"},{scale:1,duration:0.4,ease:"back.out(2)"},T[3]+1.0);
write("#s8-c",T[3]+1.0,0.9); hl("#s8-ch",T[3]+1.9);
write("#s8-c2",T[3]+4.0,1.0); write("#s8-c3",T[3]+5.6,1.2); write("#s8-c4",T[3]+6.8,0.6);
"""
    return svg, html, js


@scene
def s9():
    zones = [(-30, "10:00"), (-15, "11:00"), (0, "12:00"), (15, "13:00"), (30, "14:00")]
    svg = ""
    html = title("s9", "8 · La hora en aviación", "blue")
    for i, (deg, hh) in enumerate(zones):
        x = 360 + i * 300
        fill = "rgba(255,92,168,.25)" if deg == 0 else "rgba(66,188,240,.15)"
        svg += f'<rect class="s9-z" id="s9-z{i}" x="{x-140}" y="430" width="280" height="300" fill="{fill}" stroke="#23307a" stroke-width="3"/>'
        html += text(f"s9-d{i}", x - 140, 450, f"{deg:+d}°" if deg else "0°", "sm", "width:280px;text-align:center")
        html += text(f"s9-h{i}", x - 140, 540, hh, "big", "width:280px;text-align:center;font-size:96px")
    html += (text("s9-u", 200, 250, mark("UTC = GMT = Zulu (Z)", "pink", "s9-uh"), "lbl")
             + text("s9-e", 1100, 770, "este → + 1 h cada 15°", "lbl") + text("s9-w", 220, 770, "oeste → − 1 h cada 15°", "lbl")
             + text("s9-l", 200, 880, "hora de cada lugar: " + mark("hora local", "blue", "s9-lh"), "lbl"))
    js = """
write("#s9-title",T[0]+0.1,0.9); hl("#s9-title-hl",T[0]+1.0);
write("#s9-u",T[0]+1.8,2.0); hl("#s9-uh",T[0]+3.8);
tl.set(q(".s9-z, [id^=s9-d], [id^=s9-h]"),{opacity:0},0);
tl.to(q("#s9-z2, #s9-d2, #s9-h2"),{opacity:1,duration:0.3},T[0]+2.0);
tl.to(q("#s9-z3, #s9-d3, #s9-h3"),{opacity:1,duration:0.3},T[1]+2.4); tl.to(q("#s9-z4, #s9-d4, #s9-h4"),{opacity:1,duration:0.3},T[1]+2.9);
write("#s9-e",T[1]+3.0,1.0);
tl.to(q("#s9-z1, #s9-d1, #s9-h1"),{opacity:1,duration:0.3},T[1]+4.6); tl.to(q("#s9-z0, #s9-d0, #s9-h0"),{opacity:1,duration:0.3},T[1]+5.1);
write("#s9-w",T[1]+5.0,1.0);
write("#s9-l",T[2]+0.3,1.4); hl("#s9-lh",T[2]+1.7);
"""
    return svg, html, js


@scene
def s10():
    svg = (arrow(440, 760, 440, 360, "ink", 7, 30, "s10-ng") + arrow(440, 760, 560, 380, "pk", 7, 30, "s10-nm")
           + ln("s10-arc", "M440,540 A220,220 0 0 1 510,550", "inkp", 5)
           + f'<g id="s10-dv"><g transform="translate(960,620) rotate(90) scale(0.35)">{PLANE_TOP}</g></g>'
           + '<g id="s10-cmp"><circle cx="960" cy="460" r="60" fill="#fdfdff" stroke="#23307a" stroke-width="5"/><path id="s10-cn" fill="none" stroke="#ff3d96" stroke-width="7" stroke-linecap="round" d="M960,500 L960,420"/></g>'
           + f'<g id="s10-dr"><g transform="translate(1500,680) rotate(90) scale(0.35)">{PLANE_TOP}</g></g>'
           + ln("s10-hdg", "M1500,680 L1500,300", "ink", 4) + ln("s10-trk", "M1500,680 L1600,320", "pk", 6)
           + "".join(arrow(1240, y, 1380, y, "bl", 5, 22, f"s10-wd{i}") for i, y in enumerate([480, 560, 640])))
    html = (title("s10", "9 · Norte, desvío y deriva")
            + text("s10-a", 340, 290, "N geográfico", "sm") + text("s10-b", 540, 330, "N magnético", "sm", "color:#ff3d96")
            + text("s10-c", 200, 820, mark("Declinación", "blue", "s10-ch"), "lbl")
            + text("s10-d", 820, 820, mark("Desvío", "pink", "s10-dh"), "lbl") + text("s10-d2", 820, 890, "imanes del propio avión", "sm")
            + text("s10-e", 1380, 820, mark("Deriva", "blue", "s10-eh"), "lbl") + text("s10-e2", 1380, 890, "corrige el viento", "sm")
            + text("s10-v", 1220, 400, "viento", "sm", f"color:{BLUE_T}"))
    js = """
write("#s10-title",T[0]+0.1,1.0); hl("#s10-title-hl",T[0]+1.1);
draw("#s10-ng path",T[0]+0.6,0.6); write("#s10-a",T[0]+0.9,0.6);
draw("#s10-nm path",T[0]+1.6,0.6); write("#s10-b",T[0]+1.9,0.6);
draw("#s10-arc",T[0]+3.8,0.5); write("#s10-c",T[0]+4.0,0.9); hl("#s10-ch",T[0]+4.9);
tl.set(q("#s10-dv, #s10-cmp, #s10-dr, #s10-v"),{opacity:0},0); tl.set(q("svg > g .ln"),{strokeDashoffset:0},0);
show("#s10-dv",T[1]+0.2,0.3); show("#s10-cmp",T[1]+0.4,0.3);
tl.fromTo(q("#s10-cn"),{rotation:-14,svgOrigin:"960 460"},{rotation:14,svgOrigin:"960 460",duration:0.5,yoyo:true,repeat:7,ease:"sine.inOut"},T[1]+0.8);
write("#s10-d",T[1]+0.6,0.6); hl("#s10-dh",T[1]+1.2); write("#s10-d2",T[1]+2.4,1.0);
show("#s10-dr",T[2]+0.2,0.3); draw("#s10-hdg",T[2]+0.4,0.5);
draw("[id^=s10-wd] path",T[2]+1.4,0.5); show("#s10-v",T[2]+1.4,0.3); draw("#s10-trk",T[2]+2.2,0.6);
write("#s10-e",T[2]+0.6,0.6); hl("#s10-eh",T[2]+1.2); write("#s10-e2",T[2]+3.0,0.9);
"""
    return svg, html, js


@scene
def s11():
    svg = ('<path id="s11-sea" fill="rgba(66,188,240,.3)" d="M200,860 C260,845 320,875 380,860 C440,845 500,875 560,860 L560,960 L200,960 Z"/>'
           + ln("s11-msl", "M200,860 L1720,860", "bl", 4)
           + '<path id="s11-mt" fill="rgba(120,140,110,.35)" stroke="#23307a" stroke-width="5" d="M700,860 L1000,560 L1200,680 L1460,860 Z"/>'
           + f'<g transform="translate(900,250) scale(0.6)">{PLANE_SIDE}</g>'
           + arrow(1060, 340, 1060, 640, "pk", 6, 24, "s11-h1") + arrow(1060, 640, 1060, 340, "pk", 6, 24, "s11-h2")
           + arrow(820, 340, 820, 855, "inkp", 6, 24, "s11-a1") + arrow(820, 855, 820, 340, "inkp", 6, 24, "s11-a2")
           + arrow(1000, 575, 1000, 855, "bl", 6, 24, "s11-e1") + arrow(1000, 855, 1000, 575, "bl", 6, 24, "s11-e2"))
    html = (title("s11", "10 · Altura, altitud, elevación", "blue")
            + text("s11-ht", 1100, 440, mark("Altura", "pink", "s11-hh") + " · avión → terreno", "lbl")
            + text("s11-at", 200, 520, mark("Altitud", "blue", "s11-ah"), "lbl") + text("s11-at2", 200, 590, "avión → nivel del mar", "sm")
            + text("s11-et", 1280, 620, mark("Elevación", "blue", "s11-eh"), "lbl") + text("s11-et2", 1280, 690, "terreno → nivel del mar", "sm")
            + text("s11-sl", 220, 880, "nivel del mar", "sm"))
    js = """
write("#s11-title",T[0]+0.1,1.0); hl("#s11-title-hl",T[0]+1.1);
tl.set(q("svg > g:not([id]) .ln"),{strokeDashoffset:0},0);
draw("#s11-msl",T[0]+0.6,0.6); write("#s11-sl",T[0]+0.8,0.6);
draw("#s11-h1 path, #s11-h2 path",T[1]+0.2,0.6); write("#s11-ht",T[1]+0.3,1.0); hl("#s11-hh",T[1]+1.3);
draw("#s11-a1 path, #s11-a2 path",T[2]+0.2,0.6); write("#s11-at",T[2]+0.3,0.6); hl("#s11-ah",T[2]+0.9); write("#s11-at2",T[2]+1.2,0.9);
draw("#s11-e1 path, #s11-e2 path",T[3]+0.4,0.6); write("#s11-et",T[3]+0.5,0.6); hl("#s11-eh",T[3]+1.1); write("#s11-et2",T[3]+1.6,1.0);
"""
    return svg, html, js


@scene
def s12():
    svg = (ln("s12-frac", "M1080,430 L1560,430", "ink", 6)
           + '<g id="s12-sun"><circle cx="420" cy="800" r="50" fill="rgba(255,214,90,.7)" stroke="#23307a" stroke-width="4"/></g>'
           + cloud(1100, 740, 1.2, "s12-cl"))
    html = (title("s12", "11 · Mach y reglas de vuelo")
            + text("s12-s", 200, 250, mark("Velocidad del sonido", "pink", "s12-sh"), "lbl")
            + text("s12-s2", 220, 320, "1225 km/h · 340 m/s · 661 kt", "lbl")
            + text("s12-m", 900, 400, "Mach =", "lbl")
            + text("s12-m1", 1080, 340, "V avión", "lbl", "width:480px;text-align:center")
            + text("s12-m2", 1080, 440, "V sonido", "lbl", "width:480px;text-align:center")
            + text("s12-m3", 1080, 540, "comercial: " + mark("M 0,70 – 0,88", "blue", "s12-m3h"), "lbl")
            + text("s12-v", 500, 760, mark("VFR", "blue", "s12-vh") + " · visual", "lbl") + text("s12-v2", 500, 830, "condiciones VMC", "sm")
            + text("s12-i", 1440, 760, mark("IFR", "pink", "s12-ih") + " · instrumental", "lbl") + text("s12-i2", 1440, 830, "condiciones IMC", "sm"))
    js = """
write("#s12-title",T[0]+0.1,1.0); hl("#s12-title-hl",T[0]+1.1);
write("#s12-s",T[0]+0.6,0.9); hl("#s12-sh",T[0]+1.5); write("#s12-s2",T[0]+2.6,4.6);
write("#s12-m",T[1]+0.4,0.5); write("#s12-m1",T[1]+1.6,0.6); draw("#s12-frac",T[1]+2.2,0.4); write("#s12-m2",T[1]+2.8,0.7);
write("#s12-m3",T[1]+5.0,1.2); hl("#s12-m3h",T[1]+6.2);
tl.set(q("#s12-sun, #s12-cl"),{opacity:0},0);
show("#s12-sun",T[2]+1.4,0.4); write("#s12-v",T[2]+1.4,0.8); hl("#s12-vh",T[2]+2.2); write("#s12-v2",T[2]+4.0,0.9);
show("#s12-cl",T[3]+0.6,0.4); write("#s12-i",T[3]+0.6,0.9); hl("#s12-ih",T[3]+1.5); write("#s12-i2",T[3]+3.6,0.9);
"""
    return svg, html, js


@scene
def s13():
    html = (text("s13-a", 0, 380, "Instrumentos → " + mark("cómo vuelas", "blue", "s13-ah"), "big", "width:1920px;text-align:center")
            + text("s13-b", 0, 560, "Radioayudas y coordenadas →", "big", "width:1920px;text-align:center")
            + text("s13-c", 0, 700, mark("dónde estás y a dónde vas", "pink", "s13-ch"), "big", "width:1920px;text-align:center"))
    js = """
write("#s13-a",T[0]+0.1,1.4); hl("#s13-ah",T[0]+1.5,0.4);
write("#s13-b",T[0]+2.2,1.4); write("#s13-c",T[0]+3.8,1.4); hl("#s13-ch",T[0]+5.2,0.5);
"""
    return "", html, js


if __name__ == "__main__":
    build(ROOT, S)
