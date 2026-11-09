"""Verb-system cards: tent cards for the words that orbit the verb, made on 6 November 2026 to go with the Session 1 handouts.

Every form of be, have and do, the nine modals, not and the n't contractions, the semi-modals, the endings -s, ed, ing
and en, and the to of to go: 53 cards and a blank. They are the sentence cards' size, six to a landscape page, so they
stand with the sentence cards' actors and actions. The first page lists the set, says which words can move to the
front to make a question, and gives flips to try, with the card that moves outlined.

The cards carry no colour for the sentence roles. The first page says in words which cards move, and its flips outline
the card that moves, in ink.

The cards are drawn with build_handouts.py's pieces (fonts, card geometry, marking), so the sets match. The codes the
notation didn't have are below. CALLS lists the choices they rest on; they wait in the manual's Marking calls tab under
"From the verb-system cards".

Run:  python3 build/build_verb_cards.py <node_modules with the @fontsource packages> docs/sessions/handouts <work folder>
"""
import asyncio, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_handouts as H          # reads the same three arguments; its own build runs only as a script
from playwright.async_api import async_playwright
LW, esc = H.LW, H.esc

VERB_CODES = {
    "being": "c.b l.e + | s.i k.ng",                 # be + ing, as going
    "having": "c.h s.a | c.v + s.i k.ng",            # the e of have drops, as in making; the a stays short, so no vault
    "doing": "c.d b.o + | s.i k.ng",                 # do + ing, as going
    "n’t": "c.n ap c.t",                             # the red apostrophe stands in for the o of not
    "isn’t": "s.i c.s | c.n ap c.t", "wasn’t": "c.w b.a c.s | c.n ap c.t",
    "aren’t": "r.ar e0 c.n ap c.t", "weren’t": "c.w r.er e0 c.n ap c.t",
    "hasn’t": "c.h s.a c.s | c.n ap c.t", "hadn’t": "c.h s.a c.d | c.n ap c.t",
    "haven’t": "c.h s.a c.v | b.e c.n ap c.t",        # as seven: the v closes the first syllable, and the e is said weakly
    "don’t": "c.d l.o c.n ap c.t",                   # as on the Dolch cards
    "doesn’t": "c.d b.o + e0 c.s | c.n ap c.t", "didn’t": "c.d s.i c.d | c.n ap c.t",
    "can’t": "c.c s.a c.n ap c.t",                   # can and n't share one n
    "couldn’t": "c.c t.oul c.d | c.n ap c.t", "wouldn’t": "c.w t.oul c.d | c.n ap c.t",
    "shouldn’t": "g.sh t.oul c.d | c.n ap c.t",
    "won’t": "c.w l.o c.n ap c.t",                   # will becomes wo-, and the o spells its name, as in don't
    "mustn’t": "c.m s.u k.st | c.n ap c.t",          # the t of must goes quiet, so st spells one sound
    "ought": "t.ough c.t",                           # ough as one vowel sound, as oul in could
    "used": "l.u c.s + e> c.d",                      # use + d, as liked
    "ed": "e0 c.d",                                  # the e in a cone, as in played
    "en": "b.e c.n",                                 # a weak vowel, as in taken
}
LW.KEY_ONLY.update(VERB_CODES)
LW.NO_SWOOP.update({"ed", "n’t"})

