"""Builds index.html and compositions/*.html for episode 1 from timings.json.

Every scene is a page of the same squared notebook: diagrams are drawn in blue
ink (SVG strokes revealed with stroke-dashoffset), handwritten labels are
revealed left to right (clip-path), key words get a highlighter swipe.
"""
import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TIM = json.loads((ROOT / "build/timings.json").read_text())
(ROOT / "compositions").mkdir(exist_ok=True)

PAN = 700          # px the camera travels along the page at each cut
ENTER, EXIT = 0.55, 0.5

# ---------------------------------------------------------------- shared bits
CSS = """
@font-face{font-family:'Caveat';src:url('assets/fonts/caveat.woff2') format('woff2');font-weight:400 700;font-display:block}
#root{position:absolute;inset:0;font-family:'Caveat',cursive;color:#23307a}
.stage{position:absolute;inset:0}
svg.dg{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible}
.ln{fill:none;stroke-dasharray:1 1}
.t{position:absolute;white-space:nowrap;line-height:1.08;font-weight:700}
.h1{font-size:100px}
.lbl{font-size:56px}
.sm{font-size:46px;font-weight:600;color:#3a3f8f}
.big{font-size:120px}
.w{position:relative;display:inline-block;isolation:isolate}
.hl{position:absolute;left:-12px;right:-12px;top:34%;bottom:2%;transform-origin:0 50%;border-radius:8px 14px 10px 6px;z-index:-1;mix-blend-mode:multiply}
.pink{background:rgba(255,92,168,.48)}
.blue{background:rgba(66,188,240,.45)}
.ink{stroke:#23307a}
.inkp{stroke:#5a3fb0}
.pk{stroke:#ff3d96}
.bl{stroke:#1ea7e4}
"""

JS_HELPERS = """
const host=document.querySelector('[data-composition-id="__ID__"]');
const q=gsap.utils.selector(host);
const T=__T__, D=__D__;
const tl=gsap.timeline({paused:true});
const draw=(s,t,d=0.9,e="power1.inOut")=>tl.fromTo(q(s),{strokeDashoffset:1},{strokeDashoffset:0,duration:d,ease:e,stagger:0.12},t);
const write=(s,t,d=0.7)=>tl.fromTo(q(s),{clipPath:"inset(-30% 100% -30% -2%)"},{clipPath:"inset(-30% -2% -30% -2%)",duration:d,ease:"none"},t);
const hl=(s,t,d=0.35)=>tl.fromTo(q(s),{scaleX:0},{scaleX:1,duration:d,ease:"power2.out"},t);
const show=(s,t,d=0.3)=>tl.fromTo(q(s),{opacity:0},{opacity:1,duration:d,ease:"none"},t);
const hide=(s,t,d=0.3)=>tl.to(q(s),{opacity:0,duration:d,ease:"none"},t);
"""


def arrow(x1, y1, x2, y2, cls="ink", w=5, head=26, ident=""):
    """A straight arrow: shaft and head as two drawable paths in one <g>."""
    a = math.atan2(y2 - y1, x2 - x1)
    hx1 = x2 - head * math.cos(a - 0.45); hy1 = y2 - head * math.sin(a - 0.45)
    hx2 = x2 - head * math.cos(a + 0.45); hy2 = y2 - head * math.sin(a + 0.45)
    i = f' id="{ident}"' if ident else ""
    return (f'<g{i} class="arr">'
            f'<path class="ln {cls} shaft" pathLength="1" stroke-width="{w}" stroke-linecap="round" d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"/>'
            f'<path class="ln {cls} head" pathLength="1" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" '
            f'd="M{hx1:.1f},{hy1:.1f} L{x2:.1f},{y2:.1f} L{hx2:.1f},{hy2:.1f}"/></g>')


def text(ident, x, y, body, cls="lbl", style=""):
    return f'<div id="{ident}" class="t {cls}" style="left:{x}px;top:{y}px;{style}">{body}</div>'


def mark(word, color="pink", ident=""):
    i = f' id="{ident}"' if ident else ""
    return f'<span class="w">{word}<span{i} class="hl {color}"></span></span>'


# Side view of an airliner, nose to the left, local box ~600 x 150.
PLANE_SIDE = """
<path class="ln ink" pathLength="1" stroke-width="4" d="M28,112 C24,92 52,80 96,78 L462,74 L528,22 L566,22 L556,76 L584,80 C598,84 598,98 584,102 L520,114 L110,124 C60,126 30,124 28,112 Z"/>
<path class="ln ink" pathLength="1" stroke-width="3" d="M56,92 L84,85 L90,95 L60,99 Z"/>
<path class="ln ink" pathLength="1" stroke-width="3.5" d="M240,110 L392,102 L346,140 L262,142 Z"/>
<path class="ln ink" pathLength="1" stroke-width="3.5" d="M262,124 L322,124 C334,124 334,146 322,146 L262,146 C250,146 250,124 262,124 Z"/>
<path class="ln ink" pathLength="1" stroke-width="3.5" d="M494,86 L580,72 L586,82 L518,94 Z"/>
<path class="ink" fill="none" stroke-width="7" stroke-linecap="round" stroke-dasharray="0.1 22" d="M128,93 L440,89"/>
"""
GEAR = """
<path class="ink" fill="none" stroke-width="3.5" d="M150,124 L150,140 M390,116 L390,140"/>
<circle class="ink" fill="#fdfdff" stroke-width="3.5" cx="150" cy="146" r="7"/>
<circle class="ink" fill="#fdfdff" stroke-width="3.5" cx="390" cy="146" r="7"/>
"""

# Wing profile, leading edge at (0,80), trailing edge at (760,90).
AIRFOIL = "M0,80 C0,30 110,0 280,0 C460,0 650,50 760,90 C650,92 460,108 280,112 C110,114 0,108 0,80 Z"
AIRFOIL_TOP = "M0,80 C0,30 110,0 280,0 C460,0 650,50 760,90"
AIRFOIL_BOT = "M760,90 C650,92 460,108 280,112 C110,114 0,108 0,80"

# Front view (centre 0,0) and top view (nose left, centre 0,0).
PLANE_FRONT = """
<circle class="ln ink" pathLength="1" stroke-width="4" fill="none" cx="0" cy="0" r="72"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M-70,12 L-470,-22 L-472,-8 L-68,34"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M70,12 L470,-22 L472,-8 L68,34"/>
<circle class="ln ink" pathLength="1" stroke-width="4" fill="none" cx="-210" cy="44" r="32"/>
<circle class="ln ink" pathLength="1" stroke-width="4" fill="none" cx="210" cy="44" r="32"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M-9,-70 L-7,-240 L7,-240 L9,-70"/>
<path class="ln ink" pathLength="1" stroke-width="3" d="M-60,-46 L-190,-60 M60,-46 L190,-60"/>
"""
PLANE_TOP = """
<path class="ln ink" pathLength="1" stroke-width="4" d="M-330,0 C-330,-26 -300,-34 -260,-34 L250,-30 C290,-28 320,-12 340,0 C320,12 290,28 250,30 L-260,34 C-300,34 -330,26 -330,0 Z"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M-70,-32 L120,-330 L170,-330 L80,-31"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M-70,32 L120,330 L170,330 L80,31"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M228,-28 L292,-128 L320,-128 L300,-26"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M228,28 L292,128 L320,128 L300,26"/>
<path class="ln ink" pathLength="1" stroke-width="3.5" d="M10,-120 L60,-120 C72,-120 72,-100 60,-100 L10,-100 Z M10,120 L60,120 C72,120 72,100 60,100 L10,100 Z"/>
"""


