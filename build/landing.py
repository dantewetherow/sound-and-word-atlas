"""The landing section at the top of the home page: the name, the subtitle and the three layers, then note to notate to
notation, with the e dropping at each seam and its job moving on. Made on 6 November 2026; on 12 November 2026
legomorphic, built up the way the decks build a word (sounds first, then letters, then marks), moved to the *leg-
page (lego_block).

The words are drawn with legomorphic_words.py, with its layer classes (nz1 to nz9, and the wt band that stands in for
the letters while only the sounds show), and site.css times the layers. Without script, or with reduced motion, the
page shows the finished words and no animation. The codes for legomorphic, note, notate and notation are in
site_codes.py, with the calls they rest on."""
import html

LEGO_STEPS = [   # (layers it brings in, caption)
    ("1", "Sounds first: a circle for each sound."),
    ("2", "Red for the vowel sounds."),
    ("3", "A swoop for each syllable: <i>leg, o, mor, phic</i>."),
    ("4", "Bars where letters spell a single sound: <i>or</i> and <i>ph</i>."),
    ("5", "Then the letters."),
    ("6", "A cup over a short vowel, a bar over a long one."),
    ("9", "Seams where the parts join: <i>leg + o + morph + ic</i>. The <i>o</i> is a part of its own, meaning &ldquo;I,&rdquo; so it spells its name, as in <i>go</i>."),
]
STEP = 1.6          # seconds between steps
START = 0.4

MORPH = [   # (word, word sum, caption)
    ("note", "<i>note</i>", "The silent <i>e</i> sends a vault back, so the <i>o</i> spells its name."),
    ("notate", "<i>not(e) + ate</i> &rarr; <i>notate</i>",
     "The <i>e</i> drops at the seam, and the <i>a</i> of <i>ate</i> takes over its job."),
    ("notation", "<i>notat(e) + ion</i> &rarr; <i>notation</i>",
     "The <i>e</i> drops again. The <i>i</i> of <i>ion</i> takes over the vault, and spells <i>sh</i> with the <i>t</i>, "
     "right across the seam."),
]


def svg(LW, word, F, width=None, label=None, klass=""):
    g, w, H = LW.svg_word(word, F, 0.0, cls=True)
    for layer in ("3", "8"):         # swoops and vaults are drawn, not faded in
        g = g.replace(f'<path class="nz{layer}"', f'<path pathLength="1" class="nz{layer} dr"')
    W = width or w
    return (f'<svg class="{klass}" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="{html.escape(label or word)}">'
            f'{g}</svg>'), w


def css():
    """The timing: each of legomorphic's steps brings in its layers, and the morph stage runs as three scenes."""
    t = lambda i: START + STEP * i
    out = []
    for i, (layers, _) in enumerate(LEGO_STEPS):
        out.append(f".stage-lego.play .nz{layers}{{animation:lm-in .7s ease {t(i):.1f}s both}}")
        out.append(f".stage-lego.play .nz{layers}.dr{{animation:lm-draw 1s ease {t(i):.1f}s both}}")
        last = i == len(LEGO_STEPS) - 1
        out.append(f".stage-lego.play .cap > span:nth-child({i + 1}){{animation:lm-in .5s ease {t(i):.1f}s both"
                   + ("" if last else f",lm-out .4s ease {t(i + 1) - 0.35:.2f}s forwards") + "}")
    five = [i for i, (l, _) in enumerate(LEGO_STEPS) if l == "5"][0]
    out.append(f".stage-lego.play .wt{{animation:lm-in .6s ease {t(0):.1f}s both,lm-out .6s ease {t(five):.1f}s forwards}}")
    return "\n".join(out)


