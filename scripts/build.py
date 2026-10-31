"""Build the profile: assets/*.svg and README.md from data/family.json.

    python scripts/update_data.py     # numbers from gh and the local checkouts
    python scripts/build.py           # SVGs and README

The SVGs are self-contained (no scripts, no web fonts, no external requests) and animate with
SMIL and CSS, which GitHub shows in an <img>. Only public repositories are drawn or linked.
"""
import json, math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "family.json").read_text(encoding="utf-8"))
OWNER = DATA["owner"]
T = DATA["totals"]

# Tokyo Night, the palette of the wkd site's TUI skin.
BG, BG2, LINE, FG, DIM = "#1a1b26", "#16161e", "#292e42", "#c0caf5", "#565f89"
BLUE, CYAN, GREEN, YELLOW, ORANGE, RED, PURPLE = "#7aa2f7", "#7dcfff", "#9ece6a", "#e0af68", "#ff9e64", "#f7768e", "#bb9af7"
CAT_COLOR = {"ai": PURPLE, "edit": GREEN, "navigate": CYAN, "inspect": ORANGE, "project": BLUE, "view": RED, "foundation": YELLOW}
MONO = "ui-monospace, 'JetBrains Mono', 'Cascadia Code', 'Fira Code', Consolas, 'DejaVu Sans Mono', monospace"
CHAR = 0.6  # width of a monospace character in em; textLength pins it on every system


def k(n):
    if n >= 100_000:
        return f"{round(n / 1000)}k"
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def svg(w, h, body, defs="", style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'font-family="{MONO}" role="img">\n<defs>{defs}</defs>\n<style>{style}</style>\n{body}\n</svg>\n')


def txt(x, y, s, size=14, fill=FG, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}" {extra}>{escape(s)}</text>')