def title(sid, label, color="pink", x=200, y=96):
    return text(f"{sid}-title", x, y, mark(label, color, f"{sid}-title-hl"), "h1")


# ---------------------------------------------------------------- scenes
SCENES = {}


def scene(fn):
    SCENES[fn.__name__] = fn
    return fn


@scene
def s1():
    svg = f"""
<path class="ink" fill="none" stroke-width="4" stroke-linecap="round" d="M150,742 L1770,742"/>
<path class="ink" fill="none" stroke-width="3" stroke-dasharray="40 34" d="M190,770 L1730,770"/>
<g id="s1-plane"><g transform="translate(480,508) scale(1.6)">{PLANE_SIDE}{GEAR}</g></g>
{arrow(1010, 690, 1010, 940, "pk", 7, 34, "s1-down")}
{arrow(1010, 470, 1010, 250, "bl", 7, 34, "s1-up")}
"""
    html = (text("s1-weight", 1060, 846, "Peso: " + mark("decenas de toneladas", "pink", "s1-weight-hl"))
            + text("s1-q", 1060, 238, "¿Cómo se sostiene?", "lbl")
            + text("s1-title", 200, 92, mark("Cómo vuela un avión", "blue", "s1-title-hl"), "h1 big"))
    js = """
draw("#s1-down .shaft",T[0]+0.2,0.7); draw("#s1-down .head",T[0]+0.85,0.3);
write("#s1-weight",T[0]+0.9,1.1); hl("#s1-weight-hl",T[0]+2.0,0.45);
draw("#s1-up .shaft",T[1]+0.5,0.6); draw("#s1-up .head",T[1]+1.05,0.25);
tl.fromTo(q("#s1-plane"),{y:0},{y:-46,duration:1.6,ease:"power2.inOut"},T[1]+0.6);
write("#s1-q",T[1]+1.2,0.9);
write("#s1-title",T[2]+0.4,1.3); hl("#s1-title-hl",T[2]+1.8,0.5);
"""
    return svg, html, js


@scene
def s2():
    # composition bar: 1400 px wide from x=260
    x0, w, y = 260, 1400, 330
    n2, o2 = w * .78, w * .21
    svg = f"""
<g id="s2-mix">
<rect id="s2-n2" x="{x0}" y="{y}" width="{n2:.0f}" height="110" fill="rgba(66,188,240,.5)"/>
<rect id="s2-o2" x="{x0+n2:.0f}" y="{y}" width="{o2:.0f}" height="110" fill="rgba(255,92,168,.55)"/>
<rect id="s2-ar" x="{x0+n2+o2:.0f}" y="{y}" width="{w-n2-o2:.0f}" height="110" fill="#23307a"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M{x0},{y} L{x0+w},{y} L{x0+w},{y+110} L{x0},{y+110} Z" id="s2-box"/>
<path class="ln ink" pathLength="1" stroke-width="3" d="M{x0+w-6},{y-8} L{x0+w-6},{y-70}" id="s2-arlead"/>
</g>
<g id="s2-isa">
<path class="ln ink" pathLength="1" stroke-width="4" d="M1130,890 L1130,330" id="s2-ruler"/>
<path class="ln ink" pathLength="1" stroke-width="4" d="M1110,890 L1150,890 M1110,710 L1150,710 M1110,530 L1150,530 M1110,350 L1150,350" id="s2-ticks"/>
<path class="ln bl" pathLength="1" stroke-width="4" fill="none" d="M930,915 C980,900 1030,930 1080,915 C1130,900 1180,930 1230,915 C1280,900 1330,930 1380,915 C1430,900 1480,930 1530,915 C1580,900 1630,930 1680,915" id="s2-sea"/>
</g>
"""
    html = (title("s2", "1 · El aire")
            + text("s2-l-n2", 600, 462, "78 % nitrógeno")
            + text("s2-l-o2", 1360, 462, "21 % oxígeno")
            + text("s2-l-ar", 1330, 196, "1 % otros (argón)", "sm")
            + text("s2-isa-t", 200, 290, mark("ISA", "blue", "s2-isa-hl") + " · atmósfera", "lbl")
            + text("s2-isa-t2", 200, 356, "estándar internacional", "lbl")
            + text("s2-f0", 920, 868, "0 ft", "sm", "width:180px;text-align:right")
            + text("s2-f1", 920, 688, "1000 ft", "sm", "width:180px;text-align:right")
            + text("s2-f2", 920, 508, "2000 ft", "sm", "width:180px;text-align:right")
            + text("s2-f3", 920, 328, "3000 ft", "sm", "width:180px;text-align:right")
            + text("s2-sl", 1180, 846, mark("15 °C · 1013,2 hPa", "pink", "s2-sl-hl"), "lbl")
            + text("s2-c1", 1180, 680, "13 °C", "lbl")
            + text("s2-c2", 1180, 500, "11 °C", "lbl")
            + text("s2-c3", 1180, 320, "9 °C", "lbl")
            + text("s2-rule", 200, 500, mark("−2 °C cada 1000 ft", "blue", "s2-rule-hl"), "lbl")
            + text("s2-down", 200, 640, "Al subir bajan:", "lbl")
            + text("s2-d1", 230, 716, "↓ temperatura", "sm")
            + text("s2-d2", 230, 776, "↓ presión", "sm")
            + text("s2-d3", 230, 836, "↓ densidad", "sm"))
    js = """
write("#s2-title",T[0]+0.2,0.8); hl("#s2-title-hl",T[0]+1.0);
draw("#s2-box",T[1]-0.2,0.8);
const fill=(s,t,d)=>tl.fromTo(q(s),{scaleX:0,transformOrigin:"0% 50%"},{scaleX:1,duration:d,ease:"power2.out"},t);
fill("#s2-n2",T[1]+0.9,1.6); write("#s2-l-n2",T[1]+1.6,0.7);
fill("#s2-o2",T[1]+3.7,0.8); write("#s2-l-o2",T[1]+4.1,0.7);
fill("#s2-ar",T[1]+5.9,0.3); draw("#s2-arlead",T[1]+6.0,0.3); write("#s2-l-ar",T[1]+6.2,0.9);
tl.to(q("#s2-mix, #s2-l-n2, #s2-l-o2, #s2-l-ar"),{opacity:0,y:-60,duration:0.5,ease:"power2.in"},T[2]-0.3);
write("#s2-isa-t",T[2]+0.3,0.6); hl("#s2-isa-hl",T[2]+1.0); write("#s2-isa-t2",T[2]+1.6,0.9);
draw("#s2-ruler",T[2]+3.0,1.0); draw("#s2-ticks",T[2]+3.6,0.8);
draw("#s2-sea",T[3]+0.0,0.9); write("#s2-f0",T[3]+0.3,0.4);
write("#s2-sl",T[3]+1.4,1.3); hl("#s2-sl-hl",T[3]+3.0,0.5);
write("#s2-f1",T[4]+0.5,0.4); write("#s2-c1",T[4]+0.8,0.4);
write("#s2-f2",T[4]+1.4,0.4); write("#s2-c2",T[4]+1.7,0.4);
write("#s2-f3",T[4]+2.3,0.4); write("#s2-c3",T[4]+2.6,0.4);
write("#s2-rule",T[4]+2.9,1.0); hl("#s2-rule-hl",T[4]+3.9);
write("#s2-down",T[5]+0.2,0.7);
write("#s2-d1",T[5]+1.1,0.5); write("#s2-d2",T[5]+1.9,0.5); write("#s2-d3",T[5]+2.6,0.5);
"""
    return svg, html, js


