"""Printable handouts for Session 1 (Sounds, feedback and learning loops).

Builds four PDFs:
  sounds-and-marks-key.pdf        two sides, landscape: the 44 sounds, and the marks with exemplar words and contrasts
  operator-cards.pdf              three pages, portrait: the nine modal operators as fold-over tent cards, marked on one face, blank on the other,
                                  and three blank cards
  operator-cards-instructions.pdf one page, landscape: making the cards, running a loop, marking by hand
  sentence-cards.pdf              nine pages, landscape: a demonstration set of 48 shorter tent cards about reading and writing
                                  (operators, not, actors, actions, things to read, -ing and -s, an extra p and n for doubling,
                                  a period and a question mark) after a page that lists them and shows flips

Every marked word is drawn by legomorphic_words.py, so the handouts and the deck cannot drift apart.
The name of the notation is left off the handouts on purpose.

This is the site's copy of the atlas tool. It is the same except for the footer, which names the session instead of
the presenter, since the site names no one. Rebuilt on 6 November 2026, it matched the handouts given out on
18 October pixel for pixel before that change. The site serves its output from docs/sessions/handouts/.

Run:  python3 build_handouts.py <node_modules with the @fontsource packages> <output folder> <work folder>
"""
import asyncio, base64, html, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import legomorphic_words as LW
from playwright.async_api import async_playwright

FONTS, OUT, WORK = (pathlib.Path(a) for a in sys.argv[1:4])
esc = html.escape

# Two exemplar words that are in no line and no list. Both follow the author's own pages:
# napkin (two closed syllables, no box) and pony (the y reaches back over one consonant; the y-sender page).
LW.KEY_ONLY.update({"napkin": "c.n s.a c.p | c.k s.i c.n", "pony": "c.p l.o | c.n b.y ; vault 3>1", "ship": "g.sh s.i c.p",
                    # block and blocking: block has a bond bar (nothing reaches); the box comes with -ing and keeps the o short. nudge: the dg is boxed, so the e's vault is stopped,
                    # the u stays short, and the e still softens the g.
                    "block": "c.bl s.o k.ck", "blocking": "c.bl s.o x.ck + | s.i k.ng ; bv 3>2", "nudge": "c.n s.u x.dg e0 ; bv 3>2 ; nudge 3>2",
                    # blocked: the e of -ed looks like a silent e that could send a long-vowel signal; the box stops it. puny: the y reaches back.
                    "blocked": "c.bl s.o x.ck + e0 c.d ; bv 3>2", "puny": "c.p l.u | c.n b.y ; vault 3>1"})

def mark(word, f_in):
    """A marked word as inline SVG, with letters f_in inches high (font size)."""
    g, w, H = LW.svg_word(word, 100.0, 0.0, cls=False)
    return (f'<svg class="mw" viewBox="0 0 {w:.1f} {H:.1f}" style="width:{w / 100 * f_in:.3f}in;height:{H / 100 * f_in:.3f}in" '
            f'role="img" aria-label="{word}, marked">{g}</svg>')

# ------------------------------------------------------------------ fonts and shared style
def face(family, path, style="normal", weight="100 900", rng=None):
    data = base64.b64encode((FONTS / path).read_bytes()).decode()
    return (f'@font-face{{font-family:"{family}";font-style:{style};font-weight:{weight};'
            f'src:url(data:font/woff2;base64,{data}) format("woff2");' + (f"unicode-range:{rng};" if rng else "") + "}")

FONT_CSS = "\n".join([
    face("Lexend", "@fontsource-variable/lexend/files/lexend-latin-wght-normal.woff2"),
    face("Fraunces", "@fontsource-variable/fraunces/files/fraunces-latin-opsz-normal.woff2"),
    face("Fraunces", "@fontsource-variable/fraunces/files/fraunces-latin-opsz-italic.woff2", style="italic"),
    face("Gentium Plus", "@fontsource/gentium-plus/files/gentium-plus-latin-400-normal.woff2", weight="400", rng="U+0000-00FF"),
    face("Gentium Plus", "@fontsource/gentium-plus/files/gentium-plus-latin-ext-400-normal.woff2", weight="400", rng="U+0100-02FF,U+1E00-1EFF"),
    face("Gentium Plus", "@fontsource/gentium-plus/files/gentium-plus-greek-400-normal.woff2", weight="400", rng="U+0370-03FF"),
])

BASE_CSS = """
:root{--ink:#2b2b2b;--soft:#6b6256;--line:#d8d0c0;--verb:#b5402f;--subject:#3a7d44;--modal:#3f6488;
  --serif:"Fraunces",Georgia,serif;--sans:"Lexend",system-ui,sans-serif;--ipa:"Gentium Plus","Charis SIL","DejaVu Serif",serif;}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;background:#fff;color:var(--ink);font-family:var(--sans);-webkit-print-color-adjust:exact;print-color-adjust:exact;}
.page{position:relative;overflow:hidden;page-break-after:always;break-after:page;display:flex;flex-direction:column;}
.page:last-child{page-break-after:auto;break-after:auto;}
h1{font-family:var(--serif);font-weight:500;font-size:25pt;line-height:1.05;letter-spacing:-.012em;margin:0;}
.lead{font-size:10pt;line-height:1.4;margin:.07in 0 0;max-width:8.6in;}
.lead i,.d i,.cap i,li i,p i{font-family:var(--serif);font-style:italic;}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:baseline;font-size:7.6pt;color:var(--soft);padding-top:.06in;}
svg.mw{display:block;overflow:visible;}
"""

