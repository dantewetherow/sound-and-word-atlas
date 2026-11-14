"""The notation's characters: words with their letters lifted out, so their marks stand on their own as faces.

Gno, the mascot and the site's icon since 10 November 2026, is gno: gn as one sound under a black bond bar, as kn in
know, and o with a long mark, spelling its name. He sits beside the site's name in the header, stands on the About page,
and is the browser tab's icon (logo.py). He is the one character changed after lifting: his bond bar is cut to the
length of his long mark, centred where it was (SHORT_BAR), so it reads as a short brow under the raised red one, and
since 11 November 2026 it sits 0.12 letter sizes higher (LIFT_BAR), to give the black eye under it room. He is a
character first, so he needn't match the notation exactly. The others are their words' marks exactly.

Note, note lifted, was the mascot from 7 to 10 November 2026; he stays in Definitions as the worked example of a word
whose legomorphs stand on their own. The Dialogue Team is She, Could and Go, the actor, operator and action of a claim;
when Could flips to the front, the claim becomes a question. Chosen on 7 November 2026; whether the team stays, and
where each character goes, decorative, instructional or both, is open.

A lifted word keeps every mark svg_word draws, in its order. With the letters gone, the marks drawn above them (long
and short marks, the cone, the vault) come down by DROP letter sizes to close the gap, and the marks drawn under them
(bond bars, circles, nudges) stay where they were. The swoop is the mouth, and comes down MOUTH letter sizes more than
in a word, so it reads as a smile (8 November 2026; it was lowered for the faces first, then in the notation itself on
7 November, which brought the notation's swoop level with the faces' and left the faces' smile high). The drawing is then
cropped to its marks. Boxes and seams, which run through the letters, aren't moved, so a word with
either would need more thought before it joins the team."""
import math, re

DROP = 0.62
MOUTH = 0.25
TEAM = [("she", "She", "actor"), ("could", "Could", "operator"), ("go", "Go", "action")]
NUM = r"-?\d+(?:\.\d+)?"
CODES = {"gno": "k.gn l.o"}     # the characters' words that aren't on the site's path or lists
SHORT_BAR = {"gno"}             # bond bars cut to the long mark's length, centred where they were (Gno's short brow)
LIFT_BAR = {"gno": 0.12}         # bond bars raised this many letter sizes, to give the eye under them room (Gno's brow)


def _shorten_bars(els):
    """Each bond bar cut to the length of the word's long mark, centred where it was."""
    longs = [e for e in els if e.startswith('<line class="nz6"')]
    if not longs:
        return els
    x1, x2 = (float(re.search(f' {a}="({NUM})"', longs[0])[1]) for a in ("x1", "x2"))
    half = abs(x2 - x1) / 2
    def cut(e):
        if not e.startswith('<line class="nz4"'):
            return e
        a, b = (float(re.search(f' {k}="({NUM})"', e)[1]) for k in ("x1", "x2"))
        m = (a + b) / 2
        e = re.sub(f' x1="{NUM}"', f' x1="{m - half:.1f}"', e, count=1)
        return re.sub(f' x2="{NUM}"', f' x2="{m + half:.1f}"', e, count=1)
    return [cut(e) for e in els]


def _points(el):
    """Points enough to bound one drawn element: circle and line ends, and samples along each path."""
    sw = float((re.search(r'stroke-width="(' + NUM + ')"', el) or [0, 0])[1]) / 2
    if el.startswith("<circle"):
        cx, cy, r = (float(re.search(f'{a}="({NUM})"', el)[1]) for a in ("cx", "cy", "r"))
        r += sw
        return [(cx - r, cy - r), (cx + r, cy + r)]
    if el.startswith("<line"):
        x1, y1, x2, y2 = (float(re.search(f'{a}="({NUM})"', el)[1]) for a in ("x1", "y1", "x2", "y2"))
        return [(x1 - sw, y1 - sw), (x2 + sw, y2 + sw), (x1 + sw, y1 + sw), (x2 - sw, y2 - sw)]
    if el.startswith("<rect"):
        x, y, w, h = (float(re.search(f' {a}="({NUM})"', el)[1]) for a in ("x", "y", "width", "height"))
        return [(x - sw, y - sw), (x + w + sw, y + h + sw)]
    d = re.search(r' d="([^"]+)"', el)[1]
    pts, cur = [], (0.0, 0.0)
    for cmd, args in re.findall(r"([MLQC])([^MLQC]*)", d):
        v = [float(n) for n in re.findall(NUM, args)]
        ctrl = [cur] + [(v[i], v[i + 1]) for i in range(0, len(v), 2)]
        if cmd in "ML":
            pts.append(ctrl[-1])
        else:                                              # a Bezier curve: sample it, so its bulge counts and its handles don't
            n = len(ctrl) - 1
            for k in range(1, 21):
                t = k / 20
                pts.append(tuple(sum(math.comb(n, i) * (1 - t) ** (n - i) * t ** i * p[j] for i, p in enumerate(ctrl)) for j in (0, 1)))
        cur = ctrl[-1]
    return [(x + dx, y + dy) for x, y in pts for dx, dy in ((-sw, -sw), (sw, sw))]


