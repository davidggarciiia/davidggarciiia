import sys, pathlib, json, math
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "lib"))
from nb import *  # noqa

TIM = json.loads((ROOT / "build/timings.json").read_text())
S = {}
def scene(fn):
    S[fn.__name__] = fn
    return fn

GREEN, RED, ORANGE, BLUE_L = "#138a4f", "#e8364f", "#ff8a2a", "#1e6fe4"


def ln(ident, d, cls="ink", w=4, fill="none"):
    return f'<path class="ln {cls}" pathLength="1" stroke-width="{w}" fill="{fill}" d="{d}" id="{ident}"/>'


def person(x, y, ident, color="#23307a", s=1.0):
    return (f'<g class="pp" id="{ident}"><circle cx="{x}" cy="{y}" r="{16*s}" fill="{color}"/>'
            f'<path fill="{color}" d="M{x-22*s},{y+60*s} C{x-22*s},{y+26*s} {x+22*s},{y+26*s} {x+22*s},{y+60*s} Z"/></g>')


@scene
def s1():
    svg = f'<g id="s1-pl"><g transform="translate(820,650) rotate(90) scale(0.9)">{PLANE_TOP}</g></g>' + person(820, 470, "s1-p", "#ff3d96", 1.4)
    html = (text("s1-title", 0, 140, mark("La cabina y el TCP", "pink", "s1-title-hl"), "h1 big", "width:1920px;text-align:center")
            + text("s1-s", 1200, 520, "función principal:", "lbl") + text("s1-s2", 1200, 600, mark("la seguridad", "blue", "s1-s2h"), "big"))
    js = """
tl.set(q("svg > g .ln"),{strokeDashoffset:0},0); tl.fromTo(q("#s1-pl"),{y:0},{y:-20,duration:D,ease:"none"},0);
tl.fromTo(q("#s1-p"),{opacity:0,scale:0.3,transformOrigin:"50% 50%"},{opacity:1,scale:1,duration:0.5,ease:"back.out(2)"},T[0]+5.4);
write("#s1-title",T[0]+1.4,1.4); hl("#s1-title-hl",T[0]+2.8,0.5);
write("#s1-s",T[1]+0.2,0.9); write("#s1-s2",T[1]+1.0,0.9); hl("#s1-s2h",T[1]+1.9,0.4);
"""
    return svg, html, js


@scene
def s2():
    X = lambda seats: 300 + seats * 3.6
    Y = lambda n: 860 - n * 75
    steps = "M300,860 " + " ".join(f"L{X(a):.0f},{Y(n):.0f} L{X(b):.0f},{Y(n):.0f}" for n, (a, b) in enumerate([(20, 50), (51, 100), (101, 150), (151, 200), (201, 250), (251, 300)], start=1))
    ex = [(32, 1), (66, 2), (140, 3), (189, 4), (233, 5), (261, 6)]
    svg = (ln("s2-ax", f"M300,860 L{X(360):.0f},860 M300,860 L300,380", "ink", 5)
           + ln("s2-st", steps, "pk", 6)
           + "".join(f'<circle class="s2-ex" id="s2-e{i}" cx="{X(a):.0f}" cy="{Y(n):.0f}" r="14" fill="#1ea7e4" stroke="#23307a" stroke-width="3"/>' for i, (a, n) in enumerate(ex))
           + ln("s2-19", f"M{X(19.5):.0f},860 L{X(19.5):.0f},380", "inkp", 4))
    html = (title("s2", "1 · ¿Cuántos TCP?")
            + text("s2-x", X(300), 890, "asientos", "sm") + text("s2-y", 220, 330, "TCP", "sm")
            + "".join(text(f"s2-yl{n}", 250, Y(n) - 28, str(n), "sm") for n in range(1, 7))
            + text("s2-a", 420, 250, "≤ 19 asientos → sin TCP", "lbl") + text("s2-a2", 420, 320, mark("≥ 20 → obligatorio", "pink", "s2-a2h"), "lbl")
            + text("s2-b", 1180, 230, "+1 TCP cada 50 asientos", "lbl")
            + "".join(text(f"s2-el{i}", X(a) + 20, Y(n) + 10, f"{a}→{n}", "sm") for i, (a, n) in enumerate(ex))
            + text("s2-c", 420, 400, "2 o más → uno es " + mark("sobrecargo", "blue", "s2-ch"), "lbl"))
    js = """
write("#s2-title",T[0]+0.1,0.8); hl("#s2-title-hl",T[0]+0.9);
draw("#s2-ax",T[0]+0.4,0.8); write("#s2-x, #s2-y",T[0]+0.8,0.4);
tl.fromTo(q("[id^=s2-yl]"),{opacity:0},{opacity:1,duration:0.2,stagger:0.08},T[0]+0.9);
write("#s2-a",T[0]+1.0,1.4); draw("#s2-19",T[0]+2.2,0.5); write("#s2-a2",T[0]+4.0,0.9); hl("#s2-a2h",T[0]+4.9);
draw("#s2-st",T[1]+0.4,2.4); write("#s2-b",T[1]+0.6,1.4);
tl.set(q(".s2-ex"),{opacity:0},0);
const et=[1.2,2.9,4.6,6.5,8.7,10.8];
et.forEach((t,i)=>{tl.fromTo(q("#s2-e"+i),{opacity:0,scale:0.2,transformOrigin:"50% 50%"},{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"},T[2]+t); write("#s2-el"+i,T[2]+t,0.5);});
write("#s2-c",T[3]+0.4,1.4); hl("#s2-ch",T[3]+1.8);
"""
    return svg, html, js


