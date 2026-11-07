"""The landing section at the top of the home page: legomorphic marked in full, built up the way the decks build a
word (sounds first, then letters, then marks), and note to notate to notation, with the e dropping at each seam and
its job moving on. Made on 6 November 2026.

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
    ("8", "A vault: a vowel after a single consonant reaches back and makes the <i>o</i> long."),
    ("9", "Seams where the parts join: <i>lego + morph + ic</i>."),
]
STEP = 1.6          # seconds between steps
START = 0.4

MORPH = [   # (word, word sum, caption)
    ("note", "<i>note</i>", "The silent <i>e</i> sends a vault back, so the <i>o</i> says its name."),
    ("notate", "<i>not(e) + ate</i> &rarr; <i>notate</i>",
     "The <i>e</i> drops at the seam, and the <i>a</i> of <i>ate</i> takes over its job."),
    ("notation", "<i>notat(e) + ion</i> &rarr; <i>notation</i>",
     "The <i>e</i> drops again. The <i>i</i> of <i>ion</i> takes over the vault, and says <i>sh</i> with the <i>t</i>, "
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


def html_block(LW):
    lego, _ = svg(LW, "legomorphic", 80, label="legomorphic, marked in full: lego + morph + ic")
    widths = [LW.svg_word(w, 80, 0.0, cls=False)[1] for w, _, _ in MORPH]
    W = max(widths)
    words = "".join(svg(LW, w, 80, width=W, label=f"{w}, marked", klass=f"w{i + 1}")[0] for i, (w, _, _) in enumerate(MORPH))
    sums = "".join(f'<span class="s{i + 1}">{s}</span>' for i, (_, s, _) in enumerate(MORPH))
    caps = "".join(f'<span class="c{i + 1}">{c}</span>' for i, (_, _, c) in enumerate(MORPH))
    lego_caps = "".join(f"<span>{c}</span>" for _, c in LEGO_STEPS)
    return f"""<style>{css()}</style>
<script>if (!matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) document.documentElement.classList.add('js');</script>
<section class="landing" aria-labelledby="landing-h"><div class="wrap">
<p class="eyebrow">Sound and Word Atlas · For teachers</p>
<div class="stage stage-lego" id="lego">{lego}<p class="cap">{lego_caps}</p></div>
<h1 id="landing-h">Legomorphic Notation</h1>
<p class="lead">A set of marks and colours drawn on ordinary spelling, so that what a reader usually works out alone is there for everyone to see.</p>
<p class="cta"><a class="btn" href="#route">Follow the route</a><a class="btn ghost" href="about.html">About the notation</a><button class="replay" type="button" data-replay="lego">Play again</button></p>
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
<script>(() => {{
  if (!document.documentElement.classList.contains('js')) return;
  const t0 = performance.now(), lego = {int(1000 * (START + STEP * len(LEGO_STEPS)))};   // the morph waits for the name to finish
  const io = new IntersectionObserver(es => es.forEach(e => {{ if (!e.isIntersecting) return; io.unobserve(e.target);
    const wait = e.target.id === 'morph' ? Math.max(0, t0 + lego - performance.now()) : 0;
    setTimeout(() => e.target.classList.add('play'), wait); }}), {{threshold: 0.35}});
  document.querySelectorAll('.stage').forEach(s => io.observe(s));
  document.querySelectorAll('[data-replay]').forEach(b => b.addEventListener('click', () => {{
    const s = document.getElementById(b.dataset.replay); s.classList.remove('play'); void s.getBoundingClientRect(); s.classList.add('play'); }}));
}})();</script>"""