# ------------------------------------------------------------------ side 1: the 44 sounds
# (IPA, the key word in pieces): a piece is plain, or the letters that spell the sound: k consonant, g sh/th/ch, v vowel; + means a bar.
SOUNDS = {
 "pig": ("p", [("p", "k"), ("ig", "")]), "bat": ("b", [("b", "k"), ("at", "")]), "top": ("t", [("t", "k"), ("op", "")]),
 "dog": ("d", [("d", "k"), ("og", "")]), "kit": ("k", [("k", "k"), ("it", "")]), "gum": ("g", [("g", "k"), ("um", "")]),
 "fish": ("f", [("f", "k"), ("ish", "")]), "van": ("v", [("v", "k"), ("an", "")]), "thin": ("θ", [("th", "g+"), ("in", "")]),
 "this": ("ð", [("th", "g+"), ("is", "")]), "sun": ("s", [("s", "k"), ("un", "")]), "zip": ("z", [("z", "k"), ("ip", "")]),
 "ship": ("ʃ", [("sh", "g+"), ("ip", "")]), "vision": ("ʒ", [("vi", ""), ("si", "k+"), ("on", "")]), "hat": ("h", [("h", "k"), ("at", "")]),
 "chin": ("tʃ", [("ch", "g+"), ("in", "")]), "jam": ("dʒ", [("j", "k"), ("am", "")]),
 "map": ("m", [("m", "k"), ("ap", "")]), "net": ("n", [("n", "k"), ("et", "")]), "ring": ("ŋ", [("ri", ""), ("ng", "k+")]),
 "leg": ("l", [("l", "k"), ("eg", "")]), "red": ("r", [("r", "k"), ("ed", "")]), "web": ("w", [("w", "k"), ("eb", "")]), "yes": ("j", [("y", "k"), ("es", "")]),
 "cat": ("æ", [("c", ""), ("a", "v"), ("t", "")]), "bed": ("ɛ", [("b", ""), ("e", "v"), ("d", "")]), "sit": ("ɪ", [("s", ""), ("i", "v"), ("t", "")]),
 "hot": ("ɑ", [("h", ""), ("o", "v"), ("t", "")]), "cup": ("ʌ", [("c", ""), ("u", "v"), ("p", "")]),
 "day": ("eɪ", [("d", ""), ("ay", "v+")]), "see": ("i", [("s", ""), ("ee", "v+")]), "my": ("aɪ", [("m", ""), ("y", "v")]),
 "go": ("oʊ", [("g", ""), ("o", "v")]), "moon": ("u", [("m", ""), ("oo", "v+"), ("n", "")]),
 "book": ("ʊ", [("b", ""), ("oo", "v+"), ("k", "")]), "saw": ("ɔ", [("s", ""), ("aw", "v+")]), "about": ("ə", [("a", "v"), ("bout", "")]),
 "boy": ("ɔɪ", [("b", ""), ("oy", "v+")]), "cow": ("aʊ", [("c", ""), ("ow", "v+")]),
 "car": ("ɑr", [("c", ""), ("ar", "v+")]), "for": ("ɔr", [("f", ""), ("or", "v+")]), "her": ("ɝ", [("h", ""), ("er", "v+")]),
 "hair": ("ɛr", [("h", ""), ("air", "v+")]), "ear": ("ɪr", [("ear", "v+")]),
}
CONSONANTS = [("stops", "the mouth closes, then lets go", "pig bat top dog kit gum"),
              ("fricatives", "the air squeezes through a narrow gap", "fish van thin this sun zip hat ship vision"),
              ("affricates", "a stop that slides into a squeeze", "chin jam"),
              ("nasals", "the mouth closes and the air goes out the nose", "map net ring"),
              ("liquids and glides", "the mouth barely closes", "leg red web yes")]
VOWELS = [("short vowels", "", "cat bed sit hot cup"),
          ("long vowels", "long u often sounds like the oo in moon", "day see my go moon"),
          ("other vowels", "", "book saw about"), ("diphthongs", "", "boy cow"),
          ("r-controlled vowels", "", "car for her hair ear")]
assert sorted(w for _, _, ws in CONSONANTS + VOWELS for w in ws.split()) == sorted(SOUNDS) and len(SOUNDS) == 44

def key_word(word):
    ipa, parts = SOUNDS[word]
    assert "".join(t for t, _ in parts) == word, word
    out = []
    for text, kind in parts:
        if not kind: out.append(f'<span class="o">{text}</span>'); continue
        bar = kind.endswith("+"); k = kind[0]
        if k == "v" and "r" in text:                         # an r-controlled unit: the vowel is red, the r stays black, the bar is red
            out.append('<span class="u ru">' + "".join(f'<span class="{"k" if ch == "r" else "v"}">{ch}</span>' for ch in text) + "</span>")
        else:
            out.append(f'<span class="{k}{" u" if bar else ""}">{text}</span>')
    wide = ' style="grid-column:span 2"' if len(word) > 5 else ""
    return f'<div class="kw"{wide}><span class="w">{"".join(out)}</span><span class="ipa" lang="en-fonipa">/{ipa}/</span></div>'

ASIDES = {"diphthongs": "The vowel slides from one shape to another. The long vowels in <i>day, my</i> and <i>go</i> slide too.",
          "affricates": "Each begins as a stop and ends as a squeeze: <i>t</i> into <i>sh</i> in <i>chin</i>, <i>d</i> into <i>zh</i> in <i>jam</i>."}

