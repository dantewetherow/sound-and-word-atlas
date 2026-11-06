"""Build the Sound and Word Atlas site (version 1: the route and its steps) from the manual's route data.

usage: python3 build_site.py <route.json> <out dir> [--standalone]
The route.json comes from the manual (see ../README.md). Words are drawn with legomorphic_words.py and the
codes the deck tools already use, plus site_codes.py for route words that had none.
--standalone writes the home page as a full document, for a web host such as GitHub Pages. Without it the home
page has no doctype or head, because claude.ai adds those when it publishes the page as an artifact."""
import sys, json, re, html, pathlib, shutil
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
STANDALONE = "--standalone" in sys.argv[3:]
import legomorphic_words as LW
from known_codes import all_codes
import site_codes as SC

route = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = pathlib.Path(sys.argv[2]); (OUT / "steps").mkdir(parents=True, exist_ok=True)
codes, _ = all_codes()
for w, c in SC.SITE_CODES.items(): codes.setdefault(w, c)
LW.W.clear(); LW.W.update(codes)
STEPS = route["steps"]; N = len(STEPS)
BUILT = "5 November 2026"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..600;1,9..144,400..600'
         '&family=Lexend:wght@300;400;500&display=swap">')

def md(s):
    """The manual's inline markdown (italics for cited words) to HTML."""
    s = html.escape(s.replace("**", ""), quote=False)
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)

def plain(s): return re.sub(r"\*", "", s)

def groups_of(words_md):
    """The step's words, kept in the groups the manual writes them in (be/bed is a pair)."""
    main = words_md.replace("**", "").split("; contrast")[0].replace("*", "")
    out = []
    for item in re.split(r"[;,]", main):
        for part in item.split("→"):
            g = [w.strip() for w in part.split("/") if w.strip()]
            if g: out.append(g)
    return out

def svg_of(word, F, code=None, label=None):
    if code: old = LW.W.get(word); LW.W[word] = code
    try:
        svg, _, _ = LW.svg_strip([word], F=F, cls=False, label=label or f"{word}, marked")
    finally:
        if code: LW.W[word] = old
    return svg

def coloured(word, code=None):
    """A word with its letters in their colours, as the orientation map shows them."""
    if word in SC.UNMARKED or (word not in LW.W and not code): return f'<span class="cw">{html.escape(word)}</span>'
    if code: old = LW.W.get(word); LW.W[word] = code
    try: letters = LW.parse(word)["letters"]
    finally:
        if code: LW.W[word] = old
    cls = {"vowel": "v", "team": "g", "consonant": ""}
    return '<span class="cw">' + "".join(f'<span class="{cls[l["type"]]}">{html.escape(l["ch"])}</span>' if cls[l["type"]] else html.escape(l["ch"]) for l in letters) + "</span>"

def word_cells(group, F):
    cells = []
    for w in group:
        if w in SC.VARIANTS:
            for code, gloss in SC.VARIANTS[w]:
                cells.append(f'<figure class="word">{svg_of(w, F, code, f"{w}, as in {gloss}, marked")}<figcaption>{html.escape(gloss)}</figcaption></figure>')
        elif w in SC.UNMARKED or w not in LW.W:
            cells.append(f'<figure class="word unmarked"><span class="plain" style="font-size:{F:.0f}px">{html.escape(w)}</span>'
                         f'<figcaption>not marked yet</figcaption></figure>')
        else:
            cells.append(f'<figure class="word">{svg_of(w, F)}</figure>')
    return cells

