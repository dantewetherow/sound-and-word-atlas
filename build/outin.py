"""Out with the old, in with the new: a presentation for teachers, made on 10 November 2026 in the manner of ytoi.py,
whose slide vocabulary, styles and script it reuses.

It rests on Dante Wetherow's name for the convention: when a suffix that starts with a vowel joins a base that ends in
a silent e, the old vowel letter goes and the new one takes its place, and its jobs. It then follows the convention
through stacked suffixes (educate, education, educational; note, notate, notation), since each join in a stack is made
the same way, and ends with the move for a speller or reader: peel the suffixes back from the end, putting each e back.

Words with codes on the site are drawn in the notation; the rest are set in type as word sums, in the site's
convention (a letter in brackets drops at the seam). It sits on step 15 of the route, and its sources are Carney's
pages for that step.

Run:  python3 build/outin.py        writes build/sessions/out-with-the-old.html, which sessions.py copies to the site
"""
import pathlib
import ytoi                                       # runs its own slides; they're cleared below
from ytoi import word, i, slide, SLIDES, FONTS, CSS, JS, HERE

SLIDES.clear()
FILE = "out-with-the-old"
x = lambda s: f'<span class="hl">{s}</span>'       # the letter that goes


def sums(rows, cls=""):
    return f'<table class="sums {cls}">' + "".join(
        f'<tr data-s="{k + 1}"><td>{a}</td><td>&rarr; {i(b)}</td>' + (f'<td class="mis">{c}</td>' if c else "") + "</tr>"
        for k, (a, b, c) in enumerate(rows)) + "</table>"


# 1 title
slide("Title", f"""<div class="title">
<p class="kicker">Legomorphic Notation &middot; for teachers</p>
<h1 class="display small">Out with the old,<br><span class="r">in with the new</span></h1>
<p class="subtitle">What happens when a vowel suffix joins, and joins again</p>
<div class="pair">{word("make", 140)}<span class="op">+ ing &rarr;</span>{word("making", 140)}</div>
</div>""", "mid")

# 2 where it sits
slide("Where it sits", f"""<h2 class="head">Step 15 of the route: the {i("e")} drops, its jobs move</h2>
<p class="body">The words: {", ".join(i(w) for w in ("make, making", "have, having", "race, racing", "ice, icy"))}.</p>
<div class="row" data-s="1">{word("race", 130)}{word("racing", 130)}<span class="gap"></span>{word("ice", 130)}{word("icy", 130)}</div>
<p class="q" data-s="2">Where did the {i("e")} go, and who is doing its work?</p>""", steps=2)

# 3 the convention
slide("The convention", f"""<h2 class="head">The convention</h2>
<p class="q np">When a suffix that starts with a vowel joins a base that ends in a silent {i("e")}, the old vowel letter goes and the new one takes its place.</p>
<p class="body" data-s="1">The {i("e")} isn&rsquo;t lost for nothing. It was doing a job from the end of the word, and the suffix&rsquo;s vowel now stands where it stood.</p>
<p class="body" data-s="2">So the new vowel takes over the job.</p>""", steps=2)

# 4 the jobs move
slide("The jobs move", f"""<h2 class="head">The new vowel does the old one&rsquo;s jobs</h2>
<div class="cols3">
<div data-s="1"><p class="sum">mak{x("e")} + ing</p>{word("making", 110)}<p class="body">The {i("e")} of {i("make")} sent the vault that keeps the {i("a")} long. In {i("making")} the {i("i")} sends it.</p></div>
<div data-s="2"><p class="sum">rac{x("e")} + ing</p>{word("racing", 110)}<p class="body">The {i("e")} of {i("race")} also nudged the {i("c")} soft. The {i("i")} does both.</p></div>
<div data-s="3"><p class="sum">ic{x("e")} + y</p>{word("icy", 110)}<p class="body">A {i("y")} can do it too: it is a vowel letter here.</p></div>
</div>""", steps=3)