# ---------------------------------------------------------------------------------------------- hero
def hero():
    W, H = 1000, 420
    n_plugins = T["plugins"]
    code = f'require("wkd").setup({{ plugins = {n_plugins}, desktop = 3, city = "Vienna" }})'
    size = 17
    cw = size * CHAR
    tw = len(code) * cw
    steps = ";".join(f"{i * cw:.1f}" for i in range(len(code) + 1))
    nsteps = len(code) + 1
    kt = "0;" + ";".join(f"{(i * 0.2 / nsteps + 0.08):.4f}" for i in range(nsteps)) + ";0.93;1"
    cur_x = ";".join(f"{84 + i * cw + 3:.1f}" for i in range(nsteps))
    # a small module graph on the right: nodes, edges, and a pulse travelling along each edge
    nodes = [(700, 150), (790, 118), (880, 160), (760, 215), (850, 250), (700, 285), (800, 320), (900, 330), (660, 215), (930, 230)]
    edges = [(0, 1), (1, 2), (0, 3), (1, 3), (3, 4), (2, 4), (3, 5), (4, 6), (5, 6), (6, 7), (4, 7), (0, 8), (8, 5), (2, 9), (9, 4)]
    cols = [BLUE, CYAN, PURPLE, GREEN, ORANGE, RED, YELLOW, CYAN, PURPLE, BLUE]
    g = []
    for i, (a, b) in enumerate(edges):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{LINE}" stroke-width="1.4"/>')
        g.append(f'<circle r="2.6" fill="{cols[a]}" filter="url(#glow)"><animateMotion dur="{3 + i % 4}s" begin="{(i * 0.43):.2f}s" '
                 f'repeatCount="indefinite" path="M{x1},{y1} L{x2},{y2}"/></circle>')
    for i, (x, y) in enumerate(nodes):
        g.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{BG}" stroke="{cols[i]}" stroke-width="1.8" filter="url(#glow)">'
                 f'<animate attributeName="r" values="8;11;8" dur="{3 + i * 0.37:.2f}s" repeatCount="indefinite"/></circle>')
        g.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{cols[i]}"/>')
    graph = "\n".join(g)
    stars = []
    for i in range(46):
        x = (i * 211) % 960 + 20
        y = (i * 137) % 330 + 45
        r = 0.7 + (i % 3) * 0.4
        stars.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{FG}" opacity="0.5"><animate attributeName="opacity" '
                     f'values="0.1;0.8;0.1" dur="{2 + (i % 5)}s" begin="{(i % 7) * 0.6}s" repeatCount="indefinite"/></circle>')
    gutter = "\n".join(txt(54, 118 + i * 30, str(i + 1), 13, DIM, anchor="end") for i in range(7))
    defs = f'''
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>
<linearGradient id="title" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="520" y2="0">
  <stop offset="0" stop-color="{BLUE}"/><stop offset="0.35" stop-color="{CYAN}"/><stop offset="0.7" stop-color="{PURPLE}"/><stop offset="1" stop-color="{RED}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-520 0;520 0" dur="7s" repeatCount="indefinite"/>
</linearGradient>
<radialGradient id="orbB"><stop offset="0" stop-color="{BLUE}" stop-opacity=".45"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="orbP"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".4"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
<radialGradient id="orbC"><stop offset="0" stop-color="{CYAN}" stop-opacity=".3"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="glowbig" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="win"><rect x="10" y="10" width="980" height="400" rx="16"/></clipPath>
<clipPath id="typed"><rect x="84" y="244" height="30" width="0"><animate attributeName="width" values="0;{steps};{tw:.1f};{tw:.1f}" keyTimes="{kt}" dur="14s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{LINE}" stroke-width=".5" opacity=".55"/></pattern>'''
    style = f"@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}} .cur{{animation:blink 1.06s steps(1) infinite}} text{{white-space:pre}}"
    body = f'''
<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
<g clip-path="url(#win)">
  <rect x="10" y="10" width="980" height="400" fill="url(#grid)"/>
  <circle cx="200" cy="120" r="230" fill="url(#orbB)"><animateTransform attributeName="transform" type="translate" values="0 0;60 30;0 0" dur="11s" repeatCount="indefinite"/></circle>
  <circle cx="800" cy="300" r="260" fill="url(#orbP)"><animateTransform attributeName="transform" type="translate" values="0 0;-70 -30;0 0" dur="13s" repeatCount="indefinite"/></circle>
  <circle cx="520" cy="60" r="190" fill="url(#orbC)"><animateTransform attributeName="transform" type="translate" values="0 0;40 50;0 0" dur="9s" repeatCount="indefinite"/></circle>
  {"".join(stars)}
  <rect x="10" y="10" width="980" height="40" fill="{BG2}" opacity=".92"/>
  <circle cx="38" cy="30" r="6.5" fill="{RED}"/><circle cx="60" cy="30" r="6.5" fill="{YELLOW}"/><circle cx="82" cy="30" r="6.5" fill="{GREEN}"/>
  {txt(500, 35, f"nvim  ·  {OWNER}/README.md", 13, DIM, anchor="middle")}
  <rect x="10" y="50" width="980" height="28" fill="{BG2}"/>
  <rect x="10" y="50" width="150" height="28" fill="{BG}"/><rect x="10" y="50" width="150" height="2" fill="{BLUE}"/>
  {txt(26, 69, "README.md", 12.5, FG)}{txt(178, 69, "wkd.lua", 12.5, DIM)}{txt(266, 69, "family.json", 12.5, DIM)}{txt(372, 69, "init.lua", 12.5, DIM)}
  {gutter}
  {txt(84, 118, "-- hello, world. I am", 14, DIM, extra='font-style="italic"')}
  <text x="80" y="206" font-size="92" font-weight="800" fill="url(#title)" filter="url(#glowbig)" textLength="500" lengthAdjust="spacingAndGlyphs">{OWNER}</text>
  {txt(84, 236, "-- Neovim plugin family  /  local-first desktop tools", 14, DIM, extra='font-style="italic"')}
  <g clip-path="url(#typed)"><text x="84" y="266" font-size="{size}" textLength="{tw:.1f}" lengthAdjust="spacing"><tspan fill="{PURPLE}">require</tspan><tspan fill="{FG}">(</tspan><tspan fill="{GREEN}">"wkd"</tspan><tspan fill="{FG}">).</tspan><tspan fill="{BLUE}">setup</tspan><tspan fill="{FG}">({{ </tspan><tspan fill="{ORANGE}">plugins</tspan><tspan fill="{FG}"> = </tspan><tspan fill="{ORANGE}">{n_plugins}</tspan><tspan fill="{FG}">, </tspan><tspan fill="{ORANGE}">desktop</tspan><tspan fill="{FG}"> = </tspan><tspan fill="{ORANGE}">3</tspan><tspan fill="{FG}">, </tspan><tspan fill="{ORANGE}">city</tspan><tspan fill="{FG}"> = </tspan><tspan fill="{GREEN}">"Vienna"</tspan><tspan fill="{FG}"> }})</tspan></text></g>
  <rect class="cur" x="87" y="250" width="10" height="20" fill="{CYAN}"><animate attributeName="x" values="87;{cur_x};{84 + tw + 3:.1f};{84 + tw + 3:.1f}" keyTimes="{kt}" dur="14s" calcMode="discrete" repeatCount="indefinite"/></rect>
  {graph}
  <rect x="10" y="372" width="980" height="38" fill="{BG2}"/>
  <path d="M10 372h112l14 19-14 19H10z" fill="{BLUE}"/>{txt(30, 396, "NORMAL", 13, BG, 700)}
  <path d="M122 372h150l14 19-14 19H122z" fill="{LINE}"/>{txt(140, 396, f" main  +{k(T['commits'])}", 13, FG)}
  {txt(304, 396, f"{OWNER}/README.md", 13, FG)}
  {txt(970, 396, f"{T['plugins']} plugins  {k(T['commits'])} commits  {k(T['lua_lines'])} lines of lua  {k(T['spec_files'])} specs", 12.5, DIM, anchor="end")}
</g>
<rect x="10" y="10" width="980" height="400" rx="16" fill="none" stroke="{LINE}" stroke-width="1.5"/>'''
    return svg(W, H, body, defs, style)


