"""Word studies (20 November 2026): presentations for learners, one family or one idea each, built a piece at a time.

The slides speak to the learner. Teachers' notes sit in a strip along the bottom of each slide, shown with N or the
Notes button: word sums, the history, sources. The shelf is studies.html, beside Explorations under Words.

A study names the words, root page and spelling list it covers (STUDIES), and the build links it from each of them: the
word walk (walk.py), the root page (roots.py), the spelling list (lists.py) and the Presentations page (sessions.py).
A new study only has to be added here to be linked everywhere it belongs.

The deck engine is the one the teachers' decks use (ytoi.py): a 1600 by 900 stage scaled to the screen, pieces that come
in a click at a time (data-s), and keys, taps, swipes and full screen. Words with checked marks on the site are drawn;
everyday examples without them are set in type.
"""
import html, re
import legomorphic_words as LW

STUDIES = [{
    "slug": "per",
    "title": "Try it out",
    "sub": "experiment and experience",
    "root": "*per-", "root_page": "roots/per.html", "list": "lists/family-per.html",
    "words": ["experiment", "experience", "expert", "peril", "pirate", "fear", "experimental", "experienced", "expertise",
              "perilous", "empirical", "experiential", "experimentation", "fearful"],
    "blurb": "Two long words, built from parts a learner can feel: <i>ex-</i> (out), <i>per</i> (try), <i>-ment</i> and "
             "<i>-ence</i>. Read from the end, the parts give the meaning: an experiment is a trying-out. Then why the e is "
             "short in one and long in the other, and the family the root keeps: <i>expert</i>, <i>peril</i>, <i>pirate</i>, <i>fear</i>.",
}]


def for_word(w):
    return [s for s in STUDIES if w in s["words"]]


def for_page(path):
    """The studies that cover a root page or a spelling list, by its path from the site's root."""
    return [s for s in STUDIES if path in (s["root_page"], s["list"])]


def link(s, up=0):
    return f'{"../" * up}studies/{s["slug"]}.html'


# ------------------------------------------------------------------ the deck engine
LAYER_STEP = {"5": 1, "4": 1, "1": 2, "2": 2, "6": 3, "3": 4, "7": 5, "8": 5, "9": 6}


def word(w, h, steps=None, label=None):
    """A marked word as an svg, h pixels tall; set in type if the site has no checked marks for it."""
    if w not in LW.W:
        return f'<span class="tw" style="font-size:{h * 0.62:.0f}px">{html.escape(w)}</span>'
    g, wd, H = LW.svg_word(w, 100.0, 0.0, cls=steps is not None)
    if steps is not None:
        g = re.sub(r'<rect class="wt"[^>]*/>', "", g)
        g = re.sub(r'class="(nz(\d)[^"]*)"', lambda m: f'class="{m.group(1)}" data-s="{steps + LAYER_STEP[m.group(2)] - 1}"', g)
    return (f'<svg class="mw" viewBox="0 0 {wd:.0f} {H:.0f}" style="height:{h}px" role="img" '
            f'aria-label="{html.escape(label or w + ", marked")}">{g}</svg>')


def i(s): return f"<i>{s}</i>"


class Deck:
    def __init__(self): self.slides = []

    def slide(self, label, body, note="", cls="", steps=0):
        n = f'<aside class="tnote" aria-label="Teacher&rsquo;s note">{note}</aside>' if note else ""
        self.slides.append(f'<section class="slide {cls}" aria-label="{html.escape(label)}"' + (f' data-max="{steps}"' if steps else "")
                           + f">\n{body}\n{n}\n</section>")


def join(parts, meanings, word_svg, start, read_end=None):
    """Parts that join into a word: the parts (with plus signs), then what each means, then they close up, then the
    marked word, then (if given) the meaning read from the end. Uses start, start+1, ... start+3 of the slide's clicks."""
    tiles = '<span class="plus">+</span>'.join(
        f'<span class="pc"><b>{p}</b><em data-s="{start}">{m}</em></span>' for p, m in zip(parts, meanings))
    out = (f'<i class="trig" data-s="{start + 1}"></i><div class="pieces">{tiles}</div>'
           f'<div class="joined" data-s="{start + 2}">{word_svg}</div>')
    if read_end:
        out += f'<p class="q end" data-s="{start + 3}">{read_end}</p>'
    return out


FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..600;1,9..144,400..600&family=Lexend:wght@300;400;500;600&display=swap" rel="stylesheet">
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
.slide{position:absolute;inset:0;padding:84px 132px 110px;display:flex;flex-direction:column;visibility:hidden}
.slide.on{visibility:visible}
.slide.mid{justify-content:center}
.num{position:absolute;left:132px;bottom:34px;font-size:20px;color:var(--soft);font-variant-numeric:tabular-nums}
.progress{position:absolute;left:0;bottom:0;height:4px;background:var(--soft);opacity:.28;transition:width .35s ease}
.kicker{font-size:24px;letter-spacing:.08em;text-transform:uppercase;color:var(--soft);margin:0 0 18px}
.display{font-family:var(--serif);font-weight:600;font-size:132px;line-height:1;letter-spacing:-.018em;margin:0}
.subtitle{font-family:var(--serif);font-style:italic;font-size:48px;margin:18px 0 0}
.head{font-family:var(--serif);font-weight:500;font-size:68px;line-height:1.1;letter-spacing:-.012em;margin:0 0 34px}
.head i,.q i,.lede i{font-family:var(--serif);font-style:italic}
.lede{font-size:38px;line-height:1.35;color:var(--soft);margin:22px 0 0;max-width:1250px}
.q{font-family:var(--serif);font-style:italic;font-size:52px;line-height:1.2;margin:34px 0 0;max-width:1300px}
.q.end{font-size:46px;margin-top:30px;padding-top:24px;border-top:1.5px solid var(--line);font-style:normal}
.q b{color:var(--verb);font-weight:600}
.r{color:var(--verb)}
.pair{display:flex;align-items:flex-end;gap:60px;margin-top:56px;flex-wrap:wrap}
.stack{display:grid;gap:26px;margin:6px 0 0}
.mw{display:block;width:auto;max-width:100%}
.tw{font-family:var(--sans);line-height:1;display:block}
.typed{font-size:96px;line-height:1.1;letter-spacing:.01em;margin:0}
.same{color:var(--modal)}
.diff{color:var(--verb);text-decoration:underline;text-decoration-thickness:6px;text-underline-offset:14px}
.felt{display:grid;grid-template-columns:repeat(2,1fr);gap:26px 70px;margin:4px 0 0}
.felt > div{display:flex;align-items:baseline;gap:22px;border-bottom:1.5px solid var(--line);padding-bottom:16px}
.felt .w{font-size:64px;line-height:1}
.felt .w b{color:var(--verb);font-weight:500}
.felt .g{font-family:var(--serif);font-style:italic;font-size:36px;color:var(--soft)}
.fam{display:grid;grid-template-columns:repeat(2,1fr);gap:26px 70px}
.fam > div{display:flex;align-items:flex-end;gap:28px}
.fam .g{font-family:var(--serif);font-style:italic;font-size:34px;color:var(--soft);padding-bottom:12px}
.fam6{display:grid;grid-template-columns:repeat(3,1fr);gap:34px 50px;align-items:end;margin-top:10px}
.syl{display:flex;gap:16px;font-size:96px;line-height:1.1;margin:0 0 10px}
.syl span{color:var(--soft)}
.syl .hit{color:var(--verb);font-weight:500}
.syl .dot{color:var(--line)}
.blanks{list-style:none;margin:0;padding:0;display:grid;gap:34px;font-size:52px}
.blanks .gap{display:inline-block;min-width:330px;border-bottom:3px solid var(--soft);text-align:center;margin:0 10px}
.blanks .ans{font-family:var(--serif);font-style:italic;color:var(--verb)}
/* parts joining: the tiles, what each means, then they close up, then the word */
.pieces{display:flex;align-items:flex-start;gap:26px;transition:gap .6s ease}
.pc{display:grid;justify-items:center;gap:12px}
.pc b{font-weight:500;font-size:110px;line-height:1;padding:10px 26px 18px;border:2px solid var(--line);border-radius:22px;background:var(--panel);transition:border-color .6s ease,background .6s ease,padding .6s ease,border-radius .6s ease}
.pc em{font-family:var(--serif);font-size:36px;color:var(--soft)}
.plus{font-size:80px;line-height:1;color:var(--soft);padding-top:20px;max-width:80px;overflow:hidden;transition:max-width .6s ease,opacity .4s ease}
.trig{display:none}
.trig.in ~ .pieces{gap:0}
.trig.in ~ .pieces .plus{max-width:0;opacity:0}
.trig.in ~ .pieces .pc b{border-color:transparent;background:transparent;padding-left:0;padding-right:0}
.joined{margin-top:26px}
/* the teacher's notes: a strip along the bottom, hidden until N or the Notes button */
.tnote{position:absolute;left:132px;right:132px;bottom:76px;font-size:22px;line-height:1.45;color:var(--soft);border-top:1.5px solid var(--line);padding-top:14px;display:none}
.tnote i{font-family:var(--serif)}
.tnote a{color:var(--modal)}
body.notes .tnote{display:block}
body.notes .slide{padding-bottom:230px}
/* builds: a click brings the next part in */
[data-s]{opacity:0;transition:opacity .45s ease,transform .45s ease;transform:translateY(10px)}
[data-s].in{opacity:1;transform:none}
.trig[data-s]{opacity:1;transform:none}
svg [data-s]{transform:none}
@media (prefers-reduced-motion: reduce){[data-s],.pieces,.plus,.pc b{transition:none}}
#controls{position:fixed;right:18px;bottom:16px;display:flex;gap:8px;opacity:0;transition:opacity .3s ease}
body.awake #controls,#controls:focus-within{opacity:1}
#controls a,#controls button{font:inherit;font-size:22px;min-width:44px;height:44px;padding:0 10px;display:grid;place-items:center;border:1px solid var(--line);border-radius:999px;background:var(--panel);color:var(--ink);text-decoration:none;cursor:pointer}
#controls #notes{font-size:17px}
#controls button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
#controls a:focus-visible,#controls button:focus-visible{outline:3px solid var(--modal);outline-offset:3px}
"""

JS = """<script>
(function(){
  var vp = document.getElementById("viewport"), stage = document.getElementById("stage");
  var slides = [].slice.call(document.querySelectorAll(".slide")), N = slides.length, cur = 0, KEY = "study:" + document.body.dataset.slug;
  var num = document.getElementById("num"), prog = document.getElementById("progress"), nb = document.getElementById("notes");
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
  function notes(on){ document.body.classList.toggle("notes", on); nb.setAttribute("aria-pressed", String(on)); try { localStorage.setItem("study:notes", on ? "1" : ""); } catch (e) {} }
  document.getElementById("prev").addEventListener("click", function(e){ e.stopPropagation(); prev(); });
  document.getElementById("next").addEventListener("click", function(e){ e.stopPropagation(); next(); });
  document.getElementById("full").addEventListener("click", function(e){ e.stopPropagation(); full(); });
  nb.addEventListener("click", function(e){ e.stopPropagation(); notes(!document.body.classList.contains("notes")); });
  document.addEventListener("keydown", function(e){
    if (e.target && e.target.closest && e.target.closest("button,a") && (e.key === " " || e.key === "Enter")) return;
    if (["ArrowRight", "ArrowDown", "PageDown", " "].indexOf(e.key) > -1){ e.preventDefault(); next(); }
    else if (["ArrowLeft", "ArrowUp", "PageUp"].indexOf(e.key) > -1){ e.preventDefault(); prev(); }
    else if (e.key === "Home") show(0); else if (e.key === "End") show(N - 1);
    else if (e.key === "f" || e.key === "F") full();
    else if (e.key === "n" || e.key === "N") notes(!document.body.classList.contains("notes"));
  });
  stage.addEventListener("click", function(e){ if (e.target.closest("a,button,.tnote")) return;
    var r = stage.getBoundingClientRect(); if (e.clientX - r.left < r.width / 3) prev(); else next(); });
  var tx = null, ty = null;
  vp.addEventListener("touchstart", function(e){ tx = e.touches[0].clientX; ty = e.touches[0].clientY; }, {passive: true});
  vp.addEventListener("touchend", function(e){ if (tx === null) return; var dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) { if (dx < 0) next(); else prev(); } tx = null; }, {passive: true});
  var idle; function wake(){ document.body.classList.add("awake"); clearTimeout(idle); idle = setTimeout(function(){ document.body.classList.remove("awake"); }, 2600); }
  ["mousemove", "touchstart", "keydown"].forEach(function(ev){ document.addEventListener(ev, wake, {passive: true}); });
  window.addEventListener("hashchange", function(){ var h = parseInt((location.hash || "").replace("#", ""), 10); if (h >= 1 && h <= N && h - 1 !== cur) show(h - 1); });
  try { notes(localStorage.getItem("study:notes") === "1"); } catch (e) { notes(false); }
  var h = parseInt((location.hash || "").replace("#", ""), 10), s0 = 0;
  if (h >= 1 && h <= N) s0 = h - 1; else { try { var v = parseInt(localStorage.getItem(KEY), 10); if (v >= 0 && v < N) s0 = v; } catch (e) {} }
  show(s0);
})();
</script>"""


def page(s, deck):
    return f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(s["title"])}: a word study</title>
<meta name="description" content="A word study for learners: {html.escape(re.sub(r'<[^>]+>', '', s['sub']))}, built a piece at a time.">
{FONTS}<style>{CSS}</style>
</head>
<body data-slug="{s["slug"]}">
<div id="viewport"><div id="stage">
{chr(10).join(deck.slides)}
  <div class="progress" id="progress" aria-hidden="true"></div>
  <div class="num" id="num" aria-live="polite"></div>
</div>
<div id="controls">
  <a id="home" href="../studies.html" title="All word studies" aria-label="All word studies on legomorphics.ca" onclick="event.stopPropagation()">&#8962;</a>
  <button id="notes" aria-pressed="false" title="Teacher&rsquo;s notes (N)">Notes</button>
  <button id="prev" aria-label="Previous slide">&lsaquo;</button>
  <button id="next" aria-label="Next slide">&rsaquo;</button>
  <button id="full" aria-label="Full screen">&#10530;</button>
</div>
</div>
{JS}
</body>
</html>
"""


