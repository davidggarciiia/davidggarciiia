import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "lib"))
from nb import *  # noqa

S = {}
def scene(fn):
    S[fn.__name__] = fn
    return fn


def ln(ident, d, cls="ink", w=4, extra=""):
    return f'<path class="ln {cls}" pathLength="1" stroke-width="{w}" fill="none" d="{d}" id="{ident}" {extra}/>'


def box(ident, x, y, w, h, fill="none", cls="ink"):
    return (f'<path class="ln {cls}" pathLength="1" stroke-width="4" fill="{fill}" id="{ident}" '
            f'd="M{x+10},{y} L{x+w-10},{y} Q{x+w},{y} {x+w},{y+10} L{x+w},{y+h-10} Q{x+w},{y+h} {x+w-10},{y+h} '
            f'L{x+10},{y+h} Q{x},{y+h} {x},{y+h-10} L{x},{y+10} Q{x},{y} {x+10},{y} Z"/>')


@scene
def s1():
    svg = f"""<g transform="translate(520,500) scale(1.5)">{PLANE_SIDE}</g>
<path class="ln ink" pathLength="1" stroke-width="5" d="M1600,300 L1600,640 M1640,300 L1640,640 M1600,300 Q1620,270 1640,300" id="s1-th"/>
<circle class="ln ink" pathLength="1" stroke-width="5" fill="none" cx="1620" cy="680" r="40" id="s1-bulb"/>
<rect id="s1-merc" x="1606" y="560" width="28" height="120" fill="rgba(66,188,240,.7)"/>
"""
    html = (text("s1-out", 1180, 320, mark("≈ −56 °C", "blue", "s1-out-hl"), "lbl")
            + text("s1-out2", 1180, 390, "aire muy fino", "sm")
            + text("s1-in", 700, 820, "dentro: " + mark("cómodos", "pink", "s1-in-hl"), "lbl")
            + text("s1-title", 200, 110, mark("Los sistemas del avión", "pink", "s1-title-hl"), "h1 big"))
    js = """
tl.set(q("svg > g .ln"),{strokeDashoffset:0},0); tl.set(q("#s1-merc"),{opacity:0},0); show("#s1-merc",T[0]+1.3,0.2);
draw("#s1-th",T[0]+0.6,0.8); draw("#s1-bulb",T[0]+1.0,0.4);
tl.fromTo(q("#s1-merc"),{scaleY:1,transformOrigin:"50% 100%"},{scaleY:0.25,transformOrigin:"50% 100%",duration:2,ease:"power2.inOut"},T[0]+1.5);
write("#s1-out",T[0]+2.0,0.8); hl("#s1-out-hl",T[0]+2.8); write("#s1-out2",T[0]+4.5,0.8);
write("#s1-in",T[1]+0.4,1.0); hl("#s1-in-hl",T[1]+1.4);
write("#s1-title",T[1]+2.4,1.3); hl("#s1-title-hl",T[1]+3.7,0.5);
"""
    return svg, html, js


