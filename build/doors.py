"""The seven doors, the site's tree, breadcrumbs, search and the Teacher/Student view (8 November 2026).

The site plan (Sound and Word Atlas: site plan) names seven doors as one word family, each a doing turned into a thing
with -ion: Progressions, Notations, Explorations, Constructions, Derivations, Instructions and Explanations. Today's
pages sit behind them. PAGES is the one place that says which page sits behind which door: the header's doors, the
breadcrumbs, the site map and the search's page records all come from it.

The Teacher/Student switch shows the same pages two ways, as Bright/Night shows them in two colourings. Student view
shows five doors, each with a short word, draws the words on a step page big, and hides the teacher's notes and the
build's under-construction notes. Instructions and Explanations are teachers' doors, so student view leaves them out.
A link ending ?view=student opens a page in student view, for the board, and the pick is kept in this browser.
Without script, a page shows the teacher view.

Search runs in the reader's browser over search.json, which the build writes: every word on the route and the lists,
every step, mark, term and page. Nothing typed leaves the device. Without script the box stays hidden, and the header's
Site map link stands in for it."""
import html, json, re

DOORS = [   # slug, name, word sum, in plain words, the short word in student view (None: a teachers' door)
    ("progressions", "Progressions", "progress + ion + s", "The route through English spelling, step by step.", "Steps"),
    ("notations", "Notations", "not(e) + at(e) + ion + s", "The marks, and what each one shows.", "Marks"),
    ("explorations", "Explorations", "explor(e) + at(e) + ion + s", "Words to take apart and build: families and contrasts.", "Words"),
    ("constructions", "Constructions", "construct + ion + s", "How sentences are built: actors, operators and actions, and the flip from claim to question.", "Sentences"),
    ("derivations", "Derivations", "deriv(e) + at(e) + ion + s", "Where words come from: roots, and what the parts of words mean.", "Roots"),
    ("instructions", "Instructions", "instruct + ion + s", "How to teach it: presentations, word cards and word lists.", None),
    ("explanations", "Explanations", "expla(i)n + at(e) + ion + s", "Why it works: definitions, the notation and its name, and credits.", None),
]
DOOR = {d[0]: d for d in DOORS}

# The tree: (path, door, title, one-line summary). Steps join it in tree(). A page behind a teachers' door is for teachers.
PAGES = [
    ("index.html", None, "Home", "Legomorphic Notation and the seven doors into the atlas."),
    ("progressions.html", "progressions", "Progressions", "The route through English spelling: the steps in their bands."),
    ("notations.html", "notations", "Notations", "The marks of Legomorphic Notation, each drawn alone on one word."),
    ("explorations.html", "explorations", "Explorations", "Words to take apart and build, starting with note, notate and notation."),
    ("constructions.html", "constructions", "Constructions", "How sentences are built, and the flip from claim to question."),
    ("derivations.html", "derivations", "Derivations", "Where words come from, and the sources the roots will cite."),
    ("instructions.html", "instructions", "Instructions", "How to teach it: presentations, word cards and word lists."),
    ("presentations.html", "instructions", "Presentations", "The staff series: each session's deck and its handouts."),
    ("cards.html", "instructions", "Word cards", "Printable cards: the ELP and Dolch words, and grade 3 word sums."),
    ("word-lists.html", "instructions", "Word lists", "Where the ELP words come from in Dolch's lists."),
    ("explanations.html", "explanations", "Explanations", "Why it works: definitions, the notation and its name, and credits."),
    ("definitions.html", "explanations", "Definitions", "What the notation's words mean, and where they come from."),
    ("about.html", "explanations", "About the notation", "The notation, its name, and how it came about."),
    ("credits.html", "explanations", "Credits and contact", "The writers the notation draws on, and how to get in touch."),
    ("sitemap.html", None, "Site map", "Every page, door by door."),
]
TEACHERS = {s for s, *_, w in DOORS if w is None}


def tree(STEPS, plain):
    steps = [(f"steps/{s['n']:02d}.html", "progressions", f"Step {s['n']}: {plain(s['title'])}", f"The words of step {s['n']}, marked.")
             for s in STEPS]
    i = next(k for k, p in enumerate(PAGES) if p[0] == "progressions.html")
    return PAGES[:i + 1] + steps + PAGES[i + 1:]


