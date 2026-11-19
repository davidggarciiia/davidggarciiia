import sys, pathlib, math, json
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "lib"))
from nb import *  # noqa

S = {}
def scene(fn):
    S[fn.__name__] = fn
    return fn

ORANGE, RED = "#ff8a2a", "#e8364f"
BLUE_T = "#0a7fb8"
QUIZ = json.loads((ROOT / "build/quiz.json").read_text())
# Anything GSAP moves, rotates or scales is an outer <g id> around an inner <g transform>.


def ln(ident, d, cls="ink", w=4, fill="none", extra=""):
    return f'<path class="ln {cls}" pathLength="1" stroke-width="{w}" fill="{fill}" d="{d}" id="{ident}" {extra}/>'


def waves(y, x0=200, x1=1720, ident="", cls="bl"):
    d = f"M{x0},{y} " + " ".join(f"C{x+30},{y-18} {x+60},{y+18} {x+90},{y}" for x in range(x0, x1, 90))
    return ln(ident, d, cls, 5)


def person(x, y, ident, color="#23307a", s=1.0):
    return (f'<g id="{ident}"><circle cx="{x}" cy="{y}" r="{16*s}" fill="{color}"/>'
            f'<path fill="{color}" d="M{x-22*s},{y+60*s} C{x-22*s},{y+26*s} {x+22*s},{y+26*s} {x+22*s},{y+60*s} Z"/></g>')


def heli():
    return ('<path class="ink" fill="rgba(255,138,42,.35)" stroke-width="5" d="M-120,0 C-120,-60 -60,-80 20,-80 L120,-70 C150,-66 150,-20 120,-10 L60,20 L-80,20 C-110,20 -120,10 -120,0 Z"/>'
            '<path class="ink" fill="none" stroke-width="5" d="M120,-50 L320,-40 L340,-80 L350,-40 L330,-30 M20,-80 L20,-100 M-160,-104 L200,-96 M-80,40 L80,40 M-60,20 L-60,40 M50,20 L50,40"/>'
            '<path fill="rgba(66,188,240,.35)" stroke="#23307a" stroke-width="4" d="M-110,-10 C-110,-50 -70,-66 -20,-66 L-20,-10 Z"/>')


@scene
def s1():
    svg = (waves(820, ident="s1-w1") + waves(880, ident="s1-w2")
           + '<path id="s1-mt" fill="rgba(120,140,110,.35)" stroke="#23307a" stroke-width="5" d="M1240,800 L1420,560 L1520,660 L1600,580 L1720,800 Z"/>'
           + '<path id="s1-dune" fill="rgba(220,170,90,.4)" stroke="#23307a" stroke-width="5" d="M200,800 C300,700 420,700 520,800 Z"/>'
           + f'<g id="s1-pl"><g transform="translate(720,560) rotate(8) scale(0.6)">{PLANE_SIDE}</g></g>')
    html = (text("s1-l1", 220, 300, "mar", "lbl", f"color:{BLUE_T}") + text("s1-l2", 1450, 480, "montaña", "lbl") + text("s1-l3", 260, 640, "desierto", "lbl")
            + text("s1-title", 0, 130, mark("Supervivencia", "blue", "s1-title-hl"), "h1 big", "width:1920px;text-align:center")
            + text("s1-a", 0, 300, "sobrevivir el tiempo necesario hasta el " + mark("rescate", "pink", "s1-ah"), "lbl", "width:1920px;text-align:center"))
    js = """
tl.set(q("#s1-pl .ln"),{strokeDashoffset:0},0); tl.set(q("#s1-mt, #s1-dune"),{opacity:0},0);
draw("#s1-w1, #s1-w2",0,1.2);
tl.fromTo(q("#s1-pl"),{x:-120,y:-60},{x:120,y:120,duration:T[1],ease:"power1.in"},0);
write("#s1-l1",T[0]+2.2,0.4); show("#s1-mt",T[0]+3.2,0.5); write("#s1-l2",T[0]+3.2,0.5); show("#s1-dune",T[0]+4.2,0.5); write("#s1-l3",T[0]+4.2,0.5);
tl.to(q("#s1-l1, #s1-l2, #s1-l3"),{opacity:0,duration:0.3},T[1]);
write("#s1-title",T[1]+0.6,1.2); hl("#s1-title-hl",T[1]+3.4,0.5);
write("#s1-a",T[2]+3.0,2.2); hl("#s1-ah",T[2]+6.6);
"""
    return svg, html, js


@scene
def s2():
    rays = "".join(f'<path class="bl" fill="none" stroke-width="4" d="M{1500+r},{250} A{r},{r} 0 0 1 {1500},{250+r}"/>' for r in (40, 80, 120))
    svg = (f'<g id="s2-h"><g transform="translate(700,400)">{heli()}</g></g>'
           + '<path id="s2-line" class="ink" fill="none" stroke-width="3" d="M700,440 L700,640"/>' + person(700, 650, "s2-p", "#ff3d96", 1.0)
           + waves(780, 200, 1400, "s2-w")
           + f'<g id="s2-rad">{rays}<circle cx="1500" cy="250" r="12" fill="#23307a"/></g>'
           + '<g id="s2-box"><g transform="translate(1180,520)"><rect x="-40" y="0" width="80" height="60" rx="8" fill="rgba(255,138,42,.5)" stroke="#23307a" stroke-width="4"/><path class="ink" fill="none" stroke-width="3" d="M-40,0 L0,-60 L40,0"/></g></g>'
           + '<g id="s2-spk"><path class="ink" fill="rgba(255,92,168,.35)" stroke-width="4" d="M870,330 L900,330 L940,300 L940,420 L900,390 L870,390 Z"/></g>')
    html = (title("s2", "1 · ¿Quién nos rescata?")
            + text("s2-sar", 1060, 110, mark("SAR", "pink", "s2-sarh") + " · búsqueda y salvamento", "lbl")
            + text("s2-g", 760, 560, "grúa", "sm") + text("s2-r", 1560, 320, "radar", "sm") + text("s2-b", 1240, 560, "material lanzable", "sm")
            + text("s2-m", 960, 260, "megafonía", "sm")
            + text("s2-t1", 200, 860, "inicio de la misión: ☀ día " + mark("≤ 30 min", "blue", "s2-t1h") + " · ☾ noche " + mark("≤ 2 h", "pink", "s2-t2h"), "lbl"))
    js = """
write("#s2-title",T[0]+0.1,0.9); hl("#s2-title-hl",T[0]+1.0); write("#s2-sar",T[0]+1.8,1.4); hl("#s2-sarh",T[0]+3.2);
tl.set(q("#s2-line, #s2-p, #s2-rad, #s2-box, #s2-spk"),{opacity:0},0);
draw("#s2-w",T[0]+0.4,1.0);
tl.fromTo(q("#s2-h"),{x:-700,y:-80},{x:0,y:0,duration:2.4,ease:"power2.out"},T[0]+0.4);
tl.to(q("#s2-h"),{y:-10,duration:0.8,yoyo:true,repeat:Math.round((D-T[0]-3)/0.8),ease:"sine.inOut"},T[0]+2.8);
show("#s2-line",T[1]+0.8,0.3); show("#s2-p",T[1]+1.0,0.3); write("#s2-g",T[1]+1.0,0.4);
tl.fromTo(q("#s2-p"),{y:0},{y:-140,duration:2.6,ease:"power1.inOut"},T[1]+2.0);
tl.fromTo(q("#s2-line"),{scaleY:1,transformOrigin:"50% 0%"},{scaleY:0.3,transformOrigin:"50% 0%",duration:2.6,ease:"power1.inOut"},T[1]+2.0);
show("#s2-rad",T[2]+1.0,0.3); write("#s2-r",T[2]+1.0,0.4);
show("#s2-box",T[2]+3.8,0.3); tl.fromTo(q("#s2-box"),{y:-200},{y:0,duration:0.8,ease:"bounce.out"},T[2]+3.8); write("#s2-b",T[2]+4.2,0.8);
show("#s2-spk",T[2]+6.4,0.3); write("#s2-m",T[2]+6.4,0.6);
write("#s2-t1",T[3]+3.0,2.8); hl("#s2-t1h",T[3]+8.4,0.3); hl("#s2-t2h",T[3]+10.4,0.3);
"""
    return svg, html, js


