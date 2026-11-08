"""The Legomorphic Notation wordmark and logo, drawn from the fonts as paths so each file stands on its own.

The wordmark, from Dante's sketches of 6 November 2026, which replace the d b q p logo:

  whole   λέγ┊ω · morphic   the Greek verb whole, its two syllables smiling (λέ, γω), a seam between the stem and
                            the ending -ω, "I". Chosen for the About page, where it stands beside the etymology,
                            and written to build/wordmark.svg, which about_pages.py draws into the page
  split   λέγ┊ō┊morph┊ic    the word as the notation reads it in English: leg, o, morph and ic, with seams

The logo: go, chosen on 7 November 2026 for the browser tab, written to build/logo.svg with PNG copies for browsers
that can't use an SVG icon (favicon-32.png, apple-touch-icon.png). Note, the mascot, sits beside the name in the header
(characters.py). The candidates were a word's own
marks with its letters lifted out, so every mark is true (6 November 2026):

  go          two circles and a swoop, a bar over the red one: a vowel that ends its syllable says its name
  it          red first, with a cup over it: a short vowel closed by a consonant
  leg         three circles and a swoop, a cup over the red one
  leg-bare    three circles and a swoop
  note        three circles and a swoop, a bar over the red one, and the silent e's marks: the empty cone, and the
              vault reaching back to the bar. Too fine for a browser tab, so it would be the larger mark
  note-ring   note as first described, with an empty red circle for the e, a mark the notation doesn't have

Two earlier faces were set aside: a cup over a red circle that ends its syllable (true of Greek λέ, where epsilon is
short, but no English word on the site does it), and a bar over a black circle (a vowel mark over a consonant).

Marks keep the notation's colours: ink for consonants, red for vowels and their cups and bars, blue for swoops, seams
and vaults, and the soft grey of the cone. Greek in Gentium Plus, Latin in Lexend, both under the SIL Open Font
License. As files, the colours turn light on a dark screen.

Run:  python3 build/logo.py <node_modules with the @fontsource packages> <out dir for the candidates>
      (the PNGs are drawn with Playwright, which this workspace has)
"""
import math, pathlib, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.varLib import instancer

HERE = pathlib.Path(__file__).resolve().parent
INK, RED, BLUE, QUIET = "#2b2b2b", "#b5402f", "#3f6488", "#6b6256"        # the site's --ink, --verb, --modal, --soft
INK_DARK, RED_DARK, BLUE_DARK, QUIET_DARK = "#ece5d8", "#e2836e", "#95b6db", "#a89e8f"
S = 100.0                                      # the Latin letters' size; everything else is a share of it


class Face:
    def __init__(self, path, wght=None):
        f = TTFont(path)
        if wght is not None and "fvar" in f:
            f = instancer.instantiateVariableFont(f, {"wght": wght})
        self.gs, self.cmap, self.upm, self.hmtx = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm, f["hmtx"]
        self.xh = f["OS/2"].sxHeight

    def glyph(self, ch):
        name = self.cmap[ord(ch)]
        pen, bp = SVGPathPen(self.gs), BoundsPen(self.gs)
        self.gs[name].draw(pen); self.gs[name].draw(bp)
        return pen.getCommands(), self.hmtx[name][0], bp.bounds


class Line:
    """Letters set along a baseline, with their ink boxes kept for the marks."""
    def __init__(self, base):
        self.x, self.base, self.out, self.boxes = 0.0, base, [], {}

    def put(self, face, ch, size, cls, key=None, track=0.0):
        d, adv, (x0, y0, x1, y1) = face.glyph(ch)
        s = size / face.upm
        self.out.append(f'<path class="{cls}" d="{d}" transform="translate({self.x:.2f} {self.base:.2f}) scale({s:.5f} {-s:.5f})"/>')
        box = (self.x + x0 * s, self.base - y1 * s, self.x + x1 * s, self.base - y0 * s)
        if key: self.boxes[key] = box
        self.x += adv * s + track
        return box

    def gap(self, w): self.x += w


def dot(x, y, cls, r=0.062 * S): return f'<circle class="{cls}" cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}"/>'
def seam(x, y0, y1):                           # the notation's seam: a blue dashed line, as svg_word draws it
    return (f'<line class="b seam" x1="{x:.2f}" y1="{y0:.2f}" x2="{x:.2f}" y2="{y1:.2f}" '
            f'stroke-width="{0.03 * S:.2f}" stroke-dasharray="{0.057 * S:.2f} {0.057 * S:.2f}"/>')
def bar(x0, x1, y, cls): return (f'<line class="{cls} st" x1="{x0:.2f}" y1="{y:.2f}" x2="{x1:.2f}" y2="{y:.2f}" '
                                 f'stroke-width="{0.06 * S:.2f}" stroke-linecap="round"/>')
