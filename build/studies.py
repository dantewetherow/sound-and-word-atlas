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
    "words": ["experiment", "experience", "experimental", "experimentation", "experimenter", "experienced", "inexperienced",
              "experiential"],
    "blurb": "Two long words built from the same parts: <i>ex-</i> (out), <i>per</i> (try), and <i>-ment</i> or <i>-ence</i>. "
             "Read from the end, the parts give the meaning: an experiment is a trying-out. Then a test: is -ment just -ent with "
             "an m? Then the words built on the pair: <i>experimental</i>, <i>experimentation</i>, <i>inexperienced</i>, "
             "<i>experiential</i>. The beat moves and the vowels change; the spelling of each part stays the same.",
}, {
    "slug": "education",
    "title": "From duct to education",
    "sub": "duct, duce, and the words built on them",
    "root": "*deuk-", "root_page": "roots/deuk.html", "list": "lists/family-deuk.html",
    "words": ["duct", "produce", "product", "production", "reduce", "reduction", "conduct", "educate", "education",
              "educational", "educator", "miseducation", "introduce", "introduction", "aqueduct"],
    "blurb": "A duct leads air along, and duce and duct take turns: <i>produce</i>, <i>product</i>. Then <i>ex-</i> becomes "
             "<i>e-</i>, and <i>education</i> is built a part at a time. The e of <i>-ate</i> drops out, and the i of <i>-ion</i> "
             "makes the a long. The study ends with <i>educational</i>, <i>miseducation</i> and where the stress falls.",
}, {
    "slug": "leg",
    "title": "Gather, read, say",
    "sub": "from *leg- to legomorphics",
    "root": "*leg-", "root_page": "roots/leg.html", "list": "lists/family-leg.html",
    "words": ["collect", "collection", "select", "selection", "elect", "election", "lecture", "lesson", "legend", "legendary",
              "legible", "illegible", "lexicon", "lexical", "logic", "logical", "dialogue", "prologue", "catalogue", "dialect",
              "intellect", "intelligent", "eligible", "neglect", "recollect", "legomorphic", "legomorphics", "prolegomenon"],
    "blurb": "One old word for <i>gather</i>, and three meanings: choose (<i>collect</i>, <i>select</i>), read in "
             "Latin (<i>lecture</i>, <i>legend</i>), and say in Greek (<i>lexicon</i>, <i>logic</i>). A lesson "
             "was first a reading. A legend on a map is the key you read. The study builds the notation&rsquo;s own name, "
             "and ends with a look-alike: LEGO, from Danish.",
}, {
    "slug": "sign",
    "title": "The g in sign",
    "sub": "sign, signal, signature, design, and the family",
    "root": "sign", "root_page": "roots/sign.html", "list": "lists/family-sign.html",
    "words": ["sign", "signs", "signing", "signal", "signature", "signatory", "signet", "signify", "significant", "significance",
              "design", "designer", "designate", "designation", "assign", "assignment", "resign", "resignation", "consign",
              "insignia", "seal", "sigil"],
    "blurb": "The classic question: why is there a g in <i>sign</i> when you can&rsquo;t hear it? <i>Signal</i>, <i>signature</i> "
             "and <i>signify</i> sound it, and the spelling keeps the same part in all of them. Then: how the silent g makes the i "
             "long, <i>design</i> as marking out, and the sign matrix. Last, <i>seal</i>: a sign that lost its g.",
}, {
    "slug": "protect",
    "title": "Protect, part by part",
    "sub": "tect and every affix built on it",
    "root": "*(s)teg-", "root_page": "roots/steg.html", "list": "lists/family-steg.html",
    "words": ["protect", "protects", "protected", "protecting", "protection", "protective", "protectively", "protectiveness",
              "protector", "unprotected", "overprotective", "detect", "detective", "detection", "detector", "undetected"],
    "blurb": "<i>Protect</i> is pro + tect: covered in front. Learners sort the family, build it a part at a time, and watch each "
             "word turn into the next. On the way they meet Latin&rsquo;s g turning to c, the three sounds of <i>-ed</i>, and the "
             "t that spells sh in <i>protection</i>. Then the e on <i>-ive</i>, a beat that stays on tect, <i>detect</i>, and "
             "the tect matrix.",
}, {
    "slug": "phonesthemes",
    "title": "Glow, gleam, glitter",
    "sub": "sounds shared by words with related meanings",
    "root": "phonesthemes", "root_page": "lists/phonesthemes.html", "list": "lists/phonesthemes.html",
    "words": ["glow", "gleam", "glitter", "glimmer", "glint", "glisten", "sniff", "snout", "sneeze", "snore", "slide", "slip",
              "slither", "swing", "swirl", "twist", "twirl", "twin", "twelve", "growl", "howl", "scowl", "bash", "crash", "smash",
              "bump", "lump", "clump"],
    "blurb": "Why do <i>glow</i>, <i>gleam</i> and <i>glitter</i> all start with gl-, and <i>sniff</i>, <i>snout</i> and "
             "<i>sneeze</i> with sn-? Learners sort words before anything is explained. They take gl- away to see that it "
             "means nothing alone, and find the words that don&rsquo;t fit. Then they learn that many gl- and tw- words share "
             "an old root. Then they sort again and make up words of their own.",
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



def grow(words, caps, h, start):
    """One word turns into the next in place (24 November 2026). Each click fades in the next word, drawn at the same
    scale and from the same left edge, so the letters the words share stay still and only the new part and its marks
    change. caps: a line under each word. Uses start, start+1, ... for words 2, 3, ..."""
    drawn = [LW.svg_word(w, 100.0, 0.0, cls=False) for w in words]
    W, H = max(d[1] for d in drawn), max(d[2] for d in drawn)
    ds = lambda k: f' data-s="{start + k - 1}"' if k else ""
    svgs = "".join(f'<svg class="mw gw"{ds(k)} viewBox="0 0 {W:.0f} {H:.0f}" style="height:{h}px" role="img" '
                   f'aria-label="{html.escape(w)}, marked">{g}</svg>' for k, (w, (g, _, _)) in enumerate(zip(words, drawn)))
    lines = "".join(f'<span class="gc"{ds(k)}>{c}</span>' for k, c in enumerate(caps))
    return f'<div class="grow">{svgs}</div><div class="grow gcaps">{lines}</div>'


FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..600;1,9..144,400..600&family=Lexend:wght@300;400;500;600&display=swap" rel="stylesheet">
"""

CSS = """
:root{--paper:#ede5d3;--panel:#f4eddd;--line:#dacdb5;--ink:#2b2b2b;--soft:#6b6256;--subject:#3a7d44;--verb:#b5402f;--modal:#3f6488;
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
.wrow{display:flex;flex-wrap:wrap;gap:18px 44px;align-items:flex-end;margin-top:20px}
.wrow.dim{opacity:.5}
.wrow .aside{font-family:var(--serif);font-style:italic;font-size:34px;color:var(--soft);margin:0 0 12px}
.wrow .aside.old{font-family:var(--sans);font-style:normal;font-size:64px;color:var(--ink);margin:0 0 4px}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:40px 80px;margin-top:10px}
.cols2 .lede{margin-top:0}
.sorted{display:grid;gap:8px;margin-top:6px}
.sorted > div{display:flex;align-items:flex-end;gap:30px}
.sorted > div > b{font-size:40px;min-width:120px;color:var(--verb)}
.sorted .wrow{margin-top:0}
.fam > div{display:flex;align-items:flex-end;gap:28px}
.fam .g{font-family:var(--serif);font-style:italic;font-size:34px;color:var(--soft);padding-bottom:12px}
.ishas{display:grid;grid-template-columns:1fr 1fr;gap:10px 80px;margin-top:4px}
.ishas h3{margin:0 0 8px;font-family:var(--sans);font-weight:400;font-size:28px;color:var(--soft);border-bottom:1.5px solid var(--line);padding-bottom:10px}
.ishas h3 b{color:var(--verb);font-weight:500}
.ishas p{margin:0;font-size:50px;line-height:1.25}
.ishas p b{color:var(--verb);font-weight:inherit}
.tri{grid-template-columns:repeat(3,1fr);gap:10px 50px}
.tri p{font-size:46px}
.ladder{grid-template-columns:1fr;gap:22px}
/* one word turning into the next (grow): stacked in one cell; a later word fading in fades the earlier ones out */
.ovr{display:none}   /* weak and borrowed sounds stay hidden in the decks too, while they are checked (23 November 2026) */
.grow{display:grid;justify-items:start;margin-top:6px}
.grow > *{grid-area:1/1;transition:opacity .5s ease}
.grow > .gw:has(~ .in),.grow > .gc:has(~ .in){opacity:0}
.gcaps{margin-top:18px}
.gcaps .gc{font-family:var(--serif);font-style:italic;font-size:42px;color:var(--soft)}
.gcaps .gc b{font-style:normal;color:var(--verb);font-weight:500}
.cloud{display:flex;flex-wrap:wrap;gap:26px 56px;font-size:60px;line-height:1.1;max-width:1300px;margin-top:6px}
.cloud span:nth-child(3n+2){transform:translateY(18px)}
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
.pieces{display:flex;align-items:flex-start;gap:26px;padding-bottom:72px;transition:gap .6s ease}
.pc{position:relative;display:block}
.pc b{display:inline-block;font-weight:500;font-size:110px;line-height:1;padding:10px 26px 18px;border:2px solid var(--line);border-radius:22px;background:var(--panel);transition:border-color .6s ease,background .6s ease,padding .6s ease,border-radius .6s ease}
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

    # -ment and -ent (23 November 2026): two suffixes, not one with an m added. Tested on the slide, not told.
    D.slide("m or no m", f"""<h2 class="head">Is <b>-ment</b> just <b>-ent</b> with an m?</h2>
<p class="lede" data-s="1" style="margin:0 0 22px">An idea to test: the m keeps two vowels apart.</p>
<div class="ishas"><h3>a vowel before it</h3><h3>a consonant before it</h3>
<p data-s="2">agree<b>ment</b></p><p data-s="3">govern<b>ment</b></p>
<p data-s="4">flu<b>ent</b></p><p data-s="5">differ<b>ent</b></p></div>
<p class="lede" data-s="6">-ment comes after both. So does -ent, with no m.</p>
<p class="q" data-s="7"><b>-ment</b> and <b>-ent</b> are two suffixes with two jobs.</p>""",
            "If the m kept two vowels apart, -ment would come only after vowels, and -ent never would. Both come after both. "
            "<i>Experiment</i> and <i>experience</i> settle it: both endings follow the same i. "
            "Latin <i>-mentum</i> made nouns for the means or the result of a verb: <i>mon&emacr;re</i>, to warn, <i>monumentum</i>. "
            "Latin <i>-&emacr;ns</i>, <i>-entis</i> was the present form of a verb, and <i>-entia</i> its noun. "
            "The two look alike in Latin too; their histories are separate.", steps=7)

    D.slide("Build experiment", f"""<h2 class="head">Build it</h2>
{join(["ex", "peri", "ment"], ["out", "try", "the doing"], word("experiment", 150), 1,
      "Read it from the end: <b>the doing</b> of <b>trying</b> it <b>out</b>. An experiment is a trying-out.")}""",
            "Word sum: ex + peri + ment &rarr; <i>experiment</i>. Read from the last part back, the parts give the meaning in "
            "order. The suffix tells you what kind of word it is (a thing, an act). The rest tells you what it is about.", steps=4)
    D.slide("Build experience", f"""<h2 class="head">And the other one</h2>
{join(["ex", "peri", "ence"], ["out", "try", "a thing you have"], word("experience", 150), 1,
      "From the end: <b>what you have</b> from <b>trying</b> things <b>out</b>. Experience is what trying leaves you with.")}""",
            "Word sum: ex + peri + ence &rarr; <i>experience</i>. -ence names, as on the -ence slide: she <i>has</i> experience; "
            "the word that describes her is <i>experienced</i>. In Latin, <i>experientia</i> was the trying and the knowing "
            "that comes of it. English once used the two words almost the same way; French still uses one, <i>exp&eacute;rience</i>, for both.", steps=4)

    # 20 November 2026: the e is long or short by what comes after the i, not by where the syllable breaks (that was
    # circular: the break is chosen from the sound). Some say exPEERiment, as Merriam-Webster allows.
    D.slide("Listen to the e", f"""<h2 class="head">The e is short in one word and long in the other</h2>
<div class="ishas"><h3>i, then a consonant</h3><h3>i, then a vowel</h3>
<p class="typed" style="font-size:80px">exp<b class="r">e</b>r<span class="diff">i</span><b style="color:var(--ink);text-decoration:underline">m</b>ent</p>
<p class="typed" data-s="2" style="font-size:80px">exp<b class="r">e</b>r<span class="diff">i</span><b style="text-decoration:underline">e</b>nce</p>
<p data-s="1" style="font-size:34px;color:var(--soft)">The e is short:<br>ex-<b>PAIR</b>-i-ment</p>
<p data-s="3" style="font-size:34px;color:var(--soft)">The i makes the e long:<br>ex-<b>PEER</b>-i-ence</p>
</div>
<p class="q" data-s="4">Some say ex-<b>PEER</b>-i-ment too: same parts, same spelling.</p>""",
            "An i before a vowel makes the vowel before it long (<i>period</i>, <i>serious</i>); before a consonant it doesn&rsquo;t "
            "(<i>peril</i>, <i>merit</i>). The vault in <i>experience</i> draws it. Merriam-Webster gives ik-SPER-i-ment, also "
            "ik-SPIR-i-ment: mark what the learner says. More on the <a href=\"../roots/per.html#break-h\">teacher&rsquo;s page</a>.", steps=4)

    D.slide("And the i", f"""<h2 class="head">And the i?</h2>
<div class="stack"><p class="typed">exper<span class="diff">i</span>ment</p><p class="typed">exper<span class="diff">i</span>ence</p></div>
<p class="lede" data-s="1">Both words have an i after <b class="r">per</b>. It&rsquo;s left over from the old Latin word.</p>
<p class="q" data-s="2">You can read both words without knowing why the i is there.</p>""",
            "The i is Latin&rsquo;s theme vowel: <i>exper&imacr;r&imacr;</i> is a verb of the class whose stems end in &imacr; "
            "(<i>aud&imacr;re</i>: <i>audience</i>, <i>auditor</i>). It marks the verb&rsquo;s class and carries no meaning. "
            "<i>Expert</i>, from <i>expertus</i>, has none: the root is per. In <i>experience</i> it also does a job in sound, "
            "making the e long. None of this is needed to teach the morphology, phonology, spelling or history here.", steps=2)

    def ladder(head, rows, q, note):
        cells = "".join(f'<div data-s="{k + 1}">{word(w, 92)}<span class="g">{g}</span></div>' for k, (w, g) in enumerate(rows))
        D.slide(head, f"""<h2 class="head">{head}</h2>
<div class="fam ladder">{cells}</div>
<p class="q" data-s="{len(rows) + 1}">{q}</p>""", note, steps=len(rows) + 1)

    ladder("Keep building", [("experimental", "<b>+ al</b>: to do with experiments"),
                             ("experimentation", "<b>+ at(e) + ion</b>: the doing of experiments"),
                             ("experimenter", "<b>+ er</b>: one who does the experiment")],
           "Each ending makes a new kind of word.",
           "Word sums: experiment + al &rarr; <i>experimental</i>; experiment + at(e) + ion &rarr; <i>experimentation</i>; "
           "experiment + er &rarr; <i>experimenter</i>. The e of -ate drops before -ion. "
           "Read from the end: -al describes, -ion names a doing, -er names the one who does it.")

    D.slide("The beat moves", f"""<h2 class="head">Say them. The beat moves.</h2>
<p class="syl" style="font-size:64px;margin:0 0 4px"><span>ex</span><span class="dot">&middot;</span><span class="hit">PER</span><span class="dot">&middot;</span><span>i</span><span class="dot">&middot;</span><span>ment</span></p>
<p class="syl" style="font-size:64px;margin:0 0 4px" data-s="1"><span>ex</span><span class="dot">&middot;</span><span>per</span><span class="dot">&middot;</span><span>i</span><span class="dot">&middot;</span><span class="hit">MEN</span><span class="dot">&middot;</span><span>tal</span></p>
<p class="syl" style="font-size:64px;margin:0 0 4px" data-s="2"><span>ex</span><span class="dot">&middot;</span><span>per</span><span class="dot">&middot;</span><span>i</span><span class="dot">&middot;</span><span>men</span><span class="dot">&middot;</span><span class="hit">TA</span><span class="dot">&middot;</span><span>tion</span></p>
<p class="lede" data-s="3">In <b>experiment</b>, the e of <b class="r">ment</b> is hard to hear.</p>
<p class="lede" data-s="4">In <b>experimental</b>, it&rsquo;s a clear short e.</p>
<p class="q" data-s="5">Not sure of a vowel? Say a longer word in the family.</p>""",
            "-al and -ion pull the stress to the syllable just before them: exPERiment, experiMENtal, experimenTAtion. "
            "The e of ment is weak (a schwa) in <i>experiment</i>. In <i>experimental</i> it is stressed, a short e. "
            "In <i>experimentation</i> people say it both ways (Merriam-Webster). "
            "The spelling is ment in all three, so the word with the stress on that syllable tells you which vowel to write. "
            "The same test works for -ence: <i>experience</i>, <i>experiential</i>.", steps=5)

    ladder("Build on experience", [("experienced", "<b>+ ed</b>: has experience"),
                                   ("inexperienced", "<b>in + &hellip; + ed</b>: not experienced"),
                                   ("experiential", "learned by doing")],
           "experien<b>c</b>e, experien<b>t</b>ial: where does the t come from?",
           "Word sums: experienc(e) + ed &rarr; <i>experienced</i>; in + experienc(e) + ed &rarr; <i>inexperienced</i>; "
           "ex + peri + ent + ial &rarr; <i>experiential</i>. The e at the end of <i>experience</i> drops before -ed. "
           "In <i>experiential</i> the stress lands on en, and the e is a clear short e.")

    rows = [("confid<b>ent</b>", "confid<b>ence</b>", "confid<b>ential</b>"), ("resid<b>ent</b>", "resid<b>ence</b>", "resid<b>ential</b>"),
            ("", "experi<b>ence</b>", "experi<b>ential</b>")]
    cells = "".join("".join(f'<p data-s="{k + 1}">{x}</p>' for x in r) for k, r in enumerate(rows))
    D.slide("c or t", f"""<h2 class="head">A c in one word, a t in the other</h2>
<div class="ishas tri"><h3><b>-ent</b> describes</h3><h3><b>-ence</b> names</h3><h3><b>-ential</b> describes</h3>{cells}</div>
<p class="lede" data-s="4">In <b>-ence</b>, the c spells /s/. In <b>-ential</b>, ti spells /sh/.</p>
<p class="q" data-s="5"><b>-ence</b> and <b>-ential</b> both grow from <b>-ent</b>.</p>""",
            "Latin&rsquo;s present form ended in -ent- (<i>confidens</i>, <i>confidentis</i>). Its noun added -ia "
            "(<i>confidentia</i>), and the describing word -ialis. English spells the noun&rsquo;s end -ence, with c for /s/, and "
            "keeps the t before -ial. English has no <i>experient</i>, but Latin had <i>experiens</i>, so the t is in "
            "<i>experiential</i> all the same. Word sums: confid + ent + ial, resid + ent + ial, ex + peri + ent + ial.", steps=5)

    D.slide("Your turn", f"""<h2 class="head">Your turn</h2>
<ol class="blanks">
<li>We did an <span class="gap"><span class="ans" data-s="1">experiment</span></span> with ice.</li>
<li>Camp was a good <span class="gap"><span class="ans" data-s="2">experience</span></span>.</li>
<li>This plane has an <span class="gap"><span class="ans" data-s="3">experimental</span></span> engine.</li>
<li>The plan was made by an <span class="gap"><span class="ans" data-s="4">inexperienced</span></span> crew.</li>
</ol>""",
            "Say each sentence with the blank first, and let the class choose before the click shows the word. The "
            "<a href=\"../lists/family-per.html\">spelling list</a> has more to build and use.", steps=4)

    D.slide("For teachers", f"""<h2 class="head">For teachers</h2>
<p class="lede">Word sums: ex + peri + ment &rarr; <i>experiment</i>; ex + peri + ence &rarr; <i>experience</i>; experiment + al &rarr; <i>experimental</i>; experiment + at(e) + ion &rarr; <i>experimentation</i>; experiment + er &rarr; <i>experimenter</i>; in + experienc(e) + ed &rarr; <i>inexperienced</i>; ex + peri + ent + ial &rarr; <i>experiential</i>.</p>
<p class="lede">-ment and -ent are two suffixes: Latin <i>-mentum</i> (<a href="https://kaikki.org/dictionary/Latin/meaning/-/-m/-mentum.html">Wiktionary</a>), and the present form <i>-&emacr;ns</i>, <i>-entis</i>, with its noun <i>-entia</i> (Peter Smith, <a href="https://ecampusontario.pressbooks.pub/greeklatinroots/chapter/%C2%A782-english-derivatives-from-latin-present-participles/"><i>Greek and Latin Roots</i>, &sect;82</a>).</p>
<p class="lede">The wider family, with <i>expert</i>, <i>peril</i> and <i>empirical</i>, is on the <a href="../roots/per.html">*per- page</a>, after the Indo-European Lexicon (per- 2e). Words from the root that no longer look related, such as <i>pirate</i> and <i>fear</i>, are on <a href="../surprising.html">Surprising connections</a>.</p>""", cls="mid")
    return D


def per_deck_marked():
    """The words built on experiment and experience have checked codes in the data files; lent to LW.W for this deck."""
    return with_codes(per_deck, ["experimental", "experimentation", "experimenter", "experienced", "inexperienced", "experiential"])


def with_codes(make, words, strict=True):
    """Lend LW.W the codes of words it lacks while make() builds a deck. strict: every word must have a code."""
    import json, gym, pathlib
    from noun_codes import NOUN_CODES
    here = pathlib.Path(__file__).resolve().parent
    pool = json.loads((here / "data" / "auto_codes.json").read_text(encoding="utf-8")); pool.update(NOUN_CODES); pool.update(gym.codes())
    for fn in ("more_codes.json", "family_codes.json"): pool.update(json.loads((here / "data" / fn).read_text(encoding="utf-8")))
    lent = [w for w in set(words) if w not in LW.W and (strict or w in pool)]
    for w in lent:
        assert w in pool, w
        LW.W[w] = pool[w]
    try: return make()
    finally:
        for w in lent: LW.W.pop(w, None)


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
         "The verb is spelled with <b>duce</b>. Add an ending, and it is spelled with <b>duct</b>.",
         "duce is Latin&rsquo;s present form, duct its past form: <i>produce</i>, <i>product</i>, <i>production</i>; "
         "<i>reduce</i>, <i>reduction</i>. The front part tells you which way the leading goes: pro, forward; re, back; "
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
         "When -ion joins -ate, the e drops and the t spells sh: <i>decorate</i>, <i>decoration</i>.")

    D.slide("The i takes over", f"""<h2 class="head">The e drops out. The i takes over its job.</h2>
<div class="fam" style="grid-template-columns:1fr">
<div data-s="1">{word("notate", 120)}<span class="g">the e at the end makes the a spell its name</span></div>
<div data-s="2">{word("notation", 120)}<span class="g">no e now: the i of <b class="r">-ion</b> does the same job</span></div>
</div>
<p class="q" data-s="3">Letters can drop out, and others do their jobs.</p>""",
            "The notation draws it. In <i>notate</i> the vault comes from the final e. In <i>notation</i> the e is gone. The "
            "vault comes from the i of -ion, which stands before another vowel (the pattern on the "
            "<a href=\"../roots/per.html#break-h\">*per- page</a>). The t spells sh before i and a vowel: the green bar under ti.", steps=3)

    D.slide("Build educate", f"""<h2 class="head">Build it</h2>
{join(["e", "duc", "ate"], ["out", "lead, bring up", "do it"], word("educate", 150), 1,
      "Read it from the end: <b>do</b> the <b>bringing up</b>, the leading <b>out</b>. To educate is to bring someone up: to raise and teach them.")}""",
            "Word sum: e + duc + ate &rarr; <i>educate</i>. Latin <i>&emacr;duc&amacr;re</i>, to bring up, to rear, a verb "
            "beside <i>&emacr;d&umacr;cere</i>, to lead out. To educate was first to raise a child. Reading it as leading "
            "out what is in a learner came later, and it fits the parts (the <a href=\"../roots/deuk.html\">*deuk- page</a>).", steps=4)
    D.slide("Build education", f"""<h2 class="head">Name the doing</h2>
{join(["e", "duc", "at(e)", "ion"], ["out", "lead", "do it", "the doing"], word("education", 150), 1,
      "From the end: <b>the doing</b> of <b>bringing up</b> and leading <b>out</b>.")}""",
            "Word sum: e + duc + at(e) + ion &rarr; <i>education</i>. The e of -ate drops before -ion, and the i of -ion takes over "
            "its job, making the a long. The t spells sh.", steps=4)
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
<p class="lede" data-s="3">The beat moves, and the spelling stays the same.</p>
<p class="lede" data-s="4">Many people say <b>ED-ju-cate</b>. The spelling keeps the d of <b class="r">duc</b>.</p>""",
            "-ion pulls the stress to the syllable just before it: EDucate, eduCAtion, eduCAtional. The a is long in all three. "
            "In most speech the d and the u blend into the sound of j, as in <i>gradual</i> and <i>procedure</i>. The spelling "
            "keeps the parts, and the notation has no mark for the blend.", steps=4)

    six = [("duct", "a pipe that leads air"), ("product", "what is made"), ("reduce", "make less"),
           ("conduct", "how you lead yourself"), ("education", "the bringing up"), ("team", "English kept its own: a group pulling together")]
    cells = "".join(f'<div data-s="{k + 1}">{word(w, 84)}<span class="g">{g}</span></div>' for k, (w, g) in enumerate(six))
    D.slide("The family", f"""<h2 class="head">One old word for <b class="r">lead</b>, a family of words</h2>