@scene
def s3():
    items = [("Miedo", "pink"), ("Sed", "blue"), ("Frío", "blue"), ("Hambre", "pink")]
    svg = "".join(f'<rect class="s3-st" id="s3-s{i}" x="{300+i*330}" y="{720-(4-i)*90}" width="300" height="{(4-i)*90}" fill="{"rgba(255,92,168,.35)" if c=="pink" else "rgba(66,188,240,.35)"}" stroke="#23307a" stroke-width="4"/>' for i, (_, c) in enumerate(items))
    html = (title("s3", "2 · Cuatro agresiones", "blue")
            + "".join(text(f"s3-t{i}", 300 + i * 330, 720 - (4 - i) * 90 - 80, f"{i+1}. {n}", "lbl", "width:300px;text-align:center") for i, (n, _) in enumerate(items))
            + text("s3-m", 1060, 230, "bloquea · malas decisiones · se contagia", "sm")
            + text("s3-o", 1060, 290, "por orden de importancia", "sm")
            + text("s3-k", 200, 800, "herramientas: " + mark("sentido común", "blue", "s3-k1") + " + " + mark("capacidad de valorar", "pink", "s3-k2"), "lbl"))
    js = """
write("#s3-title",T[0]+0.1,0.9); hl("#s3-title-hl",T[0]+1.0);
const bar=(i,t)=>{tl.fromTo(q("#s3-s"+i),{scaleY:0,transformOrigin:"50% 100%"},{scaleY:1,duration:0.5,ease:"power2.out"},t); write("#s3-t"+i,t+0.2,0.5);};
bar(0,T[1]+0.6); write("#s3-m",T[1]+2.4,2.4);
bar(1,T[2]+0.6); bar(2,T[2]+1.4); bar(3,T[2]+2.2); write("#s3-o",T[2]+2.6,0.8);
write("#s3-k",T[3]+3.4,2.4); hl("#s3-k1",T[3]+5.2,0.3); hl("#s3-k2",T[3]+6.6,0.3);
"""
    return svg, html, js


@scene
def s4():
    Y = lambda c: 860 - (c - 28) * 30
    svg = (ln("s4-th", f"M240,{Y(46)} L240,{Y(28)} M280,{Y(46)} L280,{Y(28)} M240,{Y(46)} Q260,{Y(46)-30} 280,{Y(46)}", "ink", 5)
           + f'<rect id="s4-hot" x="244" y="{Y(46)}" width="32" height="{Y(42)-Y(46)}" fill="rgba(232,54,79,.5)"/>'
           + f'<rect id="s4-cold" x="244" y="{Y(32)}" width="32" height="{Y(28)-Y(32)}" fill="rgba(66,188,240,.6)"/>'
           + f'<path id="s4-37" class="pk" fill="none" stroke-width="6" d="M220,{Y(37)} L300,{Y(37)}"/>'
           + person(1000, 470, "s4-body", "#23307a", 3.2)
           + arrow(1060, 520, 1300, 420, "bl", 6, 26, "s4-o1") + arrow(1080, 600, 1300, 600, "bl", 6, 26, "s4-o2") + arrow(1060, 680, 1300, 780, "bl", 6, 26, "s4-o3")
           + arrow(700, 420, 920, 520, "pk", 6, 26, "s4-i1") + arrow(700, 600, 920, 600, "pk", 6, 26, "s4-i2") + arrow(700, 780, 920, 680, "pk", 6, 26, "s4-i3"))
    html = (title("s4", "3 · El frío")
            + text("s4-37t", 320, Y(37) - 36, "37 °C", "lbl", "color:#ff3d96")
            + text("s4-42", 320, Y(42) - 40, "42 °C", "sm", f"color:{RED}") + text("s4-32", 320, Y(32) - 30, "32 °C", "sm", f"color:{BLUE_T}")
            + text("s4-p", 1320, 260, mark("Pierdes calor", "blue", "s4-ph"), "lbl")
            + text("s4-p1", 1320, 390, "respiración", "sm") + text("s4-p2", 1320, 570, "ambiente (viento, agua)", "sm") + text("s4-p3", 1320, 750, "sudor que se evapora", "sm")
            + text("s4-g", 600, 260, mark("Ganas calor", "pink", "s4-gh"), "lbl", "width:400px")
            + text("s4-g1", 600, 330, "actividad muscular", "sm") + text("s4-g2", 600, 540, "refugio · sol", "sm") + text("s4-g3", 600, 830, "ropa, bebida y comida calientes", "sm")
            + text("s4-k", 1100, 900, mark("seco · abrigado · sin viento", "blue", "s4-kh"), "lbl"))
    js = """
write("#s4-title",T[0]+0.1,0.6); hl("#s4-title-hl",T[0]+0.7);
draw("#s4-th",T[0]+0.6,0.8); tl.set(q("#s4-hot, #s4-cold, #s4-37, #s4-body"),{opacity:0},0);
show("#s4-37",T[0]+2.6,0.2); write("#s4-37t",T[0]+2.6,0.5);
show("#s4-hot",T[1]+1.4,0.3); write("#s4-42",T[1]+1.4,0.4); show("#s4-cold",T[1]+3.0,0.3); write("#s4-32",T[1]+3.0,0.4);
show("#s4-body",T[2]+0.1,0.4); write("#s4-p",T[2]+0.2,0.7); hl("#s4-ph",T[2]+0.9);
draw("#s4-o1 path",T[2]+1.8,0.4); write("#s4-p1",T[2]+1.9,0.6); draw("#s4-o2 path",T[2]+3.2,0.4); write("#s4-p2",T[2]+3.3,0.8);
draw("#s4-o3 path",T[2]+5.4,0.4); write("#s4-p3",T[2]+5.5,0.9);
write("#s4-g",T[3]+0.2,0.7); hl("#s4-gh",T[3]+0.9);
draw("#s4-i1 path",T[3]+1.2,0.4); write("#s4-g1",T[3]+1.3,0.8); draw("#s4-i2 path",T[3]+2.6,0.4); write("#s4-g2",T[3]+2.7,0.6);
draw("#s4-i3 path",T[3]+4.4,0.4); write("#s4-g3",T[3]+4.5,1.2);
write("#s4-k",T[4]+0.6,1.4); hl("#s4-kh",T[4]+2.0);
"""
    return svg, html, js