# ---------------------------------------------------------------------------------------------- family
def family():
    W = 1000
    colw, gap, top = 300, 26, 96
    cats = DATA["categories"]
    maxl = max(p["lua_lines"] for c in cats for p in c["plugins"])
    heads = [0, 0, 0]
    placed = []
    for c in sorted(cats, key=lambda c: -len(c["plugins"])):
        i = heads.index(min(heads))
        placed.append((c, i, heads[i]))
        heads[i] += 44 + len(c["plugins"]) * 30 + 24
    H = top + max(heads) + 34
    out, delay = [], 0.0
    for c, col, y0 in placed:
        x0 = 22 + col * (colw + gap)
        y0 += top
        color = CAT_COLOR[c["key"]]
        out.append(f'<g><rect x="{x0}" y="{y0}" width="{colw}" height="{44 + len(c["plugins"]) * 30}" rx="12" fill="{BG2}" stroke="{LINE}"/>'
                   f'<rect x="{x0}" y="{y0}" width="5" height="{44 + len(c["plugins"]) * 30}" rx="2.5" fill="{color}"/>'
                   f'{txt(x0 + 22, y0 + 27, c["label"].upper(), 13, color, 700, extra="letter-spacing=\"2\"")}'
                   f'{txt(x0 + colw - 16, y0 + 27, str(len(c["plugins"])), 13, DIM, anchor="end")}')
        for j, p in enumerate(c["plugins"]):
            y = y0 + 44 + j * 30
            frac = math.log(p["lua_lines"] + 1) / math.log(maxl + 1)
            bw = 60 * frac
            d = delay + j * 0.07
            out.append(
                f'<g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" begin="{d:.2f}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" values="-14 0;0 0" dur="0.5s" begin="{d:.2f}s" fill="freeze"/>'
                f'<circle cx="{x0 + 24}" cy="{y - 4}" r="3.4" fill="{color}"><animate attributeName="opacity" values="1;.35;1" dur="{2.4 + (j % 4) * .5}s" repeatCount="indefinite"/></circle>'
                f'{txt(x0 + 38, y, p["name"] if len(p["name"]) <= 21 else p["name"][:20] + "…", 13, FG)}'
                f'<rect x="{x0 + colw - 84}" y="{y - 9}" width="60" height="7" rx="3.5" fill="{LINE}"/>'
                f'<rect x="{x0 + colw - 84}" y="{y - 9}" width="0" height="7" rx="3.5" fill="{color}"><animate attributeName="width" values="0;{bw:.1f}" dur="1.1s" begin="{d + .3:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect>'
                f'</g>')
        out.append("</g>")
        delay += 0.35
    head = (f'{txt(22, 42, "THE .NVIM FAMILY", 22, FG, 800, extra="letter-spacing=\"4\"")}'
            f'{txt(22, 66, f"{T["plugins"]} public plugins  ·  bar = size of the Lua code, log scale  ·  all built on lib.nvim", 13, DIM)}'
            f'<rect x="22" y="76" width="956" height="1.5" fill="{LINE}"/><rect x="22" y="76" width="140" height="1.5" fill="{CYAN}">'
            f'<animate attributeName="x" values="22;838;22" dur="6s" repeatCount="indefinite"/></rect>')
    body = f'<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>{head}{"".join(out)}'
    return svg(W, H, body)


