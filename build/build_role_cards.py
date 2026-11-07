"""Action cards and actor cards: tent cards for the content words a sentence is built from, made on 6 November 2026 to
stand with the sentence cards and the verb-system cards.

Action cards, on a pale red wash: the words E. W. Dolch's 1936 article lists as verbs (data/dolch.json, "verbs"), less
the 22 that are already verb-system cards (the forms of be, have and do, the modals, and don't), so those keep their
blue or red bands. 70 cards.
Actor cards, on a pale green wash, for actors and the acted-on: the personal pronouns I, me, you, he, him, she, her, we,
us, they, them and it, then Dolch's 95 nouns. 107 cards.

The washes follow the sentence colours: actions red, actors and the acted-on green. The wash is a panel inset from the
card's edges, so it prints whole on printers that can't print to the edge of the page.

The cards are drawn with build_handouts.py's pieces (fonts, card geometry, marking), so the sets match. NOUN_CODES has
the 72 nouns the notation didn't mark yet, each following the word named in its comment. CALLS lists the choices they
rest on; they wait in the manual's Marking calls tab under "From the action and actor cards".

Run:  python3 build/build_role_cards.py <node_modules with the @fontsource packages> docs/sessions/handouts <work folder>
"""
import asyncio, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_handouts as H          # reads the same three arguments; its own build runs only as a script
import build_verb_cards as V        # the verb-system cards' codes, sizes and list-page styles
from playwright.async_api import async_playwright
LW, esc = H.LW, H.esc

