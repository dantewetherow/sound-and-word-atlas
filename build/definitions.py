"""The Definitions page: the entry that coins legomorphic, with legomorph and legomorphics, then the words the site uses
for sentences, marks and teaching, each saying whether it was coined for the notation or taken from someone, and from
whom.

The definitions of legomorph and legomorphics are Dante Wetherow's of 7 November 2026. The second sense of legomorph
is the one his demonstration paper gives the grammar's primes. Note and the Dialogue Team come from characters.py. Sentence terms follow the About page, the verb cards and
the teaching notes (head, body and legs). The marks come from the legend (KEY in build_site.py), so the two can't drift
apart. The LEGO note follows the LEGO Group's own history page, opened on 7 November 2026.

build_site.py calls write() once every word code is in place, so the example words can be drawn."""
import html, re

PRON = '<span class="pron">/ˌlɛɡoʊˈmɔrfɪk/ <span class="say">leg-oh-MOR-fik</span></span>'
LEGO_PAGE = "https://www.lego.com/en-us/aboutus/lego-history"
ROUTE = '<a href="progressions.html">path</a>'

SENTENCES = [   # (term, part of speech, definition, source or None)
    ("kernel", "noun",
     "The small core a sentence is built from: an actor, an operator and an action, with an acted-on when there is one. "
     "On the " + ROUTE + ", a step's kernel words are the short, frequent words that fill those places first: the forms of "
     "<i>be</i>, <i>have</i> and <i>do</i>, the modals, and verbs like <i>go</i>. Learners over-practise the kernel in claims "
     "and questions, then grow it: <i>She could go. She could go up the hill.</i>",
     "Zellig Harris and Noam Chomsky called a language's simplest sentences its kernel in 1957, the sentences the others "
     "were transformed from. Here the kernel is what's built first, and the rest grows onto it in time."),
    ("actor", "noun",
     "Who or what the sentence is about, usually the one doing the action. In the picture of a sentence as a head, a body "
     "and legs, the actor is the head: <i>she</i> in <i>She could go.</i>", None),
    ("action", "noun",
     "What the actor does: the body, as <i>go</i> is in <i>She could go.</i> A sentence with a form "
     "of <i>be</i> and no other verb, like <i>She is here</i>, has no action.", None),
    ("acted-on", "noun",
     "Who or what the action is done to: the legs, as <i>the note</i> is in <i>She could read the note.</i> "
     "Not every sentence has one. <i>She could go</i> doesn't.", None),
    ("operator", "noun",
     "The first helping verb in a sentence: the word that carries <i>not</i> and moves to the front to make a question, as "
     "<i>could</i> does in <i>She could go</i> and <i>Could she go?</i> Operators are the modals and the forms of "
     "<i>be</i>, <i>have</i> and <i>do</i> that can move to the front, like <i>is</i>, <i>has</i> and <i>did</i>. "
     "<i>Been</i>, <i>being</i> and <i>done</i> never move, so they are never operators.",
     "Adopted from Randolph Quirk, Sidney Greenbaum, Geoffrey Leech and Jan Svartvik, <i>A Comprehensive Grammar of the "
     "English Language</i> (Longman, 1985)."),
    ("modal", "noun",
     "An operator that says how sure, able, allowed or bound the claim is: <i>can, could, will, would, shall, should, may, "
     "might</i> and <i>must</i>. The nine modals are always operators. The semi-modals (<i>have to, ought to, going to, "
     "used to</i>) mean what modals mean but don't move to the front themselves: <i>Do we have to go? Are we going to "
     "go?</i>", None),
    ("query", "noun",
     "A question word: <i>who, what, where, when, why</i> or <i>how</i>. A query asks for more than yes or no, and it comes "
     "before the operator: <i>Where could she go?</i> The name keeps it apart from the operator.", None),
    ("claim", "noun",
     "A sentence that says something is so: <i>She could go. I am.</i>", None),
    ("question", "noun",
     "A sentence that asks. A yes-or-no question puts the operator in front of the actor: <i>Could she go? Am I?</i> A query "
     "question starts with a query: <i>Where could she go?</i>", None),
    ("flip", "noun and verb",
     "Moving the operator across the actor, to turn a claim into a question and back: <i>She could go. Could she go?</i> On "
     "the word cards, the card that moves is outlined.", None),
]