# ------------------------------------------------------------------ the header's pieces
VIEW_HEAD = ("<script>(() => { const r = document.documentElement; let v = null;"
             " try { v = new URLSearchParams(location.search).get('view'); } catch (e) {}"
             " try { if (v === 'student' || v === 'teacher') localStorage.setItem('view', v); else v = localStorage.getItem('view'); } catch (e) {}"
             " if (v === 'student') r.dataset.view = 'student'; })();</script>")

VIEW_SWITCH = ('<div class="view" role="group" aria-label="View" hidden>'
               '<button type="button" data-v="teacher">Teacher</button><button type="button" data-v="student">Student</button></div>')


def header_parts(up):
    """The search box, the site map link, the view switch, the menu button and the doors, for header()."""
    search = (f'<div class="search" data-up="{up}" role="search" hidden><label class="sr" for="q">Search the atlas</label>'
              f'<input id="q" type="search" placeholder="Search words, steps, marks" autocomplete="off" spellcheck="false" '
              f'aria-describedby="q-count"><span class="sr" id="q-count" aria-live="polite"></span><div class="results" hidden></div></div>')
    smap = f'<a class="smap" href="{up}sitemap.html">Site map</a>'
    menu = '<button class="menu" type="button" aria-expanded="false" aria-controls="doors" hidden>Menu</button>'
    links = "".join(f'<a class="door{" t-only" if sw is None else ""}" href="{up}{slug}.html" data-door="{slug}">'
                    f'<span class="dn">{name}</span>{f"<span class=sn>{sw}</span>" if sw else ""}</a>' for slug, name, _, _, sw in DOORS)
    doors = f'<nav class="doors" id="doors" aria-label="Doors">{links}</nav>'
    return search, smap, VIEW_SWITCH, menu, doors


VIEW_JS = """<script>(() => {
  const root = document.documentElement, sw = document.querySelector('.view');
  if (!sw) return;
  const now = () => root.dataset.view === 'student' ? 'student' : 'teacher';
  const show = () => sw.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.v === now())));
  sw.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.v === 'student') root.dataset.view = 'student'; else delete root.dataset.view;
    try { localStorage.setItem('view', b.dataset.v); } catch (err) {}
    show();
  });
  sw.hidden = false; show();
})();</script>"""

# On a narrow screen the doors fold into one Menu button. Without script they stay open.
MENU_JS = """<script>(() => {
  const head = document.querySelector('header.site'), b = head && head.querySelector('.menu');
  if (!b) return;
  document.documentElement.classList.add('js-menu'); b.hidden = false;
  b.addEventListener('click', () => { const open = head.classList.toggle('open'); b.setAttribute('aria-expanded', String(open)); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && head.classList.contains('open')) { head.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); b.focus(); } });
})();</script>"""