@scene
def s2():
    svg = f"""
<circle class="ln pk" pathLength="1" stroke-width="6" fill="rgba(255,92,168,.12)" cx="960" cy="590" r="150" id="s2-hub"/>
{arrow(560, 380, 810, 520, "bl", 6, 28, "s2-i1")}{arrow(560, 590, 800, 590, "bl", 6, 28, "s2-i2")}{arrow(560, 800, 810, 660, "bl", 6, 28, "s2-i3")}
{arrow(1110, 520, 1330, 380, "ink", 6, 28, "s2-o1")}{arrow(1115, 560, 1330, 520, "ink", 6, 28, "s2-o2")}
{arrow(1115, 620, 1330, 660, "ink", 6, 28, "s2-o3")}{arrow(1110, 660, 1330, 800, "ink", 6, 28, "s2-o4")}
"""
    html = (title("s2", "1 · Sistema neumático", "blue")
            + text("s2-c", 830, 545, "aire<br>comprimido", "sm", "text-align:center;width:260px;white-space:normal;font-size:44px")
            + text("s2-a", 200, 340, "compresor<br>de los motores", "lbl", "white-space:normal;width:360px")
            + text("s2-b", 300, 560, "APU", "lbl")
            + text("s2-c2", 160, 790, "Air service unit", "lbl") + text("s2-c3", 200, 856, "(en tierra)", "sm")
            + text("s2-p1", 1350, 340, mark("presurización", "pink", "s2-p1h"), "lbl")
            + text("s2-p2", 1350, 480, "arranque de motores", "lbl")
            + text("s2-p3", 1350, 620, "aire acondicionado", "lbl")
            + text("s2-p4", 1350, 760, "antihielo", "lbl"))
    js = """
write("#s2-title",T[0]+0.1,1.0); hl("#s2-title-hl",T[0]+1.1);
draw("#s2-hub",T[0]+1.4,0.9); write("#s2-c",T[0]+2.2,1.0);
draw("#s2-i1 path",T[1]+0.6,0.5); write("#s2-a",T[1]+0.8,1.0);
draw("#s2-i2 path",T[1]+2.6,0.5); write("#s2-b",T[1]+2.8,0.4);
draw("#s2-i3 path",T[1]+3.6,0.5); write("#s2-c2",T[1]+5.0,1.0); write("#s2-c3",T[1]+4.0,0.6);
draw("#s2-o1 path",T[2]+0.4,0.4); write("#s2-p1",T[2]+0.6,0.8); hl("#s2-p1h",T[2]+1.4);
draw("#s2-o2 path",T[2]+1.6,0.4); write("#s2-p2",T[2]+1.8,0.9);
draw("#s2-o3 path",T[2]+3.2,0.4); write("#s2-p3",T[2]+3.4,0.9);
draw("#s2-o4 path",T[2]+4.8,0.4); write("#s2-p4",T[2]+5.0,0.6);
"""
    return svg, html, js


@scene
def s3():
    fus = "M1180,300 C1180,250 1210,230 1250,230 C1290,230 1320,250 1320,300 L1320,900 L1180,900 Z"
    svg = f"""
<path class="ln ink" pathLength="1" stroke-width="5" d="M220,360 L480,370 L480,440 L220,450 Z" id="s3-e1"/>
<path class="ln ink" pathLength="1" stroke-width="5" d="M220,700 L480,710 L480,780 L220,790 Z" id="s3-e2"/>
{box("s3-k1", 640, 350, 190, 110, "rgba(66,188,240,.18)")}{box("s3-k2", 640, 690, 190, 110, "rgba(66,188,240,.18)")}
{arrow(490, 405, 630, 405, "pk", 6, 24, "s3-h1")}{arrow(490, 745, 630, 745, "pk", 6, 24, "s3-h2")}
{arrow(840, 405, 1160, 450, "bl", 6, 24, "s3-c1")}{arrow(840, 745, 1160, 700, "bl", 6, 24, "s3-c2")}
<path class="ln ink" pathLength="1" stroke-width="5" d="{fus}" id="s3-fus"/>
<rect id="s3-z1" x="1186" y="300" width="128" height="190" fill="rgba(66,188,240,.35)"/>
<rect id="s3-z2" x="1186" y="500" width="128" height="190" fill="rgba(255,92,168,.3)"/>
<rect id="s3-z3" x="1186" y="700" width="128" height="194" fill="rgba(66,188,240,.35)"/>
<g id="s3-hepa"><rect x="1400" y="690" width="120" height="120" fill="none" stroke="#23307a" stroke-width="4"/>
<path class="ink" stroke-width="2.5" d="M1400,720 L1520,720 M1400,750 L1520,750 M1400,780 L1520,780 M1430,690 L1430,810 M1460,690 L1460,810 M1490,690 L1490,810"/></g>
"""
    html = (title("s3", "2 · Aire acondicionado")
            + text("s3-pk1", 680, 380, "pack", "lbl") + text("s3-pk2", 680, 720, "pack", "lbl")
            + text("s3-hot", 480, 300, "caliente", "sm", "color:#ff3d96") + text("s3-cold", 900, 330, "frío", "sm", "color:#1ea7e4")
            + text("s3-r1", 520, 870, mark("1 pack por motor", "blue", "s3-r1h"), "lbl")
            + text("s3-r2", 1360, 330, "cada zona,", "sm") + text("s3-r2b", 1360, 380, "su climatizador", "sm")
            + text("s3-r3", 1550, 720, mark("filtro HEPA", "pink", "s3-r3h"), "lbl"))
    js = """
write("#s3-title",T[0]+0.1,0.9); hl("#s3-title-hl",T[0]+1.0);
draw("#s3-e1, #s3-e2",T[0]+0.5,0.8);
draw("#s3-h1 path, #s3-h2 path",T[0]+1.4,0.5); write("#s3-hot",T[0]+1.6,0.5);
draw("#s3-k1, #s3-k2",T[0]+2.4,0.7); write("#s3-pk1, #s3-pk2",T[0]+3.0,0.5);
draw("#s3-c1 path, #s3-c2 path",T[0]+3.6,0.5); write("#s3-cold",T[0]+3.8,0.4);
write("#s3-r1",T[1]+0.2,0.9); hl("#s3-r1h",T[1]+1.1);
draw("#s3-fus",T[2]+0.1,0.8);
tl.fromTo(q("#s3-z1, #s3-z2, #s3-z3"),{opacity:0},{opacity:1,duration:0.3,stagger:0.3},T[2]+0.8);
write("#s3-r2",T[2]+1.0,0.5); write("#s3-r2b",T[2]+1.5,0.8);
show("#s3-hepa",T[2]+3.4,0.4); write("#s3-r3",T[2]+3.6,0.7); hl("#s3-r3h",T[2]+4.3);
"""
    return svg, html, js