NOUN_CODES = {
    "baby": "c.b l.a | c.b b.y ; vault 3>1",                 # as pony
    "ball": "c.b b.a k.ll",                                  # as call
    "bear": "c.b r.ear",                                     # as hear
    "bell": "c.b s.e k.ll",                                  # as tell
    "birthday": "c.b r.ir g.th + | c.d t.ay",                # birth + day, as into
    "box": "c.b s.o c.x",                                    # as six
    "brother": "c.br b.o g.th | r.er",                       # as other
    "cake": "c.c l.a c.k e>",                                # as make
    "chair": "g.ch r.air",                                   # as hair
    "chicken": "g.ch s.i x.ck | b.e c.n ; bv 3>2",           # as pretty and seven
    "children": "g.ch s.i c.l | c.d + c.r b.e c.n",          # child + ren, with the break before d, as making
    "Christmas": "k.Ch c.r s.i k.st + | c.m b.a c.s",        # Christ + mas; ch says k, and st says s, as in mustn't
    "coat": "c.c t.oa c.t",                                  # as boat
    "corn": "c.c r.or c.n",                                  # as for
    "cow": "c.c t.ow",                                       # as how
    "door": "c.d r.oor",                                     # as four
    "duck": "c.d s.u k.ck",                                  # as back
    "egg": "s.e k.gg",                                       # as off
    "eye": "t.eye",                                          # one vowel unit
    "farm": "c.f r.ar c.m",                                  # as warm
    "farmer": "c.f r.ar | c.m + r.er",                       # farm + er, as making
    "father": "c.f b.a g.th | r.er",                         # as water and other
    "feet": "c.f t.ee c.t",                                  # as keep
    "fire": "c.f l.i c.r e>",                                # as here
    "fish": "c.f s.i g.sh",                                  # as wish
    "floor": "c.fl r.oor",                                   # as door
    "flower": "c.fl t.ow | r.er",                            # as brown and water
    "game": "c.g l.a c.m e>",                                # as name
    "garden": "c.g r.ar | c.d b.e c.n",                      # as seven
    "girl": "c.g r.ir c.l",                                  # as bird
    "grass": "c.gr s.a k.ss",                                # as kiss
    "ground": "c.gr t.ou c.nd",                              # as round
    "hand": "c.h s.a c.nd",                                  # as and
    "hill": "c.h s.i k.ll",                                  # as fill
    "horse": "c.h r.or c.s e0",                              # as please
    "house": "c.h t.ou c.s e0",                              # as out and please
    "kitty": "c.k s.i x.tt | b.y ; bv 3>2",                  # as pretty
    "leg": "c.l s.e c.g",                                    # as big
    "letter": "c.l s.e x.tt | r.er ; bv 3>2",                # as better
    "man": "c.m s.a c.n",                                    # as ran
    "men": "c.m s.e c.n",                                    # as ten
    "milk": "c.m s.i c.lk",                                  # as help
    "money": "c.m b.o c.n | t.ey",                           # as many, with ey as in they
    "morning": "c.m r.or c.n + | s.i k.ng",                  # morn + ing, as heading
    "mother": "c.m b.o g.th | r.er",                         # as other
    "nest": "c.n s.e c.st",                                  # as best
    "party": "c.p r.ar | c.t b.y",                           # as only
    "picture": "c.p s.i c.c | c.t r.ur e0",                  # as were
    "pig": "c.p s.i c.g",                                    # as big
    "rabbit": "c.r s.a x.bb | s.i c.t ; bv 3>2",             # as better
    "ring": "c.r s.i k.ng",                                  # as sing
    "robin": "c.r s.o c.b | s.i c.n",                        # as lemon and napkin
    "Santa": "c.S s.a c.n | c.t b.a",                        # as under, with a bare final a
    "Claus": "c.Cl t.au c.s",                                # as because
    "school": "c.s k.ch t.oo c.l",                           # ch says k
    "seed": "c.s t.ee c.d",                                  # as see
    "sheep": "g.sh t.ee c.p",                                # as sleep
    "shoe": "g.sh t.oe",                                     # as blue
    "sister": "c.s s.i c.s | c.t r.er",                      # as after
    "snow": "c.sn t.ow",                                     # as grow
    "song": "c.s s.o k.ng",                                  # as long
    "squirrel": "c.squ r.ir | c.r b.e c.l",                  # q and u say k and w; ir as in bird
    "stick": "c.st s.i k.ck",                                # as pick
    "street": "c.str t.ee c.t",                              # as stroll and green
    "thing": "g.th s.i k.ng",                                # as sing
    "top": "c.t s.o c.p",                                    # as hop
    "tree": "c.tr t.ee",                                     # as try and three
    "watch": "c.w b.a g.tch",                                # as wash and catch
    "way": "c.w t.ay",                                       # as day
    "wind": "c.w s.i c.nd",                                  # the noun, with a short i, unlike find
    "window": "c.w s.i c.n | c.d t.ow",                      # as yellow
    "wood": "c.w t.oo c.d",                                  # as good
}
from known_codes import all_codes
from site_codes import SITE_CODES
from dolch_codes import DOLCH_CODES
codes, _ = all_codes()                      # every code the site uses, as build_dolch_cards.py loads them
for w, c in {**SITE_CODES, **DOLCH_CODES}.items(): codes.setdefault(w, c)
codes["live"] = DOLCH_CODES["live"]         # the live of "we live here"
assert not set(NOUN_CODES) & set(codes), set(NOUN_CODES) & set(codes)
codes.update(NOUN_CODES)
LW.W.clear(); LW.W.update(codes)

CALLS = [
    ("bear", "ear as an r-controlled unit, as in hear", "Here it says the sound in hair. The marks don’t show which."),
    ("door, floor", "oor as an r-controlled unit", "As our in four and your."),
    ("chicken", "a box around ck, a blocked vault from the e, and no seam",
     "The e would reach back and make the i long. Chicken isn’t chick + en: chick is the shorter word, cut from chicken."),
    ("children", "child + ren, with a seam after the d and the syllable break before it",
     "As in making. The i is short here, though it is long in child, and the marks show both."),
    ("Christmas, school", "ch as a black bond bar", "It says k, so it isn’t green."),
    ("Christmas", "st under a bar, and a seam after Christ", "The t is quiet, as in mustn’t, so st spells one sound."),
    ("eye", "all three letters as one vowel unit", "The other way to see it is ey as a unit and the final e in a cone, as bye has."),
    ("fire", "a long mark over the i, the r on its own, and the e in a cone with a vault", "As here."),
    ("horse, house", "the e in a cone with no vault", "As in please. The e keeps the s from looking like a plural."),
    ("kitty", "no seam", "As pretty. Kit + y, as fun + y gives funny, is the other reading."),
    ("money", "a bare o, and ey as a vowel unit", "The o as in come, and ey as in they, though here it says the sound in see."),
    ("picture", "the t black, and ure as an r-controlled ur with the e in a cone",
     "The t says ch here. A green circle would follow its sound; the letter stays black."),
    ("robin", "a closed first syllable with no vault", "As lemon and seven."),
    ("squirrel", "squ as three sounds, with the u black; ir as an r-controlled unit; the second r starting the next syllable",
     "The u says w, as it does after q."),
    ("wind", "a short mark over the i", "The noun. Wind, the verb, would take a long mark, as find does."),
    ("Santa Claus, good-bye", "drawn as two marked words, with a hyphen between good and bye",
     "Christmas and Santa Claus keep their capitals, as I does."),
]