@scene
def s5():
    drop = "M400,300 C340,400 320,450 320,490 C320,540 360,570 400,570 C440,570 480,540 480,490 C480,450 460,400 400,300 Z"
    svg = (ln("s5-drop", drop, "bl", 6, "rgba(66,188,240,.35)")
           + '<path id="s5-dune" fill="rgba(220,170,90,.4)" stroke="#23307a" stroke-width="5" d="M640,760 C760,620 900,620 1020,760 Z"/>'
           + ln("s5-pit", "M1060,760 C1080,820 1160,820 1180,760", "ink", 5)
           + '<g id="s5-raft"><ellipse cx="1500" cy="440" rx="170" ry="60" fill="rgba(255,138,42,.4)" stroke="#23307a" stroke-width="5"/>'
           + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="rgba(66,188,240,.8)"/>' for x, y in [(1420, 430), (1470, 445), (1530, 425), (1580, 440), (1500, 455)]) + '</g>'
           + '<g id="s5-pot"><path class="ink" fill="rgba(200,205,225,.6)" stroke-width="5" d="M1300,700 L1420,700 L1410,780 L1310,780 Z"/>'
           + '<path fill="rgba(255,92,168,.6)" d="M1320,810 c10,-20 20,-20 20,-30 c10,10 20,20 10,30 Z M1380,810 c10,-20 20,-20 20,-30 c10,10 20,20 10,30 Z"/>'
           + '<path class="s5-steam" fill="none" stroke="#9aa0b8" stroke-width="4" d="M1340,680 c10,-20 -10,-30 0,-50 M1380,680 c10,-20 -10,-30 0,-50"/></g>')
    html = (title("s5", "4 · La sed", "blue")
            + text("s5-a", 540, 300, "sin agua: " + mark("3 a 5 días", "blue", "s5-ah"), "lbl")
            + text("s5-r", 540, 380, "retener líquidos:", "lbl") + text("s5-r2", 560, 450, "sin ejercicio · sin fumar", "sm") + text("s5-r3", 560, 500, "a la sombra · sin alcohol", "sm")
            + text("s5-d", 640, 780, "pie de las dunas", "sm") + text("s5-p", 1040, 830, "cavar un pozo", "sm")
            + text("s5-m", 1340, 520, "en el mar: " + mark("rocío", "pink", "s5-mh"), "lbl")
            + text("s5-f", 1290, 840, "filtrar y hervir · pastillas", "sm"))
    js = """
write("#s5-title",T[0]+0.1,0.6); hl("#s5-title-hl",T[0]+0.7);
draw("#s5-drop",T[0]+0.6,1.0); write("#s5-a",T[0]+4.6,1.2); hl("#s5-ah",T[0]+5.8);
write("#s5-r",T[1]+0.3,0.8); write("#s5-r2",T[1]+1.6,2.0); write("#s5-r3",T[1]+3.8,2.0);
tl.set(q("#s5-dune, #s5-pot, #s5-raft"),{opacity:0},0);
show("#s5-dune",T[2]+4.4,0.4); write("#s5-d",T[2]+4.4,0.8); draw("#s5-pit",T[2]+6.6,0.5); write("#s5-p",T[2]+6.6,0.7);
show("#s5-raft",T[3]+0.6,0.4); write("#s5-m",T[3]+0.8,0.8); hl("#s5-mh",T[3]+3.4,0.3);
show("#s5-pot",T[4]+0.4,0.4); write("#s5-f",T[4]+1.0,2.0);
tl.fromTo(q(".s5-steam"),{y:0,opacity:0.9},{y:-20,opacity:0.2,duration:0.8,repeat:Math.max(1,Math.round((D-T[4]-1)/0.8)),ease:"none"},T[4]+1.0);
"""
    return svg, html, js


@scene
def s6():
    svg = ('<g id="s6-plate"><ellipse cx="560" cy="560" rx="200" ry="60" fill="#fdfdff" stroke="#23307a" stroke-width="6"/><ellipse cx="560" cy="550" rx="120" ry="30" fill="none" stroke="#23307a" stroke-width="4"/></g>'
           + '<path id="s6-x" fill="none" stroke="#e8364f" stroke-width="12" stroke-linecap="round" d="M1300,480 L1520,700 M1520,480 L1300,700"/>'
           + '<g id="s6-cal"><rect x="1280" y="460" width="260" height="260" rx="16" fill="rgba(255,92,168,.12)" stroke="#23307a" stroke-width="5"/></g>')
    html = (title("s6", "5 · El hambre")
            + text("s6-a", 200, 250, "el 1.er día es el más duro · necesidad " + mark("psicológica", "blue", "s6-ah"), "lbl")
            + text("s6-b", 300, 680, "solo con agua:", "lbl") + text("s6-b2", 300, 750, mark("≈ 10 días o algo más", "pink", "s6-b2h"), "lbl")
            + text("s6-b3", 300, 820, "según la voluntad de vivir", "sm")
            + text("s6-c", 1180, 760, "sin agua → " + mark("no comer", "pink", "s6-ch"), "lbl") + text("s6-c2", 1180, 830, "la digestión gasta agua", "sm"))
    js = """
write("#s6-title",T[0]+0.1,0.7); hl("#s6-title-hl",T[0]+0.8);
tl.set(q("#s6-plate, #s6-x, #s6-cal"),{opacity:0},0);
show("#s6-plate",T[0]+0.6,0.4); write("#s6-a",T[0]+2.4,2.6); hl("#s6-ah",T[0]+6.0);
write("#s6-b",T[1]+0.4,0.8); write("#s6-b2",T[1]+2.6,1.2); hl("#s6-b2h",T[1]+3.8); write("#s6-b3",T[1]+5.0,1.0);
show("#s6-cal",T[2]+0.6,0.3); show("#s6-x",T[2]+2.0,0.2); write("#s6-c",T[2]+2.0,1.0); hl("#s6-ch",T[2]+3.0); write("#s6-c2",T[2]+4.4,1.0);
"""
    return svg, html, js