@scene
def s4():
    y = lambda ft: 900 - ft / 40000 * 620
    ticks = "".join(f'M380,{y(f):.0f} L420,{y(f):.0f} ' for f in range(0, 40001, 10000))
    svg = f"""
<path class="ln ink" pathLength="1" stroke-width="5" d="M400,900 L400,250" id="s4-ax"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="{ticks}" id="s4-ticks"/>
<rect id="s4-band" x="380" y="{y(8000):.0f}" width="320" height="{y(6000)-y(8000):.0f}" fill="rgba(255,92,168,.45)"/>
<g id="s4-pl"><g transform="translate(460,{y(40000)-60:.0f}) scale(0.45)">{PLANE_SIDE}</g></g>
<g transform="translate(1060,520) scale(1.2)">{PLANE_SIDE}</g>
{arrow(1408, 800, 1408, 700, "bl", 6, 24, "s4-in")}
<circle id="s4-valve" cx="1684" cy="652" r="14" fill="#ff3d96"/>
{arrow(1692, 664, 1730, 760, "pk", 6, 24, "s4-out")}
<rect id="s4-cab" x="1190" y="616" width="470" height="40" fill="rgba(66,188,240,.35)"/>
"""
    labels = "".join(text(f"s4-f{i}", 200, y(f) - 30, f"{f//1000} mil ft" if f else "0 ft", "sm", "width:160px;text-align:right") for i, f in enumerate(range(0, 40001, 10000)))
    html = (title("s4", "3 · Presurización", "blue") + labels
            + text("s4-cr", 720, y(40000) - 50, "crucero ≈ 40.000 ft", "sm")
            + text("s4-mf", 720, y(40000) + 10, "+ altura → − combustible", "sm")
            + text("s4-art", 1060, 400, mark("atmósfera artificial", "blue", "s4-arth"), "lbl")
            + text("s4-ofv", 1450, 860, "outflow valve", "sm", "color:#ff3d96")
            + text("s4-inl", 1300, 820, "entra aire", "sm")
            + text("s4-cab-t", 720, y(7000) - 40, "cabina: " + mark("6.000–8.000 ft", "pink", "s4-cabh"), "lbl"))
    js = """
write("#s4-title",T[0]+0.1,0.9); hl("#s4-title-hl",T[0]+1.0);
draw("#s4-ax",T[0]+0.6,0.7); draw("#s4-ticks",T[0]+1.0,0.6);
tl.fromTo(q("[id^=s4-f]"),{opacity:0},{opacity:1,duration:0.2,stagger:0.12},T[0]+1.2);
tl.set(q("#s4-pl .ln, svg > g:not(#s4-pl) .ln"),{strokeDashoffset:0},0);
tl.fromTo(q("#s4-pl"),{y:520,opacity:0},{y:0,opacity:1,duration:2.2,ease:"power2.out"},T[0]+1.8);
write("#s4-mf",T[0]+2.6,1.0); write("#s4-cr",T[0]+4.6,0.8);
tl.fromTo(q("svg > g:not(#s4-pl):not([id])"),{opacity:0},{opacity:1,duration:0.5},T[1]+0.2);
write("#s4-art",T[1]+3.6,1.1); hl("#s4-arth",T[1]+4.7);
show("#s4-cab",T[1]+4.0,0.5);
draw("#s4-in path",T[2]+0.4,0.5); write("#s4-inl",T[2]+0.6,0.6);
show("#s4-valve",T[2]+1.6,0.2); draw("#s4-out path",T[2]+1.8,0.5); write("#s4-ofv",T[2]+2.0,0.8);
tl.fromTo(q("#s4-band"),{scaleX:0,transformOrigin:"0% 50%"},{scaleX:1,duration:0.6},T[3]+0.6);
write("#s4-cab-t",T[3]+0.8,1.2); hl("#s4-cabh",T[3]+2.0);
"""
    return svg, html, js