SEARCH_JS = """<script>(() => {
  const box = document.querySelector('.search');
  if (!box || !window.fetch) return;
  const up = box.dataset.up || '', q = box.querySelector('input'), out = box.querySelector('.results'), count = box.querySelector('#q-count');
  box.hidden = false; document.documentElement.classList.add('js-search');
  let data = null, loading = null;
  const load = () => loading || (loading = fetch(up + 'search.json').then(r => r.json()).then(j => { data = j; render(); }).catch(() => { data = []; }));
  const KINDS = [['word', 'Words'], ['step', 'Steps'], ['mark', 'Marks'], ['term', 'Terms'], ['page', 'Pages']], CAP = 6;
  const norm = s => s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').replace(/[’']/g, '');
  const esc = s => s.replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const student = () => document.documentElement.dataset.view === 'student';
  function render() {
    const said = q.value.trim(), t = norm(said);
    if (!t) { out.hidden = true; out.innerHTML = ''; count.textContent = ''; return; }
    if (!data) { load(); return; }
    // several words are also looked up one at a time, in the order typed: she could go
    const terms = [...new Set(t.split(/[^a-z0-9-]+/).filter(Boolean))], many = terms.length > 1;
    const hits = {}, found = new Set();
    for (const r of data) {
      if (r.x && student()) continue;
      const l = norm(r.l), k = r.k ? norm(r.k) : '';
      let s = l === t ? 0 : l.startsWith(t) ? 1 : l.includes(t) ? 2 : (' ' + k).includes(' ' + t) ? 3 : k.includes(t) ? 4 : -1;
      if (many && r.t === 'word' && terms.includes(l)) { s = 0.5 + terms.indexOf(l) / 1000; found.add(l); }
      else if (s < 0 && many && terms.every(w => (l + ' ' + k).includes(w))) s = 5;   // every word typed, in any order: short vowel
      if (s >= 0) (hits[r.t] = hits[r.t] || []).push([s, r]);
    }
    let h = '', n = 0;
    for (const [kind, label] of KINDS) {
      const list = (hits[kind] || []).sort((a, b) => a[0] - b[0] || a[1].l.length - b[1].l.length || a[1].l.localeCompare(b[1].l));
      if (!list.length) continue;
      const more = list.length > CAP;
      h += '<p class="rk">' + label + (more ? ' (' + list.length + ')' : '') + '</p><ul>'
         + list.map(([, r], i) => '<li' + (i >= CAP ? ' hidden' : '') + '><a href="' + esc(up + r.u) + '">' + esc(r.l) + (r.s ? '<span>' + esc(r.s) + '</span>' : '') + '</a></li>').join('')
         + '</ul>' + (more ? '<button type="button" class="more">Show all ' + list.length + '</button>' : '');
      n += list.length;
    }
    const missing = many && found.size ? terms.filter(w => !found.has(w) && (w.length > 1 || w === 'a' || w === 'i')) : [];
    if (n && missing.length) h += '<p class="rk none">Not on the site yet: ' + missing.map(esc).join(', ') + '</p>';
    out.innerHTML = n ? h : '<p class="rk none">Nothing found for \\u201c' + esc(said) + '\\u201d. The <a href="' + up + 'sitemap.html">site map</a> lists every page.</p>';
    out.hidden = false;
    count.textContent = n ? n + (n === 1 ? ' result' : ' results') : 'No results';
  }
  const links = () => [...out.querySelectorAll('a, button.more')].filter(e => !e.hidden && !e.closest('[hidden]'));
  const close = () => { out.hidden = true; };
  out.addEventListener('click', e => {             // Show all: the rest of that group, and focus on the first of them
    const b = e.target.closest('button.more'); if (!b) return;
    const ul = b.previousElementSibling, first = ul.querySelector('li[hidden] a');
    ul.querySelectorAll('li[hidden]').forEach(li => { li.hidden = false; });
    b.hidden = true; if (first) first.focus();
  });
  q.addEventListener('focus', load);
  q.addEventListener('input', render);
  q.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { const a = links()[0]; if (a) { e.preventDefault(); a.focus(); } }
    else if (e.key === 'Escape') { q.value = ''; render(); }
    else if (e.key === 'Enter') { const a = out.querySelector('a'); if (a && !out.hidden) { e.preventDefault(); location.href = a.href; } }
  });
  out.addEventListener('keydown', e => {
    const ls = links(), i = ls.indexOf(document.activeElement);
    if (e.key === 'ArrowDown' && i < ls.length - 1) { e.preventDefault(); ls[i + 1].focus(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); (i > 0 ? ls[i - 1] : q).focus(); }
    else if (e.key === 'Escape') { close(); q.focus(); }
  });
  document.addEventListener('click', e => { if (!box.contains(e.target)) close(); });
  q.addEventListener('focus', () => { if (q.value.trim()) render(); });
})();</script>"""