@scene
def s7():
    svg = ('<g id="s7-fl"><rect x="320" y="440" width="70" height="260" rx="12" fill="rgba(255,138,42,.45)" stroke="#23307a" stroke-width="5"/>'
           '<path fill="rgba(255,92,168,.75)" d="M355,440 c-30,-40 -10,-90 10,-120 c0,40 30,50 20,90 Z"/></g>'
           f'<g id="s7-elt"><rect x="820" y="480" width="200" height="200" rx="14" fill="{ORANGE}" stroke="#23307a" stroke-width="5"/>'
           '<path class="ink" fill="none" stroke-width="6" d="M920,480 L920,360"/><path class="bl" fill="none" stroke-width="4" d="M950,380 A40,40 0 0 1 950,440 M970,360 A70,70 0 0 1 970,460"/></g>'
           '<g id="s7-vest"><path fill="rgba(255,214,90,.8)" stroke="#23307a" stroke-width="5" d="M1330,400 C1330,500 1380,560 1380,700 L1460,700 C1460,600 1480,520 1520,470 C1560,520 1580,600 1580,700 L1660,700 C1660,560 1710,500 1710,400 C1640,380 1580,440 1520,440 C1460,440 1400,380 1330,400 Z"/></g>')
    html = (title("s7", "6 · Equipos de supervivencia", "blue")
            + text("s7-c", 200, 250, "zonas de " + mark("rescate difícil", "pink", "s7-ch") + " → el avión debe llevar:", "lbl")
            + text("s7-a", 220, 760, "señales pirotécnicas", "lbl") + text("s7-b", 760, 760, mark("ELT", "blue", "s7-bh") + " (mín. 1)", "lbl")
            + text("s7-b2", 760, 830, "transmisor de emergencia", "sm") + text("s7-d", 1300, 760, "supervivencia y flotación", "lbl") + text("s7-d2", 1300, 830, "según nº de pasajeros", "sm"))
    js = """
write("#s7-title",T[0]+0.1,1.0); hl("#s7-title-hl",T[0]+1.1);
write("#s7-c",T[1]+0.4,2.6); hl("#s7-ch",T[1]+3.6);
tl.set(q("#s7-fl, #s7-elt, #s7-vest"),{opacity:0},0);
show("#s7-fl",T[1]+6.0,0.4); write("#s7-a",T[1]+6.1,1.0);
show("#s7-elt",T[2]+0.2,0.4); write("#s7-b",T[2]+0.3,0.6); hl("#s7-bh",T[2]+0.9); write("#s7-b2",T[2]+1.8,1.0);
show("#s7-vest",T[2]+4.0,0.4); write("#s7-d",T[2]+4.1,1.0); write("#s7-d2",T[2]+6.0,1.0);
"""
    return svg, html, js


@scene
def s8():
    vest = "M0,0 C0,100 50,160 50,300 L130,300 C130,200 150,120 190,70 C230,120 250,200 250,300 L330,300 C330,160 380,100 380,0 C310,-20 250,40 190,40 C130,40 70,-20 0,0 Z"
    svg = (f'<g id="s8-v"><g transform="translate(260,380) scale(0.9)"><path fill="rgba(255,214,90,.8)" stroke="#23307a" stroke-width="5" d="{vest}"/></g></g>'
           + waves(320, 900, 1720, "s8-sea") + ln("s8-coast", "M900,380 L1100,380 L1100,280", "ink", 5)
           + arrow(1110, 360, 1700, 360, "pk", 5, 24, "s8-nm1") + arrow(1700, 360, 1110, 360, "pk", 5, 24, "s8-nm2")
           + '<path id="s8-x" fill="none" stroke="#e8364f" stroke-width="12" stroke-linecap="round" d="M310,400 L560,640 M560,400 L310,640"/>')
    html = (title("s8", "7 · Chalecos salvavidas", "blue")
            + text("s8-a", 1180, 400, "+ 50 NM de la costa", "lbl") + text("s8-a2", 1000, 470, "o despegue / aterrizaje sobre el agua", "sm")
            + text("s8-b", 700, 580, "bajo el asiento · " + mark("+10 %", "blue", "s8-bh"), "lbl")
            + text("s8-b2", 700, 650, "infant life vest (bebés)", "sm")
            + text("s8-c", 200, 760, mark("NUNCA", "pink", "s8-ch") + " inflar dentro del avión", "lbl", "font-size:64px")
            + text("s8-c1", 220, 840, "si entra agua, te empuja al techo", "sm")
            + text("s8-c2", 220, 840, "excepto: niños · ancianos · PMR · miedo al agua", "sm")
            + text("s8-k", 220, 910, "prevuelo: uno por asiento · adicionales · infant: " + mark("10 % de los asientos certificados", "pink", "s8-kh"), "sm"))
    js = """
write("#s8-title",T[0]+0.1,0.9); hl("#s8-title-hl",T[0]+1.0);
tl.set(q("#s8-v, #s8-x, #s8-c2"),{opacity:0},0);
show("#s8-v",T[0]+0.6,0.5);
draw("#s8-coast",T[0]+2.6,0.5); draw("#s8-sea",T[0]+3.0,1.0); draw("#s8-nm1 path, #s8-nm2 path",T[0]+4.6,0.6); write("#s8-a",T[0]+5.0,0.9);
write("#s8-a2",T[1]+0.6,2.4);
write("#s8-b",T[2]+1.4,1.4); hl("#s8-bh",T[2]+4.8); write("#s8-b2",T[2]+7.4,1.4);
tl.to(q("#s8-x"),{opacity:1,duration:0.2},T[3]+1.4); write("#s8-c",T[3]+1.0,1.2); hl("#s8-ch",T[3]+2.2,0.3); write("#s8-c1",T[3]+4.2,1.6);
tl.to(q("#s8-c1"),{opacity:0,duration:0.2},T[4]); tl.set(q("#s8-c2"),{opacity:1},T[4]); write("#s8-c2",T[4]+0.4,3.0);
write("#s8-k",T[5]+0.6,5.4); hl("#s8-kh",T[5]+8.4,0.4);
"""
    return svg, html, js