@scene
def s5():
    drops = "".join(f'<path class="s5-drop bl" fill="none" stroke-width="5" stroke-linecap="round" d="M{x},{yy} l-14,-26"/>' for x, yy in [(1420, 470), (1380, 430), (1460, 420), (1340, 480), (1500, 470), (1400, 380), (1300, 420)])
    svg = f"""<g transform="translate(240,420) scale(1.6)">{PLANE_SIDE}</g>
<path class="ln pk" pathLength="1" stroke-width="10" d="M284,596 L240,600" id="s5-pitot"/>
<path class="ln pk" pathLength="1" stroke-width="10" opacity=".8" d="M624,596 L866,582" id="s5-le"/>
<g transform="translate(640,770)"><path class="ln ink" pathLength="1" stroke-width="5" fill="#fdfdff" d="M0,60 C0,20 70,0 180,0 L360,10 L360,100 L180,110 C70,115 0,100 0,60 Z" id="s5-af"/>
<path id="s5-boot" fill="rgba(255,92,168,.55)" stroke="#23307a" stroke-width="3" d="M-6,60 C-6,22 30,4 70,2 L72,18 C40,20 16,36 16,60 C16,84 40,98 72,100 L70,116 C30,114 -6,98 -6,60 Z"/></g>
<g transform="translate(-180,0)"><g id="s5-truck"><path class="ink" fill="none" stroke-width="5" d="M1500,700 L1720,700 L1720,780 L1500,780 Z M1560,700 L1560,620 L1620,620 L1620,700 M1590,620 L1500,520"/>
<circle class="ink" fill="#fdfdff" stroke-width="5" cx="1540" cy="790" r="18"/><circle class="ink" fill="#fdfdff" stroke-width="5" cx="1690" cy="790" r="18"/></g>
<g transform="translate(0,60)"><g id="s5-drops">{drops}</g></g></g>
"""
    html = (title("s5", "4 · Antihielo")
            + text("s5-a", 200, 270, "calienta el exterior → " + mark("no se forma hielo", "blue", "s5-ah"), "lbl")
            + text("s5-p", 200, 650, "tubo pitot", "sm", "color:#ff3d96")
            + text("s5-b", 200, 860, mark("botas neumáticas", "pink", "s5-bh"), "lbl")
            + text("s5-b2", 200, 926, "se inflan y rompen el hielo", "sm")
            + text("s5-d", 1180, 830, mark("de-icing", "blue", "s5-dh"), "lbl")
            + text("s5-d2", 1180, 896, "glicol + agua caliente", "sm"))
    js = """
write("#s5-title",T[0]+0.1,0.8); hl("#s5-title-hl",T[0]+0.9);
draw("svg > g:first-child .ln",T[0]+0.4,1.2);
write("#s5-a",T[0]+2.6,1.6); hl("#s5-ah",T[0]+4.2);
draw("#s5-le",T[0]+4.0,0.6);
draw("#s5-pitot",T[1]+1.4,0.4); write("#s5-p",T[1]+1.6,0.6);
draw("#s5-af",T[1]+3.2,0.7);
tl.fromTo(q("#s5-boot"),{opacity:0,scale:1,transformOrigin:"100% 50%"},{opacity:1,duration:0.3},T[1]+4.0);
tl.to(q("#s5-boot"),{scale:1.25,transformOrigin:"100% 50%",duration:0.4,yoyo:true,repeat:3},T[1]+4.4);
write("#s5-b",T[1]+4.0,0.9); hl("#s5-bh",T[1]+4.9); write("#s5-b2",T[1]+5.6,1.1);
show("#s5-truck",T[2]+1.4,0.4);
tl.fromTo(q(".s5-drop"),{opacity:0},{opacity:1,duration:0.15,stagger:0.08},T[2]+2.0);
tl.fromTo(q("#s5-drops"),{x:0,y:0},{x:-30,y:-20,duration:0.35,yoyo:true,repeat:Math.max(1,Math.round((D-T[2]-2.2)/0.35)),ease:"sine.inOut"},T[2]+2.2);
write("#s5-d",T[2]+2.4,0.6); hl("#s5-dh",T[2]+3.0); write("#s5-d2",T[2]+3.4,1.2);
"""
    return svg, html, js