# 5 the same join everywhere
slide("The same join, everywhere", f"""<h2 class="head">The same join, in short words and long</h2>
{sums([(f"hop{x('e')} + ing", "hoping", ""), (f"not{x('e')} + ate", "notate", ""), (f"creat{x('e')} + ion", "creation", ""),
       (f"produc{x('e')} + er", "producer", ""), (f"fre{x('e')} + ed", "freed", "not freeed"), (f"se{x('e')} + en", "seen", "not seeen")])}
<p class="body" data-s="6">With {i("ee")}, one {i("e")} goes: English doesn&rsquo;t write three in a row.</p>""", steps=6)

# 6 when the old stays
slide("When the old stays", f"""<h2 class="head">When the old stays</h2>
<div class="cols3">
<div data-s="1"><p class="sum">hope + less &rarr; {i("hopeless")}</p><p class="body">The suffix starts with a consonant. Nothing new arrives to take the {i("e")}&rsquo;s job, so the {i("e")} keeps it.</p></div>
<div data-s="2"><p class="sum">notice + able &rarr; {i("noticeable")}</p><p class="body">The new vowel can&rsquo;t do the job. An {i("a")} doesn&rsquo;t nudge {i("c")} soft, so the {i("e")} stays to do it. {i("Changeable")} keeps its {i("e")} for the {i("g")}.</p></div>
<div data-s="3"><p class="sum">see + ing &rarr; {i("seeing")}</p><p class="body">The {i("e")} is half of a team, {i("ee")}. Drop it and <b>seing</b> would read as {i("ei")}. In {i("being")} the {i("e")} is the base&rsquo;s own vowel.{word("being", 90)}</p></div>
</div>""", steps=3)

# 7 the test
slide("One question", f"""<h2 class="display small">What was the {i("e")} doing,<br>and can the newcomer do it?</h2>
<p class="lede" data-s="1">If it can, the {i("e")} goes. If it can&rsquo;t, or nothing new arrives, the {i("e")} stays.</p>""", "mid", steps=1)

# 8 stacking
slide("Suffixes stack", f"""<h2 class="head">Suffixes stack, and each join is made fresh</h2>
{sums([("e + duc + ate", "educate", ""), (f"e + duc + at{x('e')} + ion", "education", "out once"),
       (f"e + duc + at{x('e')} + ion + al", "educational", "nothing to drop"), (f"e + duc + at{x('e')} + or", "educator", "out once")])}
<p class="body" data-s="4">A long word isn&rsquo;t a long string of letters. It is a short word that has been joined to, more than once, by the same convention each time.</p>""", steps=4)

# 9 note, notate, notation
slide("Out twice", f"""<h2 class="head">Out twice: {i("note")}, {i("notate")}, {i("notation")}</h2>
<div class="row big"><span data-s="1">{word("note", 150)}</span><span class="op" data-s="2">&rarr;</span><span data-s="2">{word("notate", 150)}</span><span class="op" data-s="3">&rarr;</span><span data-s="3">{word("notation", 150)}</span></div>
<p class="sum" data-s="2">not{x("e")} + ate</p>
<p class="sum" data-s="3">not{x("e")} + at{x("e")} + ion</p>
<p class="body" data-s="3">Each time, the vault that kept a vowel long is sent by the newcomer: the {i("a")} of {i("ate")} for the {i("o")}, then the {i("i")} of {i("ion")} for that {i("a")}.</p>""", steps=3)

# 10 longer stacks
slide("Longer stacks", f"""<h2 class="head">Longer stacks</h2>
{sums([(f"pro + duct + iv{x('e')} + ity", "productivity", ""), (f"ac + com + mod + at{x('e')} + ion", "accommodation", ""),
       (f"lect + ur{x('e')} + er", "lecturer", ""), (f"as + simil + at{x('e')} + ion", "assimilation", "")])}
<p class="body" data-s="4">The prefixes stack at the front by their own conventions. The suffixes stack at the back by this one.</p>""", steps=4)