<div class="fam">{cells}</div>""",
            "<i>Team</i> came down through English, not Latin. In the Germanic languages the root&rsquo;s d became t. "
            "So <i>tug</i>, <i>tow</i>, <i>tie</i> and <i>team</i> start with t where Latin&rsquo;s words start with d. The whole family is on the "
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
            "The root <i>*leg-</i> meant to gather, to collect. Latin made it <i>legere</i>. After a prefix its past form is "
            "<i>-lectus</i>, which gives English lect. In col + lect, col is con, together, changed to match the l after it.", steps=4)

    def felt(head, rows, says, note):
        cells = "".join(f'<div data-s="{k + 1}">{word(w, 96)}<span class="g">{g}</span></div>' for k, (w, g) in enumerate(rows))
        D.slide(head, f"""<h2 class="head">{head}</h2>
<div class="fam">{cells}</div>
<p class="q" data-s="{len(rows) + 1}">{says}</p>""", note, steps=len(rows) + 1)

    felt("Gather the ones you want, and you <b class='r'>choose</b>", [("select", "pick out"), ("elect", "choose by voting"), ("collect", "gather together"), ("election", "a choosing by vote")],
         "Gathering turns into <b>choosing</b>.",
         "se, apart; e, out (ex before l): select is to gather apart, elect to gather out. Latin used <i>legere</i> for choosing "
         "as well as gathering. <i>Election</i> is e + lect + ion: <i>elect</i> is the doing, and -ion names it. "
         "<i>Lesson</i> belongs on the reading road, not here: Latin <i>lectio</i>, a reading.")
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
         "<i>legend</i> is leg + end, Latin <i>legenda</i>, things to be read; <i>legible</i> is leg + ible. The g spells j before e and i.")
    felt("Gather words in your mouth, and you <b class='r'>say</b>", [("lexicon", "the words of a language"), ("logic", "reasons that hold together"),
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
    D.slide("Three roads", f"""<h2 class="head">One old word, three meanings</h2>