TEACHING = [
    ("learning loop", "noun",
     "The teaching cycle. Learners move among seeing, listening, speaking, reading and writing: a clean pass, then back to "
     "the start, back to any earlier mode, or between any two. A pass can swap a part (a sound, its articulation, an actor, "
     "an action, an operator, a preposition) to fit the learner's need, interest and skill in the moment.",
     "Coined for the notation."),
    ("analog", "noun",
     "A known word used as the model for words that share its spelling: <i>would</i> for <i>could</i> and <i>should</i>. An "
     "analog shares its letters with the words it leads to, which a rhyme doesn't have to do.", None),
    ("path", "noun",
     "This site's scope and sequence: 32 steps through English spelling, with Edward Carney's <i>A Survey of English "
     "Spelling</i> as its backbone. Called the route until 14 November 2026. See <a href=\"progressions.html\">the path</a>.", None),
    ("word sum", "noun",
     "A word written as its morphemes joined by plus signs, with an arrow to the word they make: <i>not(e) + ate &rarr; "
     "notate</i>. A letter in brackets drops at the seam.",
     "Adopted from Melvyn Ramsden's Real Spelling. Pete Bowers brought word sums into classrooms through structured word "
     "inquiry. See <a href=\"credits.html\">Credits</a>."),
    ("copywrite", "noun",
     "The older practice underneath copyright: taking what others have said and written, and writing it again in your own "
     "hand. It's what every learner does on the way to talking, reading and writing, and what this site does with the writers it "
     "builds on.", "Coined for the notation. See <a href=\"credits.html#copywrite\">Credits</a>."),
]

STUDY = [   # words for studying language, each with an everyday word to stand in for it
    ("synchronic", "adjective",
     "Looking at a language as it is at one time, the way it's used now, without its history. A synchronic reading of "
     "<i class=\"nw\">-ion</i> asks what the ending does in the words in use today: <i>action</i>, <i>notation</i>, "
     "<i>explanation</i>. In everyday words, a <b>snapshot</b>.",
     "Adopted from Ferdinand de Saussure, whose <i>Course in General Linguistics</i> (1916) set it against diachronic. From "
     "Greek <i>syn</i>, &ldquo;together,&rdquo; and <i>khronos</i>, &ldquo;time&rdquo;: belonging to the same time."),
    ("diachronic", "adjective",
     "Looking at a language through time, at how its words, sounds and spellings have changed. A diachronic reading of "
     "<i>before</i> finds Old English <i>beforan</i>, where <i>be</i>, &ldquo;by,&rdquo; was joined to <i>foran</i>, "
     "&ldquo;from the front,&rdquo; and finds <i>for</i> and <i>fore</i> growing from one root. In everyday words, a "
     "<b>time-lapse</b>.",
     "Adopted from Ferdinand de Saussure, as synchronic is. From Greek <i>dia</i>, &ldquo;through,&rdquo; and "
     "<i>khronos</i>, &ldquo;time.&rdquo;"),
    ("free", "adjective",
     "Said of a morpheme that can be a word on its own: <i>fun</i> in <i>funny</i>, <i>sun</i> in <i>sunny</i>. A seam "
     "after a free base is easy to see. In everyday words, it <b>stands alone</b>.",
     "Adopted from Leonard Bloomfield, whose <i>Language</i> (1933) set free forms, which can be said alone, against "
     "bound forms, which can&rsquo;t."),
    ("bound", "adjective",
     "Said of a morpheme that is never a word on its own: endings like <i class=\"nw\">-y</i> and <i class=\"nw\">-ness</i>, "
     "and bases that have stopped being said alone, like <i>hap</i> in <i>happy</i> and <i>mishap</i>. A family of words "
     "is what shows a bound base. See <a href=\"roots/hap.html\">hap</a>. In everyday words, it <b>needs a partner</b>.",
     "Adopted from Leonard Bloomfield, as free is."),
]

EXTRA_MARKS = [   # marks the legend doesn't list on its own
    ("Sender", "The letter a vowel vault comes from: a silent <em>e</em>, or a vowel after one consonant, like the <em>a</em> "
     "of <em class=\"nw\">-ate</em>, which sends the <em>o</em> of <em>notate</em> its vault", "notate", "vault"),
    ("Red apostrophe", "A red apostrophe in a contraction, in place of the vowel it drops", "contraction", "apostrophe"),
]


def slug(t): return "def-" + re.sub(r"[^a-z]+", "-", t.lower()).strip("-")