@scene
def s3():
    ranks = ["Comandante", "Primer oficial", "Sobrecargo", "TCP"]
    A = lambda age: 980 + (age - 18) * 13.5
    svg = (ln("s3-lad", "M300,280 L300,720 M560,280 L560,720 " + " ".join(f"M300,{320+i*120} L560,{320+i*120}" for i in range(4)), "ink", 5)
           + ln("s3-age", f"M{A(18):.0f},620 L{A(70):.0f},620", "ink", 5)
           + "".join(f'<rect class="s3-seg" id="s3-g{i}" x="{A(a):.0f}" y="560" width="{A(b)-A(a):.0f}" height="50" fill="{c}" stroke="#23307a" stroke-width="3"/>'
                     for i, (a, b, c) in enumerate([(18, 40, "rgba(66,188,240,.4)"), (40, 50, "rgba(255,214,90,.55)"), (50, 70, "rgba(255,92,168,.45)")])))
    html = (title("s3", "2 · Jerarquía y certificados", "blue")
            + "".join(text(f"s3-r{i}", 600, 290 + i * 120, f"{i+1}. {r}", "lbl") for i, r in enumerate(ranks))
            + text("s3-so", 200, 800, "sobrecargo: " + mark("tras 1 año como TCP", "pink", "s3-soh"), "lbl")
            + text("s3-m", 980, 300, mark("Certificado médico", "blue", "s3-mh"), "lbl")
            + text("s3-g0t", A(18), 450, "cada 5 años", "sm") + text("s3-g1t", A(40) - 10, 400, "cada 2", "sm") + text("s3-g2t", A(50) + 20, 450, "cada año", "sm")
            + text("s3-a40", A(40) - 30, 640, "40", "sm") + text("s3-a50", A(50) - 30, 640, "50", "sm")
            + text("s3-c", 980, 800, "certificado TCP: caduca tras", "lbl") + text("s3-c2", 980, 870, mark("5 años de inactividad", "pink", "s3-c2h"), "lbl"))
    js = """
write("#s3-title",T[0]+0.1,1.0); hl("#s3-title-hl",T[0]+1.1);
draw("#s3-lad",T[0]+0.4,1.2);
const rt=[1.6,2.6,3.6,4.6]; rt.forEach((t,i)=>write("#s3-r"+i,T[0]+t,0.7));
write("#s3-so",T[1]+0.4,1.6); hl("#s3-soh",T[1]+2.0);
write("#s3-m",T[2]+0.2,0.8); hl("#s3-mh",T[2]+1.0); draw("#s3-age",T[2]+0.6,0.6);
tl.set(q(".s3-seg"),{opacity:0},0);
const seg=(i,t)=>{tl.fromTo(q("#s3-g"+i),{opacity:0,scaleX:0,transformOrigin:"0% 50%"},{opacity:1,scaleX:1,duration:0.5},t); write("#s3-g"+i+"t",t+0.2,0.6);};
seg(0,T[2]+1.4); write("#s3-a40",T[2]+3.0,0.3); seg(1,T[2]+4.0); write("#s3-a50",T[2]+5.8,0.3); seg(2,T[2]+7.2);
write("#s3-c",T[3]+0.3,1.2); write("#s3-c2",T[3]+1.6,1.0); hl("#s3-c2h",T[3]+2.6);
"""
    return svg, html, js