def _weigh(el, weight):
    """Heavier marks for a small drawing: thicker strokes (and the cone's dots with them), bigger sound circles. The
    shapes and places stay the same."""
    num = lambda m: f'{m[1]}="{float(m[2]) * weight:.2f}"'
    el = re.sub(f'(stroke-width)="({NUM})"', num, el)
    el = re.sub(r'stroke-dasharray="([^"]+)"', lambda m: 'stroke-dasharray="' + " ".join(
        f"{float(v) * weight:.2f}" for v in re.findall(NUM, m[1])) + '"', el)
    if re.search(r'class="nz(1|2)"', el):                  # sound circles, not the cone
        el = re.sub(f' (r)="({NUM})"', lambda m: f' r="{float(m[2]) * weight:.2f}"', el)
    return el


def lifted(LW, word, F=58.0, label=None, pad=0.08, scale=1.0, em=None, px_height=None, weight=1.0):
    """The word's marks with its letters lifted out and the gap closed, cropped to the marks. Colours come from the
    site's variables, so it follows the page between bright and night. With em, the width is set in ems, so a group of
    drawings can be scaled together by its font size. With px_height, the drawing is sized to that height. Weight
    thickens the marks for small sizes, like the header's."""
    if word in CODES and word not in LW.W:
        LW.W[word] = CODES[word]
    g, _, _ = LW.svg_word(word, F, 0.0, cls=True)
    B = 1.44 * F                                           # svg_word's baseline
    g = re.sub(r'<rect class="wt"[^>]*/>', "", g)
    g = re.sub(r'<g class="nz5".*?</g>', "", g, flags=re.S)
    els = re.findall(r"<[^>]+/>", g)
    if word in SHORT_BAR:
        els = _shorten_bars(els)
    out, pts = [], []
    for el in els:
        first = re.search(f'(?:cy|y1)="({NUM})"', el) or re.search(f'd="M{NUM} ({NUM})', el)
        dy = DROP * F if re.search(r'class="nz(6|8)"', el) and first and float(first[1]) < B else 0.0
        if 'class="nz3"' in el:                            # the swoop is the mouth: lower than in a word, so it reads as a smile
            dy = MOUTH * F
        if 'class="nz4"' in el and word in LIFT_BAR:
            dy = -LIFT_BAR[word] * F
        if weight != 1.0:
            el = _weigh(el, weight)
        el = re.sub(r' class="nz\d"', "", el)
        pts += [(x, y + dy) for x, y in _points(el)]
        out.append(f'<g transform="translate(0 {dy:.1f})">{el}</g>' if dy else el)
    x0, y0 = min(p[0] for p in pts) - pad * F, min(p[1] for p in pts) - pad * F
    w, h = max(p[0] for p in pts) + pad * F - x0, max(p[1] for p in pts) + pad * F - y0
    aria = f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"'
    if px_height:
        scale = px_height / h
    size = f' style="width:{w * em:.2f}em;height:auto"' if em else ""
    return (f'<svg class="lifted" viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}" width="{w * scale:.0f}" height="{h * scale:.0f}"{size}{aria}>'
            + "".join(out) + "</svg>")


def team(LW, scale=0.95):
    """The Dialogue Team making a claim, then the flip: Could moves to the front, outlined as on the word cards."""
    def member(word, name, role, moving=False):
        return (f'<figure class="member{" moving" if moving else ""}">{lifted(LW, word, label=f"{name}, {word} with its letters lifted out", scale=scale, em=scale / 16)}'
                f'<figcaption><b>{name}</b><span>{role}</span></figcaption></figure>')
    claim = "".join(member(*m) for m in TEAM)
    flipped = [TEAM[1], TEAM[0], TEAM[2]]
    question = "".join(member(*m, moving=(m[0] == "could")) for m in flipped)
    return (f'<figure class="team" aria-label="The Dialogue Team"><div class="team-line">{claim}<p class="say">She could go.</p></div>'
            f'<div class="team-line">{question}<p class="say">Could she go?</p></div>'
            f'<figcaption>The Dialogue Team. She, Could and Go, the actor, operator and action, make a claim. When Could, the '
            f'operator, flips to the front, the claim becomes a question. Their faces are their words with the letters lifted '
            f'out, like Note&rsquo;s.</figcaption></figure>')