# ------------------------------------------------------------------ the pages
def door_head(slug, extra=""):
    _, name, ws, plain_words, sw = DOOR[slug]
    word = name[:-1].lower()
    student = f'<h1 class="s-only">{sw}</h1>' if sw else ""
    board = '<p class="board t-only"><a href="?view=student">Open this page in student view</a>, for the board.</p>' if sw else ""
    return (f'<section class="hero door-hero"><div class="wrap">'
            f'<p class="eyebrow t-only">One of seven doors</p>'
            f'<h1 class="t-only">{name}</h1>{student}'
            f'<p class="sum t-only" aria-label="Word sum: {html.escape(ws)} makes {word}s"><span>{html.escape(ws)}</span> &rarr; <i>{word}s</i></p>'
            f'<p class="lead t-only">{plain_words}</p>{extra}{board}'
            f'</div></section>')


def write(OUT, page, header, footer, X):
    """The seven door pages and the site map. X carries what they need from build_site: the route, the legend, the
    drawing tools and the helpers."""
    uc, md = X["uc"], X["md"]

    def door_page(slug, title, desc, inner):
        body = f"""{header(0)}
<main class="door-page" data-door="{slug}">
{inner}
</main>
{footer(0)}"""
        (OUT / f"{slug}.html").write_text(page(title, body, 0, desc), encoding="utf-8")

    # Progressions: the route, moved from the home page.
    door_page("progressions", "Progressions · Sound and Word Atlas", "The route through English spelling, step by step.", f"""{door_head("progressions")}
<section class="route" id="route" aria-labelledby="route-h"><div class="wrap">
<h2 id="route-h" class="t-only">The route at a glance</h2>
<p class="lead t-only">{X["route_lead"]} Open a step to see its words marked, the marks it brings in, and the pages in Carney's survey that back it.</p>
<p class="sub t-only">Each word is shown with its letters in colour: red for vowel letters, green for <em>sh</em>, <em>th</em> and <em>ch</em>, black for the rest.</p>
{X["bands_html"]}
{uc(X["draft_note"])}
</div></section>""")

    # Notations: the legend, moved from the home page.
    note_word = X["svg_of"]("notation", 58, label="notation, marked")
    door_page("notations", "Notations · Sound and Word Atlas", "The marks of Legomorphic Notation, each drawn alone on one word.", f"""{door_head("notations", f'<div class="door-word">{note_word}</div>')}
<section class="marks" id="marks" aria-labelledby="marks-h"><div class="wrap">
<h2 id="marks-h">Reading the marks</h2>
<p class="sub t-only">Twelve marks, each drawn alone on one word. A step page shows a word with all its marks at once, and <a href="definitions.html#marks">Definitions</a> says where each name comes from.</p>
<div class="key">{X["key_html"]}</div>
{uc("next, a page for each mark, with its rule, the contrasts that teach it, and an animation of the mark at work.")}
</div></section>""")

    # Explorations: the first family on the site, note to notation; hop and hope come next.
    LW, svg_of = X["LW"], X["svg_of"]
    fam = "".join(f'<figure class="word" id="{word_id(w)}">{svg_of(w, 58, label=f"{w}, marked")}<figcaption><span class="ws">{s}</span><span class="t-only">{c}</span></figcaption></figure>'
                  for w, s, c in X["morph"])
    door_page("explorations", "Explorations · Sound and Word Atlas", "Words to take apart and build: families and contrasts.", f"""{door_head("explorations")}
<section class="about" id="note-family" aria-labelledby="nf-h"><div class="wrap">
<h2 id="nf-h">A family: <i>note</i>, <i>notate</i>, <i>notation</i></h2>
<p class="sub t-only">Each word is built from the one before it. At each seam the <i>e</i> drops, and its job, making the <i>o</i> say its name, passes to the next vowel.</p>
<div class="words fam">{fam}</div>
</div></section>
<section class="about" aria-labelledby="next-h"><div class="wrap">
<h2 id="next-h" class="t-only">Coming next</h2>
{uc("next, the first contrast, <i>hop</i> and <i>hope</i>, built in full: their families marked, cards to print, a presentation for teachers and an exercise for students. Then more families and contrasts, and a page for every word.")}
<p class="t-only">For word sums now, the <a href="cards.html#word-sums">grade 3 word sum cards</a> take high-frequency words apart at their seams.</p>
<p class="s-only s-soon">More words to take apart are coming soon.</p>
</div></section>""")

    # Constructions: the Dialogue Team and the sentence cards.
    import characters, sessions
    team = characters.team(LW)
    hand = []
    for d in sessions.DECKS:
        for name, title, what in d.get("handouts", []):
            if any(k in name for k in ("operator", "modal", "sentence", "verb", "action", "actor")) and (OUT / "sessions" / "handouts" / f"{name}.pdf").exists():
                hand.append(f'<li><a href="sessions/handouts/{name}.pdf">{html.escape(title)}</a><span class="what">{what}</span></li>')
    hands = f'<ul class="handouts">{"".join(hand)}</ul>' if hand else ""
    door_page("constructions", "Constructions · Sound and Word Atlas", "How sentences are built, and the flip from claim to question.", f"""{door_head("constructions")}
<section class="about" id="flip" aria-labelledby="flip-h"><div class="wrap">
<h2 id="flip-h">From a claim to a question</h2>
<p class="sub t-only">An actor, an operator and an action make a claim. When the operator moves to the front, the claim becomes a question. The Dialogue Team acts it out with their faces: their words with the letters lifted out.</p>
{team}
</div></section>
<section class="about t-only" id="sentence-cards" aria-labelledby="sc-h"><div class="wrap">
<h2 id="sc-h">Cards for building sentences</h2>
<p class="sub">From the first session of the staff series, on <a href="presentations.html">Presentations</a>. Print them in colour on card stock.</p>
{hands}
{uc("next, each sentence pattern as a concept of its own, with cards, a presentation for teachers and an exercise for students.")}
</div></section>""")

    # Derivations: the plan for the roots, and what's here now.
    door_page("derivations", "Derivations · Sound and Word Atlas", "Where words come from, and the sources the roots will cite.", f"""{door_head("derivations")}
<section class="about t-only" aria-labelledby="dv-h"><div class="wrap prose">
<h2 id="dv-h">Roots, and the meanings of parts</h2>
<p>A word can be read as it is used now, or traced back through time: <a href="definitions.html#study">synchronic and diachronic</a>, a snapshot and a time-lapse. This door is for the time-lapse. <i>Before</i> is an example: Old English <i>beforan</i>, from <i>be-</i> &lsquo;by&rsquo; and <i>foran</i> &lsquo;in front&rsquo;, and <i>for</i> and <i>fore</i> grow from the same root.</p>
<p>The roots will follow Calvert Watkins&rsquo;s <i>American Heritage Dictionary of Indo-European Roots</i> (3rd ed., 2011), which is built root first and lists the English words from each root, with links to the <a href="https://lrc.la.utexas.edu/lex">Indo-European Lexicon</a> of the Linguistics Research Center at the University of Texas at Austin. Not every word has a known root. <i>Hop</i> and <i>hope</i> go back through Old English to early Germanic, and no further that anyone can show, and their pages will say so.</p>
{uc("next, a root page for every root behind the route's words, each citing its source, and a plain meaning for every part of a word.")}
</div></section>
<section class="about s-only"><div class="wrap"><p class="s-soon">Where words come from is coming soon.</p></div></section>""")

    # Instructions and Explanations: teachers' doors, leading to the pages that are already here.
    def tiles(items):
        return '<div class="door-tiles">' + "".join(
            f'<a class="dtile" href="{p}"><b>{t}</b><span>{s}</span></a>' for p, t, s in items) + "</div>"
    pick = lambda door: [(p, t, s) for p, d, t, s in PAGES if d == door and p != f"{door}.html"]
    door_page("instructions", "Instructions · Sound and Word Atlas", "How to teach it: presentations, word cards and word lists.", f"""{door_head("instructions")}
<section class="about"><div class="wrap">
{tiles(pick("instructions"))}
{uc("next, the routines: the learning loop, marking a word by hand, flips from claim to question, and word sums at the seam.")}
</div></section>""")
    door_page("explanations", "Explanations · Sound and Word Atlas", "Why it works: definitions, the notation and its name, and credits.", f"""{door_head("explanations")}
<section class="about"><div class="wrap">
{tiles(pick("explanations"))}
{uc("next, pages of ideas: the primary terms from phone to sememe, grapheme two ways, why English spells the way it does, and what the name claims.")}
</div></section>""")

    # The site map: the tree, written out.
    items = []
    for slug, name, _, plain_words, sw in DOORS:
        sub = [(p, t, s) for p, d, t, s in X["pages"] if d == slug and p != f"{slug}.html"]
        kids = ""
        if slug == "progressions":
            kids = "".join(f'<li><a href="steps/{s["n"]:02d}.html">Step {s["n"]}: {md(s["title"])}</a></li>' for s in X["STEPS"])
        else:
            kids = "".join(f'<li><a href="{p}">{t}</a> <span>{html.escape(s)}</span></li>' for p, t, s in sub)
        who = '<span class="who">for teachers</span>' if sw is None else ""
        items.append(f'<li{" class=t-only" if sw is None else ""}><a href="{slug}.html"><b>{name}</b></a> {who}<span>{plain_words}</span>'
                     + (f'<ol class="kids">{kids}</ol>' if slug == "progressions" else f'<ul class="kids">{kids}</ul>' if kids else "") + "</li>")
    door_page("sitemap", "Site map · Sound and Word Atlas", "Every page of the Sound and Word Atlas, door by door.", f"""<section class="hero"><div class="wrap">
<h1>Site map</h1>
<p class="lead">Every page, door by door. The doors are named as one family: each turns a doing into a thing with <i>-ion</i>.</p>
</div></section>
<section class="about"><div class="wrap"><ul class="smap-tree"><li><a href="index.html"><b>Home</b></a></li>{"".join(items)}</ul></div></section>""")