# ---------------------------------------------------------------------------------------------- native
def native():
    W, H = 1000, 352
    cards = [
        ("takt", "Rust · concept", "modular media suite", "Player, live studio, video editor and DAW on one shared core. Time is the hard part.", ORANGE, "wave"),
    ]
    cw, gap = 304, 22
    out = []
    for i, (name, lang, tag, desc, color, kind) in enumerate(cards):
        x = (W - len(cards) * cw - (len(cards) - 1) * gap) // 2 + i * (cw + gap)
        out.append(f'<g><rect x="{x}" y="64" width="{cw}" height="268" rx="14" fill="{BG2}" stroke="{LINE}"/>'
                   f'<rect x="{x}" y="64" width="{cw}" height="4" rx="2" fill="{color}"/>')
        # illustration
        ix, iy = x + 20, 84
        out.append(f'<rect x="{ix}" y="{iy}" width="{cw - 40}" height="86" rx="8" fill="{BG}" stroke="{LINE}"/>')
        if kind == "graph":
            pts = [(40, 60), (90, 25), (140, 55), (190, 28), (240, 62)]
            for a, b in zip(pts, pts[1:] + [pts[0]]):
                out.append(f'<line x1="{ix + a[0]}" y1="{iy + a[1] * 0.9}" x2="{ix + b[0]}" y2="{iy + b[1] * 0.9}" stroke="{color}" stroke-opacity=".4"/>')
            for j, (px, py) in enumerate(pts):
                out.append(f'<circle cx="{ix + px}" cy="{iy + py * .9}" r="6" fill="{BG}" stroke="{color}" stroke-width="1.6"><animate attributeName="r" values="5;8;5" dur="{2 + j * .4}s" repeatCount="indefinite"/></circle>')
        elif kind == "chat":
            for j, (w, yy, right) in enumerate([(120, 14, False), (150, 38, True), (90, 62, False)]):
                bx = ix + (cw - 40 - w - 14 if right else 14)
                out.append(f'<rect x="{bx}" y="{iy + yy}" width="{w}" height="16" rx="8" fill="{color if right else LINE}" opacity="{.85 if right else 1}">'
                           f'<animate attributeName="width" values="0;{w};{w}" keyTimes="0;.2;1" dur="5s" begin="{j * .8}s" repeatCount="indefinite"/></rect>')
        else:
            for j in range(26):
                hgt = 10 + 30 * abs(math.sin(j * .7)) * (0.5 + 0.5 * math.sin(j * .31))
                out.append(f'<rect x="{ix + 14 + j * 10}" y="{iy + 43 - hgt / 2:.1f}" width="6" height="{hgt:.1f}" rx="3" fill="{color}">'
                           f'<animate attributeName="height" values="{hgt:.1f};{hgt * .35 + 4:.1f};{hgt:.1f}" dur="{1.1 + (j % 5) * .17:.2f}s" repeatCount="indefinite"/>'
                           f'<animate attributeName="y" values="{iy + 43 - hgt / 2:.1f};{iy + 43 - (hgt * .35 + 4) / 2:.1f};{iy + 43 - hgt / 2:.1f}" dur="{1.1 + (j % 5) * .17:.2f}s" repeatCount="indefinite"/></rect>')
        out.append(txt(x + 20, 204, name, 20, FG, 800))
        out.append(f'<rect x="{x + 20}" y="214" width="{len(lang) * 7.6 + 18:.0f}" height="20" rx="10" fill="{color}" opacity=".18"/>{txt(x + 29, 228, lang, 12, color, 600)}')
        out.append(txt(x + 20, 256, tag, 13, color, 600))
        for j, line in enumerate(wrap(desc, 38)):
            out.append(txt(x + 20, 276 + j * 17, line, 12, DIM))
        out.append("</g>")
    head = (f'{txt(22, 42, "NATIVE", 22, FG, 800, extra="letter-spacing=\"4\"")}'
            f'{txt(22, 58, "", 1)}'
            f'{txt(978, 42, "local-first desktop tools", 13, DIM, anchor="end")}')
    return svg(W, H, f'<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>{head}{"".join(out)}')