def sound_groups(groups, cols):
    rows = []
    for name, note, words in groups:
        ws = words.split()
        aside = (f'<p class="aside" style="grid-column:span {cols - len(ws)}">{ASIDES[name]}</p>' if name in ASIDES else "")
        rows.append(f'<div class="grp"><div class="gl"><span class="gn">{name}</span>' + (f'<span class="gd">{note}</span>' if note else "") + "</div>"
                    f'<div class="gw" style="grid-template-columns:repeat({cols},1fr)">' + "".join(key_word(w) for w in ws) + aside + "</div></div>")
    return "".join(rows)

SOUNDS_CSS = """
@page{size:11in 8.5in;margin:0;}
.page{width:11in;height:8.5in;padding:.48in .55in .36in;}
.two{display:grid;grid-template-columns:5fr 4.6fr;column-gap:.36in;margin-top:.2in;align-items:start;}
.col h2{font-family:var(--serif);font-style:italic;font-weight:500;font-size:16pt;margin:0 0 .04in;padding-bottom:.05in;border-bottom:1.2pt solid var(--ink);}
.col.vow h2{color:var(--verb);border-bottom-color:var(--verb);}
.hn{font-size:8.3pt;line-height:1.35;color:var(--soft);margin:.05in 0 0;}
.grp{display:grid;grid-template-columns:1.14in 1fr;column-gap:.1in;padding:.2in 0 .17in;border-bottom:.6pt solid var(--line);}
.vow .grp{grid-template-columns:1.06in 1fr;}
.gn{display:block;font-family:var(--serif);font-style:italic;font-weight:500;font-size:12pt;line-height:1.15;}
.gd{display:block;font-size:7.8pt;line-height:1.32;color:var(--soft);margin-top:.03in;}
.gw{display:grid;row-gap:.15in;}
.kw{display:flex;flex-direction:column;align-items:flex-start;}
.kw .w{font-size:16.5pt;line-height:1.28;font-weight:400;white-space:nowrap;}
.kw .o{color:#8f8676;} .kw .k{color:var(--ink);font-weight:600;} .kw .g{color:var(--subject);font-weight:600;} .kw .v{color:var(--verb);font-weight:600;}
.kw .u{border-bottom:1.9pt solid currentColor;padding-bottom:.6pt;} .kw .ru{border-bottom-color:var(--verb);}
.kw .ipa{font-family:var(--ipa);font-size:12pt;line-height:1.3;color:var(--soft);margin-top:.03in;}
.aside{font-size:7.8pt;line-height:1.38;color:var(--soft);margin:.02in 0 0;align-self:start;}
.aside i{font-family:var(--serif);font-style:italic;}
.note{font-size:8.6pt;line-height:1.45;color:var(--soft);margin:.16in 0 0;}
.note b{font-weight:500;color:var(--ink);}
"""

def sounds_page():
    return f'''<section class="page">
  <h1>The 44 sounds of English</h1>
  <p class="lead">A key word for every sound, with the letters that spell it marked: consonants in black, <i>sh, ch</i> and <i>th</i> in green, vowels in red. A bar under two or more letters marks a single sound. The symbols are from the International Phonetic Alphabet, so /j/ is the <i>y</i> in <i>yes</i>, and the <i>j</i> in <i>jam</i> is /dʒ/.</p>
  <div class="two">
    <div class="col"><h2>24 consonants</h2><p class="hn">The mouth closes or narrows somewhere. Each label says how.</p>{sound_groups(CONSONANTS, 6)}</div>
    <div class="col vow"><h2>20 vowels</h2><p class="hn">The mouth stays open, and the tongue and lips shape the sound.</p>{sound_groups(VOWELS, 5)}
      <p class="note"><b>About the count.</b> Forty-four is a teaching count, and it shifts with accent. Many Canadians say <i>hot</i> and <i>saw</i> with the same vowel, which takes one away. Count <i>car, for, hair</i> and <i>ear</i> as a vowel followed by <i>r</i>, and four more go, which leaves 39. Check this sheet against your program’s sound wall.</p></div>
  </div>
  <div class="foot"><span>Sounds, Symbols and Sentences · Session 1</span><span>Over: marking a word</span></div>
</section>'''