def page(title, body, depth, desc):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{html.escape(desc)}">
<title>{html.escape(title)}</title>
{FONTS}
<link rel="stylesheet" href="{up}site.css">
</head>
<body>
{body}
</body>
</html>
"""

def header(depth):
    up = "../" * depth
    return (f'<header class="site"><div class="wrap"><a class="brand" href="{up}index.html"><small>Legomorphic notation</small>Sound and Word Atlas</a>'
            f'<nav class="site" aria-label="Site"><a href="{up}index.html#route">The route</a><a href="{up}index.html#marks">Reading the marks</a>'
            f'<a href="{up}cards.html">Word cards</a><a href="{up}index.html#about">About</a></nav></div></header>')

def footer(depth):
    return ('<footer class="site"><div class="wrap"><p>Built on ' + BUILT + ' from the <i>Legomorphic notation</i> manual. '
            'Steps 16 to 32 are a draft. Page references are to Edward Carney, <i>A Survey of English Spelling</i> (Routledge, 1994).</p></div></footer>')

def fname(n): return f"{n:02d}.html"

def open_items_for(n):
    out = []
    for item in route["open"]:
        nums = {int(x) for x in re.findall(r"\b(?:step|steps)\s+(\d+)", item, re.I)}
        nums |= {int(x) for x in re.findall(r"\band\s+(\d+)\)", item)}
        if n in nums: out.append(item)
    return out

# ------------------------------------------------------------------ step pages
for i, s in enumerate(STEPS):
    n = s["n"]; band = s["band"]
    prev_s = STEPS[i - 1] if i else None; next_s = STEPS[i + 1] if i + 1 < N else None
    cells = []
    for g in groups_of(s["words_md"]):
        inner = word_cells(g, 58)
        cells.append(f'<div class="group{" pair" if len(inner) > 1 else ""}">' + "".join(inner) + "</div>")
    notes = []
    marks = s["marks"].strip()
    notes.append(f'<div class="note"><h2>New marks</h2><p>{md(marks) if marks.lower() != "none" else "None: the step uses marks already met."}</p></div>')
    if s.get("contrast_md"):
        notes.append(f'<div class="note"><h2>Contrast</h2><p>{md(s["contrast_md"])}</p></div>')
    k = s["kernel_md"].strip()
    notes.append(f'<div class="note"><h2>Kernel words</h2><p>{md(k) if k.lower() != "none" else "None at this step."}</p></div>')
    notes.append(f'<div class="note"><h2>Carney (1994)</h2><p>{md(s.get("carney", ""))}</p></div>')
    for item in open_items_for(n):
        notes.append(f'<div class="note open"><h2>Open on this step</h2><p>{md(item)}</p></div>')
    unmarked = sorted({SC.UNMARKED[w] for g in groups_of(s["words_md"]) for w in g if w in SC.UNMARKED})
    um = f'<p class="unmarked-note">Words in plain letters are not marked yet: {html.escape("; ".join(unmarked))}.</p>' if unmarked else ""
    draft = ' <span class="badge">Draft</span>' if n >= 16 else ""
    pn = '<nav class="pn" aria-label="Steps">'
    pn += (f'<a class="prev" href="{fname(prev_s["n"])}"><span>Step {prev_s["n"]}</span>{md(prev_s["title"])}</a>' if prev_s else '<span></span>')
    pn += (f'<a class="next" href="{fname(next_s["n"])}"><span>Step {next_s["n"]}</span>{md(next_s["title"])}</a>' if next_s else '<span></span>')
    pn += "</nav>"
    body = f"""{header(1)}