@scene
def s6():
    loop = "M300,820 L300,420 L1620,420 L1620,820 Z"
    nodes = [("bomba", 300, 620), ("filtro", 640, 420), ("acumulador", 1000, 420), ("válvula selectora", 1380, 420), ("actuador", 1620, 620), ("válvula de liberación", 960, 820)]
    svg = (ln("s6-loop", loop, "bl", 6)
           + f'<path class="s6-flow" fill="none" stroke="#1ea7e4" stroke-width="8" stroke-dasharray="16 34" d="{loop}"/>'
           + "".join(f'<circle class="s6-n" id="s6-n{i}" cx="{x}" cy="{y}" r="26" fill="#fdfdff" stroke="#23307a" stroke-width="5"/>' for i, (_, x, y) in enumerate(nodes))
           + '<g id="s6-act"><path class="ink" fill="none" stroke-width="10" d="M1650,620 L1760,620"/></g>')
    pos = [(140, 600), (560, 330), (900, 330), (1250, 330), (1500, 670), (760, 860)]
    html = (title("s6", "5 · Sistema hidráulico", "blue")
            + text("s6-u", 200, 230, mark("líquido a presión", "blue", "s6-uh") + " → mueve piezas pesadas", "lbl")
            + text("s6-u2", 520, 520, "superficies · mandos · reversas", "lbl")
            + text("s6-u3", 520, 600, "tren · puertas · escaleras", "lbl")
            + "".join(text(f"s6-t{i}", x, y, n, "sm") for i, ((n, _, _), (x, y)) in enumerate(zip(nodes, pos))))
    js = """
write("#s6-title",T[0]+0.1,0.9); hl("#s6-title-hl",T[0]+1.0);
draw("#s6-loop",T[0]+0.6,1.4); write("#s6-u",T[0]+1.4,1.4); hl("#s6-uh",T[0]+2.6);
tl.fromTo(q(".s6-flow"),{opacity:0,strokeDashoffset:0},{opacity:1,duration:0.4},T[0]+2.0);
tl.fromTo(q(".s6-flow"),{strokeDashoffset:0},{strokeDashoffset:-50*Math.round(D*2),duration:D,ease:"none",immediateRender:false},0);
write("#s6-u2",T[1]+0.8,1.8); write("#s6-u3",T[1]+3.6,1.8);
tl.to(q("#s6-u2, #s6-u3"),{opacity:0,duration:0.3},T[2]-0.2);
const ns=["#s6-n0","#s6-n1","#s6-n2","#s6-n3","#s6-n5","#s6-n4"], ts=["#s6-t0","#s6-t1","#s6-t2","#s6-t3","#s6-t5","#s6-t4"];
tl.set(q(".s6-n"),{opacity:0},0); tl.set(q("#s6-act"),{opacity:0},0);
const at=[1.0,1.8,2.6,3.6,4.8,5.8];
ns.forEach((n,i)=>{ tl.fromTo(q(n),{opacity:0,scale:0.3,transformOrigin:"50% 50%"},{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"},T[2]+at[i]); write(ts[i],T[2]+at[i],0.6); });
show("#s6-act",T[2]+5.8,0.2);
tl.fromTo(q("#s6-act"),{x:0},{x:-50,duration:0.5,yoyo:true,repeat:3,ease:"sine.inOut"},T[2]+6.0);
"""
    return svg, html, js