<div class="roads3">{cols}</div>
<p class="q" data-s="4">Gather, choose, read, say: all <b>leg</b>.</p>""",
            "Greek and Latin used the root for words about words: gathering words, choosing them, reading them and saying them. "
            "English borrowed from this family many times, from Latin, Greek and French.", steps=4)

    D.slide("legend", f"""<h2 class="head">A <b class="r">legend</b> is something to read</h2>
{join(["leg", "end"], ["read", "to be"], word("legend", 150), 1,
      "From the end: something <b>to be read</b>. On a map, the legend is the key to the marks.")}""",
            "Medieval Latin <i>legenda</i>, things to be read, first the lives of saints read aloud. Later a legend was also the "
            "words written on a coin or a map, and so the key to a map&rsquo;s marks. This site was called <i>A Legend for "
            "English Words</i> for a week in November 2026.", steps=4)

    D.slide("lesson", f"""<h2 class="head">Spellings change when words are borrowed</h2>
<div class="chain">
<p data-s="1">lectio<small>Latin: a reading</small></p>
<p data-s="2">le&ccedil;on<small>French: the c and t dropped out</small></p>
<p data-s="3">{word("lesson", 110)}</p>
</div>
<p class="q" data-s="4">A <b>lesson</b> was first a reading.</p>""",
            "Latin <i>lectio</i>, a reading (lect + ion), became Old French <i>le&ccedil;on</i>, and English <i>lesson</i>. "
            "The spelling no longer shows lect. The meaning still links it to <i>lecture</i> and <i>lectern</i>, a stand to read from.", steps=4)

    D.slide("Build legomorphic", f"""<h2 class="head">Build the notation&rsquo;s name</h2>
{join(["leg", "o", "morph", "ic"], ["gather", "I", "form", "to do with"], word("legomorphic", 140), 1,
      "From the end: <b>to do with</b> the <b>forms I gather</b>. Legomorphic: how sounds and letters gather into words.")}""",
            "Word sum: leg + o + morph + ic &rarr; <i>legomorphic</i>. The o is the ending for I in Greek and Latin alike. So "
            "<i>leg&omacr;</i> is I gather, as Latin <i>veto</i> is I forbid. Morph is Greek <i>morph&emacr;</i>, form. The verb in both languages, with the poets&rsquo; lines, is in <a href='../roots/leg.html#lego-h'>Leg&omacr; in Latin and in Greek</a>.", steps=4)

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
            "The whole family is on the <a href='../roots/leg.html'>*leg- page</a>. It shows lig and lect taking turns "
            "(<i>eligible</i>, <i>elect</i>; <i>intelligent</i>, <i>intellect</i>), the words the sources disagree about "
            "(<i>legal</i>, <i>loyal</i>), and <i>prolegomenon</i>.", steps=7)

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
<p class="lede">The family follows Etymonline and the Indo-European Lexicon on <i>*leg-</i>, with Wiktionary on Greek <i>l&eacute;g&omacr;</i> and Latin <i>leg&omacr;</i>. The teacher&rsquo;s page is <a href="../roots/leg.html">*leg-</a>. Its section <a href="../roots/leg.html#lego-h">Leg&omacr; in Latin and in Greek</a> follows the verb through the poets, from a last breath to a name read on a tomb. The list to print is the <a href="../lists/family-leg.html">*leg- spelling list</a>.</p>
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
{join(["sign", "al"], ["a mark", "to do with"], word("signal", 150), 1, "From the end: something <b>to do with</b> a <b>sign</b>. A signal is a sign that sends a message.")}""",
            "Word sum: sign + al &rarr; <i>signal</i>. Late Latin <i>sign&amacr;le</i>, through French. Say it in syllables: "
            "sig-nal. The g closes the first syllable, so it is said.", steps=4)

    D.slide("Build signature", f"""<h2 class="head">Build <b class="r">signature</b></h2>
{join(["sign", "at(e)", "ure"], ["a mark", "do, make", "what comes of it"], word("signature", 140), 1, "From the end: <b>what comes of making</b> a <b>mark</b>. Your signature is the mark your name makes.")}""",
            "Word sum: sign + at(e) + ure &rarr; <i>signature</i>, from Medieval Latin <i>sign&amacr;t&umacr;ra</i>. The e of -ate "
            "drops before the vowel of -ure, and the t and ure join as they do in <i>picture</i> and <i>nature</i>.", steps=4)

    D.slide("The g keeps the family", f"""<h2 class="head">One part, one spelling</h2>
<div class="duo">
<figure data-s="1">{word("sign", 150)}<figcaption>the g is silent</figcaption></figure>
<figure data-s="2">{word("signal", 150)}<figcaption>the g is said</figcaption></figure>
</div>
<p class="q" data-s="3">Keep the g, and you can <b>see</b> the family.</p>""",
            "This is the answer to the first question. Written <i>sine</i>, the word would lose its family. Carney calls a letter "
            "like this inert: silent in one word, said in another (<i>A Survey of English Spelling</i>, 1994: 41). The cone keeps "
            "the g in the same place in every word of the family.", steps=3)

    D.slide("Silent g, long i", f"""<h2 class="head">When the g is silent, the <b class="r">i</b> spells its name</h2>
<div class="pair" style="margin-top:20px" data-s="1">{word("sign", 120)}{word("find", 120)}{word("child", 120)}</div>
<p class="syl" data-s="2" style="margin-top:40px"><span class="hit">sig</span><span class="dot">&middot;</span><span>nal</span></p>
<p class="q" data-s="3">When the g is said, it closes the syllable: <b>sig</b>. The i is short.</p>""",
            "Sign, find, child: the i spells its name with no e after it to make it long (Carney&rsquo;s rules I.11 and I.12). In "
            "<i>signal</i> the g closes the syllable and the i is short. Venezky calls this a compensatory alternation: the vowel "
            "is long where the consonant is silent.", steps=3)

    D.slide("Build design", f"""<h2 class="head">Build <b class="r">design</b></h2>
{join(["de", "sign"], ["out", "mark"], word("design", 150), 1, "From the end: <b>mark</b> it <b>out</b>. A design is a plan, marked out.")}""",
            "Word sum: de + sign &rarr; <i>design</i>, from Latin <i>d&emacr;sign&amacr;re</i>, to mark out. The g is silent again: "
            "sign ends the word.", steps=4)

    fam("The g stays <b class='r'>silent</b>", [("designer", "someone who designs"), ("assign", "to give someone a job"),
                                              ("assignment", "a job you are given"), ("resign", "to give up a job")],
        "With <b>-er</b> and <b>-ment</b>, the g is still silent.",
        "English endings after sign leave the g silent: <i>signs</i>, <i>signing</i>, <i>designer</i>, <i>assignment</i>. "
        "<i>Assign</i> is as + sign: Latin <i>ad-</i>, to, written <i>as-</i> before the s, so each part brings its own s. "
        "<i>Resign</i> is re + sign: to sign back, to give up.")

    D.slide("Build signify", f"""<h2 class="head">Build <b class="r">signify</b></h2>
{join(["sign", "i", "fy"], ["a mark", "joins", "make"], word("signify", 140), 1, "From the end: <b>make</b> a <b>sign</b>. To signify is to show, to mean.")}""",
            "Word sum: sign + i + fy &rarr; <i>signify</i>, from Latin <i>signific&amacr;re</i>, to make a sign. The i is a "
            "connecting vowel. Saussure&rsquo;s <i>signifier</i> and <i>signified</i> come from this verb: the sound of a word, and "
            "the idea it stands for.", steps=4)

    fam("The g is <b class='r'>said</b> again", [("significant", "full of meaning: it matters"), ("designation", "a name or a title"),
                                               ("resignation", "the giving up of a job"), ("signatory", "someone who signs an agreement")],
        "A <b>Latin</b> ending after sign, and you hear the g.",
        "sign + i + fic + ant; de + sign + at(e) + ion; re + sign + at(e) + ion; sign + at(e) + ory. In <i>designation</i> "
        "and <i>resignation</i> the s spells z and the e is short: des-ig-na-tion.", h=88)

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
<p data-s="2">seel<small>French: the g dropped out</small></p>
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
            "which word is the g silent? The <a href='../lists/family-sign.html'>spelling list</a> has more to build and use.", steps=3)

    D.slide("For teachers", f"""<h2 class="head">For teachers</h2>
<p class="lede">Word sums: sign + al &rarr; <i>signal</i>; sign + at(e) + ure &rarr; <i>signature</i>; de + sign &rarr; <i>design</i>; de + sign + er &rarr; <i>designer</i>; as + sign + ment &rarr; <i>assignment</i>; sign + i + fy &rarr; <i>signify</i>; sign + i + fic + ant &rarr; <i>significant</i>.</p>
<p class="lede">The g follows Carney and Venezky, as the site ruled on 12 November 2026. Chomsky and Halle used <i>sign</i> and <i>signify</i> for the same point. Where Latin <i>signum</i> comes from is debated: a root meaning follow, or one meaning cut. The teacher&rsquo;s page is <a href="../roots/sign.html">sign</a>, with the root, Saussure&rsquo;s signifier, and the sources. The list to print is the <a href="../lists/family-sign.html">sign spelling list</a>.</p>""", cls="mid")
    return D



