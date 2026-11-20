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
}, {
    "slug": "education",
    "title": "From duct to education",
    "sub": "duct, duce, and the words built on them",
    "root": "*deuk-", "root_page": "roots/deuk.html", "list": "lists/family-deuk.html",
    "words": ["duct", "produce", "product", "production", "reduce", "reduction", "conduct", "educate", "education",
              "educational", "educator", "miseducation", "introduce", "introduction", "aqueduct"],
    "blurb": "A duct leads air along, and duce and duct take turns: <i>produce</i>, <i>product</i>. Then <i>ex-</i> shrinks to "
             "<i>e-</i>, and <i>education</i> is built a part at a time, with the e of <i>-ate</i> dropping out and the i of "
             "<i>-ion</i> taking over its job, up to <i>educational</i> and <i>miseducation</i>. Last, where the beat moves.",
}, {
    "slug": "leg",
    "title": "Gather, read, say",
    "sub": "from *leg- to legomorphics",
    "root": "*leg-", "root_page": "roots/leg.html", "list": "lists/family-leg.html",
    "words": ["collect", "collection", "select", "selection", "elect", "election", "lecture", "lesson", "legend", "legendary",
              "legible", "illegible", "lexicon", "lexical", "logic", "logical", "dialogue", "prologue", "catalogue", "dialect",
              "intellect", "intelligent", "eligible", "neglect", "recollect", "legomorphic", "legomorphics", "prolegomenon"],
    "blurb": "One old word for <i>gather</i> and its three roads: gather and choose (<i>collect</i>, <i>select</i>), read in "
             "Latin (<i>lecture</i>, <i>lesson</i>, <i>legend</i>, <i>legible</i>), and say in Greek (<i>lexicon</i>, "
             "<i>logic</i>, <i>dialogue</i>). How a lesson was first a reading, what a legend is on a map, and how the "
             "notation&rsquo;s own name is built. And one look-alike: the bricks.",
}, {
    "slug": "sign",
    "title": "The g in sign",
    "sub": "sign, signal, signature, design, and the family",
    "root": "sign", "root_page": "roots/sign.html", "list": "lists/family-sign.html",
    "words": ["sign", "signs", "signing", "signal", "signature", "signatory", "signet", "signify", "significant", "significance",
              "design", "designer", "designate", "designation", "assign", "assignment", "resign", "resignation", "consign",
              "insignia", "seal", "sigil"],
    "blurb": "The classic question: why is there a g in <i>sign</i> when you can&rsquo;t hear it? <i>Signal</i>, <i>signature</i> "
             "and <i>signify</i> say it, and the spelling keeps the family together. How the quiet g makes the i say its name, "
             "how <i>design</i> marks out a plan, the sign matrix, and the little sign that lost its g: <i>seal</i>.",
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
        return f'<span class="tw" style="font-size:{h * 0.44:.0f}px;padding-bottom:{h * 0.3:.0f}px">{html.escape(w)}</span>'   # sized to sit level with a marked word
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


def drop(p):
    """at(e) shows its e until the parts close up, then the e drops out."""
    return re.sub(r"\((\w+)\)", r'<span class="xx">\1</span>', p)


def join(parts, meanings, word_svg, start, read_end=None):
    """Parts that join into a word: the parts (with plus signs), then what each means, then they close up, then the
    marked word, then (if given) the meaning read from the end. Uses start, start+1, ... start+3 of the slide's clicks."""
    tiles = '<span class="plus">+</span>'.join(
        f'<span class="pc"><b>{drop(p)}</b><em data-s="{start}">{m}</em></span>' for p, m in zip(parts, meanings))
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
.ishas{display:grid;grid-template-columns:1fr 1fr;gap:10px 80px;margin-top:4px}
.ishas h3{margin:0 0 8px;font-family:var(--sans);font-weight:400;font-size:28px;color:var(--soft);border-bottom:1.5px solid var(--line);padding-bottom:10px}
.ishas h3 b{color:var(--verb);font-weight:500}
.ishas p{margin:0;font-size:50px;line-height:1.25}
.ishas p b{color:var(--verb);font-weight:inherit}
.duo{display:flex;gap:120px;align-items:flex-end;margin-top:40px}
.duo figure{margin:0;display:grid;justify-items:start;gap:14px}
.duo figcaption{font-family:var(--serif);font-style:italic;font-size:38px;color:var(--soft)}
.matrix{display:flex;align-items:center;gap:0;margin:10px 0 0;font-family:var(--sans)}
.matrix .mbox{border:3px solid var(--ink);padding:12px 26px;display:grid;gap:0;font-size:31px;line-height:1.12;background:var(--panel)}
.matrix .mbase{font-size:80px;line-height:1;font-family:var(--serif);color:var(--verb);padding:20px 40px;border-width:4px;margin:0 -3px}
.matrix .mcols{display:flex;border:3px solid var(--ink);background:var(--panel)}
.matrix .mcols .mbox{border:0;border-left:3px solid var(--line)}
.matrix .mcols .mbox:first-child{border-left:0}
.paths{display:flex;gap:40px;flex-wrap:wrap;margin-top:18px;font-size:30px;color:var(--soft)}
.paths b{color:var(--ink);font-weight:500}
.fork{display:grid;grid-template-columns:1fr 1fr;gap:0 90px;margin:0 60px}
.fork .top{grid-column:1/-1;text-align:center;padding-bottom:14px;margin-bottom:16px;border-bottom:4px solid var(--line)}
.fork .lw{font-family:var(--serif);font-size:84px;line-height:1}
.fork .lw b{color:var(--verb);font-weight:inherit}
.fork .g{display:block;font-family:var(--serif);font-style:italic;font-size:34px;color:var(--soft);margin-top:4px}
.fork .g b{font-style:normal;color:var(--verb);font-weight:inherit}
.fork h3{font-family:var(--serif);font-weight:500;font-size:40px;margin:0 0 8px}
.fork h3 small{font-family:var(--serif);font-size:36px;color:var(--soft);font-weight:400;margin-left:14px}
.fork p{font-family:var(--serif);font-size:44px;line-height:1.05;margin:0 0 12px;padding-left:34px;position:relative}
.fork p::before{content:"↓";position:absolute;left:0;top:2px;font-size:30px;color:var(--soft)}
.fork p small{display:block;font-family:var(--sans);font-size:23px;color:var(--soft);margin-top:4px}
.roads3{display:grid;grid-template-columns:repeat(3,1fr);gap:0 46px;margin-top:4px}
.roads3 > div{border-top:4px solid var(--line);padding-top:16px;display:grid;gap:12px;align-content:start}
.roads3 h3{font-family:var(--serif);font-weight:500;font-size:46px;margin:0 0 4px}
.roads3 h3 small{display:block;font-family:var(--sans);font-size:22px;color:var(--soft);font-weight:400;margin-top:4px}
.roads3 .tw2{font-size:44px;line-height:1.1}
.roads3 .tw2 b{color:var(--verb);font-weight:500}
.chain{display:grid;gap:22px;margin-top:6px}
.chain p{margin:0;font-size:72px;line-height:1}
.chain p small{font-family:var(--serif);font-style:italic;font-size:36px;color:var(--soft);margin-left:24px}
.fam6{display:grid;grid-template-columns:repeat(3,1fr);gap:34px 50px;align-items:end;margin-top:10px}
.syl{display:flex;gap:16px;font-size:96px;line-height:1.1;margin:0 0 10px}
.syl span{color:var(--soft)}
.syl .hit{color:var(--verb);font-weight:500}
.syl .dot{color:var(--line)}
.blanks{list-style:none;margin:0;padding:0;display:grid;gap:34px;font-size:52px}
.blanks .gap{display:inline-block;min-width:330px;border-bottom:3px solid var(--soft);text-align:center;margin:0 10px}
.blanks .ans{font-family:var(--serif);font-style:italic;color:var(--verb)}
/* parts joining: the tiles, what each means, then they close up, then the word */
.pieces{display:flex;align-items:flex-start;gap:26px;padding-bottom:66px;transition:gap .6s ease}
.pc{position:relative;display:block}
.pc b{font-weight:500;font-size:110px;line-height:1;padding:10px 26px 18px;border:2px solid var(--line);border-radius:22px;background:var(--panel);transition:border-color .6s ease,background .6s ease,padding .6s ease,border-radius .6s ease}
.pc em{position:absolute;top:calc(100% + 16px);left:-240px;right:-240px;text-align:center;white-space:nowrap;font-family:var(--serif);font-size:36px;color:var(--soft)}
.trig.in ~ .pieces .pc em{opacity:0}   /* the parts have joined: their meanings come back in the line read from the end */
.plus{font-size:80px;line-height:1;color:var(--soft);padding-top:20px;max-width:80px;overflow:hidden;transition:max-width .6s ease,opacity .4s ease}
.trig{display:none}
.trig.in ~ .pieces{gap:0}
.trig.in ~ .pieces .plus{max-width:0;opacity:0}
.xx{display:inline-block;max-width:1.2em;overflow:hidden;vertical-align:bottom;color:var(--verb);transition:max-width .7s ease .2s,opacity .5s ease .2s}
.trig.in ~ .pieces .xx{max-width:0;opacity:0}
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
    # -ent describes, -ence names (20 November 2026): shown in pairs of sentences, not defined.
    rows = [("she is pati<b>ent</b>", "she has pati<b>ence</b>"), ("they are differ<b>ent</b>", "there is a differ<b>ence</b>"),
            ("he is abs<b>ent</b>", "we noticed his abs<b>ence</b>"), ("the room is sil<b>ent</b>", "we sat in sil<b>ence</b>")]
    cells = "".join(f'<p data-s="{k + 1}">{x}</p><p data-s="{k + 1}">{y}</p>' for k, (x, y) in enumerate(rows))
    D.slide("-ence", f"""<h2 class="head">-ence</h2>
<div class="ishas"><h3><b>-ent</b> describes</h3><h3><b>-ence</b> names</h3>{cells}</div>
<p class="q" data-s="5"><b>-ent</b> tells what something is like. <b>-ence</b> turns it into a thing you can have.</p>""",
            "Show the job, not a definition: -ent describes, -ence names. Latin&rsquo;s present form, <i>-ens</i> "
            "(<i>patiens</i>, enduring; <i>absens</i>, being away), and its noun, <i>-entia</i>. &lsquo;Have&rsquo; is a handle, not "
            "a rule: we sat in silence, we noticed his absence. Check by ear: The room was ___ (silent). We sat in ___ (silence).", steps=5)

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
{join(["ex", "peri", "ence"], ["out", "try", "a thing you have"], word("experience", 150), 1,
      "From the end: <b>what you have</b> from <b>trying</b> things <b>out</b>. Experience is what trying leaves you with.")}""",
            "Word sum: ex + peri + ence &rarr; <i>experience</i>. -ence names, as on the -ence slide: she <i>has</i> experience; "
            "the word that describes her is <i>experienced</i>. In Latin, <i>experientia</i> was the trying and the knowing "
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


# ------------------------------------------------------------------ *deuk-: From duct to education
def educ_deck():
    D = Deck()
    D.slide("Title", f"""<p class="kicker">A word study &middot; <i>*deuk-</i></p>
<h1 class="display">From duct to education</h1>
<p class="subtitle">a word that leads, and the words built on it</p>
<div class="pair">{word("duct", 120)}{word("education", 120)}</div>""",
            "A word study for learners. Click, tap, or press the right arrow for each next piece; N shows and hides these notes. "
            "The page for teachers is <a href=\"../roots/deuk.html\">*deuk-</a>, with its <a href=\"../lists/family-deuk.html\">spelling list</a>.", "mid")

    D.slide("duct", f"""<h2 class="head">A <b class="r">duct</b> leads something along</h2>
<div class="pair" style="margin-top:0">{word("duct", 150)}</div>
<p class="lede" data-s="1">A duct leads air through a building. An aqueduct leads water.</p>
<p class="q" data-s="2"><b>duct</b>, and its partner <b>duce</b>: <b>lead</b>.</p>""",
            "Latin <i>d&umacr;cere</i>, to lead, and <i>ductus</i>, led. English borrowed the verbs with duce and their "
            "nouns with duct. The root is <i>*deuk-</i>, to lead, to pull: English kept its own words from it too, <i>tug</i> "
            "and <i>tow</i>.", steps=2)

    def felt(head, rows, says, note):
        cells = "".join(f'<div data-s="{k + 1}"><span class="w">{w}</span><span class="g">{g}</span></div>' for k, (w, g) in enumerate(rows))
        D.slide(head, f"""<h2 class="head">{head}</h2>
<div class="felt">{cells}</div>
<p class="q" data-s="{len(rows) + 1}">{says}</p>""", note, steps=len(rows) + 1)

    felt("duce and duct take turns", [("pro<b>duce</b>", "lead forward: make"), ("pro<b>duct</b>", "what is made"),
                                      ("re<b>duce</b>", "lead back: make less"), ("re<b>duct</b>ion", "the making less")],
         "The verb says <b>duce</b>. Add an ending, and it says <b>duct</b>.",
         "duce is Latin&rsquo;s present form, duct its past form: <i>produce</i>, <i>product</i>, <i>production</i>; "
         "<i>reduce</i>, <i>reduction</i>. The front part says which way the leading goes: pro, forward; re, back; "
         "intro, inside; con, together.")

    D.slide("ex becomes e", f"""<h2 class="head"><b class="r">ex-</b> means out. Before d, it gets shorter.</h2>
<i class="trig" data-s="2"></i><div class="pieces"><span class="pc"><b>e<span class="xx">x</span></b><em data-s="1">out</em></span><span class="plus">+</span><span class="pc"><b>duc</b><em data-s="1">lead</em></span></div>
<p class="lede" data-s="3">Try saying <b>ex-duc</b>. Now <b>e-duc</b>. The x drops out: it&rsquo;s easier to say.</p>
<p class="q" data-s="4">Same part, shorter spelling: <b>e-</b> means <b>out</b>.</p>""",
            "Latin <i>ex-</i> is written <i>e-</i> before d, l, m, n, r and v: <i>educate</i>, <i>emerge</i>, <i>elect</i>, "
            "<i>evict</i>. The same thing happens inside Latin itself: it said <i>&emacr;d&umacr;cere</i>, to lead out, "
            "not <i>exd&umacr;cere</i>.", steps=4)

    felt("-ate and -ion", [("decor<b>ate</b>", "to make it pretty"), ("decor<b>ation</b>", "what you make"),
                           ("celebr<b>ate</b>", "to have a party"), ("celebr<b>ation</b>", "the party")],
         "<b>-ate</b> makes a doing word. <b>-ion</b> names the doing.",
         "Both are Latin. -ate is the past form of a verb, made into an English verb; -ion makes a noun of an act. "
         "When -ion joins -ate, the e drops and the t says sh: <i>decorate</i>, <i>decoration</i>.")

    D.slide("The i takes over", f"""<h2 class="head">The e drops out. The i takes over its job.</h2>
<div class="fam" style="grid-template-columns:1fr">
<div data-s="1">{word("notate", 120)}<span class="g">the e at the end makes the a say its name</span></div>
<div data-s="2">{word("notation", 120)}<span class="g">no e now: the i of <b class="r">-ion</b> does the same job</span></div>
</div>
<p class="q" data-s="3">Letters can drop out, and others do their jobs.</p>""",
            "The notation draws it: in <i>notate</i> the vault comes from the final e; in <i>notation</i> the e is gone and the "
            "vault comes from the i of -ion, which stands before another vowel (the pattern on the "
            "<a href=\"../roots/per.html#break-h\">*per- page</a>). The t says sh before i and a vowel: the green bar under ti.", steps=3)

    D.slide("Build educate", f"""<h2 class="head">Build it</h2>
{join(["e", "duc", "ate"], ["out", "lead, bring up", "do it"], word("educate", 150), 1,
      "Read it from the end: <b>do</b> the <b>bringing up</b>, the leading <b>out</b>. To educate is to bring someone up and on.")}""",
            "Word sum: e + duc + ate &rarr; <i>educate</i>. Latin <i>&emacr;duc&amacr;re</i>, to bring up, to rear, a verb "
            "beside <i>&emacr;d&umacr;cere</i>, to lead out. To educate was first to raise a child; leading out what is in a "
            "learner is a later reading of the word, and a fair one (the <a href=\"../roots/deuk.html\">*deuk- page</a>).", steps=4)
    D.slide("Build education", f"""<h2 class="head">Name the doing</h2>
{join(["e", "duc", "at(e)", "ion"], ["out", "lead", "do it", "the doing"], word("education", 150), 1,
      "From the end: <b>the doing</b> of <b>bringing up</b> and leading <b>out</b>.")}""",
            "Word sum: e + duc + at(e) + ion &rarr; <i>education</i>. The e of -ate drops before -ion, and the i of -ion takes over "
            "its job, making the a long. The t says sh.", steps=4)
    D.slide("Build educational", f"""<h2 class="head">One more part</h2>
{join(["education", "al"], ["the bringing up", "having to do with"], word("educational", 140), 1,
      "From the end: <b>having to do with</b> the <b>bringing up</b>. An educational game helps you learn.")}""",
            "Word sum: e + duc + at(e) + ion + al &rarr; <i>educational</i>. Each ending turns the word into a new kind: "
            "a doing word (-ate), a thing (-ion), a describing word (-al). Read from the last part back, they come in order.", steps=4)
    D.slide("Build miseducation", f"""<h2 class="head">And one at the front</h2>
<p class="lede" data-s="1" style="margin:0 0 26px"><b class="r">mis</b>take, <b class="r">mis</b>spell: done <b>wrongly</b>.</p>
{join(["mis", "education"], ["wrongly", "the bringing up"], word("miseducation", 120), 2,
      "<b>mis-</b> means <b>wrongly</b>: miseducation is teaching that leads you wrong.")}""",
            "Word sum: mis + e + duc + at(e) + ion &rarr; <i>miseducation</i>. A prefix joins at the front with no change: mis + "
            "spell keeps both s&rsquo;s, <i>misspell</i>.", steps=5)

    D.slide("The beat moves", f"""<h2 class="head">Say them. The beat moves.</h2>
<p class="syl"><span class="hit">ED</span><span class="dot">&middot;</span><span>u</span><span class="dot">&middot;</span><span>cate</span></p>
<p class="syl" data-s="1"><span>ed</span><span class="dot">&middot;</span><span>u</span><span class="dot">&middot;</span><span class="hit">CA</span><span class="dot">&middot;</span><span>tion</span></p>
<p class="syl" data-s="2"><span>ed</span><span class="dot">&middot;</span><span>u</span><span class="dot">&middot;</span><span class="hit">CA</span><span class="dot">&middot;</span><span>tion</span><span class="dot">&middot;</span><span>al</span></p>
<p class="lede" data-s="3">The beat moves, and the spelling stays the same. Listen to the d, too: many people say <b>ED-ju-cate</b>, and the spelling keeps the d of <b class="r">duc</b>.</p>""",
            "-ion pulls the stress to the syllable just before it: EDucate, eduCAtion, eduCAtional. The a is long in all three. "
            "The d and the u blend into the sound of j in most speech (as in <i>gradual</i> and <i>procedure</i>); the spelling "
            "keeps the parts, and the notation has no mark for the blend.", steps=3)

    six = [("duct", "a pipe that leads air"), ("product", "what is made"), ("reduce", "make less"),
           ("conduct", "how you lead yourself"), ("education", "bringing up"), ("team", "English kept its own: pulling together")]
    cells = "".join(f'<div data-s="{k + 1}">{word(w, 84)}<span class="g">{g}</span></div>' for k, (w, g) in enumerate(six))
    D.slide("The family", f"""<h2 class="head">One old word for <b class="r">lead</b>, a family of words</h2>
<div class="fam">{cells}</div>""",
            "<i>Team</i> is English&rsquo;s own: in the Germanic languages the root&rsquo;s d became t, so <i>tug</i>, <i>tow</i>, "
            "<i>tie</i> and <i>team</i> start with t where Latin&rsquo;s words start with d. The whole family is on the "
            "<a href=\"../roots/deuk.html\">*deuk- page</a>.", steps=6)

    D.slide("Your turn", f"""<h2 class="head">Your turn</h2>
<ol class="blanks">
<li>Air comes in through the <span class="gap"><span class="ans" data-s="1">duct</span></span>.</li>
<li>Farms <span class="gap"><span class="ans" data-s="2">produce</span></span> food.</li>
<li>Reading is a big part of your <span class="gap"><span class="ans" data-s="3">education</span></span>.</li>
</ol>""",
            "Say each sentence with the blank first, and let the class choose before the click shows the word. The "
            "<a href=\"../lists/family-deuk.html\">spelling list</a> has more to build and use.", steps=3)

    D.slide("For teachers", f"""<h2 class="head">For teachers</h2>
<p class="lede">Word sums: e + duc + ate &rarr; <i>educate</i>; e + duc + at(e) + ion &rarr; <i>education</i>; e + duc + at(e) + ion + al &rarr; <i>educational</i>; mis + e + duc + at(e) + ion &rarr; <i>miseducation</i>; pro + duce, pro + duct, re + duct + ion.</p>
<p class="lede">The family follows the Indo-European Lexicon (deuk-), checked against Etymonline; <i>educate</i> is from Latin <i>&emacr;duc&amacr;re</i>, to bring up. The teacher&rsquo;s page is <a href="../roots/deuk.html">*deuk-</a>; the list to print is the <a href="../lists/family-deuk.html">*deuk- spelling list</a>.</p>
<p class="lede">The words with marks are drawn in Legomorphic Notation; the marks are on the <a href="../notations.html">Notations</a> page.</p>""", cls="mid")
    return D


# ------------------------------------------------------------------ *leg-: From *leg- to legomorphics
def leg_deck():
    D = Deck()
    D.slide("Title", f"""<p class="kicker">A word study &middot; <i>*leg-</i></p>
<h1 class="display">Gather, read, say</h1>
<p class="subtitle">from an old word for gather to legomorphics</p>
<div class="pair">{word("legomorphic", 120)}</div>""",
            "A word study for learners. Click, tap, or press the right arrow for each next piece; N shows and hides these notes. "
            "The page for teachers is <a href='../roots/leg.html'>*leg-</a>, with its <a href='../lists/family-leg.html'>spelling list</a>.", "mid")

    D.slide("gather", f"""<h2 class="head"><b class="r">leg</b>: the oldest meaning is <b>gather</b></h2>
{join(["col", "lect"], ["together", "gathered"], word("collect", 150), 1, "To <b>collect</b> is to gather things <b>together</b>.")}""",
            "The root <i>*leg-</i> meant to gather, to collect. Latin made it <i>legere</i>, and after a prefix its past form "
            "is <i>-lectus</i>, which gives English lect: col + lect, where col is con, together, made like the l after it.", steps=4)

    def felt(head, rows, says, note):
        cells = "".join(f'<div data-s="{k + 1}">{word(w, 96)}<span class="g">{g}</span></div>' for k, (w, g) in enumerate(rows))
        D.slide(head, f"""<h2 class="head">{head}</h2>
<div class="fam">{cells}</div>
<p class="q" data-s="{len(rows) + 1}">{says}</p>""", note, steps=len(rows) + 1)

    felt("Gather the ones you want, and you <b class='r'>choose</b>", [("select", "pick out"), ("elect", "choose by voting"), ("collect", "gather together"), ("lesson", "something chosen to learn")],
         "Gathering turns into <b>choosing</b>.",
         "se, apart; e, out (ex before l): select is to gather apart, elect to gather out. Latin used <i>legere</i> for choosing "
         "as well as gathering. <i>Lesson</i> comes up again on the reading road.")
    # Legō itself, at the fork (20 November 2026): the same word went to reading in Latin and to saying in Greek. The
    # gentle senses only; the breath and the bones stay on the teacher's page.
    D.slide("lego: read, say", f"""<h2 class="head">One word, two languages</h2>
<div class="fork">
<div class="top"><span class="lw">leg<b>&omacr;</b></span><span class="g">gather + <b>I</b>: I gather</span></div>
<div><h3 data-s="1">Latin<small>leg&omacr;</small></h3>
<p data-s="1">I pick out<small>footprints, going back the way you came</small></p>
<p data-s="2">I <b class="r">read</b><small>letters, gathered with your eyes</small></p></div>
<div><h3 data-s="3">Greek<small lang="grc">λέγω</small></h3>
<p data-s="3">I count<small>seals on a beach, one by one</small></p>
<p data-s="4">I <b class="r">say</b><small>words, laid out in order</small></p></div>
</div>
<p class="q" data-s="5">The same word: <b>read</b> in Latin, <b>say</b> in Greek.</p>""",
            "Greek and Latin both have <i>leg&omacr;</i>; the &omacr; is the ending for I, as in Latin <i>veto</i>, I forbid. "
            "Virgil uses it for a man picking up his own footprints (<i>Aeneid</i> 9.392&ndash;393); Homer, for the sea god "
            "Proteus counting his seals (<i>Odyssey</i> 4.451). The next two slides follow each road into English. More lines are "
            "in <a href='../roots/leg.html#lego-h'>Leg&omacr; in Latin and in Greek</a>, with the poets&rsquo; uses for the dying, for teachers.", steps=5)
    felt("Gather words with your eyes, and you <b class='r'>read</b>", [("lecture", "a reading, a talk"), ("lesson", "something to read and learn"),
                                                                       ("legend", "a story to be read"), ("legible", "clear enough to read")],
         "In Latin, <b>legere</b> came to mean <b>read</b>.",
         "Latin <i>legere</i>: gather, choose, read. To read is to gather the letters with your eyes. <i>Lecture</i> is lect + ure; "
         "<i>legend</i> is leg + end, Latin <i>legenda</i>, things to be read; <i>legible</i> is leg + ible. The g says j before e and i.")
    felt("Gather words in your mouth, and you <b class='r'>say</b>", [("lexicon", "the words of a language"), ("logic", "words that hold together"),
                                                                      ("dialogue", "talk between people"), ("prologue", "words before the story")],
         "In Greek, <b>legein</b> came to mean <b>say</b>.",
         "Greek <i>leg&omacr;</i>: I gather, I count, I say: to lay words in order. Greek gave <i>lexis</i>, a word, and "
         "<i>logos</i>, a word, an account, reason: lex, log, logue. <i>Dialogue</i> and <i>prologue</i> are set in type: the "
         "site has no checked marks for -logue yet.")

    roads = [("gather, choose", "the root", ["col<b>lect</b>", "se<b>lect</b>", "e<b>lect</b>"]),
             ("read", "Latin <i>legere</i>", ["<b>lect</b>ure", "<b>les</b>son", "<b>leg</b>end", "<b>leg</b>ible"]),
             ("say", "Greek <i>legein</i>", ["<b>lex</b>icon", "<b>log</b>ic", "dia<b>logue</b>", "pro<b>logue</b>"])]
    cols = "".join(f'<div data-s="{k + 1}"><h3>{h}<small>{s}</small></h3>' + "".join(f'<span class="tw2">{w}</span>' for w in ws) + "</div>"
                   for k, (h, s, ws) in enumerate(roads))
    D.slide("Three roads", f"""<h2 class="head">One old word, three roads</h2>
<div class="roads3">{cols}</div>
<p class="q" data-s="4">Gather, choose, read, say: all <b>leg</b>.</p>""",
            "Speakers of Greek and Latin carried the root into words about words: gathering words is choosing them, reading them "
            "and saying them. English borrowed the family again and again, by many roads.", steps=4)

    D.slide("legend", f"""<h2 class="head">A <b class="r">legend</b> is something to read</h2>
{join(["leg", "end"], ["read", "to be"], word("legend", 150), 1,
      "From the end: <b>to be read</b>. On a map, the legend is the key you read to understand the marks.")}""",
            "Medieval Latin <i>legenda</i>, things to be read, first the lives of saints read aloud. Later a legend was also the "
            "words written on a coin or a map, and so the key to a map&rsquo;s marks. This site was called <i>A Legend for "
            "English Words</i> for a week in November 2026.", steps=4)

    D.slide("lesson", f"""<h2 class="head">Words wear down as they travel</h2>
<div class="chain">
<p data-s="1">lectio<small>Latin: a reading</small></p>
<p data-s="2">le&ccedil;on<small>French: the c and t worn away</small></p>
<p data-s="3">{word("lesson", 110)}</p>
</div>
<p class="q" data-s="4">A <b>lesson</b> was first a reading.</p>""",
            "Latin <i>lectio</i>, a reading (lect + ion), became Old French <i>le&ccedil;on</i>, and English <i>lesson</i>. "
            "The spelling no longer shows lect, but the family still holds it: a lesson, a lecture, a lectern to read from.", steps=4)

    D.slide("Build legomorphic", f"""<h2 class="head">Build the notation&rsquo;s name</h2>
{join(["leg", "o", "morph", "ic"], ["gather", "I", "form", "to do with"], word("legomorphic", 140), 1,
      "From the end: <b>to do with</b> the <b>forms I gather</b>. Legomorphic: how sounds and letters gather into words.")}""",
            "Word sum: leg + o + morph + ic &rarr; <i>legomorphic</i>. The o is the ending for I in Greek and Latin alike, so "
            "<i>leg&omacr;</i> is I gather, as Latin <i>veto</i> is I forbid; morph is Greek <i>morph&emacr;</i>, form. The verb in both languages, with the poets&rsquo; lines, is in <a href='../roots/leg.html#lego-h'>Leg&omacr; in Latin and in Greek</a>.", steps=4)

    D.slide("legomorphics", f"""<h2 class="head">Sounds and words, assembled</h2>
<div class="pair" style="margin-top:0">{word("legomorphics", 140)}</div>
<p class="lede" data-s="1">With <b>-s</b>, the name of the study, as in <i>phonics</i> and <i>mathematics</i>.</p>
<p class="q" data-s="2">Gathering sounds into words, and words into sentences: <b>assembling</b> them.</p>""",
            "-ics names a field of study (phonics, mathematics, linguistics). The site&rsquo;s name, <i>Sounds and Words, "
            "Assembled</i>, says the same thing in other words: assemble is another root, <i>*sem-</i>, together.", steps=2)

    D.slide("Not every leg", f"""<h2 class="head">A word that only looks like it</h2>
<p class="typed" style="font-size:90px">LEGO</p>
<p class="lede" data-s="1">The name of the bricks is Danish: <b>leg godt</b>, <b>play well</b>. A different word, from a different place.</p>
<p class="q" data-s="2">But a good picture: pieces that click together to make something new.</p>""",
            "The toy company took its name from Danish <i>leg godt</i>, play well, in the 1930s. Danish <i>lege</i>, to play, "
            "is not from <i>*leg-</i>. Look-alikes are worth naming, so learners test a family by meaning as well as by letters.", steps=2)

    six = ["collect", "select", "lesson", "legend", "lexicon", "legomorphic"]
    D.slide("The family", f"""<h2 class="head">One old word for <b class="r">gather</b>, a family of words</h2>
<div class="fam6">{"".join(f'<div data-s="{k + 1}">{word(w, 84)}</div>' for k, w in enumerate(six))}</div>
<p class="q" data-s="7">Gather, choose, read, say.</p>""",
            "The whole family, with lig and lect taking turns (<i>eligible</i>, <i>elect</i>; <i>intelligent</i>, <i>intellect</i>), "
            "the words the sources hedge (<i>legal</i>, <i>loyal</i>), and <i>prolegomenon</i>, is on the "
            "<a href='../roots/leg.html'>*leg- page</a>.", steps=7)

    D.slide("Your turn", f"""<h2 class="head">Your turn</h2>
<ol class="blanks">
<li>Write so that it is <span class="gap"><span class="ans" data-s="1">legible</span></span>.</li>
<li>We will <span class="gap"><span class="ans" data-s="2">elect</span></span> a class leader.</li>
<li>Today&rsquo;s <span class="gap"><span class="ans" data-s="3">lesson</span></span> is about maps.</li>
</ol>""",
            "Say each sentence with the blank first, and let the class choose before the click shows the word. The "
            "<a href='../lists/family-leg.html'>spelling list</a> has more to build and use.", steps=3)

    D.slide("For teachers", f"""<h2 class="head">For teachers</h2>
<p class="lede">Word sums: col + lect &rarr; <i>collect</i>; se + lect &rarr; <i>select</i>; lect + ure &rarr; <i>lecture</i>; leg + end &rarr; <i>legend</i>; leg + ible &rarr; <i>legible</i>; lex + ic + on &rarr; <i>lexicon</i>; log + ic &rarr; <i>logic</i>; leg + o + morph + ic &rarr; <i>legomorphic</i>.</p>
<p class="lede">The family follows Etymonline and the Indo-European Lexicon on <i>*leg-</i>, with Wiktionary on Greek <i>l&eacute;g&omacr;</i> and Latin <i>leg&omacr;</i>. The teacher&rsquo;s page is <a href="../roots/leg.html">*leg-</a>, where <a href="../roots/leg.html#lego-h">Leg&omacr; in Latin and in Greek</a> follows the verb through the poets, from a last breath to a name read on a tomb; the list to print is the <a href="../lists/family-leg.html">*leg- spelling list</a>.</p>
<p class="lede">The words with marks are drawn in Legomorphic Notation; the marks are on the <a href="../notations.html">Notations</a> page.</p>""", cls="mid")
    return D


def sign_deck():
    """The g in sign (20 November 2026): the classic word of structured word inquiry. The g is silent in sign and said in
    signal; the spelling keeps it, so the family stays visible. Marks follow the ruling of 12 November 2026."""
    D = Deck()
    D.slide("Title", f"""<p class="kicker">A word study &middot; <i>sign</i></p>
<h1 class="display">The g in sign</h1>
<p class="subtitle">sign, signal, signature, design, and the family</p>
<div class="pair">{word("sign", 130)}</div>""",
            "A word study for learners. Click, tap, or press the right arrow for each next piece; N shows and hides these notes. "
            "The page for teachers is <a href='../roots/sign.html'>sign</a>, with its <a href='../lists/family-sign.html'>spelling list</a>.", "mid")

    D.slide("Where's the g?", f"""<h2 class="head">Say it: <b class="r">sign</b></h2>
<div class="pair" style="margin-top:10px">{word("sign", 200)}</div>
<p class="lede" data-s="1">There&rsquo;s a <b>g</b> in it. Can you hear it?</p>
<p class="q" data-s="2">No. So why is it there?</p>""",
            "Let learners say <i>sign</i> slowly and listen for a g. The dotted ring is the cone of silence: a letter that is "
            "there but not said. Hold the question open; the next slides answer it.", steps=2)

    def fam(head, rows, says, note, h=96):
        cells = "".join(f'<div data-s="{k + 1}">{word(w, h)}<span class="g">{g}</span></div>' for k, (w, g) in enumerate(rows))
        D.slide(re.sub(r"<[^>]+>", "", head), f"""<h2 class="head">{head}</h2>
<div class="fam">{cells}</div>
<p class="q" data-s="{len(rows) + 1}">{says}</p>""", note, steps=len(rows) + 1)

    fam("Listen for the <b class='r'>g</b>", [("signal", "a light or a sound that tells you something"), ("signature", "your name, written by you"),
                                             ("signify", "to show, to mean"), ("designate", "to name, to choose")],
        "In these words, you <b>hear</b> the g.",
        "The same part, sign, in every word, and here the g is said. These are the words that keep the g in <i>sign</i>.")

    D.slide("Build signal", f"""<h2 class="head">Build <b class="r">signal</b></h2>
{join(["sign", "al"], ["a mark", "to do with"], word("signal", 150), 1, "From the end: <b>to do with</b> a <b>sign</b>. A signal is a sign that sends a message.")}""",
            "Word sum: sign + al &rarr; <i>signal</i>. Late Latin <i>sign&amacr;le</i>, through French. Say it in syllables: "
            "sig-nal. The g closes the first syllable, so it is said.", steps=4)

    D.slide("Build signature", f"""<h2 class="head">Build <b class="r">signature</b></h2>
{join(["sign", "at(e)", "ure"], ["a mark", "do, make", "what comes of it"], word("signature", 140), 1, "From the end: <b>what comes of making</b> a <b>mark</b>. Your signature is the mark your name makes.")}""",
            "Word sum: sign + at(e) + ure &rarr; <i>signature</i>, from Medieval Latin <i>sign&amacr;t&umacr;ra</i>. The e of -ate "
            "drops before the vowel of -ure, and the t and ure join as they do in <i>picture</i> and <i>nature</i>.", steps=4)

    D.slide("The g keeps the family", f"""<h2 class="head">One part, one spelling</h2>
<div class="duo">
<figure data-s="1">{word("sign", 150)}<figcaption>the g is quiet</figcaption></figure>
<figure data-s="2">{word("signal", 150)}<figcaption>the g is said</figcaption></figure>
</div>
<p class="q" data-s="3">Keep the g, and you can <b>see</b> the family.</p>""",
            "This is the answer to the first question. Written <i>sine</i>, the word would lose its family. Carney calls a letter "
            "like this inert: silent in one word, said in another (<i>A Survey of English Spelling</i>, 1994: 41). The cone keeps "
            "the g in the same place in every word of the family.", steps=3)

    D.slide("Quiet g, long i", f"""<h2 class="head">When the g is quiet, the <b class="r">i</b> says its name</h2>
<div class="pair" style="margin-top:20px" data-s="1">{word("sign", 120)}{word("find", 120)}{word("child", 120)}</div>
<p class="syl" data-s="2" style="margin-top:40px"><span class="hit">sig</span><span class="dot">&middot;</span><span>nal</span></p>
<p class="q" data-s="3">When the g is said, it closes the syllable: <b>sig</b>. The i is short.</p>""",
            "Sign, find, child: the i says its name with no e after it to make it long (Carney&rsquo;s rules I.11 and I.12). In "
            "<i>signal</i> the g closes the syllable and the i is short. Venezky calls this a compensatory alternation: the vowel "
            "is long where the consonant goes quiet.", steps=3)

    D.slide("Build design", f"""<h2 class="head">Build <b class="r">design</b></h2>
{join(["de", "sign"], ["out", "mark"], word("design", 150), 1, "From the end: <b>mark</b> it <b>out</b>. A design is a plan, marked out.")}""",
            "Word sum: de + sign &rarr; <i>design</i>, from Latin <i>d&emacr;sign&amacr;re</i>, to mark out. The g is quiet again: "
            "sign ends the word.", steps=4)

    fam("The g stays <b class='r'>quiet</b>", [("designer", "someone who designs"), ("assign", "to give someone a job"),
                                              ("assignment", "a job you are given"), ("resign", "to give up a job")],
        "The endings <b>-er</b> and <b>-ment</b> don&rsquo;t wake the g up.",
        "English endings after sign leave the g silent: <i>signs</i>, <i>signing</i>, <i>designer</i>, <i>assignment</i>. "
        "<i>Assign</i> is as + sign: Latin <i>ad-</i>, to, written <i>as-</i> before the s, so each part brings its own s. "
        "<i>Resign</i> is re + sign: to sign back, to give up.")

    D.slide("Build signify", f"""<h2 class="head">Build <b class="r">signify</b></h2>
{join(["sign", "i", "fy"], ["a mark", "joins", "make"], word("signify", 140), 1, "From the end: <b>make</b> a <b>sign</b>. To signify is to show, to mean.")}""",
            "Word sum: sign + i + fy &rarr; <i>signify</i>, from Latin <i>signific&amacr;re</i>, to make a sign. The i is a "
            "connecting vowel. Saussure&rsquo;s <i>signifier</i> and <i>signified</i> come from this verb: the sound of a word, and "
            "the idea it stands for.", steps=4)

    fam("The g is <b class='r'>said</b> again", [("significant", "it means something: it matters"), ("designation", "a name or a title"),
                                               ("resignation", "giving up a job"), ("signatory", "someone who signs an agreement")],
        "A <b>Latin</b> ending after sign, and you hear the g.",
        "sign + i + fic + ant; de + sign + at(e) + ion; re + sign + at(e) + ion; sign + at(e) + ory. In <i>designation</i> "
        "and <i>resignation</i> the s says z and the e is short: des-ig-na-tion.", h=88)

    D.slide("The sign matrix", f"""<h2 class="head">The <b class="r">sign</b> matrix</h2>
<div class="matrix">
<div class="mbox" data-s="1"><span>as</span><span>con</span><span>de</span><span>re</span></div>
<div class="mbox mbase">sign</div>
<div class="mcols" data-s="2"><div class="mbox"><span>al</span><span>ate</span><span>er</span><span>ify</span><span>ing</span><span>ment</span><span>s</span></div>
<div class="mbox"><span>ion</span><span>ure</span><span>ory</span></div></div>
</div>
<div class="paths" data-s="3"><span><b>de + sign + er</b></span><span><b>as + sign + ment</b></span><span><b>sign + at(e) + ure</b></span><span><b>re + sign + at(e) + ion</b></span></div>
<p class="q" data-s="4">Read across. Which paths make words?</p>""",
            "The word matrix is Melvyn Ramsden&rsquo;s (Real Spelling); <i>sign</i> is a classic first matrix in Pete Bowers&rsquo;s "
            "structured word inquiry. Read left to right, skipping any box. Not every path is a word (<i>con + sign + al</i>): check "
            "a path by saying it and using it. The last column follows <i>ate</i>.", steps=4)

    D.slide("seal", f"""<h2 class="head">A little sign that lost its g</h2>
<div class="chain">
<p data-s="1">sigillum<small>Latin: a little sign</small></p>
<p data-s="2">seel<small>French: the g worn away</small></p>
<p data-s="3">{word("seal", 110)}</p>
</div>
<p class="q" data-s="4">A <b>seal</b> was a little sign, pressed into wax.</p>""",
            "Latin <i>sigillum</i>, a little sign, wore down in Old French to <i>seel</i>, and English took it without the g. "
            "<i>Sigil</i>, a seal or a sign of power, came straight from Latin and kept it. The sea animal is a different word "
            "altogether, from Old English <i>seolh</i>.", steps=4)

    D.slide("Your turn", f"""<h2 class="head">Your turn</h2>
<ol class="blanks">
<li>Stop at the red <span class="gap"><span class="ans" data-s="1">sign</span></span>.</li>
<li>Write your <span class="gap"><span class="ans" data-s="2">signature</span></span> here.</li>
<li>Wait for the green <span class="gap"><span class="ans" data-s="3">signal</span></span>.</li>
</ol>""",
            "Say each sentence with the blank first, and let the class choose before the click shows the word. Then ask: in "
            "which word is the g quiet? The <a href='../lists/family-sign.html'>spelling list</a> has more to build and use.", steps=3)

    D.slide("For teachers", f"""<h2 class="head">For teachers</h2>
<p class="lede">Word sums: sign + al &rarr; <i>signal</i>; sign + at(e) + ure &rarr; <i>signature</i>; de + sign &rarr; <i>design</i>; de + sign + er &rarr; <i>designer</i>; as + sign + ment &rarr; <i>assignment</i>; sign + i + fy &rarr; <i>signify</i>; sign + i + fic + ant &rarr; <i>significant</i>.</p>
<p class="lede">The g follows Carney and Venezky, as the site ruled on 12 November 2026; Chomsky and Halle used <i>sign</i> and <i>signify</i> for the same point. The root under Latin <i>signum</i> is debated, follow or cut. The teacher&rsquo;s page is <a href="../roots/sign.html">sign</a>, with the root, Saussure&rsquo;s signifier, and the sources; the list to print is the <a href="../lists/family-sign.html">sign spelling list</a>.</p>""", cls="mid")
    return D


DECKS = {"per": per_deck, "education": educ_deck, "leg": leg_deck, "sign": sign_deck}


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