# ------------------------------------------------------------------ *per-: Try it out
def per_deck():
    D = Deck()
    D.slide("Title", f"""<p class="kicker">A word study &middot; <i>*per-</i></p>
<h1 class="display">Try it out</h1>
<p class="subtitle">experiment and experience</p>
<div class="pair">{word("experiment", 120)}{word("experience", 120)}</div>""",
            "A word study for learners. Click, tap, or press the right arrow for each next piece; N shows and hides these notes. "
            "The page for teachers is <a href=\"../roots/per.html\">*per-</a>, with its <a href=\"../lists/family-per.html\">spelling list</a>.", "mid")

    D.slide("What's the same", f"""<h2 class="head">Two long words. What&rsquo;s the same?</h2>
<div class="stack">
<p class="typed"><span class="same" data-s="1">experi</span><span class="diff" data-s="2">ment</span></p>
<p class="typed"><span class="same" data-s="1">experi</span><span class="diff" data-s="2">ence</span></p>
</div>
<p class="q" data-s="3">The same start. A different end.</p>""",
            "Both are ex + peri, with a different ending: -ment and -ence. The next three slides give each part a felt meaning "
            "from words learners know, before the parts go back together.", steps=3)

    def felt(head, rows, says, note):
        cells = "".join(f'<div data-s="{k + 1}"><span class="w">{w}</span><span class="g">{g}</span></div>' for k, (w, g) in enumerate(rows))
        D.slide(head, f"""<h2 class="head">{head}</h2>
<div class="felt">{cells}</div>
<p class="q" data-s="{len(rows) + 1}">{says}</p>""", note, steps=len(rows) + 1)

    felt("ex-", [("<b>ex</b>it", "a way out"), ("<b>ex</b>hale", "breathe out"), ("<b>ex</b>port", "send out"), ("<b>ex</b>plode", "burst out")],
         "<b>ex-</b> means <b>out</b>.",
         "Latin <i>ex</i>, out of; in some words, all the way, thoroughly. Before some letters it shrinks to e-: "
         "<i>educate</i>, <i>emerge</i>. The examples are set in type: the site has no checked marks for them yet.")
    felt("-ment", [("pay &rarr; pay<b>ment</b>", "the paying"), ("move &rarr; move<b>ment</b>", "the moving"),
                   ("agree &rarr; agree<b>ment</b>", "what you agree"), ("enjoy &rarr; enjoy<b>ment</b>", "what you get from it")],
         "<b>-ment</b>: the doing of it, or what comes of it.",
         "Latin <i>-mentum</i>: the act, the means or the result. It makes a noun from a verb.")
    felt("-ence", [("silent &rarr; sil<b>ence</b>", "being silent"), ("patient &rarr; pati<b>ence</b>", "being patient"),
                   ("absent &rarr; abs<b>ence</b>", "being away"), ("different &rarr; differ<b>ence</b>", "being different")],
         "<b>-ence</b>: being that way.",
         "-ence goes with -ent, from Latin <i>-entia</i>: <i>silent</i>, <i>silence</i>. It makes a noun of a state.")

    fam = [("expert", "someone who has tried, and knows"), ("peril", "a risk, a danger"),
           ("pirate", "someone who tries an attack"), ("fear", "what a risk makes you feel")]
    cells = "".join(f'<div data-s="{k + 1}">{word(w, 96)}<span class="g">{g}</span></div>' for k, (w, g) in enumerate(fam))
    D.slide("per", f"""<h2 class="head"><b class="r">per</b>: try, take a risk</h2>
<div class="fam">{cells}</div>
<p class="q" data-s="5">A very old word for <b>try</b>, in many words.</p>""",
            "All four come from the root *per-, to try, to risk: <i>expert</i> from Latin <i>expertus</i>, tried; <i>peril</i> from "
            "<i>per&imacr;culum</i>, a trial, a danger; <i>pirate</i> from Greek <i>peira</i>, a trial; <i>fear</i> from Old English "
            "<i>f&aelig;r</i>, a danger, a word English kept from the start.", steps=5)

    D.slide("Build experiment", f"""<h2 class="head">Build it</h2>
{join(["ex", "peri", "ment"], ["out", "try", "the doing"], word("experiment", 150), 1,
      "Read it from the end: <b>the doing</b> of <b>trying</b> it <b>out</b>. An experiment is a trying-out.")}""",
            "Word sum: ex + peri + ment &rarr; <i>experiment</i>. Read from the last part back, the parts give the meaning in "
            "order: the suffix says what kind of word it is (a thing, an act), and the rest says what of.", steps=4)
    D.slide("Build experience", f"""<h2 class="head">And the other one</h2>
{join(["ex", "peri", "ence"], ["out", "try", "being that way"], word("experience", 150), 1,
      "From the end: <b>being</b> one who has <b>tried</b> things <b>out</b>. Experience is what trying leaves you with.")}""",
            "Word sum: ex + peri + ence &rarr; <i>experience</i>. In Latin, <i>experientia</i> was the trying and the knowing "
            "that comes of it. English once used the two words almost the same way; French still uses one, <i>exp&eacute;rience</i>, for both.", steps=4)

    D.slide("Listen to the e", f"""<h2 class="head">Listen to the e</h2>
<p class="syl"><span>ex</span><span class="dot">&middot;</span><span class="hit">per</span><span class="dot">&middot;</span><span>i</span><span class="dot">&middot;</span><span>ment</span></p>
<p class="lede" data-s="1">In <b class="r">per</b>, the r closes the syllable. The e is short.</p>
<p class="syl" data-s="2" style="margin-top:40px"><span>ex</span><span class="dot">&middot;</span><span class="hit">pe</span><span class="dot">&middot;</span><span>ri</span><span class="dot">&middot;</span><span>ence</span></p>
<p class="lede" data-s="3">In <b class="r">pe</b>, the syllable is open. The e says its name.</p>""",
            "The notation draws this as closed and open: <i>per</i> in <i>experiment</i>, as in <i>very</i>; <i>pe</i> in "
            "<i>experience</i>, with the vault from the i, as in <i>here</i>. The patterns underneath (Chomsky and Halle) are "
            "on the <a href=\"../roots/per.html#break-h\">teacher&rsquo;s page</a>, with their exceptions.", steps=3)

    D.slide("And the i", f"""<h2 class="head">And the i?</h2>
<div class="stack"><p class="typed">exper<span class="diff">i</span>ment</p><p class="typed">exper<span class="diff">i</span>ence</p></div>
<p class="lede" data-s="1">Both words have an i after <b class="r">per</b>. It&rsquo;s left over from the old Latin word.</p>
<p class="q" data-s="2">You don&rsquo;t need to know why it&rsquo;s there to read them. The family is what matters.</p>""",
            "The i is Latin&rsquo;s theme vowel: <i>exper&imacr;r&imacr;</i> is a verb of the class whose stems end in &imacr; "
            "(<i>aud&imacr;re</i>: <i>audience</i>, <i>auditor</i>). It marks the verb&rsquo;s class and carries no meaning. "
            "<i>Expert</i>, from <i>expertus</i>, has none: the root is per. In <i>experience</i> it also does a job in sound, "
            "making the e long. None of this is needed to teach the morphology, phonology, spelling or history here.", steps=2)

    six = ["experiment", "experience", "expert", "peril", "pirate", "fear"]
    D.slide("The family", f"""<h2 class="head">One old word, a family of words</h2>
<div class="fam6">{"".join(f'<div data-s="{k + 1}">{word(w, 92)}</div>' for k, w in enumerate(six))}</div>
<p class="q" data-s="7">Try, risk, test: one family.</p>""",
            "The whole family, with <i>empirical</i>, <i>perilous</i>, <i>parlous</i> and <i>fearful</i>, and the roads each word "
            "came by, is on the <a href=\"../roots/per.html\">*per- page</a>.", steps=7)

    D.slide("Your turn", f"""<h2 class="head">Your turn</h2>
<ol class="blanks">
<li>We did an <span class="gap"><span class="ans" data-s="1">experiment</span></span> with ice.</li>
<li>Camp was a good <span class="gap"><span class="ans" data-s="2">experience</span></span>.</li>
<li>Ask an <span class="gap"><span class="ans" data-s="3">expert</span></span>.</li>
</ol>""",
            "Say each sentence with the blank first, and let the class choose before the click shows the word. The "
            "<a href=\"../lists/family-per.html\">spelling list</a> has more to build and use.", steps=3)

    D.slide("For teachers", f"""<h2 class="head">For teachers</h2>
<p class="lede">Word sums: ex + peri + ment &rarr; <i>experiment</i>; ex + peri + ence &rarr; <i>experience</i>; ex + pert &rarr; <i>expert</i>; peril + ous &rarr; <i>perilous</i>; em + pir + ic + al &rarr; <i>empirical</i>.</p>
<p class="lede">The family follows the Indo-European Lexicon (per- 2e), with the Middle English Dictionary on <i>experiment</i>. The teacher&rsquo;s page is <a href="../roots/per.html">*per-</a>; the list to print is the <a href="../lists/family-per.html">*per- spelling list</a>.</p>
<p class="lede">The words with marks are drawn in Legomorphic Notation; the marks are on the <a href="../notations.html">Notations</a> page.</p>""", cls="mid")
    return D