@scene
def s3():
    top = "M240,440 L480,440 C560,440 590,550 660,550 L820,550 C890,550 920,440 1000,440 L1240,440"
    bot = "M240,840 L480,840 C560,840 590,730 660,730 L820,730 C890,730 920,840 1000,840 L1240,840"
    def mano(x, wall, h, ident):
        return (f'<path class="ln ink" pathLength="1" stroke-width="4" d="M{x-18},{wall} L{x-18},{wall-230} M{x+18},{wall-230} L{x+18},{wall}" id="{ident}-tube"/>'
                f'<rect id="{ident}-liq" x="{x-14}" y="{wall-h}" width="28" height="{h}" fill="rgba(66,188,240,.65)"/>')
    flow = "".join(
        f'<path class="s3-flow bl" fill="none" stroke-width="4" stroke-linecap="round" stroke-dasharray="14 30" d="{d}"/>'
        for d in ["M250,520 L480,520 C560,520 590,590 660,590 L820,590 C890,590 920,520 1000,520 L1230,520",
                  "M250,640 L1230,640",
                  "M250,760 L480,760 C560,760 590,690 660,690 L820,690 C890,690 920,760 1000,760 L1230,760"])
    svg = f"""
<g id="s3-flowg">{flow}</g>
<path class="ln ink" pathLength="1" stroke-width="5" d="{top}" id="s3-top"/>
<path class="ln ink" pathLength="1" stroke-width="5" d="{bot}" id="s3-bot"/>
{arrow(300, 640, 440, 640, "ink", 6, 26, "s3-a1")}
{arrow(640, 640, 880, 640, "pk", 9, 34, "s3-a2")}
{arrow(1060, 640, 1200, 640, "ink", 6, 26, "s3-a3")}
{mano(360, 440, 190, "s3-m1")}{mano(740, 550, 50, "s3-m2")}{mano(1120, 440, 170, "s3-m3")}
"""
    html = (title("s3", "2 · Venturi y Bernoulli", "blue")
            + text("s3-v1", 1320, 300, mark("Venturi", "blue", "s3-v-hl"), "lbl")
            + text("s3-v2", 1320, 372, "paso estrecho", "sm") + text("s3-v3", 1320, 428, "→ el aire se acelera", "sm")
            + text("s3-b1", 1320, 540, mark("Bernoulli", "pink", "s3-b-hl"), "lbl")
            + text("s3-b2", 1320, 612, "más velocidad", "sm") + text("s3-b3", 1320, 668, "→ menos presión", "sm")
            + text("s3-k", 1320, 790, "+ velocidad", "lbl") + text("s3-k2", 1320, 860, mark("− presión", "pink", "s3-k-hl"), "lbl")
            + text("s3-p", 560, 236, "presión", "sm"))
    js = """
write("#s3-title",T[0]+0.2,1.0); hl("#s3-title-hl",T[0]+1.2);
draw("#s3-top",T[0]+1.4,1.2); draw("#s3-bot",T[0]+1.6,1.2);
show("#s3-flowg",T[0]+2.6,0.6);
tl.fromTo(q(".s3-flow"),{strokeDashoffset:0},{strokeDashoffset:-44*Math.round(D*2.2),duration:D,ease:"none"},0);
draw("#s3-a1 path",T[1]+0.2,0.4); draw("#s3-a2 path",T[1]+1.3,0.6); draw("#s3-a3 path",T[1]+2.6,0.4);
write("#s3-v1",T[1]+0.0,0.6); hl("#s3-v-hl",T[1]+0.6); write("#s3-v2",T[1]+0.9,0.6); write("#s3-v3",T[1]+1.9,0.9);
const liq=(s,t)=>tl.fromTo(q(s),{scaleY:0,transformOrigin:"50% 100%"},{scaleY:1,duration:0.9,ease:"power2.out"},t);
draw("#s3-m1-tube, #s3-m2-tube, #s3-m3-tube",T[2]-0.2,0.7);
write("#s3-p",T[2]+0.3,0.6);
liq("#s3-m1-liq",T[2]+0.9); liq("#s3-m2-liq",T[2]+1.4); liq("#s3-m3-liq",T[2]+1.9);
write("#s3-b1",T[2]+0.1,0.7); hl("#s3-b-hl",T[2]+0.8); write("#s3-b2",T[2]+1.4,0.6); write("#s3-b3",T[2]+2.3,0.8);
write("#s3-k",T[3]+0.1,0.6); write("#s3-k2",T[3]+0.8,0.6); hl("#s3-k-hl",T[3]+1.4,0.45);
"""
    return svg, html, js


