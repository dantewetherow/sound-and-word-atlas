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


def html_block(LW):
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
<p class="eyebrow t-only">Legomorphic Notation</p>
<h1 id="landing-h">A Legend for English Words</h1>
<p class="sublead">Orthography, morphology, phonology and etymology, brought to light.</p>
<p class="lead t-only">Legomorphic Notation is a set of marks and colours drawn on ordinary spelling, so that what a reader usually works out alone is there for everyone to see.</p>
<p class="cta three"><a class="btn" href="progressions.html">Steps</a><a class="btn" href="walk.html">Words</a><a class="btn" href="parts.html">Parts</a></p>
<p class="ctasub t-only">Learn the notation in order, look up a word, or see what words share. <a href="about.html">About the notation</a>.</p>
</div></section>
<section class="morph" aria-labelledby="morph-h"><div class="wrap">
<h2 id="morph-h">From <i>note</i> to <i>notation</i></h2>
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