CALLS = [
    ("isn’t, wasn’t, hasn’t, hadn’t, haven’t, doesn’t, didn’t, couldn’t, wouldn’t, shouldn’t, mustn’t",
     "a syllable break before the n, the red apostrophe in the second syllable, and no seam",
     "The n of n’t is a syllable of its own here, and the apostrophe stands in for its missing vowel, the o of not. "
     "In can’t, won’t, don’t, aren’t and weren’t it isn’t a syllable, so there is no break."),
    ("haven’t", "the v closing the first syllable, and the e bare", "As in seven. The e is said weakly."),
    ("mustn’t", "a bar under st", "The t of must goes quiet before n’t, so st spells one sound, as kn does in know."),
    ("won’t, can’t", "won’t as don’t: a long mark over the o; can’t with one n",
     "Will changes its vowel in won’t, as do does in don’t. In can’t the n of can and the n of n’t are one letter."),
    ("having", "a break before v, the seam after it, and no vault", "The e of have drops, as in making, but the a stays short."),
    ("ought", "ough as one vowel unit", "As oul in could and igh in light."),
    ("used", "use + d, with the e in a cone and a vault back to the u",
     "As liked. In used to, the s spells s and the d spells t, and the marks don’t show that."),
    ("ed, n’t (cards on their own)", "no syllable swoop",
     "Each is a syllable in some words and not in others (wanted, played; isn’t, can’t). The -s card has none either."),
    ("ed", "the e in a cone", "Silent, as in played and hopped. In wanted it is said weakly: mark it again on the blank face."),
]

FAMILIES = [   # (group, note, [(word, moves to the front)])
    ("Be", "", [("be", 0), ("am", 1), ("is", 1), ("are", 1), ("was", 1), ("were", 1), ("been", 0), ("being", 0)]),
    ("Have", "", [("have", 1), ("has", 1), ("had", 1), ("having", 0)]),
    ("Do", "", [("do", 1), ("does", 1), ("did", 1), ("done", 0), ("doing", 0)]),
    ("Modals", "", [(m, 1) for m in "can could will would shall should may might must".split()]),
    ("Not", "", [("not", 0), ("n’t", 1)]),
    ("Contractions", "", [(w, 1) for w in "isn’t aren’t wasn’t weren’t haven’t hasn’t hadn’t don’t doesn’t didn’t can’t couldn’t won’t wouldn’t shouldn’t mustn’t".split()]),
    ("Semi-modals", "", [("have to", 0), ("ought to", 0), ("going to", 0), ("used to", 0)]),
    ("Endings", "", [("-s", 1), ("ed", 1), ("ing", 0), ("en", 0)]),
    ("To", "", [("to", 0)]),
]
CARDS = [c for _, _, cs in FAMILIES for c in cs]
assert len(CARDS) == 53 and len({w for w, _ in CARDS}) == 53
LEFT = {"ing", "ed", "en"}           # at the left edge, so laid over a final e they cover it: take + en, bake + ed, write + ing
AVAIL, GAP = 3.16, 0.12              # inches a card face can give a word (the edge check allows 3.17), and the space in a semi-modal


def width_f(w):
    """A card's width in letter heights (multiply by the letter size in inches)."""
    if w == "-s": return 0.46 + (0.60 + 0.67) - 0.30
    return sum(LW.svg_word(x, 100.0, 0.0, cls=False)[1] / 100 for x in w.split())

# Two letter sizes: the sentence cards' size for every word that fits it, so a sentence built from both sets looks even,
# and one smaller size shared by the long contractions and the semi-modals.
fits = lambda w, f: width_f(w) * f + GAP * w.count(" ") <= AVAIL
F_BIG = H.SENT_F
F_SMALL = min((AVAIL - GAP * w.count(" ")) / width_f(w) for w, _ in CARDS if not fits(w, F_BIG))
size = lambda w: F_BIG if fits(w, F_BIG) else F_SMALL


def card_face(w):
    F = size(w)
    if w == "-s": return f'<div class="aff">{H.hyphen_svg(F)}<div style="margin-left:{-0.30 * F:.3f}in">{H.letter_svg("s", F)}</div></div>'
    if " " in w: return '<div class="pair">' + "".join(H.mark(x, F) for x in w.split()) + "</div>"
    return H.mark(w, F)