# ------------------------------------------------------------------ side 2: the marks
MARKS = [   # (exemplar or exemplars, name, what it shows, columns it spans)
 ("ship", "Sound circle", "A circle under each sound: red for a vowel, black for a consonant, green for <i>sh, th, ch</i>.", 1),
 ("napkin", "Syllable swoop", "A swoop under each syllable.", 1),
 ("it", "Short mark", "A cup over a vowel that keeps its short sound.", 1),
 ("go", "Long mark", "A bar over a vowel that says its name.", 1),
 ("do", "No mark", "A lone vowel with no cup and no bar borrows another vowel’s sound, or is said weakly.", 1),
 ("should", "Bond bar", "A bar under the letters of a single sound. All the letters of a vowel sound are red.", 1),
 ("her", "R-controlled unit", "A red bar under a vowel and its <i>r</i>. The <i>r</i> stays black, and they share a circle.", 1),
 ("have", "Cone of silence", "A dotted ring around a silent <i>e</i>.", 1),
 ("make", "Vowel vault", "An arc from a silent <i>e</i>, or from a vowel one consonant later, back to the vowel it makes long.", 1),
 ("going", "Morpheme seam", "A dotted line between the parts of a word that carry meaning.", 1),
 (["block", "blocked"], "Block box", "A box around a pair that stops a vowel after it from reaching back, such as <i>ll, nn, ck, tch</i> or <i>dg</i>. <i>Block</i> has a bar: nothing reaches yet. <i>Blocked</i> keeps it, and the box stops the <i>e</i>’s vault, so the <i>o</i> stays short.", 2),
 (["nice", "nudge"], "Nice-nudge", "A small arc from <i>e, i</i> or <i>y</i> to a <i>c</i> it softens, or from a final <i>e</i> to a <i>g</i>. In <i>nice</i> the <i>e</i> also makes the <i>i</i> long. In <i>nudge</i> a box stops that vault, so the <i>u</i> stays short.", 2),
 ("funny", "Blocked vault", "The arc ends in a red X where a box stops it, so the vowel stays short.", 1),
]
CONTRASTS = [
 (["not", "no", "do"], "The same letter three ways: short, long, and borrowing another vowel’s sound."),
 (["know", "no"], "The same two sounds, spelled with four letters and with two."),
 (["gave", "give"], "In <i>gave</i> the silent <i>e</i> makes the <i>a</i> long. In <i>give</i> it only keeps <i>v</i> off the end."),
 (["puny", "funny"], "After a single <i>n</i> the <i>y</i> reaches back and the <i>u</i> is long. A doubled <i>n</i> in a box stops it."),
]
MARKS_CSS = """
.grid{display:grid;grid-template-columns:repeat(5,1fr);column-gap:.2in;row-gap:.07in;margin-top:.16in;}
.cell{border-top:.6pt solid var(--line);padding-top:.05in;}
.cell .cw{display:flex;column-gap:.22in;}
.cell b{display:block;font-weight:500;font-size:11pt;line-height:1.2;margin-top:.01in;}
.cell .d{display:block;font-size:8.3pt;line-height:1.36;margin-top:.03in;}
.cx{margin-top:.1in;border-top:1.2pt solid var(--ink);padding-top:.06in;}
.cx h2{font-family:var(--serif);font-style:italic;font-weight:500;font-size:13pt;margin:0;}
.sets{display:flex;justify-content:space-between;column-gap:.3in;margin-top:.02in;}
.set .ws{display:flex;column-gap:.14in;}
.set .cap{font-size:8.3pt;line-height:1.36;margin:.02in 0 0;max-width:2.5in;}
"""

def marks_page():
    words = lambda w: [w] if isinstance(w, str) else w
    cells = "".join(f'<div class="cell" style="grid-column:span {span}"><div class="cw">{"".join(mark(x, .35) for x in words(w))}</div><b>{name}</b><span class="d">{text}</span></div>'
                    for w, name, text, span in MARKS)
    sets = "".join('<div class="set"><div class="ws">' + "".join(mark(w, .31) for w in words) + f'</div><p class="cap">{cap}</p></div>' for words, cap in CONTRASTS)
    return f'''<section class="page">
  <h1>Marking a word</h1>
  <p class="lead" style="max-width:9.9in">Vowels are red, consonants black, and <i>sh, th</i> and <i>ch</i> green. Say the word slowly, count its sounds, then mark it by hand. Use the colours and marks selectively: choose the ones that show a pattern or how two marks interact, especially in a new word.</p>
  <div class="grid">{cells}</div>
  <div class="cx"><h2>Contrasts</h2><div class="sets">{sets}</div></div>
  <div class="foot"><span>Sounds, Symbols and Sentences · Session 1</span><span>Over: the 44 sounds of English</span></div>
</section>'''

# ------------------------------------------------------------------ the operator cards (the nine modals)
MODALS = "can could will would shall should may might must".split()
CARDS_CSS = """
@page{size:8.5in 11in;margin:0;}
.page{width:8.5in;height:11in;display:block;}
.card{position:absolute;width:4.25in;height:5.5in;}
.face{position:absolute;left:0;top:2.75in;width:4.25in;height:2.75in;display:flex;align-items:center;justify-content:center;}
.cut{position:absolute;background:#8d8577;}
.cut.v{left:4.25in;top:0;width:.5pt;height:11in;margin-left:-.25pt;} .cut.h{left:0;top:5.5in;height:.5pt;width:8.5in;margin-top:-.25pt;}
.fold{position:absolute;left:0;width:8.5in;height:0;border-top:.8pt dotted #8d8577;}
.tag{position:absolute;font-size:6.6pt;letter-spacing:.04em;color:#8d8577;background:#fff;padding:0 .04in;}
"""