<main class="wrap">
<div class="step-head">
<p class="eyebrow"><a href="../index.html#band-{re.sub(r'[^a-z]+', '-', band.lower()).strip('-')}">{html.escape(band)}</a> · Step {n} of {N}{draft}</p>
<h1>{md(s['title'])}</h1>
</div>
<div class="plate">
<section class="words" aria-label="The step's words, marked">
{''.join(cells)}
</section>
<aside class="notes">
{''.join(notes)}
</aside>
</div>
{um}
{pn}
</main>
{footer(1)}"""
    t = f"Step {n}: {plain(s['title'])}"
    (OUT / "steps" / fname(n)).write_text(page(t, body, 1, f"{t}, on the Sound and Word Atlas route."), encoding="utf-8")

# ------------------------------------------------------------------ home page (the artifact's own page: no doctype, the host adds it)
def tile(s):
    words = []
    for g in groups_of(s["words_md"]):
        for w in g:
            if w in SC.VARIANTS:
                words.append(coloured(w, SC.VARIANTS[w][0][0]))
            else:
                words.append(coloured(w))
    seen, uniq = set(), []
    for w in words:
        if w not in seen: seen.add(w); uniq.append(w)
    return (f'<a class="tile" href="steps/{fname(s["n"])}"><span class="num">{s["n"]}</span>'
            f'<span class="t">{md(s["title"])}</span><span class="w">{" ".join(uniq)}</span></a>')

bands_html = []
for b in route["bands"]:
    ss = [x for x in STEPS if x["n"] in b["steps"]]
    slug = re.sub(r"[^a-z]+", "-", b["name"].lower()).strip("-")
    draft = '<span class="badge">Draft</span>' if min(b["steps"]) >= 16 else ""
    bands_html.append(f'<section class="band" id="band-{slug}"><div class="band-label"><h3>{html.escape(b["name"])}</h3>'
                      f'<p>Steps {min(b["steps"])} to {max(b["steps"])}</p>{draft}</div>'
                      f'<div class="tiles">{"".join(tile(x) for x in ss)}</div></section>')

KEY = [("Sound circle", "One circle under each sound: red for a vowel sound, black for a consonant, green for <em>sh</em>, <em>th</em>, <em>ch</em>", ["it", "she"]),
       ("Syllable swoop", "One swoop under each syllable", ["happy"]),
       ("Short mark", "A cup over a vowel that keeps its short sound", ["get"]),
       ("Long mark", "A bar over a vowel that says its name", ["go"]),
       ("Bond bar", "A bar under letters that spell one sound: black for consonant units and for doubled letters, boxed or not, green for <em>sh</em>, <em>th</em>, <em>ch</em>, red for vowel units", ["will", "she", "night"]),
       ("R-controlled unit", "A red bar under a vowel and its <em>r</em>, with the vowel red, the <em>r</em> black and one circle", ["car"]),
       ("Block box", "A box around the vowel protector at work: a pair or cluster with a vowel after it, which it stops from reaching back. A pair keeps its bond bar when the box comes; a cluster has none", ["hopping"]),
       ("Cone of silence", "A dotted ring around a silent <em>e</em>", ["have"]),
       ("Vowel vault", "An arc from an <em>e</em>, or a vowel after one consonant, back to the vowel it makes long", ["make"]),
       ("Nice-nudge", "A small arc under the letters from <em>e</em>, <em>i</em> or <em>y</em> to the <em>c</em> or <em>g</em> it softens", ["nice"]),
       ("Blocked vault", "A half-arc that ends in a red X where a box stops the vault", ["getting"]),
       ("Morpheme seam", "A dotted line between morphemes", ["going"])]
key_html = "".join(f'<figure class="mark"><div class="mw">{"".join(svg_of(w, 34) for w in ws)}</div>'
                   f'<figcaption><b>{name}</b>{what}</figcaption></figure>' for name, what, ws in KEY)

uniq = {w for s in STEPS for g in groups_of(s["words_md"]) for w in g}
n_words = len(uniq) + sum(len(v) - 1 for w, v in SC.VARIANTS.items() if w in uniq)
n_marked = n_words - len([w for w in uniq if w in SC.UNMARKED or (w not in LW.W and w not in SC.VARIANTS)])

home_head = f"""<title>Sound and Word Atlas</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<link rel="stylesheet" href="site.css">
"""
home_body = f"""{header(0)}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">For teachers · Version 1</p>
<h1>Sound and Word Atlas</h1>
<p class="lead">{md(route["intro"].split(" The orientation map")[0])} Open a step to see its words marked, the marks it brings in, and the pages in Carney's survey that back it.</p>
</div></section>
<section class="route" id="route" aria-labelledby="route-h"><div class="wrap">
<h2 id="route-h">The route at a glance</h2>
<p class="sub">Each word is shown with its letters in colour: red for vowels, green for <em>sh</em>, <em>th</em> and <em>ch</em>, black for the rest.</p>
{''.join(bands_html)}
</div></section>
<section class="marks" id="marks" aria-labelledby="marks-h"><div class="wrap">
<h2 id="marks-h">Reading the marks</h2>
<p class="sub">Twelve marks, as the manual's legend gives them. The rules behind them are in the manual.</p>
<div class="key">{key_html}</div>
</div></section>
<section class="about" id="about" aria-labelledby="about-h"><div class="wrap">
<h2 id="about-h">About this version</h2>
<div class="cols">
<div><h3>What's here</h3><p>The route: {N} steps in {len(route["bands"])} bands, {n_words} different words, {n_marked} of them marked. Printable cards for the ELP high-frequency words are on the <a href="cards.html">Word cards</a> page. The legend in full, the word families and the teaching routines come next.</p></div>
<div><h3>Where it comes from</h3><p>The route and its notes come from the <i>Legomorphic notation</i> manual, and the site is rebuilt from it, so corrections go into the manual first. The marks are drawn with the same tools as the session decks.</p></div>
<div><h3>Still settling</h3><p>Steps 16 to 32 were added as a draft on 15 October 2026. A few words show in plain letters until their marking is decided.</p></div>
</div>
</div></section>
</main>
{footer(0)}"""
if STANDALONE:
    home = page("Sound and Word Atlas", home_body, 0,
                "A route through English spelling for teachers: 32 steps, with every word marked in legomorphic notation.")
else:
    home = home_head + home_body
(OUT / "index.html").write_text(home, encoding="utf-8")

# The word cards page, written when the card PDFs are in <out>/cards (build_elp_cards.py makes them).
CARD_SETS = [("elp-word-cards-kindergarten.pdf", "Kindergarten", "K", "List 1", 8),
             ("elp-word-cards-grade-1.pdf", "Grade 1", "1", "Lists 2 to 10", 10),
             ("elp-word-cards-grade-2.pdf", "Grade 2", "2", "Lists 11 to 13", 10)]
ELP_FILE = HERE / "data" / "elp_hfw.json"
if ELP_FILE.exists() and all((OUT / "cards" / f).exists() for f, *_ in CARD_SETS):
    ELP = json.loads(ELP_FILE.read_text(encoding="utf-8"))
    tiles = []
    for f, title, grade, lists, per in CARD_SETS:
        n = sum(len(v["words"]) for v in ELP["lists"].values() if v["grade"] == grade)
        kb = round((OUT / "cards" / f).stat().st_size / 1024)
        tiles.append(f'<div><h3>{title}</h3><p>{lists}: {n} cards on {-(-n // per)} sheets, {per} to a page.</p>'
                     f'<p><a href="cards/{f}" download>Download the PDF</a> ({kb} KB)</p></div>')
    sample = (f'<div class="words"><figure class="word"><span class="plain" style="font-size:58px">make</span><figcaption>front</figcaption></figure>'
              f'<figure class="word">{svg_of("make", 58)}<figcaption>back</figcaption></figure></div>')

    # The grade 3 word sum cards (build_word_sum_cards.py), shown when their PDF is there too.
    WS_FILE = "word-sum-cards-grade-3.pdf"
    ws_html = ""
    if (OUT / "cards" / WS_FILE).exists():
        import word_sum_codes as WS
        groups = []
        for short, title, rows in WS.SECTIONS:
            groups.append((title, len(rows)))
            if short == "Prefixes": groups.append(("Pairs that aren't word sums", len(WS.PAIRS)))
        sheet, ranges = 1, []
        for title, n in groups:
            k = -(-n // 10)
            ranges.append(f'<li>{"Sheets" if k > 1 else "Sheet"} {sheet}{f"&ndash;{sheet + k - 1}" if k > 1 else ""}: {html.escape(title[0].lower() + title[1:])} ({n} cards)</li>')
            sheet += k
        n_cards = sum(n for _, n in groups)
        kb = round((OUT / "cards" / WS_FILE).stat().st_size / 1024)
        ws_sample = (f'<div class="words"><figure class="word"><span class="plain" style="font-size:58px">making</span><figcaption>front</figcaption></figure>'
                     f'<figure class="word"><span style="font-size:15px;color:var(--soft)">make + ing &rarr; making</span>{svg_of("making", 58)}<figcaption>back</figcaption></figure></div>')
        ws_html = f"""
