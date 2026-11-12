"""The About page (the word legomorphic and what the notation does) and the Credits page (sources, copyright, the
idea of copywrite, and contact).

build_site.py calls write() with its page, header, footer and svg_of functions. The etymology follows the Online
Etymology Dictionary's entries for *leg- and morphology, opened on 6 November 2026. The marks are described as the site's
legend gives them. The copyright holder, the licence and the contact address are the author's choices of 6 November 2026.
The site is static, so contact is a mail link: the address is put together in the page, which keeps it out of the HTML
that address harvesters read.

The wordmark, λέγω · morphic, stands beside the etymology. logo.py draws it from the fonts into build/wordmark.svg (the
fonts are not in the repository), and this draws it into the page with the site's colours, as every marked word on the
site is drawn, so it follows the page between bright and night. As an image it took its colours from the device instead,
and showed black Greek on a black page where the two disagreed."""
import pathlib, re
HERE = pathlib.Path(__file__).resolve().parent

HOLDER = "Dante Wetherow, B.Ed., M.Ed."
LICENCE = ('<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike '
           '4.0 International licence</a> (CC BY-NC-SA 4.0)')
CONTACT = """<p class="contact"><a class="btn" id="contact" href="#contact-note">Email Dante Wetherow</a></p>
<p class="sub" id="contact-note">It opens a new message in your email app.<noscript> Write to dante.wetherow at sd23.bc.ca.</noscript></p>
<script>(() => { const a = document.getElementById('contact'); const u = ['dante', 'wetherow'].join('.'), d = ['sd23', 'bc', 'ca'].join('.');
  a.href = 'mailto:' + u + '@' + d + '?subject=' + encodeURIComponent('A Legend for English Words'); })();</script>"""

EXAMPLES = [("could", "A red bond bar under <i>oul</i>, the letters that spell its vowel sound."),
            ("like", "The silent <i>e</i> sits in its cone, and its vault reaches back to make the <i>i</i> long."),
            ("nice", "The same vault, and a nudge from the <i>e</i> softens the <i>c</i>."),
            ("funny", "The box around <i>nn</i> stops the <i>y</i> from reaching back, so the <i>u</i> stays short.")]


SITE_COLOURS = {'class="k"': 'fill="var(--ink)"', 'class="r"': 'fill="var(--verb)"',
                'class="k st"': 'fill="none" stroke="var(--ink)"', 'class="r st"': 'fill="none" stroke="var(--verb)"',
                'class="b st"': 'fill="none" stroke="var(--modal)"', 'class="b seam"': 'fill="none" stroke="var(--modal)"',
                'class="q st"': 'fill="none" stroke="var(--soft)"'}


def in_site_colours(name):
    """A file logo.py drew, ready to draw into a page: its own colour rules out, the site's colours in, so it follows
    the page between bright and night."""
    s = re.sub(r"<style>.*?</style>\n?", "", (HERE / name).read_text(encoding="utf-8"), flags=re.S)
    for cls, paint in sorted(SITE_COLOURS.items(), key=lambda kv: -len(kv[0])):    # the two-class names first
        s = s.replace(cls, paint)
    assert "class=" not in s, f"{name} has a class the page doesn't colour"
    return s


def wordmark():
    s = in_site_colours("wordmark.svg")
    s = s.replace('aria-label="Legomorphic Notation: λέγω, morphic. Language, form, meaning"',
                  'aria-label="The wordmark: λέγω · morphic, over the words language, form, meaning"')
    return (f'<figure class="wordmark">{s}'
            f'<figcaption>λέγω marked as the notation marks English: a circle under each sound, red for the vowels, a swoop '
            f'under each syllable (λέ and γω), and a seam where the stem λεγ- meets the ending -ω, &ldquo;I.&rdquo; The seam '
            f'falls inside a syllable, as it does in <i>making</i>.</figcaption></figure>')