@scene
def s9():
    cx, cy = 760, 600
    loops = "".join(f'<path fill="none" stroke="#1ea7e4" stroke-width="4" d="M{cx + 270*math.cos(a):.0f},{cy + 200*math.sin(a):.0f} Q{cx + 320*math.cos(a+0.2):.0f},{cy + 245*math.sin(a+0.2):.0f} {cx + 270*math.cos(a+0.4):.0f},{cy + 200*math.sin(a+0.4):.0f}"/>' for a in [k*math.pi/4 for k in range(8)])
    svg = (f'<ellipse id="s9-c1" cx="{cx}" cy="{cy}" rx="270" ry="200" fill="rgba(255,138,42,.35)" stroke="#23307a" stroke-width="6"/>'
           + f'<ellipse id="s9-c2" cx="{cx}" cy="{cy}" rx="210" ry="145" fill="rgba(255,214,90,.35)" stroke="#23307a" stroke-width="6"/>'
           + f'<g id="s9-lps">{loops}</g>'
           + f'<g id="s9-st"><path class="ink" fill="none" stroke-width="6" d="M{cx-300},{cy-20} L{cx-260},{cy-20} M{cx-300},{cy+20} L{cx-260},{cy+20} M{cx-300},{cy-30} L{cx-300},{cy+30}"/>'
           + f'<path class="ink" fill="none" stroke-width="6" d="M{cx+300},{cy-20} L{cx+260},{cy-20} M{cx+300},{cy+20} L{cx+260},{cy+20} M{cx+300},{cy-30} L{cx+300},{cy+30}"/></g>'
           + ln("s9-moor", f"M{cx},{cy-200} C{cx+40},{cy-300} {cx+160},{cy-320} {cx+300},{cy-330}", "ink", 4)
           + ln("s9-anc", f"M{cx+250},{cy+120} C{cx+330},{cy+200} {cx+380},{cy+260} {cx+420},{cy+300}", "ink", 4)
           + f'<path id="s9-ank" class="ink" fill="none" stroke-width="5" d="M{cx+420},{cy+290} L{cx+420},{cy+350} M{cx+395},{cy+330} Q{cx+420},{cy+360} {cx+445},{cy+330}"/>'
           + f'<circle id="s9-heav" cx="{cx-380}" cy="{cy-230}" r="34" fill="none" stroke="#ff3d96" stroke-width="7"/>' + ln("s9-hl", f"M{cx-350},{cy-210} C{cx-300},{cy-180} {cx-260},{cy-160} {cx-200},{cy-150}", "pk", 4))
    html = (title("s9", "8 · Balsas salvavidas")
            + text("s9-r", 1100, 220, "+120 min sobre el agua o +400 NM", "lbl") + text("s9-r2", 1100, 290, mark("plazas para todos", "blue", "s9-rh"), "lbl")
            + text("s9-l1", 1260, 410, "2 cámaras de aire · si una falla, flota", "sm") + text("s9-l2", 1260, 460, "cuerda de amarre (mooring line)", "sm")
            + text("s9-l3", 1260, 510, "líneas de salvamento", "sm") + text("s9-l4", 1260, 560, "cuerda de rescate (heaving line)", "sm")
            + text("s9-l5", 1260, 610, "ancla · reduce la deriva", "sm") + text("s9-l6", 1260, 660, "2 estaciones de abordaje", "sm")
            + text("s9-l7", 1260, 740, mark("+ kit de supervivencia", "pink", "s9-l7h"), "lbl"))
    js = """
write("#s9-title",T[0]+0.1,0.9); hl("#s9-title-hl",T[0]+1.0);
tl.set(q("#s9-c1, #s9-c2, #s9-lps, #s9-st, #s9-ank, #s9-heav"),{opacity:0},0);
show("#s9-c1",T[0]+0.6,0.4); show("#s9-c2",T[0]+1.0,0.4);
write("#s9-r",T[0]+2.6,3.0); write("#s9-r2",T[0]+10.0,1.0); hl("#s9-rh",T[0]+11.0);
write("#s9-l1",T[1]+0.6,1.2); tl.fromTo(q("#s9-c1, #s9-c2"),{scale:1,transformOrigin:"50% 50%"},{scale:1.04,transformOrigin:"50% 50%",duration:0.3,yoyo:true,repeat:1},T[1]+0.8);
write("#s9-l2",T[1]+5.0,1.0); draw("#s9-moor",T[1]+5.0,0.8);
write("#s9-l3",T[2]+0.4,0.8); show("#s9-lps",T[2]+0.4,0.4);
write("#s9-l4",T[2]+3.6,1.0); show("#s9-heav",T[2]+3.6,0.3); draw("#s9-hl",T[2]+3.8,0.5);
write("#s9-l5",T[3]+0.6,0.8); draw("#s9-anc",T[3]+0.6,0.5); show("#s9-ank",T[3]+1.0,0.3);
write("#s9-l6",T[3]+3.4,0.9); show("#s9-st",T[3]+3.4,0.3);
write("#s9-l7",T[3]+5.8,0.8); hl("#s9-l7h",T[3]+6.6);
"""
    return svg, html, js


@scene
def s10():
    sw = "".join(f'<text x="{x}" y="736" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="44" fill="#23307a">{t}</text>' for x, t in [(520, "OFF"), (660, "ARM"), (800, "ON")])
    svg = (f'<rect id="s10-box" x="400" y="320" width="520" height="460" rx="24" fill="{ORANGE}" stroke="#23307a" stroke-width="6"/>'
           + '<rect x="440" y="360" width="440" height="120" rx="10" fill="rgba(255,255,255,.85)" stroke="#23307a" stroke-width="4"/>'
           + '<text x="660" y="440" text-anchor="middle" font-family="Caveat" font-weight="700" font-size="64" fill="#23307a">KANNAD 406</text>'
           + ln("s10-track", "M520,660 L800,660", "ink", 8)
           + sw + '<g id="s10-knob"><circle cx="520" cy="660" r="26" fill="#fdfdff" stroke="#23307a" stroke-width="6"/></g>'
           + f'<circle id="s10-led" cx="820" cy="560" r="22" fill="{RED}" stroke="#23307a" stroke-width="4"/>'
           + '<g id="s10-buzz"><path class="bl" fill="none" stroke-width="5" d="M940,520 q20,40 0,80 M970,500 q30,60 0,120 M1000,480 q40,80 0,160"/></g>')
    html = (title("s10", "9 · Radiobaliza Kannad 406", "blue")
            + text("s10-a", 1080, 280, "batería seca · " + mark("no necesita agua", "blue", "s10-ah"), "lbl")
            + text("s10-f1", 1080, 380, "continua: 121,5 / 243 MHz", "lbl") + text("s10-f1b", 1100, 445, "civil / militar", "sm")
            + text("s10-f2", 1080, 500, "discontinua: 406 MHz (satélite)", "lbl")
            + text("s10-s", 1080, 600, "OFF apagada · ARM con agua · ON encendida", "sm")
            + text("s10-z", 1080, 660, "activada: " + mark("luz roja + señal acústica", "pink", "s10-zh"), "sm")
            + text("s10-c", 200, 840, "prevuelo: presencia y anclaje · precinto y plomo intactos · " + mark("nunca sacarla de su sitio", "pink", "s10-ch"), "sm"))
    js = """
write("#s10-title",T[0]+0.1,1.0); hl("#s10-title-hl",T[0]+1.1);
tl.set(q("#s10-led, #s10-buzz"),{opacity:0},0);
write("#s10-a",T[1]+3.4,1.6); hl("#s10-ah",T[1]+5.6);
write("#s10-f1",T[2]+0.6,1.8); write("#s10-f1b",T[2]+3.6,0.9); write("#s10-f2",T[2]+7.0,1.6);
write("#s10-s",T[3]+1.2,5.6);
tl.to(q("#s10-knob"),{x:140,duration:0.5,ease:"power2.inOut"},T[3]+2.4);
tl.to(q("#s10-knob"),{x:280,duration:0.5,ease:"power2.inOut"},T[3]+6.4);
tl.to(q("#s10-led"),{opacity:1,duration:0.1,yoyo:true,repeat:Math.round((D-T[4]-0.4)/0.4)},T[4]+0.4);
tl.to(q("#s10-buzz"),{opacity:1,duration:0.15,yoyo:true,repeat:Math.round((D-T[4]-0.4)/0.3)},T[4]+0.4);
write("#s10-z",T[4]+0.2,1.4); hl("#s10-zh",T[4]+1.6);
write("#s10-c",T[5]+0.6,5.0); hl("#s10-ch",T[5]+6.6,0.4);
"""
    return svg, html, js


