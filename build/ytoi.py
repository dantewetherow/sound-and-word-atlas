"""Y to i at the seam: a presentation for teachers, made on 8 November 2026 in the manner of the Session 1 deck.

It rests on Dante Wetherow's reading of the rule: the y becomes i where, as y, it would be read wrong in its new place
(funnyer would read funn-yer; happyness and merryment invite misreads too, and i lets the long-e sound shorten), and it
stays where i would be read wrong (slyly, since slily would read as slilly) or where it is part of a team (played). The
usual rule is kept as what it is, a mnemonic, and "English words don't end in i" as a reason without a premise.

Words with codes on the site (happy, happier, happily, carry, carries, try, tried, play, played, pretty) are drawn in the
notation; the rest are set in type. It sits on step 29 of the route, and its sources are Carney's pages for that step.

Run:  python3 build/ytoi.py        writes build/sessions/y-to-i.html, which sessions.py copies to the site
"""
import html, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import legomorphic_words as LW
from known_codes import all_codes
from site_codes import SITE_CODES
from dolch_codes import DOLCH_CODES

codes, _ = all_codes()
for w, c in {**SITE_CODES, **DOLCH_CODES}.items(): codes.setdefault(w, c)
LW.W.clear(); LW.W.update(codes)

LAYER_STEP = {"5": 1, "4": 1, "1": 2, "2": 2, "6": 3, "3": 4, "7": 5, "8": 5, "9": 6}   # the notation slide's build


def word(w, h, steps=None, label=None):
    """A marked word as an svg, h pixels tall. With steps, its layers come in on the slide's clicks (LAYER_STEP)."""
    g, wd, H = LW.svg_word(w, 100.0, 0.0, cls=steps is not None)
    if steps is not None:
        g = re.sub(r'<rect class="wt"[^>]*/>', "", g)
        for layer in ("3", "8"):
            g = g.replace(f'<path class="nz{layer}"', f'<path pathLength="1" class="nz{layer} dr"')
        g = re.sub(r'class="(nz(\d)[^"]*)"', lambda m: f'class="{m.group(1)}" data-s="{steps + LAYER_STEP[m.group(2)] - 1}"', g)
    return (f'<svg class="mw" viewBox="0 0 {wd:.0f} {H:.0f}" style="height:{h}px" role="img" '
            f'aria-label="{html.escape(label or w + ", marked")}">{g}</svg>')


def i(s): return f"<i>{s}</i>"


SLIDES = []
def slide(label, body, cls="", steps=0):
    SLIDES.append(f'<section class="slide {cls}" aria-label="{html.escape(label)}"' + (f' data-max="{steps}"' if steps else "") + f">\n{body}\n</section>")


# 1 title
slide("Title", f"""<div class="title">
<p class="kicker">Legomorphic Notation &middot; for teachers</p>
<h1 class="display">Y to <span class="r">i</span> at the seam</h1>
<p class="subtitle">How a spelling would read decides the letter</p>
<div class="pair">{word("happy", 150)}<span class="op">+ er &rarr;</span>{word("happier", 150)}</div>
</div>""", "mid")

# 2 where it sits
slide("Where it sits", f"""<h2 class="head">Step 29 of the route: <i>-y</i>, <i>-ly</i> and y turns to i</h2>
<p class="body">The words: {", ".join(i(w) for w in ("sadly", "slowly", "happily", "happier", "tried", "carries"))}. The contrast: {i("try")} and {i("tried")}, {i("play")} and {i("played")}.</p>
<div class="row" data-s="1">{word("try", 130)}{word("tried", 130)}<span class="gap"></span>{word("play", 130)}{word("played", 130)}</div>
<p class="q" data-s="2">Why does {i("try")} change and {i("play")} not?</p>""", steps=2)

# 3 the rule as taught
slide("The rule as it is often taught", f"""<h2 class="head">The rule as it is often taught</h2>
<p class="q np">Change y to i before a suffix, unless the suffix begins with i.</p>
<p class="body" data-s="1">It works as a mnemonic: it says what to do. It doesn&rsquo;t say why.</p>
<p class="body" data-s="2">The reason often given, that English words don&rsquo;t end in i, lacks a premise: once a suffix joins, the y isn&rsquo;t at the end of anything.</p>""", steps=2)

# 4 the question
slide("A better question", f"""<h2 class="display small">Put the y back,<br>and read what you&rsquo;ve written.</h2>
<p class="lede" data-s="1">The y becomes i where, as y, it would be read wrong in its new place.</p>""", "mid", steps=1)