@scene
def s4():
    sc = 1.1
    fy, ry = 560 - 230 * sc, 560 + 200 * sc
    lx, rx = 960 - 37, 960 + 37
    door = lambda x, y, i: f'<rect class="s4-d" id="s4-d{i}" x="{x-9}" y="{y-24}" width="18" height="48" rx="4" fill="#ff3d96"/>'
    ow = lambda x, y, i: f'<rect class="s4-o" id="s4-o{i}" x="{x-7}" y="{y-14}" width="14" height="28" rx="3" fill="#1ea7e4"/>'
    svg = (f'<g transform="translate(960,560) rotate(90) scale({sc})">{PLANE_TOP}</g>'
           + door(lx, fy, 0) + door(rx, fy, 1) + door(lx, ry, 2) + door(rx, ry, 3)
           + ow(lx, 590, 0) + ow(rx, 590, 1) + ow(lx, 630, 2) + ow(rx, 630, 3)
           + arrow(600, fy, lx - 20, fy, "pk", 6, 24, "s4-board")
           + f'<g id="s4-trk"><rect x="1240" y="{fy-60}" width="150" height="80" rx="10" fill="rgba(255,214,90,.5)" stroke="#23307a" stroke-width="4"/>'
           + f'<rect x="1240" y="{ry-40}" width="190" height="80" rx="14" fill="rgba(66,188,240,.4)" stroke="#23307a" stroke-width="4"/></g>')
    html = (title("s4", "3 · Puertas y posiciones")
            + text("s4-op", 200, 230, "corto (< 6 h) · 1 pasillo", "sm") + text("s4-op2", 200, 280, "largo (> 6 h) · 2 pasillos", "sm")
            + text("s4-1l", 760, fy - 70, "1L", "lbl", "color:#ff3d96") + text("s4-1r", 1110, fy - 70, "1R", "lbl", "color:#ff3d96")
            + text("s4-4l", 760, ry + 20, "4L", "lbl", "color:#ff3d96") + text("s4-4r", 1110, ry + 20, "4R", "lbl", "color:#ff3d96")
            + text("s4-lr", 200, 360, "L = izquierda · R = derecha", "sm")
            + text("s4-ow", 200, 560, mark("Overwings", "blue", "s4-owh") + " (2 y 3)", "lbl") + text("s4-ow2", 200, 626, "salidas sobre el ala", "sm")
            + text("s4-p1", 200, 800, "1L sobrecargo · 1R TCP", "sm") + text("s4-p2", 200, 850, "4L TCP + experiencia · 4R TCP", "sm")
            + text("s4-b", 620, fy + 20, "embarque", "sm", "color:#ff3d96")
            + text("s4-r", 1440, fy - 50, "catering", "sm") + text("s4-r2", 1460, ry - 30, "bus · asistencias", "sm"))
    js = """
write("#s4-title",T[0]+0.1,0.9); hl("#s4-title-hl",T[0]+1.0);
draw("svg > g:first-child .ln",T[0]+0.4,1.4); write("#s4-op",T[0]+1.6,1.0); write("#s4-op2",T[0]+4.4,1.0);
tl.set(q(".s4-d, .s4-o, #s4-trk"),{opacity:0},0);
const d=(i,l,t)=>{tl.to(q("#s4-d"+i),{opacity:1,duration:0.2},t); write(l,t,0.3);};
d(0,"#s4-1l",T[1]+4.6); d(1,"#s4-1r",T[1]+5.4); d(2,"#s4-4l",T[1]+6.2); d(3,"#s4-4r",T[1]+7.0); write("#s4-lr",T[1]+7.8,1.2);
tl.to(q(".s4-o"),{opacity:1,duration:0.2,stagger:0.15},T[2]+1.4); write("#s4-ow",T[2]+1.2,0.8); hl("#s4-owh",T[2]+2.0); write("#s4-ow2",T[2]+3.0,0.9);
tl.to(q(".s4-d"),{scale:1.5,transformOrigin:"50% 50%",duration:0.2,yoyo:true,repeat:1,stagger:1.6},T[3]+0.4);
write("#s4-p1",T[3]+0.4,2.4); write("#s4-p2",T[3]+3.8,2.6);
draw("#s4-board path",T[4]+0.3,0.5); write("#s4-b",T[4]+0.5,0.5);
show("#s4-trk",T[4]+2.6,0.4); write("#s4-r",T[4]+2.8,0.6); write("#s4-r2",T[4]+4.0,0.9);
"""
    return svg, html, js