@scene
def s11():
    svg = (waves(700, 200, 1000, "s11-sea")
           + f'<g id="s11-bc"><g transform="translate(560,560)"><rect x="-50" y="-40" width="100" height="220" rx="20" fill="{ORANGE}" stroke="#23307a" stroke-width="5"/></g>'
           + '<g id="s11-ant"><path class="ink" fill="none" stroke-width="6" d="M560,520 L560,520"/></g></g>'
           + '<path id="s11-x" fill="none" stroke="#e8364f" stroke-width="10" stroke-linecap="round" d="M1300,560 L1440,700 M1440,560 L1300,700"/>'
           + f'<g id="s11-hz"><g transform="translate(1370,640)"><rect x="-110" y="-35" width="220" height="70" rx="20" fill="{ORANGE}" stroke="#23307a" stroke-width="5"/></g></g>')
    html = (title("s11", "10 · Radiobaliza Honeywell")
            + text("s11-a", 200, 250, "cabina de pasajeros · junto a una balsa o rampa · " + mark("tierra y agua", "blue", "s11-ah"), "lbl")
            + text("s11-f", 1060, 330, "121,5 / 243 MHz · ≈ 50 h", "lbl") + text("s11-f2", 1060, 400, "406 MHz · 24 h", "lbl")
            + text("s11-b", 700, 470, "electrolito + agua → se activa", "sm") + text("s11-b2", 700, 520, "antena autoeréctil", "sm")
            + text("s11-h", 1180, 760, "en horizontal deja de emitir", "sm", f"color:{RED}")
            + text("s11-c", 200, 840, "prevuelo: presencia y anclaje · antena asegurada · " + mark("bolsa de sal", "pink", "s11-ch") + " en buen estado", "sm")
            + text("s11-l", 200, 910, "se lanza al agua: " + mark("lo antes posible", "blue", "s11-lh"), "lbl"))
    js = """
write("#s11-title",T[0]+0.1,1.0); hl("#s11-title-hl",T[0]+1.1);
write("#s11-a",T[0]+1.6,4.0); hl("#s11-ah",T[0]+6.6);
write("#s11-f",T[1]+2.4,1.6); write("#s11-f2",T[1]+7.4,1.2);
tl.set(q("#s11-x, #s11-hz"),{opacity:0},0); draw("#s11-sea",T[2],0.8);
tl.fromTo(q("#s11-bc"),{y:-300},{y:0,duration:0.8,ease:"bounce.out"},T[2]+0.4);
tl.to(q("#s11-ant path"),{attr:{d:"M560,520 L560,300"},duration:0.8,ease:"power2.out"},T[2]+3.4);
write("#s11-b",T[2]+0.8,1.4); write("#s11-b2",T[2]+3.4,1.0);
show("#s11-hz",T[2]+6.0,0.3); show("#s11-x",T[2]+6.8,0.2); write("#s11-h",T[2]+6.8,1.2);
write("#s11-c",T[3]+0.4,4.4); hl("#s11-ch",T[3]+4.6,0.3);
write("#s11-l",T[4]+0.3,1.0); hl("#s11-lh",T[4]+1.6);
"""
    return svg, html, js