VERB_CSS = """
.pair{display:flex;column-gap:""" + f"{GAP}in" + """;align-items:flex-end;}
.rule p{font-size:9.6pt;line-height:1.4;margin:0 0 .05in;}
.rule i{font-family:var(--serif);font-style:italic;}
.duo{display:grid;grid-template-columns:5.85in 1fr;column-gap:.35in;}
.duo .fs,.duo .notes{margin-top:.12in;}
.duo .notes p{font-size:9.6pt;line-height:1.4;margin:0 0 .06in;}
.flips1{display:grid;row-gap:.055in;margin-top:.07in;}
.fp{display:flex;align-items:center;column-gap:.1in;}
.fp .fl{display:flex;column-gap:.05in;flex:none;}
.fp .jn{display:flex;}
.fp .jn .tile:not(:first-child){border-left-style:dashed;border-top-left-radius:0;border-bottom-left-radius:0;}
.fp .jn .tile:not(:last-child){border-top-right-radius:0;border-bottom-right-radius:0;}
.fp .tile{white-space:nowrap;font-size:10.5pt;padding:.05in .08in .06in;}
.fp .arrow{color:var(--soft);font-size:11pt;}
"""

FLIPS = [("she is read+ing .", "is she read+ing ?"),
         ("she has been read+ing .", "has she been read+ing ?"),
         ("she could+n’t read .", "could+n’t she read ?"),
         ("she read+-s .", "does she read ?"),
         ("they hop+p+ed .", "did they hop ?"),
         ("we have_to read .", "do we have_to read ?"),
         ("he is going_to read .", "is he going_to read ?")]
MOVES = {w for w, m in CARDS if m}
STAYS = {w for w, m in CARDS if not m}


def tiles(line):
    out = []
    for tok in line.split():
        parts = []
        for t in tok.split("+"):
            word = t.replace("_", " ")
            cls = " op" if word in MOVES else ""
            parts.append(f'<span class="tile{cls}">{esc(word)}</span>')
        out.append(parts[0] if len(parts) == 1 else f'<span class="jn">{"".join(parts)}</span>')
    return "".join(out)


ROWS = [["Be"], ["Have", "Do"], ["Modals"], ["Contractions"], ["Not", "Semi-modals"], ["Endings", "To"]]
assert sorted(n for r in ROWS for n in r) == sorted(n for n, _, _ in FAMILIES)


def list_page():
    fam = {name: cs for name, _, cs in FAMILIES}
    def row(names):
        return '<div class="srow">' + "".join(
            f'<span class="g">{n}<span>{len(fam[n])}</span></span><span class="w">'
            + " ".join(esc(w) for w, _ in fam[n]) + "</span>" for n in names) + "</div>"
    flips = "".join(f'<div class="fp"><div class="fl">{tiles(a)}</div><div class="arrow">→</div><div class="fl">{tiles(b)}</div></div>' for a, b in FLIPS)
    return f"""<section class="page">
  <h1>Verb-system cards</h1>
  <p class="lead">Tent cards for the words that orbit the verb: every form of <i>be</i>, <i>have</i> and <i>do</i>, the nine modals, <i>not</i> and the <i>n’t</i> contractions, the semi-modals, the endings, and the <i>to</i> of <i>to go</i>. They are the size of the sentence cards, so they stand with its actors and actions.</p>
  <div class="sl"><h2>In the set</h2>{"".join(row(r) for r in ROWS)}</div>
  <div class="duo">
    <div class="fs"><h2>Flips to try</h2>
      <div class="rule"><p>These move to the front to make a question: <i>am, is, are, was, were, have, has, had, do, does, did</i>, the modals and the <i>n’t</i> contractions. <i>Be, been, being, having, done, doing, not, to</i>, the semi-modals and the endings <i>ing</i> and <i>en</i> stay where they are. The <i>-s</i> and <i>ed</i> go with <i>do</i>: <i>she reads, does she read?</i> The <i>-s</i> of a plural, as in <i>books</i>, stays. The outlined card is the one that moves.</p></div>
      <div class="flips1">{flips}</div></div>
    <div class="notes"><h2>Notes</h2>
      <p><i>N’t</i> goes where its operator goes: <i>Couldn’t she read?</i> <i>Not</i> stays after the actor: <i>Could she not read?</i> The red apostrophe stands in for the <i>o</i> of <i>not</i>. <i>Can’t</i> keeps one <i>n</i>, and <i>won’t</i> and <i>don’t</i> change the vowel. <i>Shan’t</i> and <i>mightn’t</i> are left out as rare.</p>
      <p>The semi-modals mean what modals mean but don’t move, so <i>do</i> comes to the front: <i>Do we have to read?</i></p>
      <p>Lay <i>ing</i>, <i>ed</i> or <i>en</i> over a final <i>e</i>: <i>write + ing</i>, <i>bake + ed</i>, <i>take + en</i>. After a short vowel, double the last letter first, with the sentence cards’ extra <i>p</i> and <i>n</i>: <i>hop + p + ed</i>.</p>
      <p>Print pages 2 to 10 in colour on card stock, single-sided, at actual size. Cut on the solid lines, fold on the dotted ones, and stand each card up.</p>
    </div>
  </div>
  <div class="foot"><span>Sounds, Symbols and Sentences</span><span>Goes with the sentence cards and the key to the marks</span></div>
</section>"""