def smile(x0, x1, y, depth=0.2 * S): return (f'<path class="b st" d="M{x0:.2f} {y:.2f} Q{(x0 + x1) / 2:.2f} {y + 2 * depth:.2f} '
                                             f'{x1:.2f} {y:.2f}" stroke-width="{0.055 * S:.2f}" stroke-linecap="round"/>')
cx = lambda b: (b[0] + b[2]) / 2
SMILE = 0.26 * S          # the smiles' ends under the sound circles: 0.14 S until the swoop came down on 7 November 2026


def build(nm):
    nm = pathlib.Path(nm)
    lat = Face(nm / "@fontsource-variable/lexend/files/lexend-latin-wght-normal.woff2", wght=480)
    tag = Face(nm / "@fontsource-variable/lexend/files/lexend-latin-wght-normal.woff2", wght=400)
    grk = Face(nm / "@fontsource/gentium-plus/files/gentium-plus-greek-700-normal.woff")
    G = S * (lat.xh / lat.upm) / (grk.xh / grk.upm)      # Greek sized so its x-height matches the Latin
    xh = S * lat.xh / lat.upm
    return lat, tag, grk, G, xh


def tagline(tag, x_mid, y):
    words, size, track = ["LANGUAGE", "FORM", "MEANING"], 0.27 * S, 0.27 * 0.36 * S
    widths = []
    for w in words:
        widths.append(sum(tag.glyph(c)[1] * size / tag.upm + track for c in w) - track)
    gapw = 1.15 * S
    total = sum(widths) + gapw * (len(words) - 1)
    line, out = Line(y), []
    line.x = x_mid - total / 2
    for i, w in enumerate(words):
        for c in w: line.put(tag, c, size, "k", track=track)
        line.x -= track
        if i < len(words) - 1:
            out.append(dot(line.x + gapw / 2, y - 0.095 * S, "r", r=0.045 * S))
            line.gap(gapw)
    return line.out + out


STYLE = (f'<style>.k{{fill:{INK}}}.r{{fill:{RED}}}.k.st,.r.st,.b.st,.b.seam,.q.st{{fill:none}}.k.st{{stroke:{INK}}}.r.st{{stroke:{RED}}}'
         f'.b.st,.b.seam{{stroke:{BLUE}}}.q.st{{stroke:{QUIET}}}@media (prefers-color-scheme:dark){{.k{{fill:{INK_DARK}}}.r{{fill:{RED_DARK}}}'
         f'.k.st{{stroke:{INK_DARK}}}.r.st{{stroke:{RED_DARK}}}.b.st,.b.seam{{stroke:{BLUE_DARK}}}.q.st{{stroke:{QUIET_DARK}}}}}</style>')


def svg(body, x0, y0, x1, y1, label, pad=0.18 * S):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0 - pad:.0f} {y0 - pad:.0f} {x1 - x0 + 2 * pad:.0f} {y1 - y0 + 2 * pad:.0f}" '
            f'role="img" aria-label="{label}">\n<title>{label}</title>\n{STYLE}\n' + "\n".join(body) + "\n</svg>\n")


def whole(nm):
    lat, tag, grk, G, xh = build(nm)
    B = S
    L, marks = Line(B), []
    l = L.put(grk, "λ", G, "k"); e = L.put(grk, "έ", G, "r"); g = L.put(grk, "γ", G, "k")
    L.gap(0.16 * S); sx = L.x; L.gap(0.16 * S)
    w = L.put(grk, "ω", G, "r")
    L.gap(0.30 * S); marks.append(dot(L.x, B - xh / 2, "k", r=0.07 * S)); L.gap(0.30 * S)
    for c in "morphic": L.put(lat, c, S, "k")
    low = max(b[3] for b in (l, e, g, w))
    dy = low + 0.13 * S                                   # the sound circles sit under the lowest letter
    for b, cls in ((l, "k"), (e, "r"), (g, "k"), (w, "r")): marks.append(dot(cx(b), dy, cls))
    marks.append(smile(cx(l) - 0.13 * S, cx(e) + 0.13 * S, dy + SMILE))
    marks.append(smile(cx(g) - 0.13 * S, cx(w) + 0.13 * S, dy + SMILE))
    marks.append(seam(sx, B - 0.92 * S, dy - 0.12 * S))
    width = L.x
    body = L.out + marks + tagline(tag, width / 2, dy + SMILE + 0.4 * S + 0.65 * S)
    return svg(body, 0, B - 1.05 * S, width, dy + 1.37 * S, "Legomorphic Notation: λέγω, morphic. Language, form, meaning")