DOLCH = json.loads((HERE / "data" / "dolch.json").read_text(encoding="utf-8"))
VERB_SYSTEM = {w for w, _ in V.CARDS}
ACTIONS = [w for w in DOLCH["verbs"] if w not in VERB_SYSTEM]
PRONOUNS = "I me you he him she her we us they them it".split()
NOUNS = DOLCH["nouns"]
assert len(ACTIONS) == 70 and len(PRONOUNS) == 12 and len(NOUNS) == 95
PAIRS = {"Santa Claus": ("Santa", "Claus")}
HYPHENED = {"good-bye": ("good", "bye")}
HY = 0.46                                   # the hyphen's width, in letter heights (build_handouts.hyphen_svg)
TUCK = 0.24                                 # how far each side of the hyphen tucks under the words' margins


def width_f(w):
    """A card's width in letter heights, without the space in a pair."""
    one = lambda x: LW.svg_word(x, 100.0, 0.0, cls=False)[1] / 100
    if w in HYPHENED: a, b = HYPHENED[w]; return one(a) + HY + one(b) - 2 * TUCK
    return sum(one(x) for x in PAIRS.get(w, (w,)))


AVAIL, GAP = V.AVAIL, V.GAP
fits = lambda w, f: width_f(w) * f + GAP * (w in PAIRS) <= AVAIL
F_BIG = H.SENT_F
SIZES = [F_BIG, 0.58, 0.50]                 # the sentence cards' size where a word fits it, then two smaller steps


def size(w):
    for f in SIZES:
        if fits(w, f): return f
    return (AVAIL - GAP * (w in PAIRS)) / width_f(w)


def card_face(w):
    F = size(w)
    if w in HYPHENED:
        a, b = HYPHENED[w]
        return (f'<div class="pair hy">{H.mark(a, F)}<div style="margin-left:{-TUCK * F:.3f}in;margin-right:{-TUCK * F:.3f}in">'
                f'{H.hyphen_svg(F)}</div>{H.mark(b, F)}</div>')
    if w in PAIRS: return '<div class="pair">' + "".join(H.mark(x, F) for x in PAIRS[w]) + "</div>"
    return H.mark(w, F)


WASH = {"an": ("#f5e6e4", "#dea9a1"), "ac": ("#e5eee7", "#a6c4ab")}      # action and actor: the verb red and subject green, pale
ROLE_CSS = """
.wash{position:absolute;left:.2in;right:.2in;top:2.225in;bottom:.2in;border-radius:.1in;border:.9pt solid;}
""" + "".join(f".wash.{k}{{background:{bg};border-color:{edge};}} .tile.{k}{{background:{bg};border-color:{edge};}}\n"
              for k, (bg, edge) in WASH.items()) + """
.scard .face.w{padding:.1in 0 .2in;box-sizing:border-box;}
.pair.hy{column-gap:0;}
.key span{white-space:nowrap;}
.key i.w{display:inline-block;width:.42in;height:.2in;border-radius:2pt;border:.9pt solid;}
.wrapw .w{line-height:1.45;}
"""
CSS = (H.SOUNDS_CSS + H.CARDS_CSS.replace("@page{size:8.5in 11in;margin:0;}", "").replace(".page{width:8.5in;height:11in;display:block;}", "")
       + H.SENT_CSS + V.VERB_CSS + ROLE_CSS)

ACTION_SET, ACTOR_SET = set(ACTIONS), set(PRONOUNS) | set(NOUNS)