def phon_deck():
    """Glow, gleam, glitter (21 November 2026): phonesthemes, from Dante's question whether a sound can mean anything on
    its own ("try growling at a cat"). Clusters, evidence and sources are in phonesthemes.py."""
    D = Deck()
    row = lambda ws, h=96, start=1, dim=False: (f'<div class="wrow{" dim" if dim else ""}">' + "".join(
        f'<div data-s="{start + k}">{word(w, h)}</div>' if start else f'<div>{word(w, h)}</div>' for k, w in enumerate(ws)) + "</div>")
    D.slide("Title", f"""<p class="kicker">A word study &middot; phonesthemes</p>
<h1 class="display">Glow, gleam, glitter</h1>
<p class="subtitle">sounds shared by words with related meanings</p>
{row(["glow", "gleam", "glitter"], 120, 0)}""",
            "A word study for learners. Click, tap, or press the right arrow for each next piece; N shows and hides these notes. "
            "The teacher&rsquo;s page is <a href='../lists/phonesthemes.html'>Sound and meaning</a>, with ten clusters to sort and the sources.", "mid")

    mixed = ["glimmer", "sniff", "crash", "swirl", "glint", "snout", "lump", "swoop", "smash", "glow", "sneeze", "bump"]
    D.slide("Sort", f"""<h2 class="head">Sort these into groups</h2>
{row(mixed, 74, 0)}
<p class="q" data-s="1">Any groups you like. <span data-s="2">How did you decide?</span></p>""",
            "Before anything is explained (22 November 2026: the sort comes first, to start the wondering). Say each word and "
            "let learners group them however they like: by sound, by letters, by meaning. Don&rsquo;t confirm or correct yet; "
            "collect their reasons on the board. The class comes back to this pile near the end, with names for what they found.", steps=2)

    D.slide("grr", f"""<h2 class="head">Growl like a dog: <b class="r">grr</b></h2>
<p class="lede" data-s="1">What does it mean?</p>
<p class="q" data-s="2">Most people say anger, or a warning. You can tell from the sound.</p>""",
            "Let the class growl. <i>Grr</i> is an interjection, like <i>shh</i> and <i>ouch</i>: its sound suggests its "
            "meaning. This study is about a related pattern inside ordinary words: groups of words that share a sound and a "
            "meaning.", steps=2)

    D.slide("-owl", f"""<h2 class="head">Words that end in -owl</h2>
{row(["growl", "howl", "yowl", "scowl", "prowl"], 96)}
<p class="q" data-s="6">All five are angry sounds or looks, or creeping up to hunt.</p>
<div class="wrow dim" data-s="7"><div>{word("bowl", 96)}</div><p class="aside">same letters, a different sound: not in the group</p></div>""",
            "-owl: growl, howl, yowl, scowl, prowl, and the owl that hunts at night. <i>Bowl</i> spells the o of <i>snow</i> with "
            "its ow, so it doesn&rsquo;t sound like the others and isn&rsquo;t in the group. A phonestheme is a shared sound; "
            "the spelling usually shows it.", steps=7)

    D.slide("gl-", f"""<h2 class="head">Words that start with gl-</h2>
{row(["glow", "gleam", "glint", "glitter", "glimmer", "glisten"], 92)}
<p class="q" data-s="7">What do they share? <span data-s="8"><b>Light</b>, and seeing.</span></p>""",
            "Every one of these is about light: glow, gleam, glint, glitter, glimmer, glisten. Add glare, glance and glimpse for "
            "seeing. In one count of written English, about 4 in 10 different gl- words had to do with light or seeing, and "
            "6 in 10 of their uses (Bergen 2004).", steps=8)

    D.slide("Take gl away", f"""<h2 class="head">Take the <b class="r">gl</b> away</h2>
<div class="chain">
<p data-s="1">gl + ow<small>ow?</small></p>
<p data-s="2">gl + eam<small>eam?</small></p>
<p data-s="3">gl + itter<small>itter?</small></p>
</div>
<p class="q" data-s="4">What&rsquo;s left means nothing, so gl- is not a morpheme. A shared sound like this is a <b>phonestheme</b>.</p>""",
            "Here is the line between a phonestheme and a morpheme. A word sum needs every part to carry meaning: re + play, "
            "sign + al. With gl-, the rest of the word means nothing, so there is no sum. J. R. Firth named this in 1930: a "
            "<i>phonestheme</i>, from Greek <i>ph&omacr;n&emacr;</i>, sound, and <i>aisth&emacr;ma</i>, what is felt.", steps=4)

    D.slide("Not every gl-", f"""<h2 class="head">Not every <b class="r">gl</b> word</h2>
{row(["glove", "glue", "globe", "glum"], 100)}
<p class="q" data-s="5">Many gl- words are about light. Not all of them are.</p>""",
            "A glove, glue and a globe don&rsquo;t shine. Every cluster has words like these. Showing them keeps learners from treating "
            "the pattern as a rule.", steps=5)

    D.slide("An old family", f"""<h2 class="head">Many gl- light words share a root</h2>
<div class="chain"><p data-s="1">*ghel-<small>a very old word: to shine</small></p></div>
{row(["gleam", "glow", "glass", "gold", "yellow"], 90, 2)}
<p class="q" data-s="7">These words all come from one old root meaning <b>to shine</b>.</p>""",
            "The Indo-European root <i>*ghel-</i>, to shine, is behind gleam, glow, glass, glare, glimmer, glitter and glisten. "
            "It is also behind gold and yellow (Indo-European Lexicon, University of Texas, after Pokorny). So the gl- light words are "
            "partly one word family and partly words that joined the group later.", steps=7)

    D.slide("sn-", f"""<h2 class="head">Words that start with sn-</h2>
{row(["sniff", "snout", "sneeze", "snore", "snort"], 96)}
<p class="q" data-s="6">The <b>nose</b>.</p>
<div class="wrow" data-s="7"><p class="aside old">fnese &rarr;</p><div>{word("sneeze", 90)}</div><p class="aside">the Old English word changed its first sound</p></div>""",
            "<i>Sneeze</i> was <i>fn&emacr;san</i> in Old English, and should have come down as <i>fnese</i>. The fn- dropped "
            "out and sn- took its place, perhaps because sn- suited the nose (Anatoly Liberman, OUPblog, 2019). So a group can "
            "change the spelling of a word that joins it. Snail, snake and snow don&rsquo;t fit.", steps=7)

    D.slide("sl-", f"""<h2 class="head">Words that start with sl-</h2>
{row(["slide", "slip", "slick", "slither", "slush", "slime"], 92)}
<p class="q" data-s="7">Sliding and slipping. <span data-s="8">But <b>sleep</b> and <b>slim</b> are not.</span></p>""",
            "sl- was Firth&rsquo;s own first example. A count of the whole dictionary didn&rsquo;t back it up (Otis and Sagi "
            "2008): there are plenty of sl- words that don&rsquo;t slide. Many readers notice the pattern; the numbers do not support it.", steps=8)

    D.slide("sw- and tw-", f"""<h2 class="head">Words that start with sw- and tw-</h2>
<div class="cols2">
<div><p class="lede" data-s="1"><b>sw-</b>: swinging and sweeping</p>{row(["swing", "sway", "swirl", "swoop"], 84, 2)}</div>
<div><p class="lede" data-s="6"><b>tw-</b>: twisting</p>{row(["twist", "twirl", "twitch", "tweak"], 84, 7)}</div>
</div>""",
            "sw- words name swinging, sweeping or circling movements: swing, sway, sweep, swirl, swoop, swish. tw- words name twisting: twist, twirl, twine, "
            "twitch, tweak. Sweet, swan and swamp don&rsquo;t swing.", steps=10)

    D.slide("tw- and two", f"""<h2 class="head">tw- and <b class="r">two</b></h2>
{row(["two", "twin", "twelve", "twenty", "twice", "twig", "between"], 84)}
<p class="q" data-s="8">These come from the old word for <b>two</b>. <span data-s="9">So does <b>twist</b>: two strands.</span></p>""",
            "Indo-European <i>*dwo-</i>, two, gives two, twin, twelve, twenty, twice, between, and twig (where a branch splits). "
            "<i>Twist</i> and <i>twine</i> are in the family too, as thread of two strands. <i>Twirl</i>, <i>tweak</i> and "
            "<i>twitch</i> share only the sound and a related meaning. <i>Between</i> is be + tween, &ldquo;by two&rdquo;, marked with its seam like <i>before</i> and <i>behind</i>.", steps=9)

    D.slide("-ash and -ump", f"""<h2 class="head">Words that end in -ash and -ump</h2>
<div class="cols2">
<div><p class="lede" data-s="1"><b>-ash</b>: a hard, fast hit</p>{row(["bash", "crash", "smash", "splash"], 84, 2)}</div>
<div><p class="lede" data-s="6"><b>-ump</b>: a rounded lump</p>{row(["bump", "lump", "clump", "stump"], 84, 7)}</div>
</div>
<p class="q" data-s="11">And <b>wash</b>? The w changes the a&rsquo;s sound. It isn&rsquo;t in the group.</p>""",
            "-ash: bash, crash, smash, splash, clash, dash, flash. -ump: bump, lump, clump, stump, plump. Cash and ash don&rsquo;t "
            "hit; jump and pump aren&rsquo;t lumps. In <i>wash</i> the a spells a different sound after w, so it falls out of "
            "the cluster altogether.", steps=11)

    D.slide("In your head?", f"""<h2 class="head">What an experiment found</h2>
<p class="lede" data-s="1">People saw pairs like <b>glitter</b> and <b>glow</b>, then read the second word.</p>
<p class="lede" data-s="2">This was faster than for pairs sharing only letters or meaning.</p>
<p class="q" data-s="3">Readers connect words that share both a sound and a meaning.</p>""",
            "Benjamin Bergen, &ldquo;The psychological reality of phonaesthemes,&rdquo; <i>Language</i> 80 (2004): a priming "
            "test with gl- and sn- pairs. Pairs that shared a phonestheme were read faster than pairs that "
            "shared only letters or only meaning. Otis and Sagi (2008) then counted the whole dictionary: gl-, sn-, sw-, tw-, "
            "str-, -ash and -ump held up; sl- didn&rsquo;t.", steps=3)

    D.slide("Sorted", f"""<h2 class="head">Back to the sort</h2>
<div class="sorted">
<div data-s="1"><b>gl-</b>{row(["glimmer", "glint", "glow"], 64, 0)}</div>
<div data-s="2"><b>sn-</b>{row(["sniff", "snout", "sneeze"], 64, 0)}</div>
<div data-s="3"><b>-ash</b>{row(["crash", "smash"], 64, 0)}</div>
<div data-s="4"><b>sw-</b>{row(["swirl", "swoop"], 64, 0)}</div>
<div data-s="5"><b>-ump</b>{row(["lump", "bump"], 64, 0)}</div>
</div>""",
            "The pile from the start, sorted by phonestheme. Compare it with the groups learners made: who sorted by meaning, who "
            "by letters, and where the two agreed. Then go back to the odd ones: glove, snail, sleep, cash.", steps=5)

    D.slide("Make one up", f"""<h2 class="head">Make one up</h2>
<p class="lede" data-s="1">A <b>glimp</b> is probably&hellip; <span data-s="2"><i>a tiny flash of light</i></span></p>
<p class="lede" data-s="3">A <b>snoffle</b> is probably&hellip; <span data-s="4"><i>a small, quick sniff</i></span></p>
<p class="q" data-s="5">Your turn: a gl- word, an sn- word, an -ash word. What do they mean?</p>""",
            "Made-up words test the pattern: learners often agree on what a <i>glimp</i> might be without being told. People coining "
            "new words follow these clusters too. Keep the words silly, not awkward.", steps=5)

    D.slide("For teachers", f"""<h2 class="head">For teachers</h2>
<p class="lede">A phonestheme is a sound many words with a shared meaning have in common. It isn&rsquo;t a morpheme: the rest of the word means nothing alone, so there is no word sum. It isn&rsquo;t a rule either: every cluster has words with the letters but not the meaning. Some clusters are partly old families (gl- from <i>*ghel-</i>, to shine; tw- from <i>*dwo-</i>, two).</p>
<p class="lede">Sources: J. R. Firth, <i>Speech</i> (1930); Bolinger (1949); Marchand (1959); Bergen, <i>Language</i> 80 (2004); Otis and Sagi (2008); Liberman, OUPblog (2019). The ten clusters, each word marked, are on <a href="../lists/phonesthemes.html">Sound and meaning</a>.</p>""", cls="mid")
    return D

