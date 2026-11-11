"""A, E, I, O, U and typically Y: a presentation for teachers, made on 10 November 2026 in the manner of ytoi.py,
whose slide vocabulary, styles and script it reuses.

The saying is "a, e, i, o, u and sometimes y". Dante Wetherow's correction is "typically": y spells a vowel nearly
everywhere, and a consonant in one place, at the start of a word or syllable before a vowel. The deck gives a count,
the one consonant place (after Carney, p. 255), the four vowel jobs (alone at the end of a short word, at the end of a
longer word, in a team at the end, and inside words from Greek), how y and i trade places, and a sort to try.

The count was made for this deck from the 20,000 commonest English words in the wordfreq list (Robyn Speer): 2,197
have a y; 75 begin with one; 1,581 end in one. In running text the share that begin with y is higher, about a fifth,
because you, your, year and yes are so common.

Run:  python3 build/aeiouy.py        writes build/sessions/typically-y.html, which sessions.py copies to the site
"""
import pathlib
import ytoi
from ytoi import word, i, slide, SLIDES, FONTS, CSS, JS, HERE

SLIDES.clear()
FILE = "typically-y"
r = lambda s: f'<span class="r">{s}</span>'

# 1 title
slide("Title", f"""<div class="title">
<p class="kicker">Legomorphic Notation &middot; for teachers</p>
<h1 class="display small">A, E, I, O, U<br>and <span class="r">typically</span> Y</h1>
<p class="subtitle">Where y spells a vowel, and the one place it doesn&rsquo;t</p>
<div class="pair">{word("yes", 130)}<span class="gap" style="width:40px"></span>{word("my", 130)}<span class="gap" style="width:40px"></span>{word("happy", 130)}</div>
</div>""", "mid")

# 2 the saying
slide("The saying", f"""<h2 class="head">The saying</h2>
<p class="q np">The vowels are a, e, i, o, u, and sometimes y.</p>
<p class="body" data-s="1">It is true that y does two jobs. The trouble is the word {i("sometimes")}, which makes the vowel job sound like the rare one.</p>
<p class="q" data-s="2">How often is sometimes?</p>""", steps=2)

# 3 the count
slide("A count", f"""<h2 class="head">A count</h2>
<p class="body">Of the 20,000 commonest English words, 2,197 have a y in them.</p>
<table class="sums">
<tr data-s="1"><td>begin with y</td><td>75</td><td class="mis">about 3 in 100</td></tr>
<tr data-s="2"><td>end in y</td><td>1,581</td><td class="mis">about 72 in 100</td></tr>
</table>
<p class="body" data-s="3">A y at the start of a word is the consonant. Nearly every other y is a vowel.</p>
<p class="body" data-s="4">In running text the consonant shows up more, about one y-word in five, because {i("you")}, {i("your")}, {i("year")} and {i("yes")} are so common. The words are few; they are just said a lot.</p>""", steps=4)

# 4 the one place
slide("The one place y is a consonant", f"""<h2 class="head">The one place y is a consonant</h2>
<p class="q np">At the start of a word or a syllable, before a vowel.</p>
<div class="row" data-s="1">{word("yes", 120)}{word("you", 120)}{word("yellow", 120)}{word("your", 120)}</div>
<p class="body" data-s="2">Inside a single word part it is rare: {i("canyon")}, {i("beyond")}. In {i("lawyer")} it starts the ending.</p>
<p class="body" data-s="3">The notation draws this y in black, as a consonant, with a black circle under it.</p>""", steps=3)

# 5 everywhere else
slide("Everywhere else", f"""<h2 class="display small">Everywhere else,<br>y spells a vowel.</h2>
<p class="lede" data-s="1">It has four vowel jobs, and where it sits tells you which.</p>""", "mid", steps=1)

# 6 job 1
slide("Alone at the end of a short word", f"""<h2 class="head">1. Alone at the end of a short word: the name of {i("i")}</h2>
<div class="row">{word("my", 150)}{word("by", 150)}{word("try", 150)}{word("fly", 150)}{word("why", 150)}{word("sky", 150)}</div>
<p class="body" data-s="1">The syllable is open, so the vowel spells its name, as the {i("e")} of {i("me")} and the {i("o")} of {i("go")} do. The y is red, with a long mark.</p>
<p class="body" data-s="2">In a longer word the same y has the stress: {i("reply")}, {i("deny")}, {i("July")}.</p>""", steps=2)

# 7 job 2
slide("At the end of a longer word", f"""<h2 class="head">2. At the end of a longer word: the light sound of {i("happy")}</h2>
<div class="row">{word("happy", 140)}{word("funny", 140)}{word("baby", 140)}{word("very", 140)}{word("only", 140)}</div>
<p class="body" data-s="1">The syllable has no stress, so the y is bare: red, with no mark over it.</p>
<p class="body" data-s="2">Often it is a part of its own, the suffix {i("-y")} or {i("-ly")}: hap + p + y, fun + n + y, on(e) + ly.</p>""", steps=2)