def tiles(line):
    out = []
    for tok in line.split():
        parts = []
        for t in tok.split("+"):
            word = t.replace("_", " ")
            cls = (" op" if word in V.MOVES else " st" if word in V.STAYS else " an" if word in ACTION_SET
                   else " ac" if word in ACTOR_SET else "")
            parts.append(f'<span class="tile{cls}">{esc(word)}</span>')
        out.append(parts[0] if len(parts) == 1 else f'<span class="jn">{"".join(parts)}</span>')
    return "".join(out)


FLIPS = [("the dog can jump .", "can the dog jump ?"),
         ("the girl is read+ing .", "is the girl read+ing ?"),
         ("the bird sing+-s .", "does the bird sing ?"),
         ("they ate the cake .", "did they eat the cake ?"),
         ("she saw him .", "did she see him ?")]


def key_html():
    sw = lambda k: f'<i class="w" style="background:{WASH[k][0]};border-color:{WASH[k][1]}"></i>'
    return (f'<div class="key"><span>{sw("ac")}actors and the acted-on</span><span>{sw("an")}actions</span>'
            '<span><i class="b" style="background:var(--modal)"></i>operators</span></div>')


def list_page(kind):
    flips = "".join(f'<div class="fp"><div class="fl">{tiles(a)}</div><div class="arrow">→</div><div class="fl">{tiles(b)}</div></div>' for a, b in FLIPS)
    row = lambda name, ws: (f'<div class="srow wrapw"><span class="g">{name}<span>{len(ws)}</span></span>'
                            f'<span class="w">{" ".join(esc(w).replace(" ", "&nbsp;") for w in ws)}</span></div>')
    if kind == "an":
        title, rows, pages = "Action cards", row("Actions", ACTIONS), f"2 to {1 + -(-len(ACTIONS) // 6)}"
        lead = ("Tent cards on a pale red wash for the actions: the words E. W. Dolch’s 1936 sight vocabulary lists as verbs, "
                "less the forms of <i>be</i>, <i>have</i> and <i>do</i>, the modals and <i>don’t</i>, which are verb-system cards. "
                "They are the size of the sentence cards, so they stand with its actors and operators.")
        notes = ("<p>Ten cards are past forms: <i>ate, came, found, gave, got, made, ran, said, saw</i> and <i>went</i>. In a question, "
                 "<i>did</i> carries the past and the action goes back to its plain form: <i>they ate the cake, did they eat the cake?</i></p>"
                 "<p><i>Goes</i> and <i>going</i> are <i>go</i> with an ending. For the others, lay an ending from the verb-system cards "
                 "beside the card: <i>help + -s, jump + ing</i>.</p>"
                 "<p>A word that moves to the front is never on a red wash. <i>Have</i> and <i>do</i> can be actions too "
                 "(<i>do you have a dog?</i>), but their cards are in the verb-system set.</p>")
    else:
        title, rows, pages = ("Actor cards", row("Pronouns", PRONOUNS) + row("Nouns", NOUNS),
                              f"2 to {1 + -(-(len(PRONOUNS) + len(NOUNS)) // 6)}")
        lead = ("Tent cards on a pale green wash for the actors and the acted-on: twelve personal pronouns from E. W. Dolch’s "
                "1936 sight vocabulary, and his separate list of 95 nouns. The same card can be either: "
                "<i>the dog saw the cat, the cat saw the dog</i>.")
        notes = ("<p>The pronouns come in pairs, one for the actor and one for the acted-on: <i>I</i> and <i>me</i>, <i>he</i> and "
                 "<i>him</i>, <i>she</i> and <i>her</i>, <i>we</i> and <i>us</i>, <i>they</i> and <i>them</i>. <i>You</i> and "
                 "<i>it</i> do both jobs.</p>"
                 "<p>The nouns are all Dolch’s, including <i>good-bye</i>, and <i>Christmas</i> and <i>Santa Claus</i>, which keep "
                 "their capitals as <i>I</i> does. Most are marked here for the first time, and a few marks wait on a ruling "
                 "in the manual.</p>"
                 "<p><i>The</i> and <i>a</i> are on the sentence cards, and the operators on the verb-system cards.</p>")
    notes += (f"<p>Print pages {pages} in colour on card stock, single-sided, at actual size. Cut on the solid lines, fold on "
              "the dotted ones, and stand each card up. The wash stops short of the edges, so most printers print it whole.</p>")
    return f"""<section class="page">
  <h1>{title}</h1>
  <p class="lead">{lead}</p>
  <div class="sl"><h2>In the set</h2>{rows}</div>
  <div class="duo">
    <div class="fs"><h2>Green, red and blue</h2>{key_html()}
      <div class="rule"><p>The wash gives a card’s job in the sentence, and the operators keep the verb-system cards’ blue band. Stand up an actor, an operator and an action, then move the operator to the front.</p></div>
      <div class="flips1">{flips}</div></div>
    <div class="notes"><h2>Notes</h2>{notes}</div>
  </div>
  <div class="foot"><span>Sounds, Symbols and Sentences</span><span>Goes with the sentence cards and the verb-system cards</span></div>
</section>"""