def _play_js(after_lego):
    """Each stage plays once it's in view; the morph waits for legomorphic to finish when both are on the page."""
    wait = int(1000 * (START + STEP * len(LEGO_STEPS))) if after_lego else 0
    return f"""<script>(() => {{
  if (!document.documentElement.classList.contains('js')) return;
  const t0 = performance.now(), lego = {wait};
  const io = new IntersectionObserver(es => es.forEach(e => {{ if (!e.isIntersecting) return; io.unobserve(e.target);
    const wait = e.target.id === 'morph' ? Math.max(0, t0 + lego - performance.now()) : 0;
    setTimeout(() => e.target.classList.add('play'), wait); }}), {{threshold: 0.35}});
  document.querySelectorAll('.stage').forEach(s => io.observe(s));
  document.querySelectorAll('[data-replay]').forEach(b => b.addEventListener('click', () => {{
    const s = document.getElementById(b.dataset.replay); s.classList.remove('play'); void s.getBoundingClientRect(); s.classList.add('play'); }}));
}})();</script>"""


JS_ON = "<script>if (!matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) document.documentElement.classList.add('js');</script>"


def hero_only(doors_html):
    """The home page as a clean place to land (22 November 2026, a trial): the name, one line, and the buttons."""
    return f"""<style>{css()}</style>
<section class="landing solo" aria-labelledby="landing-h"><div class="wrap">
<h1 id="landing-h">Sounds and Words, Assembled</h1>
<p class="sublead">Orthography, morphology, phonology and etymology, brought to light.</p>
<p class="motto">I thought it through and though it was tough I was thorough.</p>
<p class="motto-ipa" lang="en-fonipa" title="IPA, North American">/a&#618; &#712;&#952;&#593;t &#618;t &#712;&#952;&#633;u &#601;n &#712;&eth;o&#650; &#618;t w&#601;z &#712;t&#652;f a&#618; w&#601;z &#712;&#952;&#605;o&#650;/</p>
{doors_html}
</div></section>"""


def morph_block(LW):
    """note to notate to notation, played once when it scrolls into view. On the About page since 22 November 2026,
    when the home page became buttons only."""
    widths = [LW.svg_word(w, 80, 0.0, cls=False)[1] for w, _, _ in MORPH]
    W = max(widths)
    words = "".join(svg(LW, w, 80, width=W, label=f"{w}, marked", klass=f"w{i + 1}")[0] for i, (w, _, _) in enumerate(MORPH))
    sums = "".join(f'<span class="s{i + 1}">{s}</span>' for i, (_, s, _) in enumerate(MORPH))
    caps = "".join(f'<span class="c{i + 1}">{c}</span>' for i, (_, _, c) in enumerate(MORPH))
    return f"""<style>{css()}</style>
{JS_ON}
<section class="morph" aria-labelledby="morph-h"><div class="wrap">
<h2 id="morph-h">See it work: from <i>note</i> to <i>notation</i></h2>
<div class="stage stage-morph" id="morph">
<p class="sums">{sums}</p>
<div class="mstack">{words}</div>
<p class="cap">{caps}</p>
</div>
<p><button class="replay" type="button" data-replay="morph">Play again</button></p>
</div></section>
{_play_js(False)}"""


def html_block(LW, doors_html=""):
    """The home page's top: the name, the subtitle, the three layers as buttons, then note to notate to notation.
    Since 12 November 2026; legomorphic, built up, is on the *leg- page (lego_block)."""
    widths = [LW.svg_word(w, 80, 0.0, cls=False)[1] for w, _, _ in MORPH]
    W = max(widths)
    words = "".join(svg(LW, w, 80, width=W, label=f"{w}, marked", klass=f"w{i + 1}")[0] for i, (w, _, _) in enumerate(MORPH))
    sums = "".join(f'<span class="s{i + 1}">{s}</span>' for i, (_, s, _) in enumerate(MORPH))
    caps = "".join(f'<span class="c{i + 1}">{c}</span>' for i, (_, _, c) in enumerate(MORPH))
    return f"""<style>{css()}</style>
{JS_ON}
<section class="landing" aria-labelledby="landing-h"><div class="wrap">
<h1 id="landing-h">Sounds and Words, Assembled</h1>
<p class="sublead">Orthography, morphology, phonology and etymology, brought to light.</p>
<p class="lead t-only">Legomorphic Notation is a set of marks and colours drawn on ordinary spelling, so that what a reader usually works out alone is there for everyone to see.</p>
{doors_html}
<p class="ctasub t-only"><a href="about.html">About the notation</a> · <a href="notations.html">The marks</a></p>
</div></section>
<section class="morph" aria-labelledby="morph-h"><div class="wrap">
<h2 id="morph-h">See it work: from <i>note</i> to <i>notation</i></h2>
<div class="stage stage-morph" id="morph">
<p class="sums">{sums}</p>
<div class="mstack">{words}</div>
<p class="cap">{caps}</p>
</div>
<p><button class="replay" type="button" data-replay="morph">Play again</button></p>
</div></section>
{_play_js(False)}"""