@scene
def s4():
    svg = f"""
<g id="s4-wing" transform="translate(310,420) scale(1.7)">
<path class="ln ink" pathLength="1" stroke-width="5" d="{AIRFOIL}" id="s4-af"/>
<path class="ln pk" pathLength="1" stroke-width="10" stroke-linecap="round" opacity=".7" d="{AIRFOIL_TOP}" id="s4-ext"/>
<path class="ln bl" pathLength="1" stroke-width="10" stroke-linecap="round" opacity=".7" d="{AIRFOIL_BOT}" id="s4-int"/>
<path class="ln inkp" pathLength="1" stroke-width="4" stroke-dasharray="1 1" d="M0,80 L760,90" id="s4-chord"/>
</g>
<path class="ln ink" pathLength="1" stroke-width="3" d="M300,566 L250,700" id="s4-le-lead"/>
<path class="ln ink" pathLength="1" stroke-width="3" d="M1606,576 L1640,700" id="s4-te-lead"/>
<g id="s4-top" transform="translate(760,540) rotate(90) scale(0.85)">{PLANE_TOP}</g>
<path class="ln inkp" pathLength="1" stroke-width="3" stroke-dasharray="1 1" d="M480,700 L480,910 M1040,700 L1040,910" id="s4-ext-l"/>
{arrow(500, 885, 1020, 885, "pk", 6, 28, "s4-span1")}
{arrow(1020, 885, 500, 885, "pk", 6, 28, "s4-span2")}
"""
    html = (title("s4", "3 · El perfil del ala")
            + text("s4-le", 160, 700, "Borde de ataque", "lbl")
            + text("s4-te", 1420, 700, "Borde de salida", "lbl")
            + text("s4-ex", 760, 300, mark("Extradós", "pink", "s4-ex-hl") + " (arriba)", "lbl")
            + text("s4-in", 760, 640, mark("Intradós", "blue", "s4-in-hl") + " (abajo)", "lbl")
            + text("s4-ch", 900, 472, "cuerda", "sm", "color:#5a3fb0")
            + text("s4-sp", 1100, 840, mark("Envergadura", "pink", "s4-sp-hl"), "lbl")
            + text("s4-sp2", 1100, 912, "de punta a punta", "sm"))
    js = """
write("#s4-title",T[0]+0.2,0.9); hl("#s4-title-hl",T[0]+1.1);
draw("#s4-af",T[0]+0.6,1.8);
draw("#s4-le-lead",T[1]+0.2,0.4); write("#s4-le",T[1]+0.5,0.9);
draw("#s4-te-lead",T[1]+2.0,0.4); write("#s4-te",T[1]+2.3,0.9);
draw("#s4-ext",T[2]+0.2,1.0); write("#s4-ex",T[2]+0.4,0.9); hl("#s4-ex-hl",T[2]+1.3);
draw("#s4-int",T[2]+1.9,1.0); write("#s4-in",T[2]+2.1,0.9); hl("#s4-in-hl",T[2]+3.0);
draw("#s4-chord",T[3]+0.6,1.0); write("#s4-ch",T[3]+1.2,0.5);
tl.to(q("#s4-wing, #s4-le, #s4-te, #s4-ex, #s4-in, #s4-ch, #s4-le-lead, #s4-te-lead"),{opacity:0,duration:0.4,ease:"none"},T[4]-0.3);
draw("#s4-top .ln",T[4]+0.1,1.2);
draw("#s4-ext-l",T[4]+1.0,0.4); draw("#s4-span1 .shaft",T[4]+1.2,0.6); draw("#s4-span1 .head",T[4]+1.7,0.2); draw("#s4-span2 .head",T[4]+1.2,0.2);
write("#s4-sp",T[4]+1.4,0.8); hl("#s4-sp-hl",T[4]+2.2); write("#s4-sp2",T[4]+2.4,0.8);
"""
    return svg, html, js


@scene
def s5():
    ups = ["M120,470 C300,470 400,420 820,410 C1150,405 1400,470 1780,500",
           "M120,380 C320,380 420,340 820,330 C1150,325 1400,390 1780,420"]
    los = ["M120,660 C300,660 400,700 820,700 C1150,700 1400,672 1780,660",
           "M120,760 C300,760 420,790 820,790 C1150,790 1400,770 1780,760"]
    svg = f"""
<g id="s5-lines">
{''.join(f'<path class="s5-up bl" fill="none" stroke-width="4" stroke-linecap="round" stroke-dasharray="16 28" d="{d}"/>' for d in ups)}
{''.join(f'<path class="s5-lo bl" fill="none" stroke-width="4" stroke-linecap="round" stroke-dasharray="16 28" d="{d}"/>' for d in los)}
</g>
<g transform="translate(380,500) scale(1.5)"><path class="ink" fill="#fdfdff" stroke-width="5" d="{AIRFOIL}"/></g>
{arrow(990, 540, 990, 190, "pk", 10, 44, "s5-lift")}
"""
    html = (title("s5", "4 · La sustentación", "blue")
            + text("s5-fast", 1240, 250, "arriba: " + mark("más rápido", "blue", "s5-fast-hl"), "lbl")
            + text("s5-m1", 640, 300, "−", "big", "color:#ff3d96;font-size:170px")
            + text("s5-m2", 880, 286, "−", "big", "color:#ff3d96;font-size:170px")
            + text("s5-m3", 1300, 302, "−", "big", "color:#ff3d96;font-size:170px")
            + text("s5-lowp", 1240, 320, mark("menos presión", "pink", "s5-lowp-hl"), "lbl")
            + text("s5-p1", 620, 720, "+", "big", "color:#1ea7e4;font-size:150px")
            + text("s5-p2", 900, 720, "+", "big", "color:#1ea7e4;font-size:150px")
            + text("s5-p3", 1240, 700, "+", "big", "color:#1ea7e4;font-size:150px")
            + text("s5-slow", 260, 860, "abajo: más lento → " + mark("más presión", "blue", "s5-slow-hl"), "lbl")
            + text("s5-L", 1040, 170, mark("SUSTENTACIÓN", "pink", "s5-L-hl") + " (Lift)", "lbl"))
    js = """
write("#s5-title",T[0]+0.1,0.9); hl("#s5-title-hl",T[0]+1.0);
show("#s5-lines",T[0]+0.6,0.6);
tl.fromTo(q(".s5-up"),{strokeDashoffset:0},{strokeDashoffset:-44*Math.round(D*3.4),duration:D,ease:"none"},0);
tl.fromTo(q(".s5-lo"),{strokeDashoffset:0},{strokeDashoffset:-44*Math.round(D*1.5),duration:D,ease:"none"},0);
write("#s5-fast",T[0]+2.8,0.9); hl("#s5-fast-hl",T[0]+3.7);
const pop=(s,t)=>tl.fromTo(q(s),{scale:0.2,opacity:0},{scale:1,opacity:1,duration:0.35,ease:"back.out(2)"},t);
pop("#s5-m1",T[1]+1.4); pop("#s5-m2",T[1]+1.65); pop("#s5-m3",T[1]+1.9);
write("#s5-lowp",T[1]+2.0,0.8); hl("#s5-lowp-hl",T[1]+2.8);
pop("#s5-p1",T[2]+0.9); pop("#s5-p2",T[2]+1.15); pop("#s5-p3",T[2]+1.4);
write("#s5-slow",T[2]+0.4,1.4); hl("#s5-slow-hl",T[2]+1.9);
draw("#s5-lift .shaft",T[3]+0.6,1.2,"power2.out"); draw("#s5-lift .head",T[3]+1.7,0.3);
write("#s5-L",T[3]+2.9,0.9); hl("#s5-L-hl",T[3]+3.7,0.45);
"""
    return svg, html, js