def cards_pages():
    slots = MODALS + [None] * ((-len(MODALS)) % 4)
    pages = []
    for p in range(0, len(slots), 4):
        cards = ""
        for k, w in enumerate(slots[p:p + 4]):
            x, y = (k % 2) * 4.25, (k // 2) * 5.5
            cards += f'<div class="card" style="left:{x}in;top:{y}in">' + (f'<div class="face">{mark(w, .80)}</div>' if w else "") + "</div>"
        guides = '<div class="cut v"></div><div class="cut h"></div><div class="fold" style="top:2.75in"></div><div class="fold" style="top:8.25in"></div>'
        pages.append(f'<section class="page">{cards}{guides}</section>')
    return "".join(pages)

# ------------------------------------------------------------------ the instruction sheet
def fold_picture():
    """A card flat and a card standing, drawn small."""
    return '''<svg viewBox="0 0 330 150" style="width:2.5in;height:auto;display:block;margin:.08in 0 0" role="img" aria-label="A card flat, with the word on the lower half and a dotted fold across the middle, and the same card standing as a tent.">
  <rect x="6" y="6" width="96" height="124" fill="#fff" stroke="#8d8577" stroke-width="1"/>
  <line x1="6" y1="68" x2="102" y2="68" stroke="#8d8577" stroke-width="1.2" stroke-dasharray="1.5 3"/>
  <text x="54" y="42" text-anchor="middle" font-family="Lexend, sans-serif" font-size="14.5" fill="#6b6256">blank</text>
  <text x="54" y="106" text-anchor="middle" font-family="Lexend, sans-serif" font-size="19" fill="#2b2b2b">could</text>
  <text x="108" y="73" font-family="Lexend, sans-serif" font-size="14.5" fill="#6b6256">fold</text>
  <path d="M152 68 H184 M178 62 L184 68 L178 74" fill="none" stroke="#6b6256" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M214 40 L304 40 L322 112 L232 112 Z" fill="#fff" stroke="#8d8577" stroke-width="1"/>
  <path d="M214 40 L200 104 L232 112" fill="#f1ede4" stroke="#8d8577" stroke-width="1" stroke-linejoin="round"/>
  <text x="270" y="86" text-anchor="middle" font-family="Lexend, sans-serif" font-size="19" fill="#2b2b2b">could</text>
</svg>'''

SHEET_CSS = """
.cols{display:grid;grid-template-columns:1fr 1fr 1fr;column-gap:.42in;margin-top:.17in;}
.cols h2,.why h2{font-family:var(--serif);font-style:italic;font-weight:500;font-size:15pt;margin:0 0 .08in;padding-bottom:.045in;border-bottom:1.2pt solid var(--ink);}
.cols ol{margin:0;padding:0 0 0 1.25em;font-size:10.1pt;line-height:1.4;}
.cols li{margin:0 0 .06in;padding-left:.02in;}
.cols li::marker{font-family:var(--serif);color:var(--soft);}
.cols p{font-size:10.1pt;line-height:1.4;margin:0 0 .07in;}
.cols p.say{font-weight:500;margin-top:.1in;}
.why{margin-top:.15in;display:grid;grid-template-columns:1fr 1fr 1fr;column-gap:.42in;}
.why h2{grid-column:1 / -1;}
.why p{font-size:9.4pt;line-height:1.4;margin:0 0 .07in;}
.why .src{grid-column:1 / -1;font-size:7.2pt;line-height:1.45;color:var(--soft);margin:.03in 0 0;}
"""

def sheet_page():
    return f"""<section class="page">
  <h1>Operator cards</h1>
  <p class="lead">Tent cards for the nine modals, the operators that turn a statement into a question, plus three blank ones.</p>
  <div class="cols">
    <div>
      <h2>Make the cards</h2>
      <ol>
        <li>Print the card pages in colour on card stock, single-sided, at actual size.</li>
        <li>Cut along the solid lines. Each page gives four cards.</li>
        <li>Fold each card in half on the dotted line, so its top and bottom edges meet. Stand it up as a tent.</li>
        <li>Three cards are blank on both faces, for other words your group is working on.</li>
      </ol>
      {fold_picture()}
    </div>
    <div>
      <h2>Run a loop</h2>
      <ol>
        <li>Pick a card, stand it up and build a sentence around it: <i>We&nbsp;could&nbsp;go.</i></li>
        <li>Make a clean pass through each mode: see it, hear it, say it, read it, write it.</li>
        <li>Swap a part: the actor, the action or the operator. <i>She&nbsp;should&nbsp;run.</i></li>
        <li>Tip it into a question, then say both: <i>Should&nbsp;she&nbsp;run?</i></li>
        <li>Loop back to whichever mode needs another pass.</li>
      </ol>
      <p class="say">Point to the word, or the part of the word, as you say it and as the learner says it. That pointing is the feedback.</p>
    </div>
    <div>
      <h2>Mark it by hand</h2>
      <p>Look at the printed word and say it. Then lay the card flat, printed face down, with the fold away from you.</p>
      <ol>
        <li>Write the word on the blank face, and say it slowly.</li>
        <li>Put a circle under each sound, and a swoop under the syllable.</li>
        <li>Draw a bar under letters that spell a sound together, like <i>sh</i>, <i>oul</i> and the <i>ll</i> of <i>will</i>. Add a box only when a vowel follows, as in <i>filling</i>, and keep the bar.</li>
        <li>Go over each vowel in red, with any letters that share its bar, and <i>sh</i> in green.</li>
        <li>Add a cup over a short vowel.</li>
        <li>Turn the card over and check it against the printed face.</li>
      </ol>
    </div>
  </div>
  <div class="why">
    <h2>Why mark by hand</h2>
    <div>
      <p>Marking makes the learner decide how many sounds a word has and which letters spell each one. On the printed face those decisions are already made.</p>
      <p>Elkonin boxes ask for the same two decisions, and a 2019 review of small studies found that they help with phonemic awareness, letter sounds and spelling.</p>
    </div>
    <div>
      <p>Handwriting has support while letters are still new: across 50 experiments, learners who wrote new letters or symbols by hand recognised them better than learners who typed them or only looked. In a kindergarten study, the children who wrote also read the new words better.</p>
    </div>
    <div>
      <p>Once letters are known, studies of spelling mostly find no difference between pencil and keyboard. In one small study of Italian middle-school students, those with dyslexia learned new words better on a keyboard. Where forming letters is the hard part, write the word for the learner to mark.</p>
      <p>These marks themselves have not been tested.</p>
    </div>
    <p class="src">Boxes: Lane (2021), <i>Using Elkonin Boxes</i>, University of Florida Literacy Institute; Ross &amp; Joseph (2019), <i>Preventing School Failure</i> 63, 43–51. New letters: Araújo, Domingues &amp; Fernandes (2022), <i>Educational Psychology Review</i> 34, 1577–1612; Ibaibarriaga, Acha &amp; Perea (2026), <i>Reading and Writing</i> 39, 2389–2411. Spelling: Cunningham &amp; Stanovich (1990), <i>Journal of Educational Psychology</i> 82, 159–162; Vaughn, Schumm &amp; Gordon (1993), <i>Journal of Learning Disabilities</i> 26, 191–198; Ouellette &amp; Tims (2014), <i>Frontiers in Psychology</i> 5, 117. Dyslexia: Cerni, Lonciari &amp; Job (2025), <i>Learning and Instruction</i> 98, 102119.</p>
  </div>
  <div class="foot"><span>Sounds, Symbols and Sentences · Session 1</span><span>Goes with the operator cards and the key to the marks</span></div>
</section>"""

# ------------------------------------------------------------------ the sentence cards: a demonstration set, landscape
# Words the set adds to the notation. Each follows the rules and passes check_marks.py, except page, whose nudged g says /j/.
LW.KEY_ONLY.update({
 "run": "c.r s.u c.n", "hop": "c.h s.o c.p", "hear": "c.h r.ear", "speak": "c.sp t.ea c.k", "spell": "c.sp s.e k.ll",
 "mark": "c.m r.ar c.k", "book": "c.b t.oo c.k", "word": "c.w r.or c.d", "page": "c.p l.a c.g e> ; nudge 3>2",
 "note": "c.n l.o c.t e>", "his": "c.h s.i c.s", "ing": "s.i k.ng"})

SENTENCE_ROWS = [   # the list page: each row holds one or more (group, words) pairs; · separates subgroups
 [("Operators", "[modals] can could will would shall should may might must · [be_forms] am is are was were")],
 [("Actors", "I you he she we they"), ("Not", "not"), ("Joining", "and")],
 [("Before a thing", "the a his her"), ("Things to read", "book word page note")],
 [("Actions", "see hear speak read write spell draw mark · run hop")],
 [("Endings", "ing ing -s -s"), ("Extra letters", "p n"), ("Marks", ". ?")],
]
SENT_WORDS = ("can could will would shall should may might must am is are was were not I you he she we they the a his her "
              "book word page note and see hear speak read write spell draw mark run hop p n ing ing -s -s . ?").split()
LISTED = lambda ws: [w for w in ws.split() if w != "·" and not w.startswith("[")]     # [labels] name a subgroup and are not cards
assert len(SENT_WORDS) == 48 and sorted(SENT_WORDS) == sorted(w for row in SENTENCE_ROWS for _, ws in row for w in LISTED(ws))
OPERATORS = set(LISTED(SENTENCE_ROWS[0][0][1]))
SENT_F = 0.68            # letter size on the sentence cards, in inches (the operator cards use 0.80)
FLIPS = [("she could read .", "could she read ?"), ("she could not read .", "could she not read ?"),
         ("he is read+ing .", "is he read+ing ?"), ("we were hop+p+ing .", "were we hop+p+ing ?"),
         ("they can spell word+-s .", "can they spell word+-s ?")]

def letter_svg(ch, f_in):
    """A single letter, black, with its circle and no swoop: a letter alone is not a syllable."""
    F = 100.0; S, M, B, H = 0.67 * F, 0.30 * F, 1.44 * F, 2.36 * F; w = 2 * M + S; x = M + S / 2
    g = (f'<text x="{x:.1f}" y="{B:.1f}" font-family="Lexend, system-ui, sans-serif" font-size="{F:.1f}" text-anchor="middle" fill="var(--ink)">{ch}</text>'
         f'<circle cx="{x:.1f}" cy="{B + 0.56 * F:.1f}" r="{0.072 * F:.1f}" fill="var(--ink)"/>')
    return f'<svg class="mw" viewBox="0 0 {w:.1f} {H:.1f}" style="width:{w / 100 * f_in:.3f}in;height:{H / 100 * f_in:.3f}in" role="img" aria-label="{ch}">{g}</svg>'

def hyphen_svg(f_in):
    """The hyphen that marks an ending, at the height of the middle of a small letter."""
    F = 100.0; B, H, w = 1.44 * F, 2.36 * F, 0.46 * F
    return (f'<svg class="mw" viewBox="0 0 {w:.1f} {H:.1f}" style="width:{w / 100 * f_in:.3f}in;height:{H / 100 * f_in:.3f}in" aria-hidden="true">'
            f'<line x1="{0.12 * F:.1f}" y1="{B - 0.29 * F:.1f}" x2="{0.36 * F:.1f}" y2="{B - 0.29 * F:.1f}" stroke="var(--ink)" stroke-width="{0.07 * F:.1f}" stroke-linecap="round"/></svg>')

def card_face(w):
    if w in (".", "?"): return f'<span class="punct" aria-label="{"period" if w == "." else "question mark"}">{w}</span>'
    if w == "ing": return mark("ing", SENT_F)
    if w == "-s": return f'<div class="aff">{hyphen_svg(SENT_F)}<div style="margin-left:{-0.30 * SENT_F:.3f}in">{letter_svg("s", SENT_F)}</div></div>'
    if len(w) == 1 and w not in "aI": return letter_svg(w, SENT_F)
    return mark(w, SENT_F)

SENT_CSS = """
.page.cards{display:block;padding:0;width:11in;height:8.5in;}
.scard{position:absolute;width:3.6667in;height:4.25in;}
.scard .face{position:absolute;left:0;top:2.125in;width:3.6667in;height:2.125in;display:flex;align-items:center;justify-content:center;}
.aff{display:flex;}
.scard .face.left{justify-content:flex-start;padding-left:.04in;}
.punct{font-family:var(--sans);font-weight:500;font-size:1.35in;line-height:1;color:var(--ink);transform:translateY(-.1in);}
.sl{margin-top:.13in;}
.sl h2,.fs h2,.notes h2{font-family:var(--serif);font-style:italic;font-weight:500;font-size:15pt;margin:0 0 .07in;padding-bottom:.045in;border-bottom:1.2pt solid var(--ink);}
.srow{display:flex;align-items:baseline;margin:.03in 0;}
.srow .g{font-family:var(--serif);font-style:italic;font-weight:500;font-size:12pt;flex:none;}
.srow .g:first-child{width:1.6in;}
.srow .g:not(:first-child){margin-left:.5in;margin-right:.14in;}
.srow .g span{font-family:var(--sans);font-style:normal;font-size:8.5pt;color:var(--soft);margin-left:.06in;}
.srow .w{font-size:12.5pt;word-spacing:.12em;}
.srow .w .dot{color:var(--soft);padding:0 .08in;}
.srow .w .sub{font-size:8.5pt;color:var(--soft);font-style:italic;font-family:var(--serif);margin-right:.07in;}
.fs{margin-top:.12in;}
.flips{display:grid;grid-template-columns:auto auto auto;justify-content:start;align-items:center;column-gap:.16in;row-gap:.075in;margin-top:.09in;}
.flips .fl{display:flex;column-gap:.06in;}
.flips .jn{display:flex;}
.flips .jn .tile:not(:first-child){border-left-style:dashed;border-top-left-radius:0;border-bottom-left-radius:0;}
.flips .jn .tile:not(:last-child){border-top-right-radius:0;border-bottom-right-radius:0;}
.tile{display:inline-block;font-size:11.5pt;line-height:1;padding:.055in .09in .065in;border:.8pt solid #b9b0a1;border-radius:3pt;min-width:.3in;text-align:center;background:#fff;}
.tile.op{border:1.6pt solid var(--modal);color:var(--modal);font-weight:500;}
.flips .arrow{color:var(--soft);font-size:12pt;}
.fs > p{font-size:8.6pt;color:var(--soft);margin:.08in 0 0;}
.notes{margin-top:.12in;}
.notes .nc{display:grid;grid-template-columns:1fr 1fr;column-gap:.42in;}
.notes p{font-size:9.6pt;line-height:1.4;margin:0 0 .06in;}
.notes i,.fs i{font-family:var(--serif);font-style:italic;}
"""

def sentence_list_page():
    def row(groups):
        out = ""
        for name, ws in groups:
            n = len(LISTED(ws))
            shown = re.sub(r"\[([a-z_]+)\] ", lambda m: f'<span class="sub">{m.group(1).replace("_", " ")}</span>', ws).replace(" · ", "<span class=dot>·</span>")
            out += f'<span class="g">{name}<span>{n}</span></span><span class="w">{shown}</span>'
        return f'<div class="srow">{out}</div>'
    def tiles(line):
        out = []
        for tok in line.split():
            parts = [f'<span class="tile{" op" if t in OPERATORS else ""}">{t}</span>' for t in tok.split("+")]
            out.append(parts[0] if len(parts) == 1 else f'<span class="jn">{"".join(parts)}</span>')
        return "".join(out)
    flips = "".join(f'<div class="fl">{tiles(a)}</div><div class="arrow">→</div><div class="fl">{tiles(b)}</div>' for a, b in FLIPS)
    return f"""<section class="page">
  <h1>Sentence cards</h1>
  <p class="lead">A demonstration set of 48 tent cards about reading and writing. Stand up an actor, an operator and an action, then move the operator to the front to turn the statement into a question.</p>
  <div class="sl"><h2>In the set</h2>{"".join(row(r) for r in SENTENCE_ROWS)}</div>
  <div class="fs"><h2>Flips to try</h2><div class="flips">{flips}</div>
    <p>The outlined card is the operator. It is the only word that moves. <i>Not</i> stays after the actor, and the period and the question mark swap.</p></div>
  <div class="notes"><h2>Notes</h2><div class="nc">
    <div>
      <p>Add <i>ing</i> or <i>-s</i> to an action or a thing: <i>read + ing, word + -s</i>. Before <i>ing</i>, a short vowel needs its last letter doubled, so that a box can stop the vault: <i>hop + p + ing, run + n + ing</i>. That is what the extra <i>p</i> and <i>n</i> are for.</p>
      <p>For <i>writing</i>, lay <i>ing</i> over the <i>e</i> of <i>write</i>. The <i>i</i> covers the final <i>e</i>, so no vowel team forms, and it still reaches back to keep the first <i>i</i> long.</p>
      <p>Match the form of <i>be</i> to the actor: <i>I am, she is, they were</i>.</p>
    </div>
    <div>
      <p>The words are in lower case, so a card works at the start of a sentence or after the operator. <i>I</i> is always a capital.</p>
      <p>There are no cards for <i>do, does</i> and <i>did</i>. Those flips change the verb (<i>she reads, does she read?</i>), so they are left for later.</p>
      <p>Print pages 2 to 9 in colour on card stock, single-sided, at actual size. Cut along the solid lines: each page gives six cards. Fold each card in half on the dotted line so its top and bottom edges meet, and stand it up.</p>
    </div>
  </div></div>
  <div class="foot"><span>Sounds, Symbols and Sentences · Session 1</span><span>Goes with the operator cards and the key to the marks</span></div>
</section>"""

def sentence_card_pages():
    pages = []
    for p0 in range(0, len(SENT_WORDS), 6):
        cards = ""
        for k, w in enumerate(SENT_WORDS[p0:p0 + 6]):
            x, y = (k % 3) * 3.6667, (k // 3) * 4.25
            edge = ' left' if w == "ing" else ""          # ing sits at the left edge, so laid over write it covers the e
            cards += f'<div class="scard" style="left:{x:.4f}in;top:{y}in"><div class="face{edge}">{card_face(w)}</div></div>'
        guides = ('<div class="cut v" style="left:3.6667in;height:8.5in"></div><div class="cut v" style="left:7.3333in;height:8.5in"></div>'
                  '<div class="cut h" style="width:11in;top:4.25in"></div>'
                  '<div class="fold" style="top:2.125in;width:11in"></div><div class="fold" style="top:6.375in;width:11in"></div>')
        pages.append(f'<section class="page cards">{cards}{guides}</section>')
    return "".join(pages)

# ------------------------------------------------------------------ build
def doc(title, css, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(title)}</title><style>{FONT_CSS}\n{BASE_CSS}\n{css}</style></head>'
            f"<body>{body}</body></html>")

DOCS = [
 ("sounds-and-marks-key", "The 44 sounds of English, and marking a word", SOUNDS_CSS + MARKS_CSS, sounds_page() + marks_page(), ("11in", "8.5in")),
 ("operator-cards", "Operator cards", CARDS_CSS, cards_pages(), ("8.5in", "11in")),
 ("operator-cards-instructions", "Operator cards: instructions", SOUNDS_CSS + SHEET_CSS, sheet_page(), ("11in", "8.5in")),
 ("sentence-cards", "Sentence cards", SOUNDS_CSS + CARDS_CSS.replace("@page{size:8.5in 11in;margin:0;}", "").replace(".page{width:8.5in;height:11in;display:block;}", "") + SENT_CSS,
  sentence_list_page() + sentence_card_pages(), ("11in", "8.5in")),
]

# Run in the page before printing. A page clips what does not fit, so nothing here may be left to the eye alone.
CHECK_JS = """() => [...document.querySelectorAll('.page')].map((pg, i) => {
  const R = pg.getBoundingClientRect(), o = {page: i + 1, overflowY: pg.scrollHeight - pg.clientHeight, overflowX: pg.scrollWidth - pg.clientWidth, outside: [], crowded: [], free: null};
  pg.querySelectorAll('h1,h2,p,li,b,svg,.kw,.cell,.set,.face,.foot').forEach(el => { const b = el.getBoundingClientRect();
    if (b.width && (b.right > R.right + .5 || b.bottom > R.bottom + .5 || b.left < R.left - .5 || b.top < R.top - .5)) o.outside.push((el.className && el.className.baseVal === undefined ? el.className : el.tagName) + ':' + (el.textContent || '').trim().slice(0, 24)); });
  pg.querySelectorAll('.gw').forEach(row => { const ws = [...row.querySelectorAll('.kw')].map(k => [k.textContent, k.querySelector('.w').getBoundingClientRect(), k.querySelector('.ipa').getBoundingClientRect(), k.closest('.col').getBoundingClientRect()]);
    ws.forEach(([t, a, ia, col], x) => { if (a.right > col.right + .5 || ia.right > col.right + .5) o.crowded.push(t + ' leaves its column');
      ws.slice(x + 1).forEach(([u, c]) => { if (Math.abs(a.top - c.top) < 4 && a.right > c.left - 8 && a.left < c.right) o.crowded.push(t + ' runs into ' + u); }); }); });
  pg.querySelectorAll('.cell, .set, .face').forEach(box => { const B = box.getBoundingClientRect(); box.querySelectorAll('svg').forEach(v => { const b = v.getBoundingClientRect(); if (b.right > B.right + .5) o.crowded.push('a marked word is wider than its place: ' + v.getAttribute('aria-label')); }); });
  pg.querySelectorAll('.face:not(.left)').forEach(box => { const B = box.getBoundingClientRect(); [...box.children].forEach(v => { const b = v.getBoundingClientRect(), m = 24;
    if (b.left < B.left + m || b.right > B.right - m || b.top < B.top + m / 2 || b.bottom > B.bottom - m / 2) o.crowded.push('too close to the edge of its card: ' + (v.getAttribute('aria-label') || v.textContent)); }); });
  const f = pg.querySelector('.foot'); if (f && f.previousElementSibling) o.free = +((f.getBoundingClientRect().top - f.previousElementSibling.getBoundingClientRect().bottom) / 96).toFixed(2);
  return o; })"""

async def main():
    OUT.mkdir(parents=True, exist_ok=True); WORK.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        br = await p.chromium.launch()
        page = await br.new_page()
        for name, title, css, body, (w, h) in DOCS:
            f = WORK / f"{name}.html"; f.write_text(doc(title, css, body), encoding="utf-8")
            await page.goto(f.as_uri()); await page.evaluate("document.fonts.ready")
            fonts = await page.evaluate("Array.from(document.fonts).filter(f => f.status === 'loaded').map(f => f.family).length")
            await page.emulate_media(media="print")
            for r in await page.evaluate(CHECK_JS):
                bad = r["overflowY"] > 1 or r["overflowX"] > 1 or r["outside"] or r["crowded"]
                print(f"  {name} p{r['page']}: free above footer {r['free']} in" + (f" | PROBLEM {r}" if bad else ""))
                assert not bad, (name, r)
            await page.pdf(path=str(OUT / f"{name}.pdf"), width=w, height=h, print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            print("wrote", OUT / f"{name}.pdf", "| fonts loaded:", fonts)
        await br.close()

asyncio.run(main())