def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur]


# ---------------------------------------------------------------------------------------------- stats
def stats():
    W, H = 1000, 270
    tiles = [
        (str(T["plugins"]), "public plugins", CYAN, .82),
        (k(T["commits"]), "commits", PURPLE, .9),
        (k(T["lua_lines"]), "lines of Lua", GREEN, .75),
        (k(T["spec_files"]), "spec files", ORANGE, .66),
    ]
    out = []
    tw, gap = 224, 20
    for i, (num, label, color, frac) in enumerate(tiles):
        x = 22 + i * (tw + gap)
        cx, cy, r = x + tw / 2, 108, 54
        circ = 2 * math.pi * r
        out.append(f'<g><rect x="{x}" y="22" width="{tw}" height="170" rx="14" fill="{BG2}" stroke="{LINE}"/>'
                   f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="7"/>'
                   f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round" '
                   f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}" transform="rotate(-90 {cx} {cy})" filter="url(#glow)">'
                   f'<animate attributeName="stroke-dashoffset" values="{circ:.1f};{circ * (1 - frac):.1f}" dur="1.6s" begin="{i * .25}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></circle>'
                   f'{txt(cx, cy + 9, num, 30, FG, 800, "middle")}{txt(cx, 182, label, 13, DIM, anchor="middle")}</g>')
    # commits per category as one stacked bar
    cats = DATA["categories"]
    per = [(c["label"], c["key"], sum(p["commits"] for p in c["plugins"])) for c in cats]
    total = sum(v for _, _, v in per)
    bx, by, bw = 22, 222, 956
    out.append(txt(bx, 214, "where the commits went", 12.5, DIM))
    x = bx
    for j, (label, key, v) in enumerate(per):
        w = bw * v / total
        out.append(f'<rect x="{x:.1f}" y="{by}" width="0" height="14" fill="{CAT_COLOR[key]}"><animate attributeName="width" values="0;{max(w - 3, 1):.1f}" dur="1.2s" begin="{.4 + j * .12:.2f}s" fill="freeze"/></rect>')
        if w > 70:
            out.append(txt(x + 2, by + 32, label, 11, CAT_COLOR[key]))
        x += w
    defs = '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    return svg(W, H, f'<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>{"".join(out)}', defs)