<section class="about" id="word-sums" aria-labelledby="ws-h"><div class="wrap">
<h2 id="ws-h">Grade 3 word sums</h2>
<p class="sub">An extension for students who have finished the ELP lists: {n_cards} cards built on the list words. The front has the whole word. The back has its word sum, such as make + ing &rarr; making, and the word coded with a seam at each join. Each group starts on a new sheet, so you can print just the rule you're teaching.</p>
<p><a href="cards/{WS_FILE}" download>Download the PDF</a> ({kb} KB, {sheet - 1} sheets, 10 to a page)</p>
<ul class="sub">{''.join(ranges)}</ul>
{ws_sample}
</div></section>"""
    cards_body = f"""{header(0)}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">Downloads</p>
<h1>Word cards</h1>
<p class="lead">Printable cards with the plain word on the front and the coded word on the back: high-frequency words from the SD23 Early Literacy Profile lists, and word sums for students who have finished them.</p>
</div></section>
<section class="about" id="elp" aria-labelledby="elp-h"><div class="wrap">
<h2 id="elp-h">ELP high-frequency words</h2>
<div class="cols">{''.join(tiles)}</div>
{sample}
</div></section>{ws_html}
<section class="about" aria-label="Notes"><div class="wrap"><div class="cols">
<div><h3>Printing</h3><p>Print in colour and double-sided, flipping on the long edge, so each back lands behind its front. Print one sheet first and hold it up to a window to check that the backs line up, then cut on the grey lines. Spaces left over on a sheet are blank cards to write on.</p></div>
<div><h3>The coding</h3><p>The coded sides show the markings as they stand in the manual now. Some words still have marking calls open, including most of the word sum markings, which are new, and the cards will be rebuilt when those are ruled.</p></div>
<div><h3>Where the words come from</h3><p>The Early Literacy Profile (ELP) Assessment &amp; Instructional Guide, Central Okanagan Public Schools (2025), pp. 16&ndash;17. The guide doesn't name a source for its lists; it says they were aligned with a phonics scope and sequence, keeping one word for each pattern. These cards aren't an SD23 publication. The district's own <a href="https://assessment.sd23.bc.ca/elp">ELP page</a> is the place for the assessment itself.</p></div>
<div><h3>Word sums</h3><p>Word sums and word matrices come from Melvyn Ramsden's Real Spelling, and Peter Bowers brought them into classrooms as structured word inquiry. The base words come from the ELP lists and E. W. Dolch's grade 3 list (Dolch, 1936).</p></div>
</div></div></section>
</main>
{footer(0)}"""
    (OUT / "cards.html").write_text(page("Word cards · Sound and Word Atlas", cards_body, 0,
                                         "Printable high-frequency word cards from the SD23 ELP lists, plain on the front and coded on the back."), encoding="utf-8")
    print("wrote cards.html |", ", ".join(t for _, t, *_ in CARD_SETS))

if (HERE / "site.css").exists():
    shutil.copy(HERE / "site.css", OUT / "site.css")
print("wrote", OUT, "| words", n_words, "marked", n_marked)