DECKS = {"per": per_deck}


def write(OUT, door_page):
    (OUT / "studies").mkdir(exist_ok=True)
    cards = []
    for s in STUDIES:
        D = DECKS[s["slug"]]()
        (OUT / "studies" / f"{s['slug']}.html").write_text(page(s, D), encoding="utf-8")
        cards.append(f"""<article class="study">
<p class="eyebrow">{s["root"]} &middot; {len(D.slides)} slides</p>
<h2><a href="studies/{s['slug']}.html">{s["title"]}</a>: <i>{s["sub"]}</i></h2>
<p>{s["blurb"]}</p>
<p class="deck-links"><a class="btn" href="studies/{s['slug']}.html">Open the word study</a> <span class="t-only">&middot; for teachers: <a href="{s["root_page"]}">the {s["root"]} page</a> and <a href="{s["list"]}">its spelling list</a></span></p>
</article>""")
    door_page("studies", "Word studies · Sounds and Words, Assembled",
              "Presentations for learners: a family of words built a piece at a time, from parts you can feel.",
              f"""<section class="hero door-hero"><div class="wrap">
<p class="eyebrow t-only">Words &middot; for learners</p>
<h1>Word studies</h1>
<p class="lead">Presentations for learners. Each takes one family of words and builds it a piece at a time: what each part means, how the parts join, and how to read the word they make.</p>
<p class="sub t-only">Click, tap, or press the right arrow for each next piece; the left third of a slide goes back. N, or the Notes button that shows when you move the mouse, opens a strip of teacher&rsquo;s notes along the bottom: word sums, the history and sources. Each study is linked from its words in the word walk, its root page and its spelling list.</p>
</div></section>
<section class="about"><div class="wrap">
{"".join(cards)}
</div></section>""")
    print(f"wrote studies.html | {len(STUDIES)} word stud{'y' if len(STUDIES) == 1 else 'ies'}")