@scene
def s7():
    svg = f"""<g transform="translate(330,330) scale(1.9)">{PLANE_SIDE}</g>
<g id="s7-ng"><path class="ink" fill="none" stroke-width="6" d="M610,560 L610,640"/><circle class="ink" fill="#fdfdff" stroke-width="6" cx="610" cy="652" r="14"/></g>
<g id="s7-mg"><path class="ink" fill="none" stroke-width="6" d="M1070,545 L1070,640"/><circle class="ink" fill="#fdfdff" stroke-width="6" cx="1070" cy="652" r="14"/></g>
<path class="ink" fill="none" stroke-width="4" d="M200,668 L1760,668" id="s7-ground"/>
<circle id="s7-rat" cx="900" cy="640" r="20" fill="none" stroke="#ff3d96" stroke-width="5"/>
<path id="s7-gpu" class="ln bl" pathLength="1" stroke-width="5" fill="none" d="M450,580 C420,640 360,660 300,700 L240,700 L240,760 L330,760 L330,700"/>
"""
    html = (title("s7", "6 · Tren y electricidad")
            + text("s7-a", 200, 230, mark("Tren triciclo y retráctil", "blue", "s7-ah"), "lbl")
            + text("s7-b", 200, 300, "frenos con " + mark("ABS y antiskid", "pink", "s7-bh"), "lbl")
            + text("s7-e1", 960, 760, "generadores (motores)", "sm") + text("s7-e2", 1500, 440, "APU", "sm")
            + text("s7-e3", 300, 440, "baterías", "sm") + text("s7-e4", 200, 790, "GPU (en tierra)", "sm")
            + text("s7-e5", 820, 830, "RAT (emergencia)", "sm", "color:#ff3d96")
            + text("s7-el", 1100, 230, mark("Electricidad", "blue", "s7-elh"), "lbl"))
    js = """
write("#s7-title",T[0]+0.1,0.9); hl("#s7-title-hl",T[0]+1.0);
tl.set(q("svg > g:first-child .ln"),{strokeDashoffset:0},0);
write("#s7-a",T[0]+0.6,1.4); hl("#s7-ah",T[0]+2.0);
tl.fromTo(q("#s7-ng"),{opacity:0},{opacity:1,duration:0.3},T[0]+3.4); tl.fromTo(q("#s7-mg"),{opacity:0},{opacity:1,duration:0.3},T[0]+4.4);
tl.to(q("#s7-ng"),{rotation:-80,svgOrigin:"610 560",duration:0.9,ease:"power2.inOut"},T[0]+6.0);
tl.to(q("#s7-mg"),{rotation:-80,svgOrigin:"1070 545",duration:0.9,ease:"power2.inOut"},T[0]+6.2);
tl.to(q("#s7-ng, #s7-mg"),{opacity:0,duration:0.3},T[0]+7.0);
tl.set(q("#s7-ng"),{rotation:0,svgOrigin:"610 560"},T[1]-0.2);tl.set(q("#s7-mg"),{rotation:0,svgOrigin:"1070 545"},T[1]-0.2);
tl.to(q("#s7-ng, #s7-mg"),{opacity:1,duration:0.3},T[1]);
write("#s7-b",T[1]+0.4,1.2); hl("#s7-bh",T[1]+1.6);
write("#s7-el",T[2]+0.4,0.8); hl("#s7-elh",T[2]+1.2);
write("#s7-e1",T[2]+2.4,1.0); write("#s7-e2",T[2]+4.3,0.4); write("#s7-e3",T[2]+5.0,0.6);
draw("#s7-gpu",T[2]+5.8,0.8); write("#s7-e4",T[2]+6.0,0.8);
tl.fromTo(q("#s7-rat"),{opacity:0,y:-40},{opacity:1,y:0,duration:0.6,ease:"back.out(2)"},T[2]+7.6); write("#s7-e5",T[2]+7.8,0.9);
"""
    return svg, html, js