def lego_block(LW):
    """Legomorphic built up the way the decks build a word, for the *leg- page (on the home page until 12 November 2026)."""
    lego, _ = svg(LW, "legomorphic", 80, label="legomorphic, marked in full: leg + o + morph + ic")
    lego_caps = "".join(f"<span>{c}</span>" for _, c in LEGO_STEPS)
    return f"""<style>{css()}</style>
{JS_ON}
<div class="stage stage-lego" id="lego">{lego}<p class="cap">{lego_caps}</p></div>
<p><button class="replay" type="button" data-replay="lego">Play again</button></p>
{_play_js(False)}"""


# ------------------------------------------------------------------ the welcome page (27 November 2026)
# Dante: the landing page as a welcome. Legomorphics assembles: its parts arrive from four sides (leg from the left, o from
# above, morph from below, ics from the right), then the notation's marks come in a layer at a time, the seams last.
# Under it, what the site is, a Welcome button to the tools, and Where does the word come from? The tiles moved to
# tools.html.
WELCOME_TEXT = ("Legomorphics is a set of tools for teaching how English words work: their sounds, their letters and the "
                "parts they are built from. It is made for a teacher and a class to use together, on the board. It "
                "isn&rsquo;t a program that moves a learner through on their own: choose the page that fits the lesson.")
# 27 November 2026, Dante: not levelled by grade. Any learner may want or need any part of it.
WELCOME_ALL = ("It isn&rsquo;t levelled by grade or age. It is for all learners, and any learner may want or need some "
               "part of it to see how English spelling works.")
# where each letter comes from (dx, dy in the drawing's units), by part: l e g | o | m o r p h | i c s
FROM = [(-420, -60), (-380, 40), (-340, -20), (0, -260), (-60, 300), (-20, 340), (20, 300), (60, 340), (100, 300),
        (420, -40), (380, 50), (440, 10)]
LAYERS = [1, 2, 3, 4, 6, 7, 8, 9]   # the marks, in the order they come in (circles first, seams last)