def split(nm):
    lat, tag, grk, G, xh = build(nm)
    B = S
    L, marks, seams = Line(B), [], []
    l = L.put(grk, "λ", G, "k"); e = L.put(grk, "έ", G, "r"); g = L.put(grk, "γ", G, "k")
    for part in ("ō", "morph", "ic"):
        L.gap(0.15 * S); seams.append(L.x); L.gap(0.15 * S)
        for c in part:
            if c == "ō":
                o = L.put(lat, "o", S, "r", "o1")
                marks.append(bar(cx(o) - 0.20 * S, cx(o) + 0.20 * S, B - xh - 0.20 * S, "r"))
            else:
                L.put(lat, c, S, "r" if c in "oi" else "k", c + part)
    o2, r = L.boxes["omorph"], L.boxes["rmorph"]
    marks.append(bar(o2[0] + 0.02 * S, r[2] + 0.02 * S, B + 0.20 * S, "r"))     # or: one sound, an r-controlled unit
    low = max(b[3] for b in (l, e, g))
    dy = low + 0.13 * S
    for b, cls in ((l, "k"), (e, "r"), (g, "k")): marks.append(dot(cx(b), dy, cls))
    marks.append(smile(cx(l) - 0.20 * S, cx(g) + 0.20 * S, dy + SMILE))
    for x in seams: marks.append(seam(x, B - 0.92 * S, B + 0.10 * S))
    width = L.x
    body = L.out + marks + tagline(tag, width / 2, dy + SMILE + 0.4 * S + 0.65 * S)
    return svg(body, 0, B - 1.05 * S, width, dy + 1.37 * S, "Legomorphic Notation: λέγ, ō, morph, ic. Language, form, meaning")


# ------------------------------------------------------------------ the logo candidates
# Measures in F, the letter size, as svg_word draws them: circles a slot of .67F apart, the swoop's ends .29F under the
# circles' centres with its control .49F under them and .107F past the outer circles (since 7 November 2026), then MOUTH lower
# again, as on Note and the Dialogue Team, so it reads as a smile (8 November 2026); the cup .257F each side of its
# vowel with its control .2F under its ends; the bar .279F each side; the cone a dotted ring; the vault leaving the
# cone's top and ending .21F over the bar, with its arrowhead. A logo drops the letters, so the marks above come down
# to sit BROW over the circles, the cone sits in the row of circles where the e would be, and WEIGHT thickens circles
# and strokes so they hold at small sizes.
MARKS = {   # name: (circles left to right, (mark above, over which circle), what follows the circles, what it is)
    "go": (["k", "r"], ("bar", 1), None, "two sound circles and a swoop, a bar over the red one: the marks of go"),
    "it": (["r", "k"], ("cup", 0), None, "two sound circles and a swoop, red first with a cup over it: the marks of it"),
    "leg": (["k", "r", "k"], ("cup", 1), None, "three sound circles and a swoop, a cup over the red one: the marks of leg"),
    "leg-bare": (["k", "r", "k"], None, None, "three sound circles and a swoop"),
    "note": (["k", "r", "k"], ("bar", 1), "cone", "three sound circles and a swoop, a bar over the red one, and an empty "
             "cone with a vault reaching back to the bar: the marks of note"),
    "note-ring": (["k", "r", "k"], ("bar", 1), "ring", "three sound circles and a swoop, a bar over the red one, and an "
                  "empty red circle"),
}
WEIGHT, BROW, SLOT, CONE = 1.5, 0.33, 0.67, 0.30
from characters import MOUTH                                 # the faces' mouths sit lower than a word's swoop (8 November 2026)
CHOSEN = "go"
PAPER = "#f4efe6"                                          # the site's --paper, behind the PNG icons