def write(OUT, page, header, footer, svg_of, LW):
    import characters
    mark = wordmark()
    gno = characters.lifted(LW, "gno", label="Gno, the notation's mascot: gno with its letters lifted out", scale=1.2)
    examples ="".join(f'<figure class="ex">{svg_of(w, 56)}<figcaption>{cap}</figcaption></figure>' for w, cap in EXAMPLES)
    about = f"""{header(0)}
<main>
<section class="hero"><div class="wrap about-hero">
<div>
<p class="eyebrow">About</p>
<h1>Legomorphic Notation</h1>
<p class="lead">A set of marks and colours drawn on ordinary spelling, so that what a reader usually has to work out alone is there for everyone to see: how many sounds a word has, which letters spell each sound, where its meaningful parts join, and which letters change the sounds of others.</p>
</div>
<figure class="mascot-hero"><a href="definitions.html#def-legomorph">{gno}</a><figcaption>Gno, the notation&rsquo;s mascot: <i>gno</i> with its letters lifted out, gn under one black bar and o spelling its name. His bar is cut short, for a brow.</figcaption></figure>
</div></section>

<section class="about" aria-labelledby="word-h"><div class="wrap prose">
<h2 id="word-h">The word</h2>
<p><i>Legomorphic</i> is built from two old words, a word for gathering and a word for shape.</p>
{mark}
<p><i>Lego</i> is the same word in Greek and in Latin, and in both it means &ldquo;I gather.&rdquo; Greek <i>legō</i> (λέγω) first meant to pick out, to gather and to count, and from picking out words it came to mean to say and to tell. Latin <i>legō</i> (<i>legere</i>) means to gather and to choose, and also to read. The root gives a speaker&rsquo;s word in Greek and a reader&rsquo;s word in Latin, and <i>legomorphic</i> takes both. In both languages the <i>ō</i> is the ending for &ldquo;I&rdquo;: <i>leg-ō</i>, &ldquo;gather-I,&rdquo; as Latin <i>veto</i> is &ldquo;I forbid.&rdquo; So the notation puts a seam on each side of the <i>o</i>: <i>leg + o + morph + ic</i>.</p>
<p>English has both families. From the Greek come <i>lexicon</i>, <i>dialogue</i> and <i>logic</i>; from the Latin, <i>legible</i>, <i>lecture</i>, <i>collect</i> and <i>select</i>. Linguists trace them all to a Proto-Indo-European root, written *leg-, to collect or gather.</p>
<p><i>Morphē</i> (μορφή) is Greek for form or shape. It gives us <i>morpheme</i>, and <i>morphology</i>, the study of word forms, which joins the same two roots the other way round.</p>
<p>So the notation is named for the shapes words take when we gather them: the sounds we pick out and say, the letters we pick out and read, and the parts they build together.</p>
<p>The site is called <i>A Legend for English Words</i> after the other sense of <i>legend</i>: the key on a map that tells you how to read it. The word is Latin <i>legenda</i>, things to be read, from <i>legere</i>, so it comes from the same root as the notation. The notation is a legend in that sense: it doesn&rsquo;t claim to have mapped every word, but gives the key for reading the one in front of you. The light in the subtitle is another root, <a href="roots/leuk.html"><i>*leuk-</i></a>, the one in <i>illustrate</i> and <i>illuminate</i>.</p>
<p>The dictionary entry for <i>legomorphic</i>, with <i>legomorph</i> and <i>legomorphics</i>, is on the <a href="definitions.html">Definitions</a> page.</p>
<p class="sub">Etymologies from the Online Etymology Dictionary: <a href="https://www.etymonline.com/word/*leg-">*leg-</a> and <a href="https://www.etymonline.com/word/morphology">morphology</a>.</p>
</div></section>

<section class="about" aria-labelledby="shows-h"><div class="wrap prose">
<h2 id="shows-h">What it shows</h2>
<p>The notation explores four systems at once: orthography, phonology, morphology and syntax. It works through graphemes, phonemes and morphemes, and through the order in time in which a message is put together.</p>
<p>In a word, vowel letters are red, even inside a unit (the <i>u</i> of <i>buy</i>), consonant letters black, and <i>sh</i>, <i>th</i> and <i>ch</i> green. The marks fall into three groups.</p>
<ul class="marks-list">
<li><b>Sounds.</b> A sound circle under each sound, a bond bar under letters that work as one unit, a cup or a bar over a vowel for short or long, and a red bar under a vowel and its <i>r</i>.</li>
<li><b>Parts.</b> A syllable swoop under each syllable, and a morpheme seam between meaningful parts.</li>
<li><b>Letters working on letters.</b> The vowel vault, an arc from an <i>e</i>, or from a vowel after a single consonant, back to the vowel it makes long. The block box, around a pair or cluster of consonants that stops that reach, and the blocked vault, which ends in a red X where it does. The cone of silence around a silent <i>e</i>, and the nice-nudge from <i>e</i>, <i>i</i> or <i>y</i> to the <i>c</i> or <i>g</i> it softens.</li>
</ul>
<p>Contractions take a red apostrophe in place of the vowel they drop.</p>
<div class="examples">{examples}</div>
<p>In a sentence, the parts are named for their jobs: the actor, the operator, the action and the acted-on. The operator is the word that can move to the front to make a question. <a href="definitions.html#sentences">Definitions</a> has each of them, and <a href="notations.html#marks">Notations</a> has the legend, with a drawing of each mark.</p>
</div></section>

<section class="about" aria-labelledby="use-h"><div class="wrap prose">
<h2 id="use-h">How it&rsquo;s used</h2>
<p>It isn&rsquo;t a program. It&rsquo;s an exploration of ways to provide access, and an invitation to experiment with our methods and synthesize our understandings. It can sit beside any systematic phonics program, synthetic or analytic, and it aims to be systematic, analytic, synthetic, responsive, diagnostic and agnostic.</p>
<p>Its teaching cycle is the learning loop. Learners move among seeing, listening, speaking, reading and writing: a clean pass, then back to the start, back to any earlier mode, or between any two. Each pass can swap a part (a sound, its articulation, an actor, an action, an operator, a preposition) to fit the learner&rsquo;s need, interest and skill in the moment.</p>
<p>The <a href="progressions.html">route</a> through English spelling on this site is its own scope and sequence, with Edward Carney&rsquo;s <i>A Survey of English Spelling</i> as its backbone and his page references on every step.</p>
</div></section>

<section class="about" aria-labelledby="who-h"><div class="wrap prose">
<h2 id="who-h">Who made it</h2>
<p>Legomorphic Notation and this site are the work of {HOLDER} The writers it builds on are on the <a href="credits.html">Credits</a> page.</p>
{CONTACT}
</div></section>
</main>
{footer(0)}"""
    (OUT / "about.html").write_text(page("About Legomorphic Notation · A Legend for English Words", about, 0,
                                         "What Legomorphic Notation is, where the word comes from, and how it's used."), encoding="utf-8")

    credits = f"""{header(0)}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">Credits</p>
<h1>Credits and copyright</h1>
<p class="lead">Legomorphic Notation stands on other people&rsquo;s work. These are the writers it draws on, and the terms for using what&rsquo;s here.</p>
</div></section>

<section class="about" aria-labelledby="sp-h"><div class="wrap prose">
<h2 id="sp-h">Spelling and words</h2>
<ul class="credits">
<li><b>Edward Carney</b>, <i>A Survey of English Spelling</i> (Routledge, 1994). The backbone of the route, cited by page on every step.</li>
<li><b>Richard Venezky</b>, &ldquo;English Orthography: Its Graphical Structure and Its Relation to Sound,&rdquo; <i>Reading Research Quarterly</i> 2 (1967), and <i>The Structure of English Orthography</i> (Mouton, 1970). Spelling as a system, including the letters that mark how other letters are read, such as a silent <i>e</i>: the job the vault, the nudge and the cone show. His later book is <i>The American Way of Spelling</i> (Guilford, 1999).</li>
<li><b>Greg Brooks</b>, <i>Dictionary of the British English Spelling System</i> (Open Book Publishers, 2015), open access (<a href="https://doi.org/10.11647/OBP.0053">doi</a>). Every spelling of every sound, with its frequency and its exceptions. A doubled letter spells one sound, and <i>happy</i> is among his doubled p&rsquo;s, on the <a href="roots/hap.html">hap</a> page.</li>
<li><b>Noam Chomsky and Morris Halle</b>, <i>The Sound Pattern of English</i> (Harper &amp; Row, 1968). Their argument that English spelling keeps a word&rsquo;s parts the same when their sounds change, as in <i>sign</i> and <i>signature</i>, is the premise word sums rest on.</li>
<li><b>Carol Chomsky</b>, &ldquo;Reading, Writing, and Phonology,&rdquo; <i>Harvard Educational Review</i> 40, no. 2 (1970): 287&ndash;309 (<a href="https://doi.org/10.17763/haer.40.2.y7u0242x76w05624">doi</a>). She carried that morphophonemic view of spelling into teaching learners to read and write.</li>
<li><b>Melvyn Ramsden</b>, whose <a href="http://www.realspelling.com/">Real Spelling</a> gave us word sums and word matrices, the basis of the grade 3 word sum cards. His book is <i>Rescuing Spelling</i> (Southgate Publishers).</li>
<li><b>Pete Bowers</b>, who brought word sums and matrices into classrooms as structured word inquiry. His book is <i>Teaching How the Written Word Works</i>. With John R. Kirby and S. H&eacute;l&egrave;ne Deacon he wrote &ldquo;The Effects of Morphological Instruction on Literacy Skills: A Systematic Review of the Literature,&rdquo; <i>Review of Educational Research</i> 80, no. 2 (2010) (<a href="https://doi.org/10.3102/0034654309359353">doi</a>), and with Jeffrey Bowers, &ldquo;Beyond Phonics: The Case for Teaching Children the Logic of the English Spelling System,&rdquo; <i>Educational Psychologist</i> 52, no. 2 (2017): 124&ndash;141 (<a href="https://doi.org/10.1080/00461520.2017.1288571">doi</a>).</li>
<li><b>Sue Scibetta Hegland</b>, <i><a href="https://shop.thereadingleague.org/products/beneath-the-surface-of-words-what-english-spelling-reveals-and-why-it-matters">Beneath the Surface of Words: What English Spelling Reveals and Why It Matters</a></i> (Learning About Spelling).</li>
<li><b>E. W. Dolch</b>, &ldquo;A Basic Sight Vocabulary,&rdquo; <i>The Elementary School Journal</i> 36, no. 6 (1936): 456&ndash;460. The Dolch cards and the <a href="word-lists.html">Word lists</a> page.</li>
<li><b>Edward Fry</b>, whose first 100 Instant Words hold the three words on the Early Literacy Profile (Central Okanagan) lists that aren&rsquo;t Dolch&rsquo;s: <i>each</i>, <i>other</i> and <i>people</i>.</li>
<li><b>Central Okanagan Public Schools</b>, <i>Early Literacy Profile (ELP) Assessment &amp; Instructional Guide</i> (2025), pp. 16&ndash;17, for the ELP word lists. The cards made from them aren&rsquo;t an SD23 publication.</li>
</ul>
</div></section>

<section class="about" id="histories" aria-labelledby="wh-h"><div class="wrap prose">
<h2 id="wh-h">Words and their histories</h2>
<ul class="credits">
<li><b>Douglas Harper</b>, <a href="https://www.etymonline.com/">Online Etymology Dictionary</a>. The histories behind <a href="parts.html">Parts</a>: every word in a family links to its entry.</li>
<li><b>Calvert Watkins</b>, <i>The American Heritage Dictionary of Indo-European Roots</i>, 3rd ed. (Houghton Mifflin Harcourt, 2011). The roots are to follow it; the families aren&rsquo;t checked against it yet.</li>
<li><b>The Linguistics Research Center</b>, University of Texas at Austin, <a href="https://lrc.la.utexas.edu/lex">Indo-European Lexicon</a>, which follows <b>Julius Pokorny</b>, <i>Indogermanisches etymologisches W&ouml;rterbuch</i> (1959). The English, Latin and Greek words from each root, as on the <a href="roots/leg.html">*leg-</a> and <a href="roots/hap.html">hap</a> pages.</li>
<li><b>Wiktionary</b>, for the verb in both languages, <a href="https://en.wiktionary.org/wiki/%CE%BB%CE%AD%CE%B3%CF%89">Greek λέγω</a> and <a href="https://en.wiktionary.org/wiki/lego#Latin">Latin <i>legō</i></a>, and for the root, <a href="https://en.wiktionary.org/wiki/Reconstruction:Proto-Indo-European/le%C7%B5-">*leǵ-</a>.</li>
<li><b>Ferdinand de Saussure</b>, <i>Course in General Linguistics</i> (1916), for <a href="definitions.html#def-synchronic">synchronic</a> and <a href="definitions.html#def-diachronic">diachronic</a>.</li>
<li><b>Leonard Bloomfield</b>, <i>Language</i> (1933), for <a href="definitions.html#def-free">free</a> and <a href="definitions.html#def-bound">bound</a> forms.</li>
</ul>
</div></section>

<section class="about" id="sounds" aria-labelledby="ss-h"><div class="wrap prose">
<h2 id="ss-h">Sounds and syllables</h2>
<ul class="credits">
<li><b>Daniel Kahn</b>, <i>Syllable-Based Generalizations in English Phonology</i> (PhD diss., MIT, 1976), and <b>Elisabeth Selkirk</b>, &ldquo;The Syllable,&rdquo; in <i>The Structure of Phonological Representations</i>, Part II, ed. Harry van der Hulst and Norval Smith (Foris, 1982). Kahn put a consonant like the p of <i>happy</i> in both syllables; Selkirk put it in the first, as the swoops do. <b>Alice Turk</b> measured lip movements to test the two: &ldquo;Articulatory Phonetic Clues to Syllable Affiliation,&rdquo; in <i>Phonological Structure and Phonetic Form</i>, ed. Patricia Keating (Cambridge University Press, 1994), 107&ndash;135 (<a href="https://www.cambridge.org/core/books/phonological-structure-and-phonetic-form/articulatory-phonetic-clues-to-syllable-affiliation-gestural-characteristics-of-bilabial-stops/55D545433F8A1184F9992C1E25902D68">publisher</a>).</li>
<li><b>Catherine Anderson</b> and colleagues, <i>Essentials of Linguistics</i>, an open textbook: &ldquo;<a href="https://open.maricopa.edu/essentialsoflinguistics/chapter/3-5-aspirated-stops-in-english/">Aspirated Stops in English</a>,&rdquo; on the puff of breath after a p, t or k that starts a stressed syllable.</li>
<li><b>Sonia Ben Hedia</b>, <i>Gemination and Degemination in English Affixation</i> (Language Science Press, 2019), open access (<a href="https://langsci-press.org/catalog/book/221">publisher</a>). English has two of the same consonant sound in a row only across a join, as in <i>unnamed</i>.</li>
</ul>
</div></section>

<section class="about" aria-labelledby="sl-h"><div class="wrap prose">
<h2 id="sl-h">Reading and learning</h2>
<ul class="credits">
<li><b>Daniil Elkonin</b>. Sound circles go back to his boxes, where a learner pushes a counter into a box for each sound.</li>
<li><b>Linnea Ehri</b>, &ldquo;Orthographic Mapping in the Acquisition of Sight Word Reading, Spelling Memory, and Vocabulary Learning,&rdquo; <i>Scientific Studies of Reading</i> 18, no. 1 (2014): 5&ndash;21 (<a href="https://doi.org/10.1080/10888438.2013.819356">doi</a>). Her account of how readers bond a word&rsquo;s spelling to its sounds and meaning is why it helps to mark which letters spell which sound.</li>
<li><b>Norbert Wiener</b>, <i>Cybernetics: Or Control and Communication in the Animal and the Machine</i> (1948), for the idea of feedback the first session is built on.</li>
<li>The studies behind marking by hand are cited on <i>Using the operator cards</i>, in the <a href="presentations.html">Session 1 handouts</a>.</li>
</ul>
</div></section>

<section class="about" id="research" aria-labelledby="rs-h"><div class="wrap prose">
<h2 id="rs-h">Research on teaching the spelling system</h2>
<p>Studies that bear on whether teaching English spelling as a system helps learners read and spell, kept here so the site&rsquo;s claims can be checked against them. Bowers, Kirby and Deacon&rsquo;s review is under Pete Bowers, above.</p>
<ul class="credits">
<li><b>Kathleen Rastle, Clare Lally, Matthew H. Davis and J. S. H. Taylor</b>, &ldquo;The Dramatic Impact of Explicit Instruction on Learning to Read in a New Writing System,&rdquo; <i>Psychological Science</i> 32, no. 4 (2021) (<a href="https://doi.org/10.1177/0956797620968790">doi</a>). Adults learning an invented writing system read new words far better after a short lesson on how its spellings map to sounds and meanings than after reading alone.</li>
<li><b>Steve Graham and Tanya Santangelo</b>, &ldquo;Does Spelling Instruction Make Students Better Spellers, Readers, and Writers? A Meta-Analytic Review,&rdquo; <i>Reading and Writing</i> 27 (2014): 1703&ndash;1743 (<a href="https://acuresearchbank.acu.edu.au/item/8v7y9/does-spelling-instruction-make-students-better-spellers-readers-and-writers-a-meta-analytic-review">record</a>). Formal spelling teaching improved spelling, the gains lasted and carried into writing, and reading improved too.</li>
<li><b>V. Devonshire, P. Morris and M. Fluck</b>, &ldquo;Spelling and Reading Development: The Effect of Teaching Children Multiple Levels of Representation in Their Orthography,&rdquo; <i>Learning and Instruction</i> 25 (2013): 85&ndash;94 (<a href="https://researchportal.port.ac.uk/en/publications/spelling-and-reading-development-the-effect-of-teaching-children-/">record</a>). Five to seven year olds taught morphology, etymology and spelling rules read and spelled better than those taught phonics alone.</li>
<li><b>Danielle Colenbrander, Alexa von Hagen, Sascha Kohnen and colleagues</b>, &ldquo;The Effects of Morphological Instruction on Literacy Outcomes for Children in English-Speaking Countries: A Systematic Review and Meta-Analysis,&rdquo; <i>Educational Psychology Review</i> 36 (2024): 119 (<a href="https://doi.org/10.1007/s10648-024-09953-3">doi</a>). Across 28 studies, small effects on reading and spelling overall, with low certainty; larger effects on the words that were taught; some transfer to spelling untaught words, none to reading them.</li>
<li><b>Danielle Colenbrander, Lindsay Parsons, Jeffrey S. Bowers and Colin J. Davis</b>, &ldquo;Assessing the Effectiveness of Structured Word Inquiry for Students in Grades 3 and 5 with Reading and Spelling Difficulties: A Randomized Controlled Trial,&rdquo; <i>Reading Research Quarterly</i> 57, no. 1 (2022): 307&ndash;352 (<a href="https://doi.org/10.1002/rrq.399">doi</a>). Structured word inquiry didn&rsquo;t clearly beat an active comparison, apart from spelling untaught words in grade 3, and the teaching assistants found it harder to deliver.</li>
<li><b>Devin M. Kearns</b>, &ldquo;Does English Have Useful Syllable Division Patterns?&rdquo; <i>Reading Research Quarterly</i> 55, no. S1 (2020): S145&ndash;S160 (<a href="https://doi.org/10.1002/rrq.342">doi</a>). In 14,844 words from texts for grades 1 to 8, a vowel before two consonants was short in 78.8% of two-syllable words and 62.5% of longer ones (about 94% once weak vowels are set aside), while a vowel before one consonant was long in only 47.3% and 18.8%. Weak, unstressed vowels explain much of the gap. He concludes that dividing words by these rules costs more attention than it repays, and points to flexible trying of a vowel&rsquo;s sounds, morphology and practice instead. The data are about the words, not about learners.</li>
<li><b>Shayne B. Piasta, Carol McDonald Connor, Barry J. Fishman and Frederick J. Morrison</b>, &ldquo;Teachers&rsquo; Knowledge of Literacy Concepts, Classroom Practices, and Student Reading Growth,&rdquo; <i>Scientific Studies of Reading</i> 13, no. 3 (2009): 224&ndash;248. More time on explicit decoding went with bigger word-reading gains only when the teacher knew the content well.</li>
<li><b>Leonid Rozenblit and Frank Keil</b>, &ldquo;The Misunderstood Limits of Folk Science: An Illusion of Explanatory Depth,&rdquo; <i>Cognitive Science</i> 26, no. 5 (2002): 521&ndash;562. People believe they understand how things work in more detail than they do, until they try to explain them: a reason to test understanding on new words rather than trust the feeling of it.</li>
<li><b>Thomas R. Kratochwill and colleagues</b>, <i>Single-Case Designs Technical Documentation</i> (What Works Clearinghouse, 2010) (<a href="https://files.eric.ed.gov/fulltext/ED510743.pdf">ERIC</a>). Standards for evidence gathered with care from a few learners at a time.</li>
</ul>
<p class="uc">(Under construction: what these studies show for this notation isn&rsquo;t written up yet. Next: a page weighing them.)</p>
</div></section>

<section class="about" aria-labelledby="se-h"><div class="wrap prose">
<h2 id="se-h">Sentences</h2>
<ul class="credits">
<li><b>Randolph Quirk, Sidney Greenbaum, Geoffrey Leech and Jan Svartvik</b>, <i>A Comprehensive Grammar of the English Language</i> (Longman, 1985), for <i>operator</i>: their name for the first auxiliary, the word that carries the negative and moves to the front to make a question.</li>
<li><b>Zellig Harris</b>, &ldquo;Co-Occurrence and Transformation in Linguistic Structure,&rdquo; <i>Language</i> 33, no. 3 (1957): 283&ndash;340, and <b>Noam Chomsky</b>, <i>Syntactic Structures</i> (Mouton, 1957), for <i>kernel</i>: their name for a language&rsquo;s simplest sentences. The notation keeps the word for what&rsquo;s built first, and grows the rest from it.</li>
</ul>
</div></section>

<section class="about" aria-labelledby="ty-h"><div class="wrap prose">
<h2 id="ty-h">Type and hosting</h2>
<p>Fraunces and Lexend, with Gentium Plus in the deck and handouts, all under the SIL Open Font License. Since 8 November 2026 the site serves them itself, rather than loading them from Google Fonts. The site is hosted on GitHub Pages.</p>
</div></section>

<section class="about" id="copyright" aria-labelledby="cr-h"><div class="wrap prose">
<h2 id="cr-h">Copyright</h2>
<p>&copy; 2026 {HOLDER}</p>
<p>The pages, drawings, word cards, handouts and decks on this site are shared under the {LICENCE}. You may copy them, change them and pass them on, as long as you credit the source, don&rsquo;t sell them, and share what you make under the same terms.</p>
<p>The licence covers this site&rsquo;s own work. The works cited above, the ELP and Dolch word lists, and the fonts keep their own terms. Copyright protects the way something is expressed, not the idea or method behind it.</p>
</div></section>

<section class="about" id="copywrite" aria-labelledby="cw-h"><div class="wrap prose">
<h2 id="cw-h">Copywrite</h2>
<p>Learners come to language by copying it: the voices around them first, then letters and words, until the copies become something they can write for themselves. Every language user does the same, and so does anyone who builds on a language, whether in a lesson, a book or a notation like this.</p>
<p>Copyright guards a particular way of saying something. Copywrite is the older practice underneath it: taking what others have said and written, and writing it again in your own hand. This site is copywrite too, written in its own marks from what the people above worked out. The licence is meant to keep that open. Copy these cards, mark them, change them, and make them fit your learners.</p>
</div></section>

<section class="about" id="contact-us" aria-labelledby="ct-h"><div class="wrap prose">
<h2 id="ct-h">Contact</h2>
<p>Questions, corrections and suggestions are welcome.</p>
{CONTACT}
</div></section>
</main>
{footer(0)}"""
    (OUT / "credits.html").write_text(page("Credits and copyright · A Legend for English Words", credits, 0,
                                           "The writers Legomorphic Notation draws on, the site's copyright and licence, and how to get in touch."),
                                      encoding="utf-8")
    print("wrote about.html, credits.html")