def top_up(tx, ty, sc, ident=""):
    i = f' id="{ident}"' if ident else ""
    return f'<g{i} transform="translate({tx},{ty}) rotate(90) scale({sc})">{PLANE_TOP}</g>'


@scene
def s8():
    svg = f"""{top_up(720, 560, 1.0, "s8-pl")}
<path id="s8-tk" fill="rgba(66,188,240,.45)" d="M690,520 L460,640 L460,680 L690,590 Z M750,520 L980,640 L980,680 L750,590 Z"/>
{arrow(560, 650, 600, 580, "bl", 5, 20, "s8-f1")}{arrow(880, 650, 840, 580, "bl", 5, 20, "s8-f2")}
<path class="ln bl" pathLength="1" stroke-width="5" stroke-dasharray="1 1" d="M420,700 C420,800 430,880 440,960 M1020,700 C1020,800 1010,880 1000,960" id="s8-jet"/>
<g id="s8-fire"><path fill="rgba(255,61,150,.75)" d="M1480,700 c-60,-40 -40,-120 10,-170 c-10,50 30,60 40,20 c30,40 40,110 -10,150 Z"/></g>
<g id="s8-ext"><path class="ink" fill="rgba(255,92,168,.25)" stroke-width="5" d="M1600,560 L1660,560 L1660,760 L1600,760 Z M1615,560 L1615,530 L1650,530 L1650,560 M1650,540 L1700,520"/></g>
<g id="s8-foam">{''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="rgba(66,188,240,.55)"/>' for x, y, r in [(1700,520,16),(1660,560,22),(1610,600,26),(1560,640,30),(1510,670,30)])}</g>
"""
    html = (title("s8", "7 · Combustible e incendios", "blue")
            + text("s8-a", 1060, 300, mark("depósitos en las alas", "blue", "s8-ah"), "lbl")
            + text("s8-a2", 1060, 370, "→ a los motores", "sm")
            + text("s8-j", 200, 300, mark("fuel jettison", "pink", "s8-jh"), "lbl")
            + text("s8-j2", 200, 366, "vaciar en vuelo", "sm") + text("s8-j3", 200, 416, "para aterrizar con menos peso", "sm")
            + text("s8-x", 1300, 820, mark("detecta y extingue", "pink", "s8-xh"), "lbl"))
    js = """
write("#s8-title",T[0]+0.1,1.0); hl("#s8-title-hl",T[0]+1.1);
draw("#s8-pl .ln",T[0]+0.3,1.2);
tl.fromTo(q("#s8-tk"),{opacity:0},{opacity:1,duration:0.6},T[0]+2.4);
write("#s8-a",T[0]+2.6,1.1); hl("#s8-ah",T[0]+3.7);
draw("#s8-f1 path, #s8-f2 path",T[0]+4.4,0.5); write("#s8-a2",T[0]+4.6,0.8);
draw("#s8-jet",T[1]+3.4,1.4); write("#s8-j",T[1]+3.6,0.7); hl("#s8-jh",T[1]+4.3); write("#s8-j2",T[1]+1.4,0.8); write("#s8-j3",T[1]+2.2,1.2);
tl.to(q("#s8-tk"),{opacity:0.45,duration:1.4},T[1]+3.6);
tl.fromTo(q("#s8-fire"),{opacity:0,scale:0.4,transformOrigin:"50% 100%"},{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"},T[2]+1.4);
show("#s8-ext",T[2]+2.4,0.3);
tl.fromTo(q("#s8-foam circle"),{opacity:0,scale:0.2,transformOrigin:"50% 50%"},{opacity:1,scale:1,duration:0.3,stagger:0.1},T[2]+3.0);
tl.to(q("#s8-fire"),{opacity:0,scale:0.3,duration:0.6},T[2]+3.4);
write("#s8-x",T[2]+2.8,1.0); hl("#s8-xh",T[2]+3.8);
"""
    return svg, html, js