def card_pages(words, kind):
    slots = words + [None] * ((-len(words)) % 6)
    pages = []
    for p0 in range(0, len(slots), 6):
        cards = ""
        for k, w in enumerate(slots[p0:p0 + 6]):
            x, y = (k % 3) * 3.6667, (k // 3) * 4.25
            if w is None:
                cards += f'<div class="scard" style="left:{x:.4f}in;top:{y}in"><div class="wash {kind}"></div></div>'; continue
            cards += (f'<div class="scard" style="left:{x:.4f}in;top:{y}in"><div class="wash {kind}"></div>'
                      f'<div class="face w">{card_face(w)}</div></div>')
        guides = ('<div class="cut v" style="left:3.6667in;height:8.5in"></div><div class="cut v" style="left:7.3333in;height:8.5in"></div>'
                  '<div class="cut h" style="width:11in;top:4.25in"></div>'
                  '<div class="fold" style="top:2.125in;width:11in"></div><div class="fold" style="top:6.375in;width:11in"></div>')
        pages.append(f'<section class="page cards">{cards}{guides}</section>')
    return "".join(pages)


# Each word must sit inside its wash, clear of the panel's edge.
WASH_CHECK_JS = """() => [...document.querySelectorAll('.scard')].flatMap(c => { const w = c.querySelector('.wash'), f = c.querySelector('.face');
  if (!w || !f) return []; const W = w.getBoundingClientRect();
  return [...f.children].map(v => { const b = v.getBoundingClientRect();
    const pad = [b.left - W.left, W.right - b.right, b.top - W.top, W.bottom - b.bottom].map(x => Math.round(x));
    return Math.min(...pad) < 4 ? (v.getAttribute('aria-label') || v.textContent) + ' ' + pad.join(',') : null; }).filter(Boolean); })"""

SETS = [("action-cards", "Action cards", "an", ACTIONS), ("actor-cards", "Actor cards", "ac", PRONOUNS + NOUNS)]


async def main():
    H.OUT.mkdir(parents=True, exist_ok=True); H.WORK.mkdir(parents=True, exist_ok=True)
    for name, _, _, words in SETS:
        by = {}
        for w in words: by.setdefault(round(size(w), 3), []).append(w)
        print(name, " | ".join(f"{f} in: {len(ws)}" + ("" if f == F_BIG else " (" + ", ".join(ws) + ")") for f, ws in sorted(by.items(), reverse=True)))
    async with async_playwright() as p:
        br = await p.chromium.launch()
        page = await br.new_page()
        for name, title, kind, words in SETS:
            f = H.WORK / f"{name}.html"
            f.write_text(H.doc(title, CSS, list_page(kind) + card_pages(words, kind)), encoding="utf-8")
            await page.goto(f.as_uri()); await page.evaluate("document.fonts.ready")
            await page.emulate_media(media="print")
            for r in await page.evaluate(H.CHECK_JS):
                bad = r["overflowY"] > 1 or r["overflowX"] > 1 or r["outside"] or r["crowded"]
                if bad or r["page"] == 1: print(f"  {name} p{r['page']}: free above footer {r['free']} in" + (f" | PROBLEM {r}" if bad else ""))
                assert not bad, r
            tight = await page.evaluate(WASH_CHECK_JS)
            assert not tight, tight
            await page.pdf(path=str(H.OUT / f"{name}.pdf"), width="11in", height="8.5in", print_background=True,
                           margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            print("wrote", H.OUT / f"{name}.pdf")
        await br.close()

if __name__ == "__main__":
    asyncio.run(main())