def phon_deck_marked():
    """The clusters' words come from every code source (gym, nouns, rule-made), lent to LW.W for this deck only."""
    import phonesthemes
    return with_codes(phon_deck, set(phonesthemes.words()) | {"gold", "yellow", "two"}, strict=False)


# ------------------------------------------------------------------ *(s)teg-: Protect, part by part (24 November 2026)
def protect_deck():
    """For intermediate readers and spellers: every common affix on tect, and what each does to the sound. The root and
    its other roads are on roots/steg.html; this deck stays with tect."""
    D = Deck()
    D.slide("Title", f"""<p class="kicker">A word study &middot; <i>*(s)teg-</i></p>
<h1 class="display">Protect, part by part</h1>
<p class="subtitle">one part, every affix, and what each does to the sound</p>
<div class="pair">{word("protect", 120)}{word("overprotective", 120)}</div>""",
            "A word study for learners. Click, tap, or press the right arrow for each next piece; N shows and hides these notes. "
            "The page for teachers is <a href=\"../roots/steg.html\">*(s)teg-</a>, with its "
            "<a href=\"../lists/family-steg.html\">spelling list</a>.", "mid")

    sort = ["protection", "unprotected", "protects", "protective", "overprotective", "protector", "protecting", "protectively", "protected"]
    D.slide("What do they share?", f"""<h2 class="head">What do these words share?</h2>
<div class="cloud">{"".join(f"<span>{w}</span>" for w in sort)}</div>
<p class="lede" data-s="1">Find the part they all have.</p>
<p class="q" data-s="2">Then: what changes from word to word?</p>""",
            "Give the class time before anything is explained. Most will find protect quickly. Ask what the rest of each word "
            "adds, and keep their guesses: the slides that follow test them.", steps=2)

    D.slide("Build protect", f"""<h2 class="head">Build it</h2>
{join(["pro", "tect"], ["in front", "covered"], word("protect", 150), 1,
      "Read it from the end: <b>covered</b> in <b>front</b>. To protect is to keep safe.")}""",
            "Word sum: pro + tect &rarr; <i>protect</i>. Latin <i>pr&#x014D;tegere</i>, to cover in front, to shield: "
            "<i>pr&#x014D;</i>, in front, and <i>tegere</i>, to cover.", steps=4)

    def rows2(head, rows, says, note, extra=""):
        cells = "".join(f'<div data-s="{k + 1}"><span class="w">{w}</span><span class="g">{g}</span></div>' for k, (w, g) in enumerate(rows))
        D.slide(head, f"""<h2 class="head">{head}</h2>
<div class="felt" style="grid-template-columns:1fr">{cells}</div>
<p class="q" data-s="{len(rows) + 1}">{says}</p>{extra}""", note, steps=len(rows) + 1)

    rows2("An old word for cover", [("*(s)teg-", "to cover, often with a roof"), ("Latin <b>tegere</b>", "to cover"),
                                    ("Latin <b>tectus</b>", "covered: the part in <i>protect</i>")],
          "<b>tect</b> means <b>covered</b>.",
          "The root is <i>*(s)teg-</i>, to cover (Indo-European Lexicon, after Pokorny; Etymonline). English has words from it by "
          "other roads: <i>thatch</i> and <i>deck</i> (Germanic), <i>tile</i> and <i>toga</i> (Latin), <i>stegosaurus</i> "
          "(Greek <i>stegos</i>, a roof). They are on the <a href=\"../roots/steg.html\">*(s)teg- page</a>. This study stays with tect.")

    D.slide("g to c", f"""<h2 class="head">Why <b class="r">tect</b>, and not <b>teg</b>?</h2>
<p class="lede" data-s="1" style="margin:0 0 22px">Latin&rsquo;s word for cover was <b>tegere</b>, with a g.</p>
<div class="ishas"><h3>with a g</h3><h3>a c before t</h3>
<p data-s="2">te<b>g</b>ere: to cover</p><p data-s="2">pro<b>tect</b>: covered in front</p>
<p data-s="3">le<b>g</b>end</p><p data-s="3">col<b>lect</b></p>
<p data-s="4">re<b>g</b>al</p><p data-s="4">di<b>rect</b></p></div>
<p class="lede" data-s="5">Say /g/, then /k/. Your tongue is in the same place.</p>
<p class="q" data-s="6">Before a t, Latin&rsquo;s g turned into c.</p>""",
            "Latin <i>tegere</i>, <i>tectus</i>; <i>legere</i>, <i>lectus</i>; <i>regere</i>, <i>rectus</i>. Allen and Greenough "
            "give the rule: g before t became c (&sect;15.10). /k/ is /g/ without the voice, and the t that followed has no voice "
            "either. English borrowed the past forms, so the parts are tect, lect and rect.", steps=6)

    D.slide("-s, -ed, -ing", f"""<h2 class="head">Add an ending. Watch the word.</h2>
{grow(["protect", "protects", "protected", "protecting"],
      ["protect", "<b>+ s</b>: does it now", "<b>+ ed</b>: already done", "<b>+ ing</b>: doing it now"], 200, 1)}
<p class="lede" data-s="4">Count the beats: pro-tect, pro-tects, pro-tec-ted, pro-tec-ting.</p>""",
            "Word sums: pro + tect + s, pro + tect + ed, pro + tect + ing. Each word fades into the next at the same size, so "
            "only the new ending and its marks change. Ask which ending adds a syllable.", steps=4)

    D.slide("-ed, three sounds", f"""<h2 class="head"><b class="r">-ed</b>: one spelling, three sounds</h2>
<div class="ishas tri"><h3>/t/: no new syllable</h3><h3>/d/: no new syllable</h3><h3>/id/: a new syllable</h3>
<p data-s="1">jump<b>ed</b></p><p data-s="1">play<b>ed</b></p><p data-s="1">pro&middot;tect&middot;<b>ed</b></p>
<p data-s="2">look<b>ed</b></p><p data-s="2">rain<b>ed</b></p><p data-s="2">de&middot;tect&middot;<b>ed</b></p>
<p data-s="3">help<b>ed</b></p><p data-s="3">fill<b>ed</b></p><p data-s="3">land&middot;<b>ed</b></p></div>
<p class="lede" data-s="4">Listen to the last sound of the word before -ed.</p>
<p class="lede" data-s="5">protect ends in /t/. land ends in /d/.</p>
<p class="q" data-s="6">After /t/ or /d/, -ed is a syllable of its own.</p>""",
            "-ed spells /t/ after a sound made without the voice (p, k, s, f, sh, ch) and /d/ after one made with it, vowels "
            "included. After t or d it adds a syllable, so <i>protected</i> has three. "
            "Spelling these jumpt or playd would lose the ending, and with it the meaning: already done.", steps=6)

    D.slide("Build protection", f"""<h2 class="head">Name the act</h2>
{join(["pro", "tect", "ion"], ["in front", "covered", "the act of"], word("protection", 150), 1,
      "From the end: <b>the act of</b> covering in front. Protection keeps you safe.")}""",
            "Word sum: pro + tect + ion &rarr; <i>protection</i>. A suffix that starts with a vowel joins tect with no change "
            "to its spelling.", steps=4)

    D.slide("The t in protection", f"""<h2 class="head">The t in <b class="r">protection</b> spells /sh/</h2>
{grow(["protect", "protection"], ["the t is said", "<b>ti</b> spells /sh/, and the t stays"], 210, 1)}
<p class="lede" data-s="2">act, action &middot; collect, collection &middot; direct, direction</p>
<p class="q" data-s="3">Spell the part, not the sound: <b>tect + ion</b>.</p>""",
            "Watch the t: a black circle in <i>protect</i>, and a green bar under ti in <i>protection</i>. The green bar "
            "marks one sound spelled with two letters. The t never leaves the spelling, so <i>protection</i> still shows "
            "<i>protect</i>. A learner who writes protecshun has spelled the sound and lost the word.", steps=3)

    def ladder(head, rows, q, note):
        cells = "".join(f'<div data-s="{k + 1}">{word(w, 150)}<span class="g">{g}</span></div>' for k, (w, g) in enumerate(rows))
        D.slide(head, f"""<h2 class="head">{head}</h2>
<div class="fam ladder">{cells}</div>
<p class="q" data-s="{len(rows) + 1}">{q}</p>""", note, steps=len(rows) + 1)

    ladder("Two more endings", [("protective", "<b>+ ive</b>: that protects"), ("protector", "<b>+ or</b>: one who protects")],
           "<b>-or</b> sounds like -er. It marks a Latin ending: actor, collector.",
           "Word sums: pro + tect + ive &rarr; <i>protective</i>; pro + tect + or &rarr; <i>protector</i>. Latin&rsquo;s agent "
           "ending is -or, and words built on Latin parts usually keep it: <i>actor</i>, <i>collector</i>, <i>conductor</i>, "
           "<i>detector</i>. -er is English&rsquo;s own: <i>teacher</i>, <i>painter</i>.")

    D.slide("The e on -ive", f"""<h2 class="head">Why is there an e on <b class="r">-ive</b>?</h2>
<div class="pair" style="margin-top:0">{word("protective", 190, steps=1)}</div>
<p class="lede" data-s="7">The e is silent. The i stays short.</p>
<p class="lede" data-s="8">English words don&rsquo;t end in v: have, give, live, active.</p>
<p class="q" data-s="9">The e is there because the word would end in v.</p>""",
            "The marks come in a layer at a time: the circles, the cup on the short i, then the e that isn&rsquo;t said. The e of -ive makes no vault: the i is short. English spelling avoids a final v, so <i>give</i>, "
            "<i>have</i> and <i>live</i> carry an e that does nothing to the vowel. A few short new words break it, such as "
            "<i>rev</i>.", steps=9)

    D.slide("-ly and -ness", f"""<h2 class="head">Keep going</h2>
{grow(["protective", "protectively", "protectiveness"],
      ["protective", "<b>+ ly</b>: in a protective way", "<b>+ ness</b>: being protective"], 190, 1)}
<p class="lede" data-s="3">-ly and -ness start with a consonant. The e stays.</p>
<p class="q" data-s="4">Before a vowel, the e drops: active, activity.</p>""",
            "Word sums: pro + tect + ive + ly &rarr; <i>protectively</i>; pro + tect + ive + ness &rarr; <i>protectiveness</i>. "
            "The usual rule for a final e: it drops before a suffix that starts with a vowel, as in act + iv(e) + ity &rarr; "
            "<i>activity</i>. It stays before one that starts with a consonant.", steps=4)

    D.slide("un-", f"""<h2 class="head">A part at the front</h2>
{join(["un", "protect", "ed"], ["not", "keep safe", "done"], word("unprotected", 130), 1,
      "<b>un-</b> means <b>not</b>: not protected.")}""",
            "Word sum: un + pro + tect + ed &rarr; <i>unprotected</i>. A prefix joins with no change to either part. The -ed "
            "is still a syllable of its own after the t: un-pro-tec-ted.", steps=4)
    D.slide("over-", f"""<h2 class="head">And another</h2>
{join(["over", "protect", "ive"], ["too much", "keep safe", "that tends to"], word("overprotective", 120), 1,
      "<b>over-</b> means <b>too much</b>: protective, too much.")}""",
            "Word sum: over + pro + tect + ive &rarr; <i>overprotective</i>. One word, no hyphen. Two prefixes now stand before "
            "tect, and each keeps its spelling.", steps=4)

    syl = lambda parts, hit: ('<span class="dot">&middot;</span>'.join(f'<span class="hit">{p.upper()}</span>' if i == hit else f"<span>{p}</span>"
                                                                      for i, p in enumerate(parts)))
    beats = [(["pro", "tect"], 1), (["pro", "tec", "tion"], 1), (["un", "pro", "tec", "ted"], 2), (["o", "ver", "pro", "tec", "tive"], 3)]
    lines = "".join(f'<p class="syl" style="font-size:66px;margin:0 0 6px"{"" if k == 0 else f" data-s={chr(34)}{k}{chr(34)}"}>{syl(p, h)}</p>'
                    for k, (p, h) in enumerate(beats))
    D.slide("The beat", f"""<h2 class="head">Say them. Where is the beat?</h2>
{lines}
<p class="lede" data-s="4">The beat stays on <b class="r">tect</b> every time.</p>
<p class="lede" data-s="5">The o of pro is weak, like the a in about.</p>""",
            "-ion and -ive put the main stress on the syllable just before them, and in this family that syllable is tect "
            "already. So nothing moves, and the vowels hold. Compare <i>experiment</i> and <i>experimental</i> in "
            "<a href=\"per.html\">Try it out</a>, where the beat moves. The o of <i>pro-</i> is clear where pro- has the "
            "stress: <i>prologue</i>, <i>program</i>.", steps=5)

    D.slide("Build detect", f"""<h2 class="head">Take the cover off</h2>
{join(["de", "tect"], ["off, away", "covered"], word("detect", 150), 1,
      "From the end: the cover taken <b>off</b>. To detect is to find out.")}""",
            "Word sum: de + tect &rarr; <i>detect</i>. Latin <i>d&#x0113;tegere</i>, to uncover. A detective was first a "
            "detective police officer: one whose job was finding out.", steps=4)

    D.slide("The detect words", f"""<h2 class="head">The same endings on <b class="r">detect</b></h2>
{grow(["detect", "detective", "detection", "detector"],
      ["detect", "<b>+ ive</b>: one whose job is finding out", "<b>+ ion</b>: the finding out", "<b>+ or</b>: a thing that finds"], 210, 1)}
<p class="lede" data-s="4">The same sound changes come with each ending.</p>""",
            "Word sums: de + tect + ive, de + tect + ion, de + tect + or; and un + de + tect + ed &rarr; <i>undetected</i>. "
            "Ask learners to say which sound changes before you click: the ti of <i>detection</i>, the silent e of "
            "<i>detective</i>.", steps=4)

    D.slide("The tect matrix", f"""<h2 class="head">The <b class="r">tect</b> matrix</h2>
<div class="matrix">
<div class="mbox" data-s="1"><span>un</span><span>over</span></div>
<div class="mbox" data-s="1"><span>pro</span><span>de</span></div>
<div class="mbox mbase">tect</div>
<div class="mcols" data-s="2"><div class="mbox"><span>s</span><span>ed</span><span>ing</span><span>ion</span><span>ive</span><span>or</span></div>
<div class="mbox"><span>ly</span><span>ness</span><span>s</span></div></div>
</div>
<div class="paths" data-s="3"><span><b>un + pro + tect + ed</b></span><span><b>over + pro + tect + ive</b></span><span><b>pro + tect + ive + ness</b></span><span><b>de + tect + or + s</b></span></div>
<p class="q" data-s="4">Read across. Which paths make words?</p>""",
            "The word matrix is Melvyn Ramsden&rsquo;s (Real Spelling), brought into classrooms by Pete Bowers as structured word "
            "inquiry. Read left to right, skipping any box. Not every path is a word (<i>over + de + tect</i>): check each by saying it and using it in a sentence. The last column follows "
            "<i>ive</i> or <i>or</i>.", steps=4)

    D.slide("Your turn", f"""<h2 class="head">Your turn</h2>
<ol class="blanks" style="gap:26px;font-size:48px">
<li>The roof gives <span class="gap"><span class="ans" data-s="1">protection</span></span> from the rain.</li>
<li>The seeds were left <span class="gap"><span class="ans" data-s="2">unprotected</span></span> in the frost.</li>
<li>The case was solved by a <span class="gap"><span class="ans" data-s="3">detective</span></span>.</li>
<li>The smoke <span class="gap"><span class="ans" data-s="4">detector</span></span> beeped.</li>
<li>Put a <span class="gap"><span class="ans" data-s="5">protective</span></span> cover on the book.</li>
</ol>""",
            "Say each sentence with the blank first, and let the class build the word before the click shows it. The "
            "<a href=\"../lists/family-steg.html\">spelling list</a> has more to build and use.", steps=5)

    D.slide("For teachers", f"""<h2 class="head">For teachers</h2>
<p class="lede">Word sums: pro + tect &rarr; <i>protect</i>; pro + tect + ed; pro + tect + ion; pro + tect + ive + ly; pro + tect + ive + ness; pro + tect + or; un + pro + tect + ed; over + pro + tect + ive; de + tect + ive; de + tect + ion; un + de + tect + ed.</p>
<p class="lede">The root and its family follow the <a href="https://lrc.la.utexas.edu/lex/master/1879">Indo-European Lexicon, (s)teg-</a> and <a href="https://www.etymonline.com/word/*(s)teg-">Etymonline</a>. Latin&rsquo;s g before t: <a href="https://dcc.dickinson.edu/grammar/latin/phonetic-changes">Allen and Greenough, &sect;15.10</a>.</p>
<p class="lede">The teacher&rsquo;s page is <a href="../roots/steg.html">*(s)teg-</a>; the list to print is the <a href="../lists/family-steg.html">*(s)teg- spelling list</a>. The marks are on the <a href="../notations.html">Notations</a> page.</p>""", cls="mid")
    return D