# 8 job 3
slide("In a team at the end", f"""<h2 class="head">3. In a team, where the team ends a word</h2>
<div class="row">{word("play", 130)}{word("they", 130)}{word("key", 130)}{word("boy", 130)}{word("toy", 130)}</div>
<table class="sums" data-s="1">
<tr><td>inside a word</td><td>r{r("ai")}n</td><td>c{r("oi")}n</td><td>v{r("ei")}n</td></tr>
<tr><td>at the end</td><td>r{r("ay")}</td><td>b{r("oy")}</td><td>th{r("ey")}</td></tr>
</table>
<p class="body" data-s="2">In these teams y is the partner of {i("i")}: {i("i")} inside the word, {i("y")} at its end.</p>""", steps=2)

# 9 job 4
slide("Inside a word", f"""<h2 class="head">4. Inside a word, mostly in words from Greek</h2>
<div class="cols3">
<div data-s="1"><p class="sum">short, as {i("i")} in {i("him")}</p>{word("myth", 120)}<p class="body">{i("gym")}, {i("system")}, {i("symbol")}, {i("crystal")}</p></div>
<div data-s="2"><p class="sum">long, as {i("i")} in {i("time")}</p>{word("type", 120)}<p class="body">{i("style")}, {i("cycle")}, {i("hyphen")}, {i("rhyme")}</p></div>
<div data-s="3"><p class="sum">what it shows</p><p class="body">Here y is doing exactly what {i("i")} does, with the same marks. The letter is a sign of where the word came from.</p></div>
</div>""", steps=3)

# 10 y and i trade places
slide("Y and i trade places", f"""<h2 class="head">Y and {i("i")} trade places</h2>
<p class="body">Because they do the same vowel work, one can stand in for the other when a suffix joins.</p>
<table class="sums">
<tr data-s="1"><td>happy + er</td><td>&rarr; {i("happier")}</td><td class="mis">y to i</td></tr>
<tr data-s="1"><td>try + ed</td><td>&rarr; {i("tried")}</td><td class="mis">y to i</td></tr>
<tr data-s="2"><td>die + ing</td><td>&rarr; {i("dying")}</td><td class="mis">i to y</td></tr>
<tr data-s="2"><td>lie + ing</td><td>&rarr; {i("lying")}</td><td class="mis">i to y</td></tr>
</table>
<div class="row" data-s="3">{word("try", 110)}{word("tried", 110)}<span class="gap"></span>{word("happy", 110)}{word("happier", 110)}</div>""", steps=3)

# 11 the test
slide("One test", f"""<h2 class="head">One test, for a reader</h2>
<p class="q np">Is the y at the start of a syllable, with a vowel after it? Then it is a consonant. Anywhere else, it is a vowel.</p>
<p class="body" data-s="1">And for a speller: at the end of a word, where you hear the name of {i("i")} or the light sound of {i("happy")}, write y.</p>""", "mid", steps=1)

# 12 try these
pairs = [("yard", "consonant"), ("sky", "vowel: the name of i"), ("penny", "vowel: the light sound"), ("enjoy", "vowel: in a team"),
         ("myth", "vowel: short, as in him"), ("beyond", "consonant: it starts a syllable"), ("type", "vowel: long, as in time"), ("yawn", "consonant")]
rows = "".join(f'<tr><td>{i(a)}</td><td class="ans" data-s="{k + 1}">{b}</td></tr>' for k, (a, b) in enumerate(pairs))
slide("Try these", f"""<h2 class="head">Try these: consonant or vowel?</h2>
<table class="sums try">{rows}</table>""", steps=len(pairs))

# 13 so
slide("Typically", f"""<h2 class="display small">A, e, i, o, u,<br>and <span class="r">typically</span> y.</h2>
<p class="lede" data-s="1">Y is a vowel letter that also does one consonant job, at the front of a few very common words.</p>""", "mid", steps=1)

# 14 sources
slide("Sources", f"""<h2 class="head">Sources</h2>
<p class="body">Edward Carney, <i>A Survey of English Spelling</i> (Routledge, 1994): y as a consonant is &ldquo;usually found in word-initial position, often in very common&rdquo; words, and only occasionally inside a single word part (<i>canyon</i>), p. 255; long i at the end of a word (<i>my</i>), p. 151; <i>-y</i> and <i>-ies</i>, p. 70; <i>carry</i>, <i>carried</i>, p. 135.</p>
<p class="body">The count was made for this deck from the 20,000 commonest words in the <i>wordfreq</i> list (Robyn Speer). It counts spellings, not sounds: a word that begins with y, and a word that ends in one.</p>
<p class="body">More on y and i at a join is in <a href="y-to-i.html">Y to i at the seam</a>. The marks are on the Sound and Word Atlas&rsquo;s <a href="../notations.html">marks</a> page.</p>
<p class="source">Shared under CC BY-NC-SA 4.0.</p>""", "mid")


def main():
    doc = f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>A, E, I, O, U and typically Y</title>
<meta name="description" content="A presentation for teachers: y spells a vowel nearly everywhere, and a consonant in one place. A count, the one consonant place, the four vowel jobs, and a sort to try.">
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