@scene
def s12():
    items = ["agua embolsada", "tabletas de glucosa", "bengala de mano", "lanzador de bengalas", "código morse", "pastillas potabilizadoras",
             "heliógrafo", "silbato", "navaja", "manual de supervivencia", "botiquín de primeros auxilios"]
    svg = ('<g id="s12-bag"><path fill="rgba(255,138,42,.4)" stroke="#23307a" stroke-width="6" d="M200,520 L560,520 L600,900 L160,900 Z"/>'
           '<path class="ink" fill="none" stroke-width="6" d="M300,520 C300,440 460,440 460,520"/></g>'
           + "".join(person(220 + i * 60, 300, f"s12-p{i}", "#23307a", 0.8) for i in range(4)))
    html = (title("s12", "11 · Kit de supervivencia", "blue")
            + text("s12-a", 480, 300, "cada 4 ocupantes: " + mark("100 g de glucosa", "pink", "s12-a1") + " + " + mark("500 ml de agua", "blue", "s12-a2"), "lbl")
            + "".join(text(f"s12-i{i}", 700 + (i // 6) * 560, 450 + (i % 6) * 72, "· " + n, "lbl", "font-size:48px") for i, n in enumerate(items)))
    js = """
write("#s12-title",T[0]+0.1,1.0); hl("#s12-title-hl",T[0]+1.1);
tl.fromTo(q("[id^=s12-p]"),{opacity:0},{opacity:1,duration:0.2,stagger:0.15},T[0]+1.4);
write("#s12-a",T[0]+1.8,2.6); hl("#s12-a1",T[0]+3.6,0.3); hl("#s12-a2",T[0]+5.2,0.3);
tl.fromTo(q("#s12-bag"),{opacity:0,y:40},{opacity:1,y:0,duration:0.5},T[1]);
const n=11, span=13.6;
for(let i=0;i<n;i++){ write("#s12-i"+i,T[1]+1.4+span*i/n,0.5); }
tl.to(q("#s12-i0, #s12-i1, #s12-i5"),{color:"#0a7fb8",duration:0.3},T[2]+1.6);
tl.to(q("#s12-i6, #s12-i7, #s12-i2, #s12-i3"),{color:"#ff3d96",duration:0.3},T[2]+5.4);
"""
    return svg, html, js


@scene
def s13():
    svg = ('<g id="s13-mir"><rect x="260" y="380" width="200" height="200" rx="10" fill="rgba(200,215,240,.8)" stroke="#23307a" stroke-width="6"/><circle cx="360" cy="480" r="16" fill="#fdfdff" stroke="#23307a" stroke-width="4"/></g>'
           + ln("s13-ray", "M120,300 L360,480 L860,250", "pk", 5, extra='stroke-dasharray="1 1"')
           + f'<g id="s13-pl"><g transform="translate(860,200) scale(0.4)">{PLANE_SIDE}</g></g>'
           + '<path id="s13-dye" fill="rgba(60,220,120,.45)" d="M1000,560 C1060,500 1200,520 1240,580 C1280,640 1180,690 1090,670 C1010,650 960,610 1000,560 Z"/>'
           + waves(620, 960, 1300, "s13-sea")
           + '<rect id="s13-pan" x="1400" y="480" width="260" height="140" fill="rgba(255,92,168,.5)" stroke="#23307a" stroke-width="4"/>')
    html = (title("s13", "12 · Señales visuales")
            + text("s13-m", 200, 620, mark("Espejo", "blue", "s13-mh") + " 10 × 10 cm", "lbl") + text("s13-m1", 200, 690, "mirar por el agujero y apuntar", "sm")
            + text("s13-m2", 200, 750, mark("destello hasta 32 km", "pink", "s13-m2h"), "sm")
            + text("s13-d", 960, 700, "fluoresceína", "lbl") + text("s13-d2", 960, 760, "tiñe el agua", "sm")
            + text("s13-p", 1400, 640, "paineles", "lbl") + text("s13-p2", 1400, 700, "mín. 2,20 m", "sm"))
    js = """
write("#s13-title",T[0]+0.1,0.9); hl("#s13-title-hl",T[0]+1.0);
tl.set(q("#s13-mir, #s13-pl, #s13-dye, #s13-pan"),{opacity:0},0); tl.set(q("#s13-pl .ln"),{strokeDashoffset:0},0);
show("#s13-mir",T[1]+0.3,0.3); write("#s13-m",T[1]+0.4,1.0); hl("#s13-mh",T[1]+1.4);
write("#s13-m1",T[1]+4.0,1.4); show("#s13-pl",T[1]+6.6,0.3); draw("#s13-ray",T[1]+7.4,0.8);
tl.to(q("#s13-ray"),{opacity:0.3,duration:0.1,yoyo:true,repeat:9},T[1]+9.0);
write("#s13-m2",T[2]+0.3,1.0); hl("#s13-m2h",T[2]+1.4,0.3);
draw("#s13-sea",T[3]+0.2,0.6); tl.fromTo(q("#s13-dye"),{opacity:0,scale:0.3,transformOrigin:"50% 50%"},{opacity:1,scale:1,duration:1.4},T[3]+1.6);
write("#s13-d",T[3]+0.4,0.8); write("#s13-d2",T[3]+3.0,0.8);
show("#s13-pan",T[4]+0.4,0.4); write("#s13-p",T[4]+0.4,0.6); write("#s13-p2",T[4]+6.2,0.8);
"""
    return svg, html, js


@scene
def s14():
    syms = [("V", "necesitamos ayuda"), ("X", "ayuda médica"), ("N", "no"), ("Y", "sí"), ("↑", "avanzamos en esta dirección")]
    dots = lambda x0: "".join(f'<circle class="s14-dt" cx="{x0+i*60}" cy="380" r="16" fill="#23307a"/>' for i in range(3))
    dashes = "".join(f'<rect class="s14-dt" x="{620+i*110}" y="368" width="80" height="24" rx="12" fill="#ff3d96"/>' for i in range(3))
    svg = dots(400) + dashes + dots(1000)
    html = (title("s14", "13 · SOS y códigos", "blue")
            + text("s14-a", 360, 450, "S", "big", "width:180px;text-align:center") + text("s14-b", 640, 450, "O", "big", "width:280px;text-align:center")
            + text("s14-c", 960, 450, "S", "big", "width:180px;text-align:center")
            + text("s14-l", 1260, 330, "linterna: 3 cortos ·", "sm") + text("s14-l2", 1260, 380, "3 largos · 3 cortos", "sm")
            + "".join(text(f"s14-s{i}", 200 + i * 320, 700, f'<span style="font-size:110px;color:#ff3d96">{s}</span><br>{m}', "lbl", "width:300px;white-space:normal;line-height:1.0;text-align:center") for i, (s, m) in enumerate(syms)))
    js = """
write("#s14-title",T[0]+0.1,0.9); hl("#s14-title-hl",T[0]+1.0);
tl.set(q(".s14-dt"),{opacity:0},0);
const dt=q(".s14-dt"); dt.forEach((e,i)=>tl.to(e,{opacity:1,duration:0.1},T[0]+2.4+i*0.35));
write("#s14-a",T[0]+2.6,0.4); write("#s14-b",T[0]+3.6,0.4); write("#s14-c",T[0]+4.6,0.4);
write("#s14-l",T[0]+6.0,1.2); write("#s14-l2",T[0]+7.4,1.2);
const ss=[0.5,2.6,4.6,6.0,7.4];
ss.forEach((t,i)=>write("#s14-s"+i,T[2]+t,0.8));
"""
    return svg, html, js


@scene
def s15():
    smoke = "".join(f'<circle class="s15-sm" cx="{x}" cy="{y}" r="{r}" fill="rgba(255,138,42,.45)"/>' for x, y, r in [(470, 420, 36), (500, 370, 46), (540, 310, 54)])
    svg = (f'<g id="s15-fl"><g transform="translate(400,460)"><rect x="0" y="0" width="80" height="320" rx="14" fill="rgba(255,138,42,.4)" stroke="#23307a" stroke-width="5"/>'
           '<path class="ink" fill="none" stroke-width="4" d="M0,160 L80,160"/><path class="ink" fill="none" stroke-width="3" d="M10,300 L70,300 M10,312 L70,312"/></g></g>'
           + f'<g id="s15-sm">{smoke}</g>'
           + '<path id="s15-flame" fill="rgba(232,54,79,.85)" d="M440,840 c-30,40 -10,90 0,110 c10,-30 40,-40 20,-110 Z"/>'
           + ln("s15-ang", "M900,860 L1200,560", "pk", 8) + ln("s15-gr", "M900,860 L1260,860", "ink", 4) + ln("s15-arc", "M1060,860 A160,160 0 0 0 1013,747", "inkp", 4)
           + arrow(1300, 620, 1500, 620, "bl", 6, 24, "s15-wind")
           + '<g id="s15-pen"><rect x="1500" y="760" width="200" height="30" rx="12" fill="rgba(35,48,122,.8)"/><circle cx="1720" cy="700" r="16" fill="#e8364f"/></g>')
    html = (title("s15", "14 · Bengalas")
            + text("s15-d", 560, 470, "día: " + mark("humo naranja", "pink", "s15-dh"), "lbl") + text("s15-n", 560, 680, "noche: llama roja", "lbl", f"color:{RED}")
            + text("s15-t", 560, 760, "≈ 1 minuto", "sm")
            + text("s15-u1", 960, 300, "1 · desenroscar la tapa", "sm") + text("s15-u1b", 990, 350, "(noche = la estriada)", "sm")
            + text("s15-u2", 960, 410, "2 · tirar de la anilla", "sm") + text("s15-u3", 960, 470, "3 · a 45°, a favor del viento", "sm")
            + text("s15-45", 1080, 790, "45°", "sm") + text("s15-w", 1320, 640, "viento", "sm", f"color:{BLUE_T}")
            + text("s15-p", 1440, 860, mark("lanzador", "blue", "s15-ph") + " · como un boli", "sm")
            + text("s15-q", 200, 940, "úsalas cuando " + mark("puedan ser percibidas", "pink", "s15-qh"), "lbl"))
    js = """
write("#s15-title",T[0]+0.1,0.8); hl("#s15-title-hl",T[0]+0.9);
tl.set(q("#s15-sm, #s15-flame, #s15-pen"),{opacity:0},0);
tl.fromTo(q("#s15-fl"),{opacity:0},{opacity:1,duration:0.4},T[0]+0.6);
tl.to(q(".s15-sm"),{opacity:1,duration:0.3,stagger:0.2},T[1]+0.4); tl.set(q("#s15-sm"),{opacity:1},T[1]+0.4);
tl.to(q(".s15-sm"),{y:-20,duration:1,yoyo:true,repeat:5,ease:"sine.inOut"},T[1]+1.4);
write("#s15-d",T[1]+0.4,0.9); hl("#s15-dh",T[1]+1.3);
show("#s15-flame",T[1]+3.4,0.3); write("#s15-n",T[1]+3.4,0.9); write("#s15-t",T[1]+5.4,0.8);
tl.to(q("#s15-flame"),{scaleY:1.2,transformOrigin:"50% 0%",duration:0.2,yoyo:true,repeat:Math.round((D-T[1]-3.8)/0.2)},T[1]+3.8);
write("#s15-u1",T[2]+0.3,0.9); write("#s15-u1b",T[2]+2.6,0.9); write("#s15-u2",T[2]+6.4,0.9);
draw("#s15-gr",T[2]+8.0,0.4); draw("#s15-ang",T[2]+8.2,0.6); draw("#s15-arc",T[2]+8.6,0.4); write("#s15-45",T[2]+8.8,0.4);
write("#s15-u3",T[2]+8.0,1.2); draw("#s15-wind path",T[2]+9.6,0.5); write("#s15-w",T[2]+9.8,0.5);
show("#s15-pen",T[3]+0.4,0.3); write("#s15-p",T[3]+0.6,1.2); hl("#s15-ph",T[3]+1.8);
tl.fromTo(q("#s15-pen circle"),{y:0,opacity:1},{y:-300,opacity:0,duration:1.2,ease:"power2.out"},T[3]+4.0);
write("#s15-q",T[4]+1.4,1.4); hl("#s15-qh",T[4]+3.6);
"""
    return svg, html, js


@scene
def s16():
    svg = (ln("s16-clk", "M1500,450 m0,-160 a160,160 0 1 1 -0.1,0", "bl", 10)
           + '<path id="s16-hand" class="ink" fill="none" stroke-width="7" d="M1500,450 L1500,330"/>'
           + f'<g id="s16-bc"><g transform="translate(1440,720)"><rect x="0" y="0" width="120" height="160" rx="16" fill="{ORANGE}" stroke="#23307a" stroke-width="5"/><path class="ink" fill="none" stroke-width="6" d="M60,0 L60,-80"/></g></g>')
    reasons = ["distancias grandes o desconocidas", "problemas de orientación", "clima adverso o imprevisible", "falta de agua", "terreno difícil"]
    html = (title("s16", "15 · La gran decisión", "blue")
            + text("s16-q", 200, 240, "¿quedarse o moverse?", "lbl")
            + text("s16-a", 200, 320, "primeras " + mark("48 h", "pink", "s16-ah") + ": mejor no moverse si hay…", "lbl")
            + "".join(text(f"s16-r{i}", 240, 420 + i * 66, "· " + r, "sm") for i, r in enumerate(reasons))
            + text("s16-d", 200, 780, "desierto: " + mark("no se viaja", "pink", "s16-dh"), "lbl")
            + text("s16-48", 1440, 410, "48 h", "lbl")
            + text("s16-t", 1180, 910, "con radiobaliza: " + mark("≈ 22 h", "blue", "s16-th"), "lbl"))
    js = """
write("#s16-title",T[0]+0.1,0.9); hl("#s16-title-hl",T[0]+1.0); write("#s16-q",T[0]+1.4,1.2);
draw("#s16-clk",T[1]+0.2,1.2); write("#s16-48",T[1]+0.8,0.5);
tl.fromTo(q("#s16-hand"),{rotation:0,svgOrigin:"1500 450"},{rotation:720,svgOrigin:"1500 450",duration:3,ease:"power1.inOut"},T[1]+0.4);
write("#s16-a",T[1]+0.4,1.6); hl("#s16-ah",T[1]+2.0);
const rt=[4.4,6.4,8.4]; rt.forEach((t,i)=>write("#s16-r"+i,T[1]+t,0.9));
write("#s16-r3",T[2]+0.6,0.6); write("#s16-r4",T[2]+2.0,0.7);
write("#s16-d",T[2]+3.6,1.0); hl("#s16-dh",T[2]+4.6);
tl.fromTo(q("#s16-bc"),{opacity:0,y:30},{opacity:1,y:0,duration:0.5},T[3]+4.6);
write("#s16-t",T[3]+5.0,1.4); hl("#s16-th",T[3]+7.6);
"""
    return svg, html, js


@scene
def s17():
    html = title("s17", "Preguntas de examen", "pink")
    html += text("s17-i", 0, 500, "Intenta responder antes de ver la solución", "lbl", "width:1920px;text-align:center")
    js = 'write("#s17-title",T[0]+0.1,0.9); hl("#s17-title-hl",T[0]+1.0); write("#s17-i",T[0]+1.6,1.6); tl.to(q("#s17-i"),{opacity:0,duration:0.3},T[1]-0.3);\n'
    n = len(QUIZ)
    for i, (qq, aa) in enumerate(QUIZ):
        qi, ai = 1 + 2 * i, 2 + 2 * i
        nxt = f"T[{qi+2}]-0.3" if i < n - 1 else "D"
        html += text(f"s17-n{i}", 200, 240, f"Pregunta {i+1} / {n}", "sm")
        html += text(f"s17-q{i}", 200, 330, qq, "lbl", "width:1520px;white-space:normal;font-size:64px")
        html += text(f"s17-a{i}", 200, 640, "→ " + mark(aa, "blue" if i % 2 else "pink", f"s17-h{i}"), "lbl", "width:1520px;white-space:normal;font-size:60px")
        js += (f'tl.set(q("#s17-n{i}, #s17-q{i}, #s17-a{i}"),{{opacity:0}},0);'
               f'tl.set(q("#s17-n{i}, #s17-q{i}"),{{opacity:1}},T[{qi}]); write("#s17-n{i}",T[{qi}],0.3); write("#s17-q{i}",T[{qi}]+0.1,0.9);'
               f'tl.set(q("#s17-a{i}"),{{opacity:1}},T[{ai}]); write("#s17-a{i}",T[{ai}],0.8); hl("#s17-h{i}",T[{ai}]+0.8,0.3);')
        if i < n - 1:
            js += f'tl.to(q("#s17-n{i}, #s17-q{i}, #s17-a{i}"),{{opacity:0,duration:0.25}},{nxt});'
        js += "\n"
    return "", html, js


@scene
def s18():
    html = (text("s18-a", 0, 380, "Calma · agua · abrigo · señales", "big", "width:1920px;text-align:center")
            + text("s18-b", 0, 600, mark("quedarse, hacerse ver y esperar", "pink", "s18-bh"), "big", "width:1920px;text-align:center"))
    js = """
write("#s18-a",T[0]+0.1,3.0); write("#s18-b",T[1]+0.1,1.6); hl("#s18-bh",T[1]+1.8,0.5);
"""
    return "", html, js


if __name__ == "__main__":
    build(ROOT, S)