def mark(name, F=100.0):
    dots, top, tail, what = MARKS[name]
    n = len(dots)
    r, sws, swm = 0.072 * WEIGHT * F, 0.046 * WEIGHT * F, 0.05 * WEIGHT * F
    xs = [SLOT * F * (i - (n - 1) / 2) for i in range(n)]
    xl, xr = xs[0] - 0.107 * F, xs[-1] + 0.107 * F
    body, box = [], [xl - sws, -r, xr + sws, (0.39 + MOUTH) * F + sws]
    def grow(x0, y0, x1, y1): box[:] = [min(box[0], x0), min(box[1], y0), max(box[2], x1), max(box[3], y1)]
    for x, c in zip(xs, dots):
        body.append(f'<circle class="{c}" cx="{x:.2f}" cy="0" r="{r:.2f}"/>')
    body.append(f'<path class="b st" d="M{xl:.2f} {(.29 + MOUTH) * F:.2f} Q{(xl + xr) / 2:.2f} {(.49 + MOUTH) * F:.2f} {xr:.2f} {(.29 + MOUTH) * F:.2f}" '
                f'stroke-width="{sws:.2f}" stroke-linecap="round"/>')
    xt = 0.0
    if top:
        kind, at = top
        xt = xs[at]
        if kind == "bar":
            y = -BROW * F
            body.append(f'<line class="r st" x1="{xt - .279 * F:.2f}" y1="{y:.2f}" x2="{xt + .279 * F:.2f}" y2="{y:.2f}" '
                        f'stroke-width="{swm:.2f}" stroke-linecap="round"/>')
            grow(xt - .279 * F - swm, y - swm, xt + .279 * F + swm, y)
        else:                                              # the cup: its ends a little above the bar's line
            e = -(BROW + 0.05) * F
            body.append(f'<path class="r st" d="M{xt - .257 * F:.2f} {e:.2f} Q{xt:.2f} {e + .2 * F:.2f} {xt + .257 * F:.2f} {e:.2f}" '
                        f'stroke-width="{swm:.2f}" stroke-linecap="round"/>')
            grow(xt - .257 * F - swm, e - swm, xt + .257 * F + swm, e)
    xe = xs[-1] + SLOT * F                                 # where the e would stand
    if tail == "ring":
        body.append(f'<circle class="r st" cx="{xe:.2f}" cy="0" r="{r - swm / 2:.2f}" stroke-width="{swm * 0.8:.2f}"/>')
        grow(xe - r, -r, xe + r, r)
    if tail == "cone":
        cr, sw = CONE * F, 0.043 * WEIGHT * F
        body.append(f'<circle class="q st" cx="{xe:.2f}" cy="0" r="{cr:.2f}" stroke-width="{0.038 * WEIGHT * F:.2f}" '
                    f'stroke-linecap="round" stroke-dasharray="{0.012 * WEIGHT * F:.2f} {0.078 * WEIGHT * F:.2f}"/>')
        ys, ex, ey = -cr, xt + 0.05 * F, -(BROW + 0.21) * F
        c1, c2 = (xe - 0.04 * F, ys - 0.77 * F), (xt + 0.46 * F, min(ys - 0.77 * F, ey - 0.28 * F))
        body.append(f'<path class="b st" d="M{xe:.2f} {ys:.2f} C{c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {ex:.2f} {ey:.2f}" '
                    f'stroke-width="{sw:.2f}" stroke-linecap="round"/>')
        dx, dy = ex - c2[0], ey - c2[1]
        d = math.hypot(dx, dy); dx, dy = dx / d, dy / d
        c, s, size = math.cos(0.5), math.sin(0.5), 0.144 * F
        a = (ex + size * (-dx * c + dy * s), ey + size * (-dx * s - dy * c))
        b = (ex + size * (-dx * c - dy * s), ey + size * (dx * s - dy * c))
        body.append(f'<path class="b st" d="M{a[0]:.2f} {a[1]:.2f} L{ex:.2f} {ey:.2f} L{b[0]:.2f} {b[1]:.2f}" '
                    f'stroke-width="{sw:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')
        crest = min(0.125 * ys + 0.375 * c1[1] + 0.375 * c2[1] + 0.125 * ey, a[1], b[1])   # near the arc's top
        grow(min(a[0], b[0]) - sw, crest - sw, xe + cr + sw, cr + sw)
    side = max(box[2] - box[0], box[3] - box[1]) * 1.16
    mx, my = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    return svg(body, mx - side / 2, my - side / 2, mx + side / 2, my + side / 2,
               f"Legomorphic Notation logo: {what}", pad=0)


if __name__ == "__main__":
    nm, out = sys.argv[1], pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    (HERE / "wordmark.svg").write_text(whole(nm), encoding="utf-8")
    (out / "wordmark-split.svg").write_text(split(nm), encoding="utf-8")
    for name in MARKS: (out / f"mark-{name}.svg").write_text(mark(name), encoding="utf-8")
    logo = mark(CHOSEN)
    (HERE / "logo.svg").write_text(logo, encoding="utf-8")
    from playwright.sync_api import sync_playwright         # the PNG icons: the mark on the paper colour, light marks
    with sync_playwright() as pw:
        page = pw.chromium.launch().new_page(color_scheme="light")
        for name, px, share in (("apple-touch-icon.png", 180, 0.78), ("favicon-32.png", 32, 1.0)):
            inner = logo.replace("<svg ", f'<svg width="{px * share:.0f}" height="{px * share:.0f}" ', 1)
            page.set_content(f'<div id="t" style="width:{px}px;height:{px}px;background:{PAPER};display:grid;place-items:center">{inner}</div>')
            page.locator("#t").screenshot(path=str(HERE / name))
    print("wrote", HERE / "wordmark.svg", "and the candidates in", out)