@scene
def s6():
    # leading edge pinned at (520,560); scale 1.4
    swirl = "M1150,690 c20,-30 50,-10 40,10 c-10,22 -40,10 -30,-10 M1260,720 c22,-32 54,-10 44,12 c-10,24 -44,10 -32,-12 M1370,755 c22,-30 52,-8 42,12 c-10,22 -40,8 -30,-12"
    svg = f"""
{arrow(150, 480, 400, 480, "bl", 5, 24, "s6-w1")}{arrow(150, 560, 400, 560, "bl", 5, 24, "s6-w2")}{arrow(150, 640, 400, 640, "bl", 5, 24, "s6-w3")}
<path class="ln inkp" pathLength="1" stroke-width="3" stroke-dasharray="1 1" d="M520,560 L1620,560" id="s6-ref"/>
<g id="s6-rot"><g transform="translate(520,448) scale(1.4)">
<path class="ln ink" pathLength="1" stroke-width="5" fill="#fdfdff" d="{AIRFOIL}" id="s6-af"/>
<path class="inkp" fill="none" stroke-width="3" stroke-dasharray="10 10" d="M0,80 L760,90"/>
</g></g>
<path class="ln pk" pathLength="1" stroke-width="5" fill="none" d="M880,560 A360,360 0 0 1 858.3,683.1" id="s6-arc"/>
<path class="ln pk" pathLength="1" stroke-width="5" d="{swirl}" id="s6-swirl"/>
<g id="s6-liftg">{arrow(912, 500, 912, 230, "pk", 10, 40, "s6-lift")}</g>
"""
    html = (title("s6", "5 · Ángulo de ataque")
            + text("s6-wind", 120, 680, "viento relativo", "sm")
            + text("s6-alpha", 900, 590, "α", "lbl", "color:#ff3d96")
            + text("s6-def", 200, 820, mark("α", "pink", "s6-def-hl") + " = ángulo entre la cuerda y el viento", "lbl")
            + text("s6-more", 1060, 220, "+ ángulo → + sustentación", "lbl")
            + text("s6-stall", 1060, 310, mark("ENTRADA EN PÉRDIDA", "pink", "s6-stall-hl"), "lbl"))
    js = """
write("#s6-title",T[0]+0.1,0.9); hl("#s6-title-hl",T[0]+1.0);
draw("#s6-w1 path, #s6-w2 path, #s6-w3 path",T[0]+0.5,0.5); write("#s6-wind",T[0]+0.9,0.7);
draw("#s6-af",T[0]+0.6,1.2); draw("#s6-ref",T[0]+1.6,0.6);
const rot=(a,t,d)=>tl.to(q("#s6-rot"),{rotation:a,svgOrigin:"520 560",duration:d,ease:"power2.inOut"},t);
tl.set(q("#s6-rot"),{rotation:0,svgOrigin:"520 560"},0);
tl.set(q("#s6-arc"),{strokeDashoffset:1},0);
const arc=(a,t,d)=>tl.to(q("#s6-arc"),{strokeDashoffset:1-a/20,duration:d,ease:"power2.inOut"},t);
rot(6,T[0]+2.4,0.9); arc(6,T[0]+2.4,0.9); show("#s6-alpha",T[0]+3.0);
write("#s6-def",T[0]+2.6,1.6); hl("#s6-def-hl",T[0]+4.2,0.3);
tl.set(q("#s6-liftg"),{scaleY:0.55,svgOrigin:"912 500"},0);
draw("#s6-lift path",T[1]+0.1,0.5);
rot(12,T[1]+0.5,1.0); arc(12,T[1]+0.5,1.0);
tl.to(q("#s6-liftg"),{scaleY:1,svgOrigin:"912 500",duration:1.0,ease:"power2.out"},T[1]+0.7);
write("#s6-more",T[1]+1.0,1.0);
rot(18,T[2]+1.4,1.0); arc(18,T[2]+1.4,1.0);
draw("#s6-swirl",T[2]+2.6,1.0);
tl.to(q("#s6-liftg"),{scaleY:0.3,svgOrigin:"912 500",duration:0.8,ease:"power2.in"},T[2]+3.2);
tl.to(q("#s6-lift path"),{opacity:0.35,duration:0.5},T[2]+3.6);
write("#s6-stall",T[2]+4.2,0.9); hl("#s6-stall-hl",T[2]+5.1,0.4);
"""
    return svg, html, js


@scene
def s7():
    svg = f"""
<g id="s7-move"><g transform="translate(670,452) scale(1.3)">{PLANE_SIDE}</g></g>
{arrow(1060, 500, 1060, 250, "bl", 9, 40, "s7-L")}
{arrow(1060, 640, 1060, 900, "ink", 9, 40, "s7-W")}
{arrow(660, 572, 370, 572, "pk", 9, 40, "s7-T")}
{arrow(1480, 572, 1740, 572, "inkp", 9, 40, "s7-D")}
"""
    html = (title("s7", "6 · Las cuatro fuerzas", "blue")
            + text("s7-tL", 1100, 256, mark("Sustentación", "blue", "s7-tL-hl") + " (Lift)", "lbl")
            + text("s7-tW", 1100, 836, "Peso (Weight)", "lbl")
            + text("s7-tT", 300, 610, mark("Empuje", "pink", "s7-tT-hl") + " (Thrust)", "lbl")
            + text("s7-tD", 1440, 610, "Resistencia (Drag)", "lbl")
            + text("s7-dn", 1440, 680, "la crea el propio", "sm") + text("s7-dn2", 1440, 732, "cuerpo del avión", "sm")
            + text("s7-r1", 200, 760, "Sustentación > Peso", "lbl")
            + text("s7-r2", 200, 836, "Empuje > Resistencia", "lbl"))
    js = """
write("#s7-title",T[0]+0.1,1.0); hl("#s7-title-hl",T[0]+1.1);
draw("#s7-move .ln",T[0]+0.4,1.4);
draw("#s7-L path",T[1]+0.1,0.6); write("#s7-tL",T[1]+0.5,0.8); hl("#s7-tL-hl",T[1]+1.3);
draw("#s7-W path",T[1]+1.6,0.6); write("#s7-tW",T[1]+2.0,0.8);
draw("#s7-T path",T[2]+0.1,0.6); write("#s7-tT",T[2]+0.6,0.8); hl("#s7-tT-hl",T[2]+1.4);
draw("#s7-D path",T[2]+2.4,0.6); write("#s7-tD",T[2]+2.8,0.9);
write("#s7-dn",T[3]+1.0,0.8); write("#s7-dn2",T[3]+1.8,0.8);
tl.to(q("#s7-move .ink"),{stroke:"#ff3d96",duration:0.3,yoyo:true,repeat:1},T[3]+1.4);
tl.set(q("#s7-L"),{svgOrigin:"1060 500"},0); tl.set(q("#s7-T"),{svgOrigin:"660 572"},0);
tl.to(q("#s7-L"),{scale:1.25,svgOrigin:"1060 500",duration:0.8,ease:"power2.out"},T[4]+1.0);
tl.to(q("#s7-T"),{scale:1.25,svgOrigin:"660 572",duration:0.8,ease:"power2.out"},T[4]+2.6);
tl.to(q("#s7-move"),{x:-40,y:-50,duration:2.4,ease:"power1.inOut"},T[4]+1.2);
write("#s7-r1",T[4]+1.0,0.9); write("#s7-r2",T[4]+2.6,0.9);
"""
    return svg, html, js


