"""The Presentations page, and the decks behind it.

build_site.py calls write(), which copies each deck in build/sessions/ to docs/sessions/ and writes
docs/presentations.html. The decks here are the web copies: the title slide's byline is left off, since the site
names no one, and a small link in the slide controls leads back to the Presentations page. Everything else is the
deck as it was presented.

Run as a script, it makes the two things the page offers besides the deck itself. It needs a node_modules folder
holding @fontsource-variable/fraunces, @fontsource-variable/lexend and @fontsource/gentium-plus:

    python3 build/sessions.py <node_modules> docs

- an offline copy of each deck with its fonts built in (make_offline_deck.py), for presenting with no network;
  its link back points at the live site
- preview pictures of a few slides, taken from the offline copy so they show the deck's own fonts
"""
import html, pathlib, re, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
SITE = "https://dantewetherow.github.io/sound-and-word-atlas/"
DECKS = [{
    "file": "sounds-symbols-and-sentences",
    "title": "Sounds, Symbols and Sentences",
    "kicker": "Session 1",
    "previews": [1, 5, 6, 14],
    "about": ("This is not a program. It&rsquo;s an exploration of ways to provide access, and an invitation to experiment "
              "with our methods and synthesize our understandings. The first session starts with how many sounds a voice can "
              "make and how we write them down, works through sound circles and one letter, one beat, and ends with a "
              "learning loop to run with one student this week."),
    # The handouts given out with it, built by build_handouts.py into docs/sessions/handouts/: (file, title, what it is)
    "handouts": [
        ("sounds-and-marks-key", "The 44 sounds and marking a word",
         "Two sides: the 44 sounds of English, each with a key word marked, and how to mark a word by hand."),
        ("operator-cards", "Operator cards",
         "Fold-over tent cards for the nine modals (can, could, will, would, shall, should, may, might and must), "
         "marked on one face and blank on the other, plus three blank cards."),
        ("operator-cards-instructions", "Using the operator cards",
         "Making the cards, running a loop, and marking a word by hand."),
        ("sentence-cards", "Sentence cards",
         "A demonstration set of 48 tent cards about reading and writing. Stand up an actor, an operator and an action, "
         "then move the operator to the front to turn the statement into a question."),
    ],
}]


def kb(n):
    return f"{n / 1e6:.1f} MB" if n >= 1e6 else f"{round(n / 1024)} KB"


def slide_labels(deck_html):
    return re.findall(r'<section class="slide[^"]*"[^>]*aria-label="([^"]*)"', deck_html)


def write(OUT, page, header, footer):
    (OUT / "sessions").mkdir(parents=True, exist_ok=True)
    blocks = []
    for d in DECKS:
        f = d["file"]
        src = (HERE / "sessions" / f"{f}.html").read_text(encoding="utf-8")
        (OUT / "sessions" / f"{f}.html").write_text(src, encoding="utf-8")
        labels = slide_labels(src)
        shots = "".join(
            f'<img src="sessions/{f}-{n}.jpg" alt="Slide {n}: {html.escape(labels[n - 1])}" width="960" height="540" loading="lazy">'
            for n in d["previews"] if (OUT / "sessions" / f"{f}-{n}.jpg").exists())
        offline = OUT / "sessions" / f"{f}-offline.html"
        get = (f'<span><a href="sessions/{f}-offline.html" download="{html.escape(d["title"])}.html">Download it to present offline</a> '
               f'({kb(offline.stat().st_size)})</span>') if offline.exists() else ""
        from pypdf import PdfReader
        items = []
        for name, title, what in d.get("handouts", []):
            pdf = OUT / "sessions" / "handouts" / f"{name}.pdf"
            if not pdf.exists(): continue
            n = len(PdfReader(str(pdf)).pages)
            items.append(f'<li><a href="sessions/handouts/{name}.pdf">{html.escape(title)}</a>'
                         f'<span class="meta">PDF, {n} page{"s" if n != 1 else ""}, {kb(pdf.stat().st_size)}</span>'
                         f'<span class="what">{what}</span></li>')
        hands = (f'<h3 class="hand-h">Handouts</h3><ul class="handouts">{"".join(items)}</ul>'
                 '<p class="sub">Print them in colour. The card pages are made for card stock, and the instructions show how to fold them.</p>') if items else ""
        blocks.append(f"""<article class="deck" id="{f}">
<a class="deck-shots" href="sessions/{f}.html" aria-label="Open {html.escape(d['title'])}">{shots}</a>
<div class="deck-text">
<p class="eyebrow">{d['kicker']} &middot; {len(labels)} slides</p>
<h2>{html.escape(d['title'])}</h2>
<p>{d['about']}</p>
<p class="deck-links"><a class="btn" href="sessions/{f}.html">Open the presentation</a>{get}</p>
<p class="sub">To move on, click or tap the right side of a slide, or press the right arrow or the space bar. The left third of a slide, or the left arrow, goes back. Many slides build a step at a time, and the &#10530; button, which shows when you move the mouse, fills the screen.</p>
</div>
<div class="deck-hands">{hands}</div>
</article>""")
    body = f"""{header(0)}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">Presentations</p>
<h1>Sessions for teachers</h1>
<p class="lead">Slide decks from a staff series on legomorphic notation. They build a click at a time, the way the marks are taught, so they work for presenting to colleagues and for going through on your own.</p>
</div></section>
<section class="about" aria-label="Decks"><div class="wrap"><div class="decks">
{"".join(blocks)}
</div></div></section>
</main>
{footer(0)}"""
    (OUT / "presentations.html").write_text(
        page("Presentations · Sound and Word Atlas", body, 0, "Slide decks from a staff series on legomorphic notation, to present or go through on your own."),
        encoding="utf-8")
    print(f"wrote presentations.html | {len(DECKS)} deck(s)")


def make_files(fonts, OUT):
    from playwright.sync_api import sync_playwright
    (OUT / "sessions").mkdir(parents=True, exist_ok=True)
    for d in DECKS:
        f = d["file"]
        offline = OUT / "sessions" / f"{f}-offline.html"
        subprocess.run([sys.executable, str(HERE / "make_offline_deck.py"), str(HERE / "sessions" / f"{f}.html"), str(fonts), str(offline)], check=True)
        s = offline.read_text(encoding="utf-8")
        assert s.count('href="../presentations.html"') == 1
        offline.write_text(s.replace('href="../presentations.html"', f'href="{SITE}presentations.html"'), encoding="utf-8")
        with sync_playwright() as p:
            b = p.chromium.launch()
            for n in d["previews"]:
                pg = b.new_page(viewport={"width": 960, "height": 540}, reduced_motion="reduce", color_scheme="light")
                pg.goto(offline.as_uri() + f"#{n}")
                pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(400)
                steps = pg.evaluate(f"(() => {{ const s = document.querySelectorAll('.slide')[{n - 1}]; return parseInt(s.getAttribute('data-max') || '0', 10); }})()")
                slow = pg.evaluate(f"!!document.querySelectorAll('.slide')[{n - 1}].querySelector('.wave-draw,.ab-pen')")
                for _ in range(steps):
                    pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(250)
                pg.wait_for_timeout(8000 if slow else 3300)   # let any drawing finish, and the controls fade (a key wakes them for 2.6 s)
                assert pg.evaluate(f"document.querySelectorAll('.slide')[{n - 1}].classList.contains('on')"), n
                pg.screenshot(path=str(OUT / "sessions" / f"{f}-{n}.jpg"), type="jpeg", quality=84)
                pg.close()
                print(f"preview {f}-{n}.jpg ({steps} steps)")
            b.close()


if __name__ == "__main__":
    make_files(pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve())