# 5 happy + er
slide("happy and er", f"""<h2 class="head">{i("happy")} + {i("er")}</h2>
<div class="build">
<p class="type" data-s="1">happ<span class="hl">yer</span></p>
<p class="body" data-s="2">Before a vowel, y reads as a consonant, as it does in {i("yes")} and {i("yellow")}. A reader says <b>happ&middot;yer</b>.</p>
<div class="row" data-s="3">{word("happier", 210)}</div>
<p class="body" data-s="3">With i, nothing reads as a consonant: <b>happ&middot;i&middot;er</b>.</p>
</div>""", steps=3)

# 6 more before a vowel
slide("More before a vowel", f"""<h2 class="head">The same misread, every time</h2>
<table class="sums">
<tr data-s="1"><td>{i("funny")} + {i("er")}</td><td class="mis">funn<span class="hl">yer</span></td><td>&rarr; {i("funnier")}</td></tr>
<tr data-s="2"><td>{i("carry")} + {i("es")}</td><td class="mis">carr<span class="hl">yes</span></td><td>&rarr; {i("carries")}</td></tr>
<tr data-s="3"><td>{i("try")} + {i("ed")}</td><td class="mis">tr<span class="hl">yed</span></td><td>&rarr; {i("tried")}</td></tr>
</table>
<div class="row" data-s="4">{word("carries", 130)}{word("tried", 130)}</div>""", steps=4)

# 7 before a consonant
slide("Before a consonant", f"""<h2 class="head">Before a consonant, too</h2>
<table class="sums">
<tr data-s="1"><td>{i("happy")} + {i("ness")}</td><td class="mis">happ<span class="hl">y</span>ness</td><td>&rarr; {i("happiness")}</td></tr>
<tr data-s="1"><td>{i("merry")} + {i("ment")}</td><td class="mis">merr<span class="hl">y</span>ment</td><td>&rarr; {i("merriment")}</td></tr>
<tr data-s="1"><td>{i("happy")} + {i("ly")}</td><td class="mis">happ<span class="hl">y</span>ly</td><td>&rarr; {i("happily")}</td></tr>
</table>
<p class="body" data-s="2">Inside a word, a y between consonants invites the reading it has in {i("shyness")} and {i("dryly")}. The misreads aren&rsquo;t certain, but they&rsquo;re there to be made.</p>
<p class="body" data-s="3">An i lets the sound shorten, as it does when we say these words: <b>happ&middot;i&middot;ness</b>, <b>merr&middot;i&middot;ment</b>.</p>
<div class="row" data-s="3">{word("happily", 130)}</div>""", steps=3)

# 8 when y stays
slide("When y stays", f"""<h2 class="head">When the y stays</h2>
<div class="cols3">
<div data-s="1"><p class="sum">{i("sly")} + {i("ly")} &rarr; {i("slyly")}</p><p class="body">{i("Slily")} would read as {i("slilly")}: an i between consonants reads short, as in {i("silly")}.</p></div>
<div data-s="2"><p class="sum">{i("play")} + {i("ed")} &rarr; {i("played")}</p><p class="body">The y belongs to a team, {i("ay")}. It&rsquo;s read with the a already, so there&rsquo;s nothing to misread.</p>{word("played", 100)}</div>
<div data-s="3"><p class="sum">{i("carry")} + {i("ing")} &rarr; {i("carrying")}</p><p class="body">{i("Carriing")} would set i beside i, a pair English almost never writes. The y keeps the two apart.</p></div>
</div>""", steps=3)

# 9 the rule as reading
slide("The rule, as reading", f"""<h2 class="head">The rule, said as reading</h2>
<p class="q np">The y becomes i at a seam where y would be read wrong. It stays where i would be read wrong, or where it is part of a team.</p>
<p class="body" data-s="1">Learners can test it themselves: write the word both ways, and read each aloud as written.</p>""", "mid", steps=1)

# 10 in the notation
slide("In the notation", f"""<h2 class="head">In the notation</h2>
<div class="row big">{word("happy", 200, steps=1)}<span class="op">&rarr;</span>{word("happier", 200, steps=1)}</div>
<ol class="steps">
<li data-s="1">The letters, and the bar under {i("pp")}: two letters, one sound.</li>
<li data-s="2">A circle for each sound, red for the vowel sounds, the y&rsquo;s and the i&rsquo;s among them.</li>
<li data-s="3">A cup over the short a, and nothing over the y or the i: both are bare, unstressed, with the same sound.</li>
<li data-s="4">The syllables: {i("happy")} has two, {i("happier")} three.</li>
<li data-s="5">The box around {i("pp")} stops the reach of the y, and of the i, so the a stays short.</li>
<li data-s="6">The seams: {i("hap")} meets the y in {i("happ")} + {i("y")}, and the i takes the y&rsquo;s place in {i("happ")} + {i("i")} + {i("er")}. The letter changes; its job doesn&rsquo;t.</li>
</ol>""", steps=6)