def card_pages():
    slots = CARDS + [None] * ((-len(CARDS)) % 6)
    pages = []
    for p0 in range(0, len(slots), 6):
        cards = ""
        for k, c in enumerate(slots[p0:p0 + 6]):
            x, y = (k % 3) * 3.6667, (k // 3) * 4.25
            if c is None:
                cards += f'<div class="scard" style="left:{x:.4f}in;top:{y}in"></div>'; continue
            w, m = c
            edge = " left" if w in LEFT else ""
            cards += f'<div class="scard" style="left:{x:.4f}in;top:{y}in"><div class="face{edge}">{card_face(w)}</div></div>'
        guides = ('<div class="cut v" style="left:3.6667in;height:8.5in"></div><div class="cut v" style="left:7.3333in;height:8.5in"></div>'
                  '<div class="cut h" style="width:11in;top:4.25in"></div>'
                  '<div class="fold" style="top:2.125in;width:11in"></div><div class="fold" style="top:6.375in;width:11in"></div>')
        pages.append(f'<section class="page cards">{cards}{guides}</section>')
    return "".join(pages)


CSS = (H.SOUNDS_CSS + H.CARDS_CSS.replace("@page{size:8.5in 11in;margin:0;}", "").replace(".page{width:8.5in;height:11in;display:block;}", "")
       + H.SENT_CSS + VERB_CSS)


async def main():
    H.OUT.mkdir(parents=True, exist_ok=True); H.WORK.mkdir(parents=True, exist_ok=True)
    print(f"letter sizes: {F_BIG} in, and {F_SMALL:.3f} in for " + ", ".join(w for w, _ in CARDS if size(w) != F_BIG))
    async with async_playwright() as p:
        br = await p.chromium.launch()
        page = await br.new_page()
        f = H.WORK / "verb-system-cards.html"
        f.write_text(H.doc("Verb-system cards", CSS, list_page() + card_pages()), encoding="utf-8")
        await page.goto(f.as_uri()); await page.evaluate("document.fonts.ready")
        await page.emulate_media(media="print")
        for r in await page.evaluate(H.CHECK_JS):
            bad = r["overflowY"] > 1 or r["overflowX"] > 1 or r["outside"] or r["crowded"]
            print(f"  p{r['page']}: free above footer {r['free']} in" + (f" | PROBLEM {r}" if bad else ""))
            assert not bad, r
        await page.pdf(path=str(H.OUT / "verb-system-cards.pdf"), width="11in", height="8.5in", print_background=True,
                       margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        print("wrote", H.OUT / "verb-system-cards.pdf")
        await br.close()

if __name__ == "__main__":
    asyncio.run(main())