# ---------------------------------------------------------------------------------------------- footer
def footer():
    W, H = 1000, 150
    waves = []
    for i, (color, amp, dur, yy) in enumerate([(BLUE, 7, 9, 104), (PURPLE, 6, 12, 108), (CYAN, 5, 7, 112)]):
        def path(phase):
            pts = [f"{x},{yy + amp * math.sin((x / 1000) * 4 * math.pi + phase):.1f}" for x in range(0, 1001, 20)]
            return "M" + " L".join(pts) + f" L1000,150 L0,150 Z"
        waves.append(f'<path d="{path(0)}" fill="{color}" opacity=".16"><animate attributeName="d" dur="{dur}s" repeatCount="indefinite" '
                     f'values="{path(0)};{path(math.pi)};{path(2 * math.pi)}"/></path>')
    body = f'''<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>{"".join(waves)}
{txt(500, 40, "“Programs must be written for people to read,", 17, FG, anchor="middle", extra='font-style="italic"')}
{txt(500, 64, "and only incidentally for machines to execute.”", 17, FG, anchor="middle", extra='font-style="italic"')}
{txt(500, 88, "Harold Abelson", 13, DIM, anchor="middle")}
<rect x="0" y="118" width="1000" height="32" fill="{BG2}"/>
<path d="M0 118h96l14 16-14 16H0z" fill="{GREEN}"/>{txt(20, 140, "INSERT", 13, BG, 700)}
{txt(130, 140, ":wq", 13, FG)}{txt(980, 140, f"thanks for stopping by  ·  {OWNER}", 12.5, DIM, anchor="end")}'''
    return svg(W, H, body)


# ---------------------------------------------------------------------------------------------- readme
def desc(p):
    d = p["description"].replace("—", "-").replace("�", "-").strip()
    return d if len(d) < 170 else d[:167].rsplit(" ", 1)[0] + "..."


