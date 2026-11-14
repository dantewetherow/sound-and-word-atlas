"""Action cards and actor cards: tent cards for the content words a sentence is built from, made on 6 November 2026 to
stand with the sentence cards and the verb-system cards.

Action cards: the words E. W. Dolch's 1936 article lists as verbs (data/dolch.json, "verbs"), less the 22 that are
already verb-system cards (the forms of be, have and do, the modals, and don't). 70 cards.
Actor cards, for actors and the acted-on: the personal pronouns I, me, you, he, him, she, her, we, us, they, them and
it, then Dolch's 95 nouns. 107 cards.

The cards carry no colour for the sentence roles. The list pages name the roles in words, and their flips outline the
card that moves, in ink, as the Session 1 sentence cards do.

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

from noun_codes import NOUN_CODES          # the nouns' codes, shared with the Dolch noun cards
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
    ("bear", "ear as an r-controlled unit, as in hear", "Here it spells the sound in hair. The marks don’t show which."),
    ("door, floor", "oor as an r-controlled unit", "As our in four and your."),
    ("chicken", "a box around ck, a blocked vault from the e, and no seam",
     "The e would reach back and make the i long. Chicken isn’t chick + en: chick is the shorter word, cut from chicken."),
    ("children", "child + ren, with a seam after the d and the syllable break before it",
     "As in making. The i is short here, though it is long in child, and the marks show both."),
    ("Christmas, school", "ch as a black bond bar", "It spells k, so it isn’t green."),
    ("Christmas", "st under a bar, and a seam after Christ", "The t is quiet, as in mustn’t, so st spells one sound."),
    ("eye", "all three letters as one vowel unit", "The other way to see it is ey as a unit and the final e in a cone, as bye has."),
    ("fire", "a long mark over the i, the r on its own, and the e in a cone with a vault", "As here."),
    ("horse, house", "the e in a cone with no vault", "As in please. The e keeps the s from looking like a plural."),
    ("kitty", "no seam", "As pretty. Kit + y, as fun + y gives funny, is the other reading."),
    ("money", "a bare o, and ey as a vowel unit", "The o as in come, and ey as in they, though here it spells the sound in see."),
    ("picture", "the t black, and ure as an r-controlled ur with the e in a cone",
     "The t spells ch here. A green circle would follow its sound; the letter stays black."),
    ("robin", "a closed first syllable with no vault", "As lemon and seven."),
    ("squirrel", "qu on a black bond bar with a black circle under each letter, the u red; ir as an r-controlled unit; the second r starting the next syllable",
     "Ruled 8 November 2026. The u is red, as a vowel letter, with a black circle for the w. The black bar ties q to the u it never comes without, as the manual's cards and appendix already do (equipment), and shows a reader counting red letters that this u isn't the vowel. The two circles count the two sounds, k and w, as the path does at step 4 and as Carney's sound-to-spelling account has it (the u spells w)."),
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


ROLE_CSS = """
.pair.hy{column-gap:0;}
.wrapw .w{line-height:1.45;}
"""
CSS = (H.SOUNDS_CSS + H.CARDS_CSS.replace("@page{size:8.5in 11in;margin:0;}", "").replace(".page{width:8.5in;height:11in;display:block;}", "")
       + H.SENT_CSS + V.VERB_CSS + ROLE_CSS)

tiles = V.tiles                             # the flips outline only the card that moves


FLIPS = [("the dog can jump .", "can the dog jump ?"),
         ("the girl is read+ing .", "is the girl read+ing ?"),
         ("the bird sing+-s .", "does the bird sing ?"),
         ("they ate the cake .", "did they eat the cake ?"),
         ("she saw him .", "did she see him ?")]


def list_page(kind):
    flips = "".join(f'<div class="fp"><div class="fl">{tiles(a)}</div><div class="arrow">→</div><div class="fl">{tiles(b)}</div></div>' for a, b in FLIPS)
    row = lambda name, ws: (f'<div class="srow wrapw"><span class="g">{name}<span>{len(ws)}</span></span>'
                            f'<span class="w">{" ".join(esc(w).replace(" ", "&nbsp;") for w in ws)}</span></div>')
    if kind == "an":
        title, rows, pages = "Action cards", row("Actions", ACTIONS), f"2 to {1 + -(-len(ACTIONS) // 6)}"
        lead = ("Tent cards for the actions: the words E. W. Dolch’s 1936 sight vocabulary lists as verbs, "
                "less the forms of <i>be</i>, <i>have</i> and <i>do</i>, the modals and <i>don’t</i>, which are verb-system cards. "
                "They are the size of the sentence cards, so they stand with its actors and operators.")
        notes = ("<p>Ten cards are past forms: <i>ate, came, found, gave, got, made, ran, said, saw</i> and <i>went</i>. In a question, "
                 "<i>did</i> carries the past and the action goes back to its plain form: <i>they ate the cake, did they eat the cake?</i></p>"
                 "<p><i>Goes</i> and <i>going</i> are <i>go</i> with an ending. For the others, lay an ending from the verb-system cards "
                 "beside the card: <i>help + -s, jump + ing</i>.</p>"
                 "<p><i>Have</i> and <i>do</i> can be actions too (<i>do you have a dog?</i>), but their cards are in the "
                 "verb-system set, with the other words that can move to the front.</p>")
    else:
        title, rows, pages = ("Actor cards", row("Pronouns", PRONOUNS) + row("Nouns", NOUNS),
                              f"2 to {1 + -(-(len(PRONOUNS) + len(NOUNS)) // 6)}")
        lead = ("Tent cards for the actors and the acted-on: twelve personal pronouns from E. W. Dolch’s "
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
              "the dotted ones, and stand each card up.</p>")
    return f"""<section class="page">
  <h1>{title}</h1>
  <p class="lead">{lead}</p>
  <div class="sl"><h2>In the set</h2>{rows}</div>
  <div class="duo">
    <div class="fs"><h2>Flips to try</h2>
      <div class="rule"><p>Stand up an actor, an operator and an action, then move the operator to the front. The outlined card is the one that moves.</p></div>
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
                cards += f'<div class="scard" style="left:{x:.4f}in;top:{y}in"></div>'; continue
            cards += f'<div class="scard" style="left:{x:.4f}in;top:{y}in"><div class="face">{card_face(w)}</div></div>'
        guides = ('<div class="cut v" style="left:3.6667in;height:8.5in"></div><div class="cut v" style="left:7.3333in;height:8.5in"></div>'
                  '<div class="cut h" style="width:11in;top:4.25in"></div>'
                  '<div class="fold" style="top:2.125in;width:11in"></div><div class="fold" style="top:6.375in;width:11in"></div>')
        pages.append(f'<section class="page cards">{cards}{guides}</section>')
    return "".join(pages)


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
            await page.pdf(path=str(H.OUT / f"{name}.pdf"), width="11in", height="8.5in", print_background=True,
                           margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            print("wrote", H.OUT / f"{name}.pdf")
        await br.close()

if __name__ == "__main__":
    asyncio.run(main())
