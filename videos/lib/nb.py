"""Shared notebook look for every episode: CSS, JS helpers, drawings, assembly.

Every scene is a page of the same squared notebook: diagrams are drawn in blue
ink (SVG strokes revealed with stroke-dashoffset), handwritten labels are
revealed left to right (clip-path), key words get a highlighter swipe.
"""
import json, math, pathlib


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



# ---------------------------------------------------------------- assemble
def build(root, scenes, extra_audio=None):
    """scenes: ordered dict id -> fn() returning (svg, html, js). Writes the project."""
    root = pathlib.Path(root)
    tim = json.loads((root / "build/timings.json").read_text())
    (root / "compositions").mkdir(exist_ok=True)
    order = list(scenes)
    starts, t = {}, 0.0
    for sid in order:
        starts[sid] = round(t, 3)
        t += tim[sid]["duration"]
    total = round(t, 3)
    for idx, sid in enumerate(order):
        svg, html, js = scenes[sid]()
        d = tim[sid]["duration"]
        enter = "" if idx == 0 else f'tl.fromTo(q(".stage"),{{x:{PAN}}},{{x:0,duration:{ENTER},ease:"power3.out"}},0);'
        exit_ = "" if idx == len(order) - 1 else f'tl.fromTo(q(".stage"),{{x:0}},{{x:-{PAN},duration:{EXIT},ease:"power3.in",immediateRender:false}},D-{EXIT});'
        helpers = JS_HELPERS.replace("__ID__", sid).replace("__T__", json.dumps(tim[sid]["starts"])).replace("__D__", str(d))
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
{helpers}
{enter}
{js}
{exit_}
tl.set({{}},{{}},D);
window.__timelines["{sid}"]=tl;
}})();
</script>
</template>
"""
        (root / "compositions" / f"{sid}.html").write_text(page)
    hosts, audio, pan_js = [], [], []
    for idx, sid in enumerate(order):
        st, d = starts[sid], tim[sid]["duration"]
        hosts.append(f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{st}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="1920" data-height="1080"></div>')
        audio.append(f'<audio id="vo-{sid}" class="clip" src="assets/voice/{sid}.wav" data-start="{st}" '
                     f'data-duration="{d}" data-track-index="2" data-volume="1"></audio>')
        if idx > 0:
            k = idx
            pan_js.append(f'tl.fromTo("#paper",{{backgroundPositionX:"{-(2*k-2)*PAN}px"}},{{backgroundPositionX:"{-(2*k-1)*PAN}px",duration:{EXIT},ease:"power3.in",immediateRender:false}},{st-EXIT});')
            pan_js.append(f'tl.fromTo("#paper",{{backgroundPositionX:"{-(2*k-1)*PAN}px"}},{{backgroundPositionX:"{-(2*k)*PAN}px",duration:{ENTER},ease:"power3.out",immediateRender:false}},{st});')
            sfx = "whoosh-short" if idx % 2 else "whoosh"
            audio.append(f'<audio id="sfx-cut{idx}" class="clip" src="assets/sfx/{sfx}.mp3" data-start="{max(0, st-0.45):.3f}" '
                         f'data-duration="0.57" data-track-index="3" data-volume="0.22"></audio>')
    if extra_audio:
        audio += extra_audio(starts, tim)
    index = INDEX.replace("__TOTAL__", str(total)).replace("__HOSTS__", "\n".join(hosts)).replace("__AUDIO__", "\n".join(audio)).replace("__PAN__", "\n".join(pan_js))
    (root / "index.html").write_text(index)
    print("scenes", len(order), "total", total)
    return starts, tim


INDEX = """<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="assets/lib/gsap.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#fbfbfe}
#root{position:relative;width:1920px;height:1080px}
#paper{position:absolute;inset:0;background-color:#fbfbfe;
  background-image:linear-gradient(#d6deef 2px,transparent 2px),linear-gradient(90deg,#d6deef 2px,transparent 2px);
  background-size:46px 46px;background-position:0px 0px}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="__TOTAL__" data-width="1920" data-height="1080">
<div id="paper"></div>
__HOSTS__
__AUDIO__
</div>
<script>
window.__timelines=window.__timelines||{};
const tl=gsap.timeline({paused:true});
__PAN__
tl.set({},{},__TOTAL__);
window.__timelines["main"]=tl;
</script>
</body>
</html>
"""


def new_project(root):
    """Create an episode folder with the shared assets and config copied from episode 1."""
    import shutil
    root = pathlib.Path(root); ep1 = root.parent / "ep1-como-vuela"
    (root / "build").mkdir(parents=True, exist_ok=True)
    for sub in ["assets/fonts", "assets/lib", "assets/sfx"]:
        shutil.copytree(ep1 / sub, root / sub, dirs_exist_ok=True)
    for f in ["hyperframes.json", ".gitignore"]:
        shutil.copy(ep1 / f, root / f)
    name = root.name
    (root / "meta.json").write_text(json.dumps({"id": name, "name": name}, indent=2))
    pkg = json.loads((ep1 / "package.json").read_text()); pkg["name"] = name
    (root / "package.json").write_text(json.dumps(pkg, indent=2))