# 11 peel it back
slide("Peel it back", f"""<h2 class="head">The move: peel it back</h2>
<p class="q np">Take the suffixes off from the end, one at a time, and put each {i("e")} back.</p>
<table class="sums">
<tr data-s="1"><td>{i("accommodation")}</td><td>&minus; ion, + e</td><td>&rarr; {i("accommodate")}</td></tr>
<tr data-s="2"><td>{i("productivity")}</td><td>&minus; ity, + e</td><td>&rarr; {i("productive")}</td></tr>
<tr data-s="3"><td>{i("productive")}</td><td>&minus; ive</td><td>&rarr; {i("product")}</td></tr>
</table>
<p class="body" data-s="4">A reader finds a word they know inside the long one. A speller finds where the letters come from.</p>""", steps=4)

# 12 try these
pairs = [("hope + ing", "hoping"), ("hop + ing", "hopping"), ("notice + ing", "noticing"), ("notice + able", "noticeable"),
         ("reduce + ible", "reducible"), ("agree + ed", "agreed"), ("agree + ing", "agreeing")]
rows = "".join(f'<tr><td>{a}</td><td class="ans" data-s="{k + 1}">&rarr; {i(b)}</td></tr>' for k, (a, b) in enumerate(pairs))
slide("Try these", f"""<h2 class="head">Try these</h2>
<p class="body">For each, say what the {i("e")} was doing and whether the newcomer can do it. Then click for the answer.</p>
<table class="sums try">{rows}</table>""", steps=len(pairs))

# 13 a caution
slide("A caution", f"""<h2 class="head">A caution: the parts stay, the sounds move</h2>
<p class="body">Stacking a suffix often moves the stress, and the vowels change with it: <b>ED</b>ucate, edu<b>CA</b>tion. The spelling of each part doesn&rsquo;t change.</p>
<p class="body" data-s="1">So a word sum explains a spelling better than it predicts a pronunciation. That is a reason to teach it for spelling first.</p>
<p class="q end" data-s="2">When a learner writes {i("makeing")}, ask what the {i("e")} was doing, and who is doing it now.</p>""", steps=2)

# 14 sources
slide("Sources", f"""<h2 class="head">Sources</h2>
<p class="body">Edward Carney, <i>A Survey of English Spelling</i> (Routledge, 1994): the <i>e</i> drops before an ending that begins with a vowel, p. 130, and stays where it still nudges <i>c</i> or <i>g</i> (<i>noticeable</i>), p. 131; the <i>e</i> of <i>ee</i> and <i>oe</i> stays before <i>i</i> (<i>seeing</i>, <i>canoeing</i>), so that <i>ei</i> and <i>oi</i> aren&rsquo;t read, p. 131.</p>
<p class="body">The histories of the words are in Etymonline. The families are on the Sound and Word Atlas: <a href="../roots/deuk.html">*deuk-</a> for <i>educate</i> and <i>produce</i>, <a href="../roots/med.html">*med-</a> for <i>accommodate</i>, and <a href="../parts.html">Parts</a> for every word with each suffix. This is <a href="../steps/15.html">step 15</a> of its route.</p>
<p class="source">Shared under CC BY-NC-SA 4.0.</p>""", "mid")


def main():
    doc = f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Out with the old, in with the new</title>
<meta name="description" content="A presentation for teachers: when a vowel suffix joins, the silent e goes and the new vowel takes its jobs; and how suffixes stack, one join at a time.">
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
{JS.replace('"deck:y-to-i"', f'"deck:{FILE}"')}
</body>
</html>
"""
    out = pathlib.Path(HERE) / "sessions" / f"{FILE}.html"
    out.write_text(doc, encoding="utf-8")
    print("wrote", out, f"| {len(SLIDES)} slides | {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