@scene
def s8():
    svg = f"""
<g id="s8-fr"><g id="s8-frr"><g transform="translate(960,560)">{PLANE_FRONT}
<path class="ln pk" pathLength="1" stroke-width="12" stroke-linecap="round" d="M-460,-19 L-370,-12 M460,-19 L370,-12" id="s8-ail"/></g></g>
<circle id="s8-ax1" cx="960" cy="560" r="12" fill="#ff3d96"/></g>
<g id="s8-sd"><g id="s8-sdr"><g transform="translate(540,450) scale(1.4)">{PLANE_SIDE}
<path class="ln pk" pathLength="1" stroke-width="9" stroke-linecap="round" d="M548,80 L586,76" id="s8-elev"/></g></g>
<circle id="s8-ax2" cx="960" cy="590" r="12" fill="#ff3d96"/></g>
<g id="s8-tp"><g id="s8-tpr"><g transform="translate(960,560) scale(0.95)">{PLANE_TOP}
<path class="ln pk" pathLength="1" stroke-width="12" stroke-linecap="round" d="M300,0 L344,0" id="s8-rud"/></g></g>
<circle id="s8-ax3" cx="960" cy="560" r="12" fill="#ff3d96"/></g>
"""
    html = (title("s8", "7 · Ejes y mandos primarios")
            # roll
            + text("s8-r1", 1300, 250, mark("ALABEO", "pink", "s8-r1-hl") + " (Roll)", "lbl")
            + text("s8-r2", 200, 780, "eje longitudinal", "lbl") + text("s8-r3", 200, 846, "morro → cola", "sm")
            + text("s8-r4", 1300, 780, "alerones", "lbl")
            # pitch
            + text("s8-p1", 1300, 250, mark("CABECEO", "pink", "s8-p1-hl") + " (Pitch)", "lbl")
            + text("s8-p2", 200, 780, "eje transversal", "lbl") + text("s8-p3", 200, 846, "de ala a ala", "sm")
            + text("s8-p4", 1300, 780, "timón de profundidad", "lbl")
            # yaw
            + text("s8-y1", 1300, 250, mark("GUIÑADA", "pink", "s8-y1-hl") + " (Yaw)", "lbl")
            + text("s8-y2", 200, 780, "eje vertical", "lbl")
            + text("s8-y4", 1300, 780, "timón de dirección", "lbl") + text("s8-y5", 1300, 846, "→ con los pedales", "sm")
            # summary
            + text("s8-s0", 200, 300, mark("Mandos primarios", "blue", "s8-s0-hl"), "lbl")
            + text("s8-s1", 240, 420, "Alerones → alabeo (roll)", "lbl")
            + text("s8-s2", 240, 520, "Timón de profundidad → cabeceo (pitch)", "lbl")
            + text("s8-s3", 240, 620, "Timón de dirección → guiñada (yaw)", "lbl"))
    js = """
write("#s8-title",T[0]+0.1,1.1); hl("#s8-title-hl",T[0]+1.2);
// roll — front view
draw("#s8-fr .ln:not(#s8-ail)",T[0]+0.8,1.4); show("#s8-ax1",T[1]+0.6);
write("#s8-r2",T[1]+0.6,0.8); write("#s8-r3",T[1]+1.4,0.6);
tl.set(q("#s8-frr"),{svgOrigin:"960 560",rotation:0},0);
tl.to(q("#s8-frr"),{rotation:-14,svgOrigin:"960 560",duration:0.9,ease:"sine.inOut"},T[1]+2.0)
  .to(q("#s8-frr"),{rotation:12,svgOrigin:"960 560",duration:1.4,ease:"sine.inOut"},T[1]+2.9)
  .to(q("#s8-frr"),{rotation:0,svgOrigin:"960 560",duration:0.9,ease:"sine.inOut"},T[1]+4.3);
write("#s8-r1",T[1]+2.0,0.8); hl("#s8-r1-hl",T[1]+2.8);
draw("#s8-ail",T[1]+3.6,0.5); write("#s8-r4",T[1]+3.8,0.7);
hide("#s8-fr, #s8-r1, #s8-r2, #s8-r3, #s8-r4",T[2]-0.4,0.35);
// pitch — side view
draw("#s8-sd .ln:not(#s8-elev)",T[2]+0.0,1.2); show("#s8-ax2",T[2]+1.4,0.3);
write("#s8-p2",T[2]+1.2,0.8); write("#s8-p3",T[2]+2.0,0.6);
tl.set(q("#s8-sdr"),{svgOrigin:"960 590",rotation:0},0);
tl.to(q("#s8-sdr"),{rotation:9,svgOrigin:"960 590",duration:0.9,ease:"sine.inOut"},T[2]+2.4)
  .to(q("#s8-sdr"),{rotation:-7,svgOrigin:"960 590",duration:1.3,ease:"sine.inOut"},T[2]+3.3)
  .to(q("#s8-sdr"),{rotation:0,svgOrigin:"960 590",duration:0.9,ease:"sine.inOut"},T[2]+4.6);
write("#s8-p1",T[2]+2.4,0.8); hl("#s8-p1-hl",T[2]+3.2);
draw("#s8-elev",T[2]+3.6,0.4); write("#s8-p4",T[2]+3.8,1.0);
hide("#s8-sd, #s8-p1, #s8-p2, #s8-p3, #s8-p4",T[3]-0.4,0.35);
// yaw — top view
draw("#s8-tp .ln:not(#s8-rud)",T[3]+0.0,1.2); show("#s8-ax3",T[3]+1.0);
write("#s8-y2",T[3]+0.9,0.8);
tl.set(q("#s8-tpr"),{svgOrigin:"960 560",rotation:0},0);
tl.to(q("#s8-tpr"),{rotation:-12,svgOrigin:"960 560",duration:0.9,ease:"sine.inOut"},T[3]+1.8)
  .to(q("#s8-tpr"),{rotation:10,svgOrigin:"960 560",duration:1.3,ease:"sine.inOut"},T[3]+2.7)
  .to(q("#s8-tpr"),{rotation:0,svgOrigin:"960 560",duration:0.9,ease:"sine.inOut"},T[3]+4.0);
write("#s8-y1",T[3]+1.8,0.8); hl("#s8-y1-hl",T[3]+2.6);
draw("#s8-rud",T[3]+3.0,0.4); write("#s8-y4",T[3]+3.1,0.9); write("#s8-y5",T[3]+4.2,0.8);
hide("#s8-tp, #s8-y1, #s8-y2, #s8-y4, #s8-y5",T[4]-0.4,0.35);
// summary
write("#s8-s0",T[4]+0.0,0.8); hl("#s8-s0-hl",T[4]+0.8);
write("#s8-s1",T[4]+0.3,0.9); write("#s8-s2",T[4]+1.4,1.2); write("#s8-s3",T[4]+2.8,1.1);
"""
    return svg, html, js