@scene
def s9():
    # top view nose up, centred (960,560), scale .95: tips at x = 960 -/+ 314, y = 560 + 0.95*(120..170)
    svg = f"""{top_up(960, 560, 0.95, "s9-pl")}
<circle id="s9-bc" cx="960" cy="520" r="16" fill="#e8364f"/>
<circle id="s9-nl" cx="640" cy="690" r="16" fill="#e8364f"/>
<circle id="s9-nr" cx="1280" cy="690" r="16" fill="#138a4f"/>
<circle id="s9-nt" cx="960" cy="886" r="14" fill="#fdfdff" stroke="#23307a" stroke-width="4"/>
<g id="s9-st"><circle cx="640" cy="690" r="40" fill="none" stroke="#c9d0e6" stroke-width="10"/><circle cx="1280" cy="690" r="40" fill="none" stroke="#c9d0e6" stroke-width="10"/></g>
<path id="s9-beam" fill="rgba(255,214,90,.45)" d="M945,250 L905,130 L1015,130 L975,250 Z"/>
"""
    html = (title("s9", "8 · Luces exteriores")
            + text("s9-a", 1240, 300, mark("Beacon", "pink", "s9-ah") + " · roja intermitente", "lbl")
            + text("s9-a2", 1240, 366, "motores en marcha", "sm")
            + text("s9-n1", 260, 640, "roja · izquierda", "sm", "color:#e8364f")
            + text("s9-n2", 1340, 640, "verde · derecha", "sm", "color:#138a4f")
            + text("s9-n3", 1000, 880, "blanca · cola", "sm")
            + text("s9-s", 200, 780, mark("Strobe", "blue", "s9-sh") + " · destellos blancos", "lbl")
            + text("s9-t", 1100, 140, "taxi y aterrizaje", "lbl"))
    js = """
write("#s9-title",T[0]+0.1,0.9); hl("#s9-title-hl",T[0]+1.0);
draw("#s9-pl .ln",T[0]+0.4,1.2);
tl.set(q("#s9-bc, #s9-nl, #s9-nr, #s9-nt, #s9-st, #s9-beam"),{opacity:0},0);
tl.to(q("#s9-bc"),{opacity:1,duration:0.12,yoyo:true,repeat:Math.round((D-T[1]-0.5)/0.5)},T[1]+0.5);
write("#s9-a",T[1]+0.4,1.0); hl("#s9-ah",T[1]+1.4); write("#s9-a2",T[1]+2.6,1.0);
show("#s9-nl",T[2]+1.6,0.2); write("#s9-n1",T[2]+1.6,0.7);
show("#s9-nr",T[2]+3.2,0.2); write("#s9-n2",T[2]+3.2,0.7);
show("#s9-nt",T[2]+4.6,0.2); write("#s9-n3",T[2]+4.6,0.6);
tl.to(q("#s9-st"),{opacity:1,duration:0.06,yoyo:true,repeat:Math.round((D-T[3]-0.8)/0.4)},T[3]+0.8);
write("#s9-s",T[3]+0.4,1.2); hl("#s9-sh",T[3]+1.6);
show("#s9-beam",T[4]+0.8,0.5); write("#s9-t",T[4]+1.0,1.0);
"""
    return svg, html, js


@scene
def s10():
    html = (text("s10-a", 0, 360, "Aire · presión · hielo", "big", "width:1920px;text-align:center")
            + text("s10-b", 0, 520, "hidráulica · electricidad · luces", "big", "width:1920px;text-align:center")
            + text("s10-c", 0, 720, mark("seguro y cómodo", "pink", "s10-ch"), "big", "width:1920px;text-align:center"))
    js = """
write("#s10-a",T[0]+0.1,1.8); write("#s10-b",T[0]+2.0,2.0); write("#s10-c",T[0]+5.6,1.2); hl("#s10-ch",T[0]+6.8,0.5);
"""
    return "", html, js


if __name__ == "__main__":
    build(ROOT, S)