# 11 try these
pairs = [("cry", "ed", "cried"), ("baby", "es", "babies"), ("busy", "ly", "busily"), ("enjoy", "ed", "enjoyed"),
         ("try", "ing", "trying"), ("shy", "ly", "shyly"), ("pretty", "er", "prettier")]
rows = "".join(f'<tr><td>{i(a)} + {i(b)}</td><td class="ans" data-s="{k + 1}">&rarr; {i(c)}</td></tr>' for k, (a, b, c) in enumerate(pairs))
slide("Try these", f"""<h2 class="head">Try these</h2>
<p class="body">Write each both ways and read them aloud. Then click for the answer.</p>
<table class="sums try">{rows}</table>""", steps=len(pairs))

# 12 to take back
slide("To take back", f"""<h2 class="head">To take back to class</h2>
<p class="body">When a learner writes {i("happyness")} or {i("carryed")}, ask them to read it back exactly as written. The misread is the lesson.</p>
<p class="q end" data-s="1">Where else does a letter change at a seam so that a word reads as it should?</p>""", "mid", steps=1)

# 13 sources
slide("Sources", f"""<h2 class="head">Sources</h2>
<p class="body">Edward Carney, <i>A Survey of English Spelling</i> (Routledge, 1994): <i>-y</i> and <i>-ies</i> (<i>berry</i>, <i>berries</i>), p. 70; <i>carry</i>, <i>carried</i>, <i>carries</i>, p. 135; <i>i</i> before some endings (<i>happiness</i>), p. 136.</p>
<p class="body">The words are marked in Legomorphic Notation. The marks are on the Sound and Word Atlas&rsquo;s <a href="../notations.html">Notations</a> page, and this is <a href="../steps/29.html">step 29</a> of its route.</p>
<p class="source">Shared under CC BY-NC-SA 4.0.</p>""", "mid")

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..600;1,9..144,400..600&family=Lexend:wght@300;400;500;600&family=Gentium+Plus&display=swap" rel="stylesheet">
"""

CSS = """
:root{--paper:#f4efe6;--panel:#fbf8f1;--line:#e0d8c7;--ink:#2b2b2b;--soft:#6b6256;--subject:#3a7d44;--verb:#b5402f;--modal:#3f6488;
  --serif:"Fraunces",Georgia,serif;--sans:"Lexend",system-ui,sans-serif;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--paper:#1d1b18;--panel:#26231f;--line:#3b362f;--ink:#ece5d8;--soft:#a89e8f;--subject:#7dbb87;--verb:#e2836e;--modal:#95b6db;}}
:root[data-theme="dark"]{--paper:#1d1b18;--panel:#26231f;--line:#3b362f;--ink:#ece5d8;--soft:#a89e8f;--subject:#7dbb87;--verb:#e2836e;--modal:#95b6db;}
*,*::before,*::after{box-sizing:border-box}
html,body{height:100%;margin:0}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);overflow:hidden;-webkit-font-smoothing:antialiased}
#viewport{position:relative;width:100%;height:100%;overflow:hidden}
#stage{position:absolute;top:0;left:0;width:1600px;height:900px;transform-origin:0 0;background:var(--paper)}
.slide{position:absolute;inset:0;padding:96px 132px 110px;display:flex;flex-direction:column;visibility:hidden}
.slide.on{visibility:visible}
.slide.mid{justify-content:center}
.num{position:absolute;left:132px;bottom:40px;font-size:20px;color:var(--soft);font-variant-numeric:tabular-nums}
.progress{position:absolute;left:0;bottom:0;height:4px;background:var(--soft);opacity:.28;transition:width .35s ease}
.kicker{font-size:24px;letter-spacing:.08em;text-transform:uppercase;color:var(--soft);margin:0 0 18px}
.display{font-family:var(--serif);font-weight:600;font-size:128px;line-height:1;letter-spacing:-.018em;margin:0}
.display.small{font-size:92px;line-height:1.08}
.display .r,.r{color:var(--verb)}
.subtitle{font-family:var(--serif);font-style:italic;font-size:46px;margin:18px 0 0}
.lede{font-size:36px;color:var(--soft);margin:30px 0 0;max-width:1180px}
.head{font-family:var(--serif);font-weight:500;font-size:64px;line-height:1.1;letter-spacing:-.012em;margin:0 0 30px;max-width:1300px}
.body{font-size:30px;line-height:1.5;margin:0 0 18px;max-width:1150px}
.body i,.q i,.lede i,.head i,.sum i,.sums i,.steps i{font-family:var(--serif);font-style:italic}
.q{font-family:var(--serif);font-style:italic;font-size:44px;line-height:1.25;margin:30px 0 0;max-width:1200px}
.q.np{font-size:48px;padding-left:30px;border-left:4px solid var(--modal);margin:0 0 34px}
.q.end{font-size:38px;margin-top:40px;padding-top:28px;border-top:1.5px solid var(--line)}
.source{font-size:22px;color:var(--soft);margin:auto 0 0}
.body a{color:var(--modal);text-underline-offset:5px}
.title .pair{display:flex;align-items:center;gap:26px;margin-top:56px}
.op{font-family:var(--serif);font-size:56px;color:var(--soft)}
.row{display:flex;align-items:flex-end;gap:30px;margin:18px 0}
.row.big{gap:40px;margin:6px 0 10px}
.row .gap{width:80px}
.mw{display:block;width:auto;max-width:100%}
.type{font-family:var(--sans);font-size:120px;line-height:1;margin:6px 0 22px;letter-spacing:.02em;align-self:flex-start}
.hl{color:var(--verb);text-decoration:underline;text-decoration-thickness:6px;text-underline-offset:14px}
table.sums{border-collapse:collapse;font-size:40px;margin:6px 0 20px;align-self:flex-start}
table.sums td{padding:10px 40px 10px 0;vertical-align:baseline}
table.sums td.mis{font-family:var(--sans);color:var(--soft)}
table.sums .hl{text-decoration-thickness:4px;text-underline-offset:9px}
table.sums.try{font-size:38px}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:56px;margin-top:6px}
.cols3 > div{border-top:1.5px solid var(--line);padding-top:20px}
.sum{font-size:38px;margin:0 0 14px}
.cols3 .body{font-size:27px}
ol.steps{margin:6px 0 0;padding-left:36px;font-size:28px;line-height:1.45;max-width:1300px}
ol.steps li{margin:0 0 6px}
/* builds: a click brings the next part in */
[data-s]{opacity:0;transition:opacity .45s ease,transform .45s ease;transform:translateY(10px)}
[data-s].in{opacity:1;transform:none}
svg [data-s]{transform:none}
svg .dr[data-s]{stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset .8s ease,opacity .2s ease}
svg .dr[data-s].in{stroke-dashoffset:0}
tr[data-s]{transform:none}
@media (prefers-reduced-motion: reduce){[data-s]{transition:none}}
#controls{position:fixed;right:18px;bottom:16px;display:flex;gap:8px;opacity:0;transition:opacity .3s ease}
body.awake #controls,#controls:focus-within{opacity:1}
#controls a,#controls button{font:inherit;font-size:22px;width:44px;height:44px;display:grid;place-items:center;border:1px solid var(--line);border-radius:999px;background:var(--panel);color:var(--ink);text-decoration:none;cursor:pointer}
#controls a:focus-visible,#controls button:focus-visible{outline:3px solid var(--modal);outline-offset:3px}
"""

JS = """<script>
(function(){
  var vp = document.getElementById("viewport"), stage = document.getElementById("stage");
  var slides = [].slice.call(document.querySelectorAll(".slide")), N = slides.length, cur = 0, KEY = "deck:y-to-i";
  var num = document.getElementById("num"), prog = document.getElementById("progress");
  function fit(){ var s = Math.min(vp.clientWidth / 1600, vp.clientHeight / 900);
    stage.style.transform = "translate(" + (vp.clientWidth - 1600 * s) / 2 + "px," + (vp.clientHeight - 900 * s) / 2 + "px) scale(" + s + ")"; }
  window.addEventListener("resize", fit); fit();
  function max(sl){ return parseInt(sl.getAttribute("data-max") || "0", 10); }
  function step(sl, k){ sl._k = k; sl.querySelectorAll("[data-s]").forEach(function(el){
    var on = parseInt(el.getAttribute("data-s"), 10) <= k;
    if (el.classList.contains("in") !== on) el.classList.toggle("in", on); }); }
  function show(n, back){
    n = Math.max(0, Math.min(N - 1, n));
    slides.forEach(function(sl, i){ var on = i === n; sl.classList.toggle("on", on); sl.setAttribute("aria-hidden", on ? "false" : "true"); });
    cur = n; step(slides[n], back ? max(slides[n]) : 0);
    num.textContent = (n + 1) + " / " + N; prog.style.width = ((n + 1) / N * 100) + "%";
    try { history.replaceState(null, "", "#" + (n + 1)); } catch (e) {}
    try { localStorage.setItem(KEY, String(n)); } catch (e) {}
  }
  function next(){ var sl = slides[cur]; if ((sl._k || 0) < max(sl)) { step(sl, (sl._k || 0) + 1); return; } if (cur < N - 1) show(cur + 1); }
  function prev(){ var sl = slides[cur]; if ((sl._k || 0) > 0) { step(sl, sl._k - 1); return; } if (cur > 0) show(cur - 1, true); }
  function full(){ try { if (!document.fullscreenElement) document.documentElement.requestFullscreen(); else document.exitFullscreen(); } catch (e) {} }
  document.getElementById("prev").addEventListener("click", function(e){ e.stopPropagation(); prev(); });
  document.getElementById("next").addEventListener("click", function(e){ e.stopPropagation(); next(); });
  document.getElementById("full").addEventListener("click", function(e){ e.stopPropagation(); full(); });
  document.addEventListener("keydown", function(e){
    if (e.target && e.target.closest && e.target.closest("button,a") && (e.key === " " || e.key === "Enter")) return;
    if (["ArrowRight", "ArrowDown", "PageDown", " "].indexOf(e.key) > -1){ e.preventDefault(); next(); }
    else if (["ArrowLeft", "ArrowUp", "PageUp"].indexOf(e.key) > -1){ e.preventDefault(); prev(); }
    else if (e.key === "Home") show(0); else if (e.key === "End") show(N - 1);
    else if (e.key === "f" || e.key === "F") full();
  });
  stage.addEventListener("click", function(e){ if (e.target.closest("a,button")) return;
    var r = stage.getBoundingClientRect(); if (e.clientX - r.left < r.width / 3) prev(); else next(); });
  var tx = null, ty = null;
  vp.addEventListener("touchstart", function(e){ tx = e.touches[0].clientX; ty = e.touches[0].clientY; }, {passive: true});
  vp.addEventListener("touchend", function(e){ if (tx === null) return; var dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) { if (dx < 0) next(); else prev(); } tx = null; }, {passive: true});
  var idle; function wake(){ document.body.classList.add("awake"); clearTimeout(idle); idle = setTimeout(function(){ document.body.classList.remove("awake"); }, 2600); }
  ["mousemove", "touchstart", "keydown"].forEach(function(ev){ document.addEventListener(ev, wake, {passive: true}); });
  window.addEventListener("hashchange", function(){ var h = parseInt((location.hash || "").replace("#", ""), 10); if (h >= 1 && h <= N && h - 1 !== cur) show(h - 1); });
  var h = parseInt((location.hash || "").replace("#", ""), 10), s0 = 0;
  if (h >= 1 && h <= N) s0 = h - 1; else { try { var v = parseInt(localStorage.getItem(KEY), 10); if (v >= 0 && v < N) s0 = v; } catch (e) {} }
  show(s0);
})();
</script>"""


def main():
    doc = f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Y to i at the seam</title>
<meta name="description" content="A presentation for teachers: why the y of happy becomes i in happier, and why it stays in played, slyly and carrying, by how each spelling would read.">
{FONTS}<style>{CSS}</style>
</head>
<body>
<div id="viewport"><div id="stage">
{chr(10).join(SLIDES)}
  <div class="progress" id="progress" aria-hidden="true"></div>
  <div class="num" id="num" aria-live="polite"></div>
</div>
<div id="controls">
  <a id="home" href="../presentations.html" title="All presentations" aria-label="All presentations on the Sound and Word Atlas" onclick="event.stopPropagation()">&#8962;</a>
  <button id="prev" aria-label="Previous slide">&lsaquo;</button>
  <button id="next" aria-label="Next slide">&rsaquo;</button>
  <button id="full" aria-label="Full screen">&#10530;</button>
</div>
</div>
{JS}
</body>
</html>
"""
    out = HERE / "sessions" / "y-to-i.html"
    out.write_text(doc, encoding="utf-8")
    print("wrote", out, f"| {len(SLIDES)} slides | {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