def protect_deck_marked():
    """The family's words have checked codes in family_codes.json; lent to LW.W for this deck."""
    return with_codes(protect_deck, ["protect", "protects", "protected", "protecting", "protection", "protective", "protectively",
                                     "protectiveness", "protector", "unprotected", "overprotective", "detect", "detective",
                                     "detection", "detector"])


DECKS = {"per": per_deck_marked, "education": educ_deck, "leg": leg_deck, "sign": sign_deck, "phonesthemes": phon_deck_marked, "protect": protect_deck_marked}


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
<p class="deck-links"><a class="btn" href="studies/{s['slug']}.html">Open the word study</a> <span class="t-only">&middot; for teachers: {f'<a href="{s["list"]}">the {s["root"]} page</a>' if s["root_page"] == s["list"] else f'<a href="{s["root_page"]}">the {s["root"]} page</a> and <a href="{s["list"]}">its spelling list</a>'}</span></p>
</article>""")
    door_page("studies", "Word studies · Sounds and Words, Assembled",
              "Presentations for learners: one family of words per deck, built a part at a time.",
              f"""<section class="hero door-hero"><div class="wrap">
<p class="eyebrow t-only">Words &middot; for learners</p>
<h1>Word studies</h1>
<p class="lead">Presentations for learners, one family of words each. A study builds the words a part at a time: what each part means, how the parts join, and how to read the result.</p>
<p class="sub t-only">Click, tap, or press the right arrow for each next piece; the left third of a slide goes back. N, or the Notes button, opens teacher&rsquo;s notes along the bottom: word sums, history and sources. The button shows when you move the mouse. Each study is linked from its words in the word walk, its root page and its spelling list.</p>
</div></section>
<section class="about"><div class="wrap">
{"".join(cards)}
</div></section>""")
    print(f"wrote studies.html | {len(STUDIES)} word stud{'y' if len(STUDIES) == 1 else 'ies'}")