@scene
def s5():
    tiles = [("luces", 0), ("música", 1), ("temperatura", 2), ("rampas", 3), ("agua", 4), ("asientos / señales", 5), ("fallos", 6)]
    svg = ln("s5-fap", "M240,330 L1060,330 L1060,860 L240,860 Z", "ink", 7, "rgba(35,48,122,.06)")
    for name, i in tiles:
        x, y = 290 + (i % 2) * 380, 380 + (i // 2) * 115
        svg += f'<rect class="s5-t" id="s5-t{i}" x="{x}" y="{y}" width="340" height="90" rx="14" fill="rgba(66,188,240,.25)" stroke="#23307a" stroke-width="4"/>'
    svg += ('<g id="s5-psu"><rect x="1200" y="560" width="480" height="120" rx="14" fill="rgba(255,255,255,.9)" stroke="#23307a" stroke-width="5"/>'
            '<circle cx="1270" cy="620" r="24" fill="rgba(255,214,90,.7)" stroke="#23307a" stroke-width="3"/><circle cx="1350" cy="620" r="24" fill="rgba(255,214,90,.7)" stroke="#23307a" stroke-width="3"/>'
            '<circle cx="1440" cy="620" r="18" fill="none" stroke="#23307a" stroke-width="4"/><circle cx="1510" cy="620" r="18" fill="none" stroke="#23307a" stroke-width="4"/>'
            '<rect x="1570" y="600" width="70" height="40" rx="10" fill="rgba(255,92,168,.4)" stroke="#23307a" stroke-width="3"/></g>')
    html = (title("s5", "4 · Paneles FAP y AAP", "blue")
            + text("s5-a", 1200, 340, mark("FAP", "blue", "s5-ah") + " · flight attendant panel", "lbl") + text("s5-a2", 1200, 410, "+ AAP · panel adicional", "sm")
            + "".join(text(f"s5-l{i}", 310 + (i % 2) * 380, 395 + (i // 2) * 115, n, "lbl", "font-size:50px") for n, i in tiles)
            + text("s5-p", 1200, 720, mark("PSU", "pink", "s5-ph") + " · passenger service unit", "lbl", "font-size:50px")
            + text("s5-p2", 1200, 790, "encima de cada fila", "sm"))
    js = """
write("#s5-title",T[0]+0.1,0.9); hl("#s5-title-hl",T[0]+1.0);
draw("#s5-fap",T[0]+0.6,1.0); write("#s5-a",T[0]+1.0,1.4); hl("#s5-ah",T[0]+2.4); write("#s5-a2",T[0]+5.2,1.0);
tl.set(q(".s5-t, #s5-psu"),{opacity:0},0);
const tile=(i,t)=>{tl.to(q("#s5-t"+i),{opacity:1,duration:0.25},t); write("#s5-l"+i,t,0.5);};
tile(0,T[1]+1.4); tile(1,T[1]+2.2); tile(2,T[1]+3.0);
tile(3,T[2]+1.0); tile(4,T[2]+2.8);
tile(5,T[3]+1.0); tile(6,T[3]+3.4);
show("#s5-psu",T[4]+0.6,0.4); write("#s5-p",T[4]+1.0,1.0); hl("#s5-ph",T[4]+2.0); write("#s5-p2",T[4]+2.6,0.8);
"""
    return svg, html, js


@scene
def s6():
    lamps = [(500, 1.0, "Bright", "100 %"), (960, 0.5, "Dim 1", "50 %"), (1420, 0.1, "Dim 2", "10 %")]
    svg = "".join(f'<circle class="s6-g" id="s6-g{i}" cx="{x}" cy="520" r="150" fill="rgba(255,214,90,{0.85*a:.2f})"/>'
                  f'<path class="ln ink" pathLength="1" id="s6-b{i}" stroke-width="5" fill="#fdfdff" d="M{x-50},440 L{x+50},440 L{x+70},520 L{x-70},520 Z"/>' for i, (x, a, _, _) in enumerate(lamps))
    html = (title("s6", "5 · Luces de cabina")
            + text("s6-a", 200, 250, "en concordancia con el " + mark("exterior", "blue", "s6-ah"), "lbl")
            + "".join(text(f"s6-l{i}", x - 150, 720, f"{n}", "lbl", "width:300px;text-align:center") + text(f"s6-p{i}", x - 150, 790, p, "big", "width:300px;text-align:center;font-size:90px")
                      for i, (x, _, n, p) in enumerate(lamps)))
    js = """
write("#s6-title",T[0]+0.1,0.8); hl("#s6-title-hl",T[0]+0.9); write("#s6-a",T[0]+1.4,1.4); hl("#s6-ah",T[0]+2.8);
tl.set(q(".s6-g"),{opacity:0},0);
const lamp=(i,t)=>{draw("#s6-b"+i,t,0.5); tl.to(q("#s6-g"+i),{opacity:1,duration:0.5},t+0.4); write("#s6-l"+i,t+0.2,0.5); write("#s6-p"+i,t+0.6,0.6);};
lamp(0,T[1]+0.1); lamp(1,T[1]+2.0); lamp(2,T[1]+4.2);
"""
    return svg, html, js


@scene
def s7():
    svg = (ln("s7-aip", "M240,300 L900,300 L900,420 L240,420 Z", "ink", 5, "rgba(35,48,122,.9)")
           + f'<rect id="s7-ag" x="270" y="330" width="280" height="60" rx="8" fill="{GREEN}"/><rect id="s7-ar" x="590" y="330" width="280" height="60" rx="8" fill="{RED}"/>'
           + ln("s7-acp", "M1060,560 L1660,560 L1660,640 L1060,640 Z", "ink", 5, "rgba(35,48,122,.12)")
           + f'<rect id="s7-c1" x="1080" y="575" width="560" height="50" rx="10" fill="{BLUE_L}"/>'
           + f'<rect id="s7-c2" x="1080" y="575" width="560" height="50" rx="10" fill="{RED}"/>'
           + f'<rect id="s7-c3" x="1080" y="575" width="560" height="50" rx="10" fill="{RED}"/>'
           + f'<rect id="s7-c4" x="1080" y="575" width="560" height="50" rx="10" fill="{ORANGE}"/>'
           + f'<rect id="s7-c5" x="1080" y="575" width="560" height="50" rx="10" fill="{ORANGE}"/>')
    rows = [("azul fijo", "llamada de pasajero", BLUE_L), ("rojo fijo", "llamada normal", RED), ("rojo parpadeante", "llamada de emergencia", RED),
            ("naranja fijo", "llamada desde el baño", "#c2560a"), ("naranja parpadeante", "fuego o humo", "#c2560a")]
    html = (title("s7", "6 · Paneles AIP y ACP", "blue")
            + text("s7-a", 960, 300, mark("AIP", "blue", "s7-ah") + " · qué pasa y dónde", "lbl")
            + text("s7-ag2", 270, 440, "verde fijo · normal", "sm", f"color:{GREEN}") + text("s7-ar2", 590, 440, "rojo parpadeante · emergencia", "sm", f"color:{RED}")
            + text("s7-sm", 960, 380, "también: detector de humos", "sm")
            + text("s7-c", 1060, 480, mark("ACP", "pink", "s7-ch") + " · luces de llamada", "lbl")
            + "".join(text(f"s7-r{i}", 200, 560 + i * 78, f'{a} → {b}', "lbl", f"font-size:50px;color:{c}") for i, (a, b, c) in enumerate(rows)))
    js = """
write("#s7-title",T[0]+0.1,0.9); hl("#s7-title-hl",T[0]+1.0);
draw("#s7-aip",T[0]+0.4,0.8); write("#s7-a",T[0]+0.8,1.2); hl("#s7-ah",T[0]+2.0);
tl.set(q("#s7-ag, #s7-ar, #s7-c1, #s7-c2, #s7-c3, #s7-c4, #s7-c5"),{opacity:0},0); tl.set(q("#s7-acp"),{opacity:1},0);
tl.to(q("#s7-ag"),{opacity:1,duration:0.2},T[0]+3.6); write("#s7-ag2",T[0]+3.6,0.8);
tl.to(q("#s7-ar"),{opacity:1,duration:0.1,yoyo:true,repeat:Math.round((D-T[0]-6.2)/0.3)},T[0]+6.0); write("#s7-ar2",T[0]+6.0,1.0);
write("#s7-sm",T[0]+8.6,1.0);
draw("#s7-acp",T[1]+0.2,0.6); write("#s7-c",T[1]+0.3,0.8); hl("#s7-ch",T[1]+1.1);
const st=(i,t,flash,end)=>{ if(flash){tl.to(q("#s7-c"+i),{opacity:1,duration:0.1,yoyo:true,repeat:Math.max(1,Math.round((end-t)/0.3)-1)},t);} else {tl.to(q("#s7-c"+i),{opacity:1,duration:0.15},t);} tl.set(q("#s7-c"+i),{opacity:0},end); write("#s7-r"+(i-1),t,0.8); };
st(1,T[2]+0.1,false,T[2]+2.6); st(2,T[2]+2.6,false,T[2]+4.9); st(3,T[2]+4.9,true,T[3]);
st(4,T[3]+0.1,false,T[3]+3.6); st(5,T[3]+3.6,true,D);
"""
    return svg, html, js


@scene
def s8():
    pts = [(240, 800, "taxi"), (420, 800, "despegue"), (640, 520, "ascenso"), (960, 340, "ruta"), (1280, 520, "descenso"), (1460, 700, "aproximación"), (1600, 800, "aterrizaje"), (1720, 800, "taxi")]
    path = "M240,800 L420,800 C520,800 560,600 640,520 C740,420 800,340 960,340 L1180,340 C1220,340 1240,470 1280,520 C1340,600 1400,680 1460,700 C1520,740 1560,800 1600,800 L1720,800"
    svg = (ln("s8-path", path, "ink", 6)
           + "".join(f'<circle class="s8-p" id="s8-p{i}" cx="{x}" cy="{y}" r="12" fill="#ff3d96"/>' for i, (x, y, _) in enumerate(pts))
           + '<path id="s8-hold" fill="none" stroke="#1ea7e4" stroke-width="6" d="M1300,220 L1440,220 A50,50 0 0 1 1440,320 L1300,320 A50,50 0 0 1 1300,220 Z"/>')
    offs = [(-40, 40), (-60, 30), (-260, -40), (-40, -110), (40, -60), (40, -40), (-120, 40), (-60, 40)]
    html = (title("s8", "7 · Fases de vuelo")
            + "".join(text(f"s8-l{i}", x + dx, y + dy, n, "sm") for i, ((x, y, n), (dx, dy)) in enumerate(zip(pts, offs)))
            + text("s8-h", 1520, 250, mark("holding", "blue", "s8-hh") + " · espera", "lbl"))
    js = """
write("#s8-title",T[0]+0.1,0.8); hl("#s8-title-hl",T[0]+0.9);
draw("#s8-path",T[0]+0.6,5.6,"none");
tl.set(q(".s8-p, #s8-hold"),{opacity:0},0);
const at=[0.6,1.6,2.8,3.6,4.6,5.6,6.6,7.6];
at.forEach((t,i)=>{tl.to(q("#s8-p"+i),{opacity:1,duration:0.2},T[0]+t); write("#s8-l"+i,T[0]+t,0.5);});
tl.fromTo(q("#s8-hold"),{opacity:0,strokeDasharray:"1000 1000",strokeDashoffset:1000},{opacity:1,strokeDashoffset:0,duration:1.2},T[1]+1.0);
write("#s8-h",T[1]+1.4,0.9); hl("#s8-hh",T[1]+2.3);
"""
    return svg, html, js


@scene
def s9():
    svg = (ln("s9-tw", "M300,880 L340,600 L380,880 M300,600 L380,600 L380,540 L300,540 Z", "ink", 5)
           + f'<g transform="translate(560,380) scale(0.5)">{PLANE_SIDE}</g><g transform="translate(980,300) scale(0.5) scale(-1,1) translate(-600,0)">{PLANE_SIDE}</g>'
           + ln("s9-sep", "M880,440 L960,400", "pk", 5)
           + "".join(f'<circle class="s9-z" id="s9-z{i}" cx="{x}" cy="760" r="90" fill="{c}" stroke="#23307a" stroke-width="4"/>' for i, (x, c) in enumerate([(1060, "rgba(255,214,90,.45)"), (1290, "rgba(255,138,42,.4)"), (1520, "rgba(232,54,79,.35)")])))
    html = (title("s9", "8 · Control aéreo (ATC)", "blue")
            + text("s9-a", 200, 250, "prevenir " + mark("colisiones", "pink", "s9-ah") + " · aire y área de maniobras", "lbl")
            + text("s9-b1", 460, 600, "fluidez y orden", "sm") + text("s9-b2", 460, 650, "información para un vuelo seguro", "sm") + text("s9-b3", 460, 700, "aviso a búsqueda y salvamento", "sm")
            + "".join(text(f"s9-zl{i}", x - 90, 870, n, "sm", "width:180px;text-align:center") for i, (x, n) in enumerate([(1060, "restringida"), (1290, "peligrosa"), (1520, "prohibida")]))
            + "".join(text(f"s9-zc{i}", x - 30, 720, n, "big", "width:60px;text-align:center;font-size:72px") for i, (x, n) in enumerate([(1060, "R"), (1290, "D"), (1520, "P")])))
    js = """
write("#s9-title",T[0]+0.1,1.0); hl("#s9-title-hl",T[0]+1.1);
draw("#s9-tw",T[0]+0.4,0.8); draw("svg > g .ln",T[0]+0.8,1.0); draw("#s9-sep",T[0]+2.4,0.4);
write("#s9-a",T[0]+1.6,2.2); hl("#s9-ah",T[0]+3.8);
write("#s9-b1",T[1]+0.6,0.8); write("#s9-b2",T[1]+2.6,1.0); write("#s9-b3",T[1]+5.4,1.0);
tl.set(q(".s9-z"),{opacity:0},0);
const z=(i,t)=>{tl.to(q("#s9-z"+i),{opacity:1,duration:0.3},t); write("#s9-zc"+i,t,0.3); write("#s9-zl"+i,t+0.2,0.6);};
z(0,T[2]+1.2); z(1,T[2]+2.0); z(2,T[2]+2.8);
"""
    return svg, html, js


def glossary(sid, ttl, color, items, line_of):
    """items: list of (term, definition); line_of[i]: (line index, delay)"""
    html = title(sid, ttl, color)
    js = f'write("#{sid}-title",T[0]+0.1,0.9); hl("#{sid}-title-hl",T[0]+1.0);\n'
    n = len(items); half = (n + 1) // 2
    for i, (t, d) in enumerate(items):
        col, row = (0, i) if i < half else (1, i - half)
        x, y = 200 + col * 820, 250 + row * 128
        html += text(f"{sid}-t{i}", x, y, mark(t, "pink" if i % 2 else "blue", f"{sid}-h{i}"), "lbl", "font-size:50px")
        html += text(f"{sid}-d{i}", x + 20, y + 58, d, "sm", "font-size:40px")
        li, dl = line_of[i]
        js += f'write("#{sid}-t{i}",T[{li}]+{dl},0.6); hl("#{sid}-h{i}",T[{li}]+{dl}+0.6,0.3); write("#{sid}-d{i}",T[{li}]+{dl}+0.7,1.2);\n'
    return "", html, js


@scene
def s10():
    items = [("Finger", "pasarela telescópica"), ("Cachonda", "tubo amarillo · aire frío/caliente"), ("Remoto", "parking a la intemperie · escaleras"),
             ("Jardinera", "bus de la terminal al avión"), ("Pushback", "empuja el avión hacia atrás"), ("Hangar", "parking techado · mantenimiento"),
             ("Handling", "servicios de tierra"), ("Despachador / coordinador", "enlace terminal ↔ tripulación")]
    lines = [(0, 1.0), (0, 5.4), (1, 0.6), (1, 2.6), (2, 0.4), (2, 5.4), (3, 0.4), (3, 2.6)]
    return glossary("s10", "9 · Vocabulario: aeropuerto", "pink", items, lines)


@scene
def s11():
    items = [("Sector / salto / leg", "del despegue al aterrizaje"), ("ETD · ETA", "hora estimada de salida · de llegada"),
             ("Frustrada / go around", "no aterriza y vuelve al aire"), ("Amerizaje / ditching", "aterrizar sobre el agua"),
             ("Vuelo ferry", "sin pasajeros"), ("Posicionamiento / DHC", "te llevan a otro destino a operar"),
             ("PIL · MEL", "info de pasajeros · equipo mínimo"), ("Jumpseat · fletear", "asiento del TCP · alquilar un avión")]
    lines = [(0, 0.8), (0, 5.6), (1, 0.4), (1, 5.0), (2, 0.4), (2, 3.0), (3, 0.4), (4, 0.4)]
    return glossary("s11", "10 · Vocabulario: en vuelo", "blue", items, lines)


@scene
def s12():
    abc = ["Alfa", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet", "Kilo", "Lima", "Mike",
           "November", "Oscar", "Papa", "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor", "Whiskey", "X-ray", "Yankee", "Zulu"]
    st, en = TIM["s12"]["starts"][1], TIM["s12"]["ends"][1]
    html = title("s12", "11 · Alfabeto aeronáutico")
    js = 'write("#s12-title",T[0]+0.1,0.9); hl("#s12-title-hl",T[0]+1.0);\n'
    for i, w in enumerate(abc):
        col, row = i // 7, i % 7
        x, y = 200 + col * 400, 260 + row * 92
        html += text(f"s12-a{i}", x, y, f'<b style="color:#ff3d96">{w[0]}</b> · {w}', "lbl", "font-size:54px")
        t = st + (en - st) * i / 26
        js += f'write("#s12-a{i}",{t:.2f},0.35);\n'
    html += text("s12-ex", 1000, 930, "EC → " + mark("Echo Charlie", "pink", "s12-exh"), "lbl")
    js += 'write("#s12-ex",T[2]+0.4,1.0); hl("#s12-exh",T[2]+1.4);\n'
    return "", html, js


@scene
def s13():
    html = (text("s13-a", 0, 360, "Seguridad · orden · comunicación", "big", "width:1920px;text-align:center")
            + text("s13-b", 0, 540, "eso es el trabajo de un TCP", "lbl", "width:1920px;text-align:center;font-size:80px")
            + text("s13-c", 0, 720, mark("¡Mucha suerte en el examen!", "pink", "s13-ch"), "big", "width:1920px;text-align:center"))
    js = """
write("#s13-a",T[0]+0.1,1.8); write("#s13-b",T[0]+2.2,1.2); write("#s13-c",T[0]+4.0,1.2); hl("#s13-ch",T[0]+5.2,0.5);
"""
    return "", html, js


if __name__ == "__main__":
    build(ROOT, S)