def readme():
    L = []
    L.append('<p align="center"><img src="assets/hero.svg" alt="WKDSteve - Neovim plugin family, desktop tools, Vienna" width="100%"></p>\n')
    L.append('<p align="center">\n'
             '  <a href="https://wkdsteve.github.io/wkd/"><img alt="wkd site" src="https://img.shields.io/badge/wkd-the%20plugin%20site-7dcfff?style=for-the-badge&labelColor=1a1b26"></a>\n'
             f'  <a href="https://github.com/{OWNER}?tab=repositories&q=.nvim"><img alt="plugins" src="https://img.shields.io/badge/.nvim-{T["plugins"]}%20plugins-bb9af7?style=for-the-badge&labelColor=1a1b26"></a>\n'
             '  <a href="https://www.linkedin.com/in/stefan-bartl"><img alt="LinkedIn" src="https://img.shields.io/badge/linkedin-stefan--bartl-7aa2f7?style=for-the-badge&labelColor=1a1b26&logo=linkedin"></a>\n'
             '  <a href="mailto:l.value.impl@gmail.com"><img alt="mail" src="https://img.shields.io/badge/mail-say%20hi-9ece6a?style=for-the-badge&labelColor=1a1b26"></a>\n'
             '</p>\n')
    L.append('<p align="center"><sub><a href="#the-nvim-family">the family</a> · <a href="#native">native</a> · <a href="#in-numbers">numbers</a> · <a href="#whoami">whoami</a></sub></p>\n')
    L.append("## Hi, I'm glad you're here\n")
    L.append("I live in **Neovim** and build for it: a family of small, tested, documented plugins that share one "
             "foundation (`lib.nvim`), plus **local-first desktop tools** next to them. Based in Vienna; "
             "CLI tools, web development and security are the rest of the day. Languages I reach for: "
             "Lua, TypeScript, Rust, Go, C++, and sometimes Zig or Lisp.\n")
    L.append("Everything is built with the same habits: one command per plugin (`:Git`, `:File`, `:Pickers` ...), "
             "no hidden shell calls, specs that fail without the fix, and docs that are checked by CI. "
             "The [**wkd site**](https://wkdsteve.github.io/wkd/) reads the plugin repositories themselves and shows "
             "them as a Neovim window (still growing, already pretty).\n")
    L.append('## The .nvim family\n')
    L.append('<p align="center"><img src="assets/family.svg" alt="The .nvim plugin family by category" width="100%"></p>\n')
    for c in DATA["categories"]:
        n = len(c["plugins"])
        L.append(f'<details>\n<summary><b>{c["label"]}</b> &nbsp;<sub>{n} plugin{"s" if n != 1 else ""}</sub></summary>\n\n<br>\n')
        L.append("| plugin | what it does |\n|---|---|")
        for p in c["plugins"]:
            star = f" ⭐{p['stars']}" if p["stars"] >= 3 else ""
            L.append(f"| [**{p['name']}**](https://github.com/{OWNER}/{p['name']}){star} | {desc(p)} |")
        L.append("\n</details>\n")
    L.append("## Native\n")
    L.append('<p align="center"><img src="assets/native.svg" alt="Native desktop tools" width="100%"></p>\n')
    L.append("Local web UIs and desktop apps that sit next to the editor plugins: "
             f"[**takt**](https://github.com/{OWNER}/takt) (media suite, concept stage). "
             "More of them exist and stay private for now.\n")
    L.append("## In numbers\n")
    L.append('<p align="center"><img src="assets/stats.svg" alt="Plugins, commits, lines of Lua, spec files" width="100%"></p>\n')
    L.append(f"<sub>Counted from the public repositories by <code>scripts/update_data.py</code>: {T['plugins']} plugins, "
             f"{T['commits']:,} commits, {T['lua_lines']:,} lines of Lua, {T['spec_files']:,} spec files.</sub>\n")
    L.append("## whoami\n")
    L.append("```ts\n"
             "type Mood = \"focused\" | \"curious\" | \"shipping\";\n\n"
             "const profile = {\n"
             "  nickname: \"lavalue\",\n"
             "  city: \"Vienna\",\n"
             "  editor: \"nvim\" as const,\n"
             "  mood: \"shipping\" as Mood,\n"
             f"  plugins: {T['plugins']},\n"
             "  languages: {\n"
             "    lua: \"plugins, scripting, the whole editor\",\n"
             "    rust: \"desktop hubs and tools that must not break\",\n"
             "    typescript: \"web UIs, the wkd site\",\n"
             "    go: \"small servers and CLIs\",\n"
             "    cpp: \"when control matters\",\n"
             "  },\n"
             "  security: [\"Wireshark\", \"HackRF One\", \"Metasploit\", \"firmware tools\"],\n"
             "  learning: [\"architecture\", \"OS internals\", \"more Go\"],\n"
             "  chat: \"Discord, happy to talk shop\",\n"
             "} as const;\n"
             "```\n")
    L.append("> **One thing I care about:** access to technology should be a given for everyone, and it is not. "
             "Our data is collected daily, often without our knowledge. Transparency and control over how information is used "
             "are worth fighting for: [netzpolitik.org](https://netzpolitik.org), get organized!\n")
    L.append('<p align="center"><img src="assets/footer.svg" alt=":wq" width="100%"></p>\n')
    return "\n".join(L)


def main():
    (ROOT / "assets").mkdir(exist_ok=True)
    for name, fn in [("hero", hero), ("family", family), ("native", native), ("stats", stats), ("footer", footer)]:
        (ROOT / "assets" / f"{name}.svg").write_text(fn(), encoding="utf-8", newline="\n")
    (ROOT / "README.md").write_text(readme(), encoding="utf-8", newline="\n")
    print("built:", ", ".join(sorted(p.name for p in (ROOT / "assets").glob("*.svg"))), "+ README.md")


if __name__ == "__main__":
    main()