def terms(KEY):
    """Every entry on the page, as (term, anchor), for the site's search."""
    words = [("legomorphic", "def-legomorphic"), ("legomorph", "def-legomorph"), ("legomorphics", "def-legomorphics"),
             ("Legomorphic Notation", "def-legomorphic-notation")]
    rows = [(t, slug(t)) for t, *_ in SENTENCES + TEACHING + STUDY]
    marks = [(n.lower(), slug(n)) for n, *_ in list(KEY) + EXTRA_MARKS]
    return words + rows + marks


def entries(rows):
    out = []
    for term, pos, text, src in rows:
        note = f'<span class="src">{src}</span>' if src else ""
        out.append(f'<div class="def" id="{slug(term)}"><dt>{html.escape(term)} <span class="pos">{pos}</span></dt>'
                   f'<dd>{text}{note}</dd></div>')
    return '<dl class="defs">' + "".join(out) + "</dl>"


def write(OUT, page, header, footer, svg_of, KEY, LW):
    contraction = next((w for w in ("can’t", "don’t", "isn’t", "it’s") if w in LW.W),
                       next((w for w in LW.W if "’" in w), None))
    marks = []
    for name, text, word, mark in list(KEY) + EXTRA_MARKS:      # each mark alone on one word, under its name
        word = contraction if word == "contraction" else word
        drawn = LW.svg_one_mark(word, mark, F=44.0, label=f"{word}, with only its {name.lower()} drawn") if word in LW.W else ""
        marks.append(f'<div class="def mk" id="{slug(name)}"><dt>{html.escape(name.lower())}</dt>'
                     f'<dd><span class="mdraw">{drawn}</span><span class="mtext">{text}.</span></dd></div>')
    marks_html = '<dl class="defs marks-defs">' + "".join(marks) + "</dl>"

    import characters
    unsize = lambda svg: re.sub(r' style="[^"]*"', "", svg, count=1)
    note_marked = unsize(svg_of("note", 64, label="note, marked"))
    note_lifted = characters.lifted(LW, "note", label="Note: note with its letters lifted out")
    team = characters.team(LW)

    body = f"""{header(0)}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">Definitions</p>
<h1>The words of the notation</h1>
<p class="lead">What the words on this site mean here, and where they come from. Each says whether it was coined for the notation or taken from someone else, and from whom.</p>
<p class="toc"><a href="#word">The word</a><a href="#sentences">Sentences</a><a href="#marks">Marks</a><a href="#teaching">Teaching</a><a href="#study">Studying language</a></p>
</div></section>

<section class="about" id="word" aria-labelledby="word-h"><div class="wrap prose">
<h2 id="word-h">The word</h2>
<article class="entry" id="def-legomorphic" aria-label="Dictionary entry: legomorphic">
<p class="hw">leg&middot;o&middot;mor&middot;phic</p>
<p class="line">{PRON} <span class="pos">adjective</span></p>
<ol class="senses">
<li>Having to do with legomorphs: the sounds, meaningful parts, and changes in spelling or sound that words are gathered from. <span class="eg">A legomorphic reading of <i>notation</i> finds the <i>e</i> of <i>note</i> dropped at the seam and its job passed to the <i>a</i> of <i class="nw">-ate</i>.</span></li>
<li>Having to do with legomorphics, the joining of a language's systems through speaking, reading and writing. <span class="eg">Legomorphic Notation; legomorphic teaching.</span></li>
</ol>
<p class="ety"><b>Origin.</b> From <i>legō</i>, a verb Greek and Latin both inherited from the root <a href="roots/leg.html">*leg-</a>, to gather. Greek λέγω (<i>légō</i>) is &ldquo;I gather, I pick out,&rdquo; and so &ldquo;I count, I tell, I say&rdquo;: the speaker&rsquo;s sense. Latin <i>legō</i> is &ldquo;I gather, I choose, I read&rdquo;: the reader&rsquo;s sense. In both, the <i class="nw">-ō</i> is the ending for &ldquo;I,&rdquo; so <i>lego</i> is <i>leg-ō</i>, &ldquo;gather-I,&rdquo; as Latin <i>veto</i> is &ldquo;I forbid.&rdquo; Then Greek μορφή (<i>morphḗ</i>), &ldquo;form, shape,&rdquo; and <i class="nw">-ic</i>, &ldquo;having to do with,&rdquo; from Greek <i class="nw">-ikós</i> through Latin <i class="nw">-icus</i>. Coined by Dante Wetherow for the notation and the study it names.</p>
<p class="usage"><b>Not from the toy.</b> The word isn&rsquo;t named for the LEGO brick, though the building fits. The LEGO Group&rsquo;s name is short for the Danish <i>leg godt</i>, &ldquo;play well&rdquo; (<a href="{LEGO_PAGE}">the LEGO Group&rsquo;s history</a>).</p>
<p class="rel"><b>Related.</b> <a href="#def-legomorph">legomorph</a>, <a href="#def-legomorphics">legomorphics</a>, <a href="#def-legomorphic-notation">Legomorphic Notation</a>. From the same roots: <i>dialogue</i>, <i>lexicon</i>, <i>legible</i>, <i>morpheme</i>. See <a href="about.html#word-h">The word</a> on the About page.</p>
</article>

<dl class="defs">
<div class="def" id="def-legomorph"><dt>legomorph <span class="pos">noun</span> <span class="pron">/ˈlɛɡoʊˌmɔrf/</span></dt>
<dd><ol class="senses">
<li>A phoneme, a morpheme, or a transformation in spelling or sound: the pieces and changes a word is gathered from, and so the things the notation marks. <span class="eg">In <i>note</i> the legomorphs are its three phonemes, its one morpheme, and a transformation: the silent <i>e</i> reaching back to make the <i>o</i> long.</span></li>
<li>In the grammar of legomorphics, a prime: one of the first categories a sentence is assembled from, such as the actor, the action and the acted-on (Latin <i>primus</i>, first).</li>
</ol>
<figure class="mascot"><div class="pair">{note_marked}<span class="to" aria-hidden="true">&rarr;</span>{note_lifted}</div>
<figcaption>Note: <i>note</i> with its letters lifted out and the gap they leave closed, so its legomorphs stand on their own. The three circles are its phonemes, and the vault from the silent <i>e</i> in its cone to the bar over the <i>o</i> is its transformation.</figcaption></figure>
<span class="src">Coined for the notation.</span></dd></div>

<div class="def" id="def-legomorphics"><dt>legomorphics <span class="pos">noun, singular</span> <span class="pron">/ˌlɛɡoʊˈmɔrfɪks/</span></dt>
<dd>The integration of orthography, morphology, phonology, articulation, semantics and syntax through the legomorphic means: speaking, reading and writing, and the syntax of claims and questions. In plainer words, spelling, word parts, sounds, how the mouth makes them, meaning and word order, learned together through talk, reading and writing. Like <i>phonics</i> and <i>linguistics</i>, it takes a singular verb.<span class="src">Coined for the notation.</span></dd></div>

<div class="def" id="def-legomorphic-notation"><dt>Legomorphic Notation <span class="pos">noun</span></dt>
<dd>The marks and colours this site draws on ordinary spelling, so that a word&rsquo;s legomorphs can be seen: its sounds, the letters that spell them, its meaningful parts, and the changes letters make to one another. The marks are listed <a href="#marks">below</a> and drawn in <a href="notations.html#marks">Notations</a>.<span class="src">Coined for the notation.</span></dd></div>
</dl>
</div></section>

<section class="about" id="sentences" aria-labelledby="sent-h"><div class="wrap prose">
<h2 id="sent-h">Sentences</h2>
<p>Every sentence has a head, a body and legs: who or what it&rsquo;s about, what they do, and what they do it to. These are the words for its parts, and for the two things a sentence can do, claim and ask.</p>
{team}
{entries(SENTENCES)}
</div></section>

<section class="about" id="marks" aria-labelledby="marks-h"><div class="wrap prose">
<h2 id="marks-h">Marks</h2>
<p>The marks Legomorphic Notation draws, each on one word with that mark alone. Their names are the notation&rsquo;s own. <a href="notations.html">The marks</a> page has them as a legend.</p>
{marks_html}
</div></section>

<section class="about" id="teaching" aria-labelledby="teach-h"><div class="wrap prose">
<h2 id="teach-h">Teaching</h2>
{entries(TEACHING)}
</div></section>

<section class="about" id="study" aria-labelledby="study-h"><div class="wrap prose">
<h2 id="study-h">Studying language</h2>
<p>Two ways to look at any word: as it is now, or as it has changed. Each comes with an everyday word that can stand in for it.</p>
{entries(STUDY)}
</div></section>
</main>
{footer(0)}"""
    (OUT / "definitions.html").write_text(page("Definitions · A Legend for English Words", body, 0,
                                               "What legomorphic, legomorph and legomorphics mean, and the words the notation uses for sentences, marks and teaching."),
                                          encoding="utf-8")