def doors_section():
    """The way in on the home page: a tile for each door, with its short word in student view."""
    out = []
    for slug, name, ws, plain_words, sw in DOORS:
        out.append(f'<a class="door-tile{" t-only" if sw is None else ""}" href="{slug}.html"><span class="dn">{name}</span>'
                   f'{f"<span class=sn>{sw}</span>" if sw else ""}<span class="pw t-only">{plain_words}</span></a>')
    return f"""<section class="doors-home" id="doors-home" aria-labelledby="doors-h"><div class="wrap">
<h2 id="doors-h"><span class="t-only">Seven doors in</span><span class="s-only">Pick a door</span></h2>
<p class="sub t-only">Each door is a ramp: its first page asks the least, and each step in asks a little more. The names are one word family, so the way in teaches the ending they share: <i>progress + ion</i>, <i>not(e) + at(e) + ion</i>, <i>construct + ion</i>.</p>
<div class="door-grid">{"".join(out)}</div>
</div></section>"""


# ------------------------------------------------------------------ search
def write_search(OUT, X):
    recs, seen = [], set()
    def add(t, l, u, s="", k="", teacher=False):
        key = (t, l.lower(), u)
        if key in seen: return
        seen.add(key)
        r = {"t": t, "l": l, "u": u}
        if s: r["s"] = s
        if k: r["k"] = k
        if teacher: r["x"] = 1
        recs.append(r)
    strip = lambda s: re.sub(r"<[^>]+>", "", html.unescape(s))
    # words on the route, at the first step that has them
    where = {}
    for st in X["STEPS"]:
        for g in X["groups_of"](st["words_md"]):
            for w in g: where.setdefault(w, []).append(st["n"])
    for w, ns in sorted(where.items()):
        add("word", w, f"steps/{ns[0]:02d}.html#{word_id(w)}", "Step " + ", ".join(str(n) for n in ns[:3]) + ("…" if len(ns) > 3 else ""))
    # Words on the lists but not the route land on their place in the word lists' table, which holds every ELP word and
    # Dolch's 220, or, for Dolch's nouns, on their page of the actor cards: six cards a page after the list page, the
    # pronouns first (build_role_cards.py)
    elp_of, dolch_of = {}, {w: "Dolch " + l["name"].lower() for l in X["dolch"]["levels"] for w in l["words"]}
    for n, L in X["elp"]["lists"].items():
        for w in L["words"]: elp_of.setdefault(w, f"ELP list {n}")
    actors = "I me you he him she her we us they them it".split() + X["dolch"]["nouns"]
    from pypdf import PdfReader
    cards = OUT / "sessions" / "handouts" / "actor-cards.pdf"
    assert len(PdfReader(str(cards)).pages) == 1 + -(-len(actors) // 6), "the actor cards' pages have changed"
    for w in sorted(X["list_words"]):
        if w in where: continue
        if w in elp_of or w in dolch_of:
            add("word", w, f"word-lists.html#{word_id(w)}", ", ".join(x for x in (elp_of.get(w), dolch_of.get(w)) if x), teacher=True)
        else:
            add("word", w, f"sessions/handouts/actor-cards.pdf#page={2 + actors.index(w) // 6}", "Dolch noun, actor cards", teacher=True)
    for w, *_ in X["morph"]:   # the family on Explorations
        if w not in where: add("word", w, f"explorations.html#{word_id(w)}", "Explorations")
    for st in X["STEPS"]:
        words = " ".join(w for g in X["groups_of"](st["words_md"]) for w in g)
        add("step", f"Step {st['n']}: {X['plain'](st['title'])}", f"steps/{st['n']:02d}.html", st["band"],
            k=words + " " + X["plain"](st.get("marks", "")) + " " + X["plain"](st.get("contrast_md", "") or ""))
    for name, what, w, m in X["KEY"]:
        add("mark", name, "notations.html#" + mark_id(name), f"drawn on {w}", k=strip(what))
    for term, anchor in X["terms"]:
        add("term", term, "definitions.html#" + anchor, "Definitions", teacher=True)
    for p, d, t, s in X["pages"]:
        if p.startswith("steps/"): continue
        add("page", t, p, "Door" if p == f"{d}.html" else DOOR[d][1] if d else "", k=s, teacher=d in TEACHERS)
    (OUT / "search.json").write_text(json.dumps(recs, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return len(recs)


def mark_id(name): return "mark-" + re.sub(r"[^a-z]+", "-", name.lower()).strip("-")


def word_id(w):
    """The id a word's figure or entry carries, so a search lands on the word itself: w-dont for don't, w-i for I."""
    return "w-" + re.sub(r"[^a-z0-9]+", "-", w.lower().replace("’", "").replace("'", "")).strip("-")


# ------------------------------------------------------------------ breadcrumbs, the current door, and teachers' pages
def door_label(d):
    """A door's name, with its short word beside it for student view (a teachers' door has none)."""
    _, name, _, _, sw = DOOR[d]
    return f'<span class="dn">{name}</span><span class="sn">{sw}</span>' if sw else name


def finish(OUT, pages):
    """Every page built: put its breadcrumb where header() left <!--crumbs-->, mark its door as the current one, and
    tell a student who lands on a teachers' page that it's for teachers."""
    done = 0
    for p, d, t, s in pages:
        f = OUT / p
        if not f.exists(): continue
        src = f.read_text(encoding="utf-8")
        if "<!--crumbs-->" not in src: continue
        up = "../" * p.count("/")
        trail = []
        if p != "index.html":
            trail.append(f'<li><a href="{up}index.html">Home</a></li>')
            if d and p != f"{d}.html":
                trail.append(f'<li><a href="{up}{d}.html">{door_label(d)}</a></li>')
            here = door_label(d) if d and p == f"{d}.html" else html.escape(t.split(":")[0] if p.startswith("steps/") else t)
            trail.append(f'<li aria-current="page">{here}</li>')
        crumbs = f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{"".join(trail)}</ol></div></nav>' if trail else ""
        if d in TEACHERS:
            crumbs += (f'<div class="for-teachers s-only"><div class="wrap"><p>This page is for teachers. To read it, pick Teacher at the top '
                       f'of the page, or go <a href="{up}index.html">back to the doors</a>.</p></div></div>')
        src = src.replace("<!--crumbs-->", crumbs, 1)
        if d:
            src = src.replace(f'data-door="{d}">', f'data-door="{d}" aria-current="{"page" if p == f"{d}.html" else "true"}">', 1)
        f.write_text(src, encoding="utf-8")
        done += 1
    return done