@scene
def s9():
    body = "M120,140 C120,95 200,70 330,66 C480,64 600,95 640,118 L640,152 C560,160 440,166 330,168 C220,170 120,165 120,140 Z"
    slat = "M106,150 C90,108 140,70 214,63 L216,78 C162,86 126,112 122,150 Z"
    flap = "M646,120 C700,128 760,144 800,160 C760,162 700,158 646,152 Z"
    svg = f"""
<g transform="translate(220,330) scale(1.6)">
<path class="ln ink" pathLength="1" stroke-width="5" fill="#fdfdff" d="{body}" id="s9-body"/>
<g id="s9-flap"><path class="ln ink" pathLength="1" stroke-width="5" fill="#fdfdff" d="{flap}"/>
<path id="s9-tab" class="ln pk" pathLength="1" stroke-width="7" stroke-linecap="round" d="M800,160 L836,166"/></g>
<path id="s9-slat" class="ln ink" pathLength="1" stroke-width="5" fill="#fdfdff" d="{slat}"/>
<path id="s9-spoiler" class="ln pk" pathLength="1" stroke-width="9" stroke-linecap="round" d="M498,80 L590,94"/>
</g>
"""
    html = (title("s9", "8 · Mandos secundarios", "blue")
            + text("s9-f1", 1160, 690, mark("Flaps", "blue", "s9-f-hl") + " · borde de salida", "lbl")
            + text("s9-f2", 1160, 760, "+ curvatura → + sustentación", "sm") + text("s9-f3", 1160, 812, "a poca velocidad", "sm")
            + text("s9-s1", 160, 690, mark("Slats", "blue", "s9-s-hl") + " · borde de ataque", "lbl")
            + text("s9-s2", 160, 760, "volar más despacio", "sm") + text("s9-s3", 160, 812, "sin entrar en pérdida", "sm")
            + text("s9-p1", 900, 250, mark("Spoilers", "pink", "s9-p-hl") + " · freno aerodinámico", "lbl")
            + text("s9-c1", 1160, 880, mark("Compensadores", "pink", "s9-c-hl"), "lbl")
            + text("s9-c2", 1160, 950, "alivian la fuerza en los mandos", "sm"))
    js = """
write("#s9-title",T[0]+0.1,1.0); hl("#s9-title-hl",T[0]+1.1);
draw("#s9-body",T[0]+0.5,1.4); draw("#s9-slat",T[0]+1.3,0.8); draw("#s9-flap .ln:not(#s9-tab)",T[0]+1.6,0.8); draw("#s9-spoiler",T[0]+2.2,0.4); draw("#s9-tab",T[0]+2.5,0.3);
tl.set(q("#s9-flap"),{transformOrigin:"0% 0%",rotation:0},0);
tl.to(q("#s9-flap"),{rotation:16,x:10,y:4,transformOrigin:"0% 0%",duration:1.2,ease:"power2.inOut"},T[1]+1.4);
write("#s9-f1",T[1]+0.3,0.9); hl("#s9-f-hl",T[1]+1.2); write("#s9-f2",T[1]+2.4,1.0); write("#s9-f3",T[1]+4.0,0.7);
tl.to(q("#s9-slat"),{x:-26,y:22,rotation:-14,transformOrigin:"100% 0%",duration:1.2,ease:"power2.inOut"},T[2]+1.0);
write("#s9-s1",T[2]+0.3,0.9); hl("#s9-s-hl",T[2]+1.2); write("#s9-s2",T[2]+2.0,0.8); write("#s9-s3",T[2]+3.0,0.9);
tl.fromTo(q("#s9-spoiler"),{rotation:0,transformOrigin:"0% 0%"},{rotation:-32,transformOrigin:"0% 0%",duration:0.8,ease:"back.out(1.6)"},T[3]+0.8);
write("#s9-p1",T[3]+0.6,1.1); hl("#s9-p-hl",T[3]+1.7);
tl.fromTo(q("#s9-tab"),{rotation:0,transformOrigin:"0% 50%"},{rotation:-24,transformOrigin:"0% 50%",duration:0.7,ease:"power2.inOut"},T[4]+1.2);
write("#s9-c1",T[4]+0.4,0.9); hl("#s9-c-hl",T[4]+1.3); write("#s9-c2",T[4]+2.2,1.2);
"""
    return svg, html, js


@scene
def s10():
    svg = f"""
<path class="ink" fill="none" stroke-width="4" d="M0,790 L1920,790"/>
<path id="s10-dash" class="ink" fill="none" stroke-width="5" stroke-dasharray="70 60" d="M0,822 L1920,822"/>
<g id="s10-lift"><g id="s10-rot"><g transform="translate(640,614) scale(1.2)">{PLANE_SIDE}{GEAR}
<path class="pk" fill="none" stroke-width="5" stroke-linecap="round" d="M346,140 L362,154 M98,98 L84,110"/></g></g></g>
<path class="ink" fill="none" stroke-width="4" d="M1000,330 L1720,330 L1720,380 L1000,380 Z"/>
<rect id="s10-speed" x="1000" y="330" width="720" height="50" fill="rgba(66,188,240,.55)"/>
<path class="ln pk" pathLength="1" stroke-width="5" d="M1432,312 L1432,398" id="s10-m1"/>
<path class="ln pk" pathLength="1" stroke-width="5" d="M1504,312 L1504,398" id="s10-m2"/>
<path class="ln pk" pathLength="1" stroke-width="5" d="M1612,312 L1612,398" id="s10-m3"/>
"""
    html = (title("s10", "9 · El despegue")
            + text("s10-vel", 1000, 250, "velocidad", "sm")
            + text("s10-k1", 1400, 404, "V1", "lbl", "color:#ff3d96")
            + text("s10-k2", 1478, 404, "VR", "lbl", "color:#ff3d96")
            + text("s10-k3", 1590, 404, "V2", "lbl", "color:#ff3d96")
            + text("s10-fl", 200, 880, "flaps y slats extendidos", "sm")
            + text("s10-d1", 200, 290, mark("V1", "pink", "s10-d1-hl") + " · decisión: ya no se interrumpe", "lbl")
            + text("s10-d2", 200, 370, mark("VR", "pink", "s10-d2-hl") + " · rotación: morro arriba", "lbl")
            + text("s10-d3", 200, 450, mark("V2", "pink", "s10-d3-hl") + " · seguridad: asciende", "lbl"))
    js = """
write("#s10-title",T[0]+0.1,0.9); hl("#s10-title-hl",T[0]+1.0);
write("#s10-vel",T[0]+1.2,0.6);
tl.fromTo(q("#s10-speed"),{scaleX:0,transformOrigin:"0% 50%"},{scaleX:0.6,duration:T[2]+0.6-T[1],ease:"power1.in"},T[1]);
tl.to(q("#s10-speed"),{scaleX:0.7,duration:T[3]+0.4-(T[2]+0.6),ease:"none"},T[2]+0.6);
tl.to(q("#s10-speed"),{scaleX:0.85,duration:T[4]+0.6-(T[3]+0.4),ease:"none"},T[3]+0.4);
tl.to(q("#s10-speed"),{scaleX:0.92,duration:D-(T[4]+0.6),ease:"none"},T[4]+0.6);
tl.fromTo(q("#s10-dash"),{strokeDashoffset:0},{strokeDashoffset:-6500,duration:D-T[1],ease:"power1.in"},T[1]);
write("#s10-fl",T[1]+1.4,1.0);
draw("#s10-m1",T[2]+0.5,0.3); write("#s10-k1",T[2]+0.6,0.3);
write("#s10-d1",T[2]+0.8,1.4); hl("#s10-d1-hl",T[2]+1.0,0.3);
draw("#s10-m2",T[3]+0.3,0.3); write("#s10-k2",T[3]+0.4,0.3);
write("#s10-d2",T[3]+0.6,1.2); hl("#s10-d2-hl",T[3]+0.8,0.3);
tl.set(q("#s10-rot"),{svgOrigin:"1108 790",rotation:0},0);
tl.to(q("#s10-rot"),{rotation:9,svgOrigin:"1108 790",duration:1.4,ease:"power2.inOut"},T[3]+1.6);
draw("#s10-m3",T[4]+0.5,0.3); write("#s10-k3",T[4]+0.6,0.3);
write("#s10-d3",T[4]+0.8,1.2); hl("#s10-d3-hl",T[4]+1.0,0.3);
tl.fromTo(q("#s10-lift"),{x:0,y:0},{x:-260,y:-330,duration:D-(T[4]+0.4),ease:"power2.in"},T[4]+0.4);
tl.to(q("#s10-fl"),{opacity:0,duration:0.3},T[4]+0.4);
"""
    return svg, html, js