def welcome(LW, code):
    """The welcome page's body: the assembling word, the name, what the site is, and the two buttons."""
    import re
    had = "legomorphics" in LW.W
    LW.W["legomorphics"] = code
    try: g, w, H = LW.svg_word("legomorphics", 100.0, 0.0, cls=True)
    finally:
        if not had: LW.W.pop("legomorphics", None)
    g = re.sub(r'<rect class="wt"[^>]*/>', "", g)
    k = iter(range(len(FROM)))
    g = re.sub(r"<text ", lambda m: f'<text class="wl-l" style="--i:{(n := next(k))};--dx:{FROM[n][0]}px;--dy:{FROM[n][1]}px" ', g)
    rules = "".join(f".wl-svg.play .nz{n}{{animation:wl-mark .6s ease {1.9 + 0.35 * i:.2f}s both}}" for i, n in enumerate(LAYERS))
    return f"""<style>
.welcome {{ min-height: calc(100vh - 140px); display: grid; align-content: center; justify-items: center; text-align: center; padding: 4vh 16px 6vh; gap: 2.2vh; }}
.wl-svg {{ width: min(980px, 92vw); height: auto; overflow: visible; }}
.wl-svg .wl-l {{ transform-box: fill-box; transform-origin: center; }}
.wl-svg.play .wl-l {{ animation: wl-in 1.1s cubic-bezier(.2,.8,.25,1) calc(.15s + var(--i) * .07s) both; }}
@keyframes wl-in {{ from {{ opacity: 0; transform: translate(var(--dx), var(--dy)) rotate(-18deg) scale(.6); }} to {{ opacity: 1; transform: none; }} }}
@keyframes wl-mark {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
{rules}
.wl-svg.play [class^="nz"]:not(.nz5) {{ opacity: 0; }}
.welcome h1 {{ font-family: var(--display, serif); font-weight: 500; font-size: clamp(1.4rem, 3.2vw, 2.2rem); margin: 0; color: var(--ink); }}
.welcome h1 small {{ display: block; font-size: .5em; letter-spacing: .12em; text-transform: uppercase; color: var(--soft); margin-bottom: .4em; }}
.wl-lead {{ max-width: 44em; font-size: clamp(1rem, 1.9vw, 1.2rem); line-height: 1.55; color: var(--ink); margin: 0; }}
.wl-btns {{ display: flex; flex-wrap: wrap; gap: 14px; justify-content: center; align-items: center; margin-top: 1vh; }}
.wl-go {{ font-size: clamp(1.3rem, 2.6vw, 1.8rem); font-weight: 600; padding: 18px 48px; border-radius: 999px; background: var(--verb); color: var(--paper); text-decoration: none; }}
.wl-go:hover, .wl-go:focus-visible {{ filter: brightness(1.08); }}
.wl-why {{ font-size: clamp(1rem, 1.8vw, 1.15rem); padding: 18px 28px; border-radius: 999px; border: 1.5px solid var(--line); color: var(--ink); text-decoration: none; background: var(--card); }}
.welcome .motto {{ margin: 2vh 0 0; }}
@media (prefers-reduced-motion: reduce) {{ .wl-svg.play .wl-l, .wl-svg.play [class^="nz"] {{ animation: none !important; opacity: 1 !important; }} }}
</style>
<section class="welcome" aria-labelledby="wl-h">
<svg class="wl-svg play" viewBox="-20 0 {w + 40:.0f} {H:.0f}" role="img" aria-label="Legomorphics, its parts arriving and the notation's marks drawn on it">{g}</svg>
<h1 id="wl-h"><small>Legomorphics</small>Sounds and Words, Assembled</h1>
<p class="wl-lead">{WELCOME_TEXT}</p>
<p class="wl-lead wl-all">{WELCOME_ALL}</p>
<div class="wl-btns"><a class="wl-go" href="tools.html">Welcome</a><a class="wl-why" href="system.html">How it fits together</a><a class="wl-why" href="about.html#word-h">Where does the word come from?</a></div>
<p class="motto">I thought it through and though it was tough I was thorough.</p>
<p class="motto-ipa" lang="en-fonipa" title="IPA, North American">/a&#618; &#712;&#952;&#593;t &#618;t &#712;&#952;&#633;u &#601;n &#712;&eth;o&#650; &#618;t w&#601;z &#712;t&#652;f a&#618; w&#601;z &#712;&#952;&#605;o&#650;/</p>
</section>"""


def tools_body(doors_html):
    """tools.html: the buttons that were the home page, in their bands."""
    return f"""<style>{css()}</style>
<section class="landing solo" aria-labelledby="tools-h"><div class="wrap">
<h1 id="tools-h">The tools</h1>
<p class="sublead">Everything on the site, from single letters to word families. Pick the one that fits the lesson.</p>
<p class="sub">None of it is levelled by grade. Any learner, at any age, may need any part of it.</p>
{doors_html}
</div></section>"""