@scene
def s11():
    svg = f"""
<g transform="translate(560,300) scale(1.05)"><path class="ln ink" pathLength="1" stroke-width="5" fill="#fdfdff" d="{AIRFOIL}" id="s11-af"/></g>
{arrow(960, 330, 960, 130, "pk", 9, 36, "s11-L")}
"""
    html = (text("s11-m", 760, 170, "−", "big", "color:#ff3d96;font-size:170px") + text("s11-m2", 1180, 180, "−", "big", "color:#ff3d96;font-size:170px")
            + text("s11-p", 840, 410, "+", "big", "color:#1ea7e4;font-size:150px") + text("s11-p2", 1100, 410, "+", "big", "color:#1ea7e4;font-size:150px")
            + text("s11-l1", 0, 620, "Los aviones vuelan por la", "big", "width:1920px;text-align:center")
            + text("s11-l2", 0, 760, mark("diferencia de presión", "pink", "s11-hl"), "big", "width:1920px;text-align:center"))
    js = """
draw("#s11-af",T[0]+0.2,1.0);
show("#s11-m, #s11-m2",T[0]+1.6,0.3); show("#s11-p, #s11-p2",T[0]+3.6,0.3);
draw("#s11-L path",T[0]+4.6,0.7);
write("#s11-l1",T[1]+0.1,1.2); write("#s11-l2",T[1]+1.2,1.1); hl("#s11-hl",T[1]+2.3,0.5);
"""
    return svg, html, js


# ---------------------------------------------------------------- assemble
order = list(SCENES)
starts, t = {}, 0.0
for sid in order:
    starts[sid] = round(t, 3)
    t += TIM[sid]["duration"]
TOTAL = round(t, 3)

for idx, sid in enumerate(order):
    svg, html, js = SCENES[sid]()
    d = TIM[sid]["duration"]
    enter = "" if idx == 0 else f'tl.fromTo(q(".stage"),{{x:{PAN}}},{{x:0,duration:{ENTER},ease:"power3.out"}},0);'
    exit_ = "" if idx == len(order) - 1 else f'tl.fromTo(q(".stage"),{{x:0}},{{x:-{PAN},duration:{EXIT},ease:"power3.in",immediateRender:false}},D-{EXIT});'
    page = f"""<template>
<style>{CSS}</style>
<div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
<div class="stage">
<svg class="dg" viewBox="0 0 1920 1080" stroke-linecap="round" stroke-linejoin="round" data-layout-ignore>{svg}</svg>
{html}
</div>
</div>
<script>
(function(){{
{JS_HELPERS.replace("__ID__", sid).replace("__T__", json.dumps(TIM[sid]["starts"])).replace("__D__", str(d))}
{enter}
{js}
{exit_}
tl.set({{}},{{}},D);
window.__timelines["{sid}"]=tl;
}})();
</script>
</template>
"""
    (ROOT / "compositions" / f"{sid}.html").write_text(page)

hosts, audio, pan_js = [], [], []
for idx, sid in enumerate(order):
    st, d = starts[sid], TIM[sid]["duration"]
    hosts.append(f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                 f'data-start="{st}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" '
                 f'data-width="1920" data-height="1080"></div>')
    audio.append(f'<audio id="vo-{sid}" class="clip" src="assets/voice/{sid}.wav" data-start="{st}" '
                 f'data-duration="{d}" data-track-index="2" data-volume="1"></audio>')
    if idx > 0:  # camera pans along the page across each cut
        k = idx
        pan_js.append(f'tl.fromTo("#paper",{{backgroundPositionX:"{-(2*k-2)*PAN}px"}},{{backgroundPositionX:"{-(2*k-1)*PAN}px",duration:{EXIT},ease:"power3.in",immediateRender:false}},{st-EXIT});')
        pan_js.append(f'tl.fromTo("#paper",{{backgroundPositionX:"{-(2*k-1)*PAN}px"}},{{backgroundPositionX:"{-(2*k)*PAN}px",duration:{ENTER},ease:"power3.out",immediateRender:false}},{st});')
        sfx = "whoosh-short" if idx % 2 else "whoosh"
        audio.append(f'<audio id="sfx-cut{idx}" class="clip" src="assets/sfx/{sfx}.mp3" data-start="{max(0, st-0.45):.3f}" '
                     f'data-duration="0.57" data-track-index="3" data-volume="0.22"></audio>')

# riser lands its peak (3.47 s into the file) on lift-off in the take-off scene
lift = starts["s10"] + TIM["s10"]["starts"][4] + 0.6
audio.append(f'<audio id="sfx-riser" class="clip" src="assets/sfx/riser.mp3" data-start="{lift-3.47:.3f}" '
             f'data-duration="4.4" data-track-index="4" data-volume="0.3" data-fade-out="0.8"></audio>')

index = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="assets/lib/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#fbfbfe}}
#root{{position:relative;width:1920px;height:1080px}}
#paper{{position:absolute;inset:0;background-color:#fbfbfe;
  background-image:linear-gradient(#d6deef 2px,transparent 2px),linear-gradient(90deg,#d6deef 2px,transparent 2px);
  background-size:46px 46px;background-position:0px 0px}}
#margin{{position:absolute;top:0;bottom:0;left:120px;width:3px;background:rgba(255,92,168,.35)}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
<div id="paper"></div>
{chr(10).join(hosts)}
{chr(10).join(audio)}
</div>
<script>
window.__timelines=window.__timelines||{{}};
const tl=gsap.timeline({{paused:true}});
{chr(10).join(pan_js)}
tl.set({{}},{{}},{TOTAL});
window.__timelines["main"]=tl;
</script>
</body>
</html>
"""
(ROOT / "index.html").write_text(index)
print("scenes", len(order), "total", TOTAL)
