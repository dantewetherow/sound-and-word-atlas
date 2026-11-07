"""The About page (the word legomorphic and what the notation does) and the Credits page (sources, copyright, the
idea of copywrite, and contact).

build_site.py calls write() with its page, header, footer and svg_of functions. The etymology follows the Online
Etymology Dictionary's entries for *leg- and morphology, opened on 6 November 2026. The marks are described as the site's
legend gives them. The copyright holder, the licence and the contact address are the author's choices of 6 November 2026.
The site is static, so contact is a mail link: the address is put together in the page, which keeps it out of the HTML
that address harvesters read."""
import pathlib, shutil
HERE = pathlib.Path(__file__).resolve().parent

HOLDER = "Dante Wetherow, B.Ed., M.Ed."
LICENCE = ('<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike '
           '4.0 International licence</a> (CC BY-NC-SA 4.0)')
CONTACT = """<p class="contact"><a class="btn" id="contact" href="#contact-note">Email Dante Wetherow</a></p>
<p class="sub" id="contact-note">It opens a new message in your email app.<noscript> Write to dante.wetherow at sd23.bc.ca.</noscript></p>
<script>(() => { const a = document.getElementById('contact'); const u = ['dante', 'wetherow'].join('.'), d = ['sd23', 'bc', 'ca'].join('.');
  a.href = 'mailto:' + u + '@' + d + '?subject=' + encodeURIComponent('Sound and Word Atlas'); })();</script>"""

EXAMPLES = [("could", "A red bond bar under <i>oul</i>, the letters that spell its vowel sound."),
            ("like", "The silent <i>e</i> sits in its cone, and its vault reaches back to make the <i>i</i> long."),
            ("nice", "The same vault, and a nudge from the <i>e</i> softens the <i>c</i>."),
            ("funny", "The box around <i>nn</i> stops the <i>y</i> from reaching back, so the <i>u</i> stays short.")]


def write(OUT, page, header, footer, svg_of):
    shutil.copyfile(HERE / "logo.svg", OUT / "logo.svg")
    examples = "".join(f'<figure class="ex">{svg_of(w, 56)}<figcaption>{cap}</figcaption></figure>' for w, cap in EXAMPLES)
    about = f"""{header(0)}
<main>
<section class="hero"><div class="wrap about-hero">
<div>
<p class="eyebrow">About</p>
<h1>Legomorphic Notation</h1>
<p class="lead">A set of marks and colours drawn on ordinary spelling, so that what a reader usually has to work out alone is there for everyone to see: how many sounds a word has, which letters spell each sound, where its meaningful parts join, and which letters change the sounds of others.</p>
</div>
<figure class="logo"><img src="logo.svg" width="150" height="150" alt="The logo: the letters d, b, q and p"><figcaption><i>d, b, q</i> and <i>p</i>: a single shape, flipped and turned</figcaption></figure>
</div></section>

<section class="about" aria-labelledby="word-h"><div class="wrap prose">
<h2 id="word-h">The word</h2>
<p><i>Legomorphic</i> is built from two old words, a word for gathering and a word for shape.</p>
<p><i>Lego</i> is the same word in Greek and in Latin, and in both it means &ldquo;I gather.&rdquo; Greek <i>legō</i> (λέγω) first meant to pick out, to gather and to count, and from picking out words it came to mean to say and to tell. Latin <i>legō</i> (<i>legere</i>) means to gather and to choose, and also to read. The root gives a speaker&rsquo;s word in Greek and a reader&rsquo;s word in Latin.</p>
<p>English has both families. From the Greek come <i>lexicon</i>, <i>dialogue</i> and <i>logic</i>; from the Latin, <i>legible</i>, <i>lecture</i>, <i>collect</i> and <i>select</i>. Linguists trace them all to a Proto-Indo-European root, written *leg-, to collect or gather.</p>
<p><i>Morphē</i> (μορφή) is Greek for form or shape. It gives us <i>morpheme</i>, and <i>morphology</i>, the study of word forms, which joins the same two roots the other way round.</p>
<p>So the notation is named for the shapes words take when we gather them: the sounds we pick out and say, the letters we pick out and read, and the parts they build together.</p>
<p class="sub">Etymologies from the Online Etymology Dictionary: <a href="https://www.etymonline.com/word/*leg-">*leg-</a> and <a href="https://www.etymonline.com/word/morphology">morphology</a>.</p>
</div></section>

<section class="about" aria-labelledby="shows-h"><div class="wrap prose">
<h2 id="shows-h">What it shows</h2>
<p>The notation explores four systems at once: orthography, phonology, morphology and syntax. It works through graphemes, phonemes and morphemes, and through the order in time in which a message is put together.</p>
<p>In a word, vowels are red, consonants black, and <i>sh</i>, <i>th</i> and <i>ch</i> green. The marks fall into three groups.</p>
<ul class="marks-list">
<li><b>Sounds.</b> A sound circle under each sound, a bond bar under letters that spell a single sound, a cup or a bar over a vowel for short or long, and a red bar under a vowel and its <i>r</i>.</li>
<li><b>Parts.</b> A syllable swoop under each syllable, and a morpheme seam between meaningful parts.</li>
<li><b>Letters working on letters.</b> The vowel vault, an arc from an <i>e</i>, or from a vowel after a single consonant, back to the vowel it makes long. The block box, around a pair or cluster of consonants that stops that reach, and the blocked vault, which ends in a red X where it does. The cone of silence around a silent <i>e</i>, and the nice-nudge from <i>e</i>, <i>i</i> or <i>y</i> to the <i>c</i> or <i>g</i> it softens.</li>
</ul>
<p>Contractions take a red apostrophe in place of the vowel they drop.</p>
<div class="examples">{examples}</div>
<p>In a sentence the colours change jobs. Actors and the things acted on are green, actions are red, and operators, the words that can move to the front to make a question, are blue. <a href="index.html#marks">Reading the marks</a> has the legend with a drawing of each mark.</p>
</div></section>

<section class="about" aria-labelledby="use-h"><div class="wrap prose">
<h2 id="use-h">How it&rsquo;s used</h2>
<p>It isn&rsquo;t a program. It&rsquo;s an exploration of ways to provide access, and an invitation to experiment with our methods and synthesize our understandings. It can sit beside any systematic phonics program, synthetic or analytic, and it aims to be systematic, analytic, synthetic, responsive, diagnostic and agnostic.</p>
<p>Its teaching cycle is the learning loop. Learners move among seeing, listening, speaking, reading and writing: a clean pass, then back to the start, back to any earlier mode, or between any two. Each pass can swap a part (a sound, its articulation, an actor, an action, an operator, a preposition) to fit the learner&rsquo;s need, interest and skill in the moment.</p>
<p>The <a href="index.html#route">route</a> through English spelling on this site is its own scope and sequence, with Edward Carney&rsquo;s <i>A Survey of English Spelling</i> as its backbone and his page references on every step.</p>
</div></section>

<section class="about" aria-labelledby="who-h"><div class="wrap prose">
<h2 id="who-h">Who made it</h2>
<p>Legomorphic Notation and this site are the work of {HOLDER} The writers it builds on are on the <a href="credits.html">Credits</a> page.</p>
{CONTACT}
</div></section>
</main>
{footer(0)}"""
    (OUT / "about.html").write_text(page("About Legomorphic Notation · Sound and Word Atlas", about, 0,
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
<li><b>Melvyn Ramsden</b>, whose <a href="http://www.realspelling.com/">Real Spelling</a> gave us word sums and word matrices, the basis of the grade 3 word sum cards. His book is <i>Rescuing Spelling</i> (Southgate Publishers).</li>
<li><b>Pete Bowers</b>, who brought word sums and matrices into classrooms as structured word inquiry. His book is <i>Teaching How the Written Word Works</i>. With John R. Kirby and S. H&eacute;l&egrave;ne Deacon he wrote &ldquo;The Effects of Morphological Instruction on Literacy Skills: A Systematic Review of the Literature,&rdquo; <i>Review of Educational Research</i> 80, no. 2 (2010) (<a href="https://doi.org/10.3102/0034654309359353">doi</a>), and with Jeffrey Bowers, &ldquo;Beyond Phonics: The Case for Teaching Children the Logic of the English Spelling System,&rdquo; <i>Educational Psychologist</i> 52, no. 2 (2017): 124&ndash;141 (<a href="https://doi.org/10.1080/00461520.2017.1288571">doi</a>).</li>
<li><b>Sue Scibetta Hegland</b>, <i><a href="https://shop.thereadingleague.org/products/beneath-the-surface-of-words-what-english-spelling-reveals-and-why-it-matters">Beneath the Surface of Words: What English Spelling Reveals and Why It Matters</a></i> (Learning About Spelling).</li>
<li><b>E. W. Dolch</b>, &ldquo;A Basic Sight Vocabulary,&rdquo; <i>The Elementary School Journal</i> 36, no. 6 (1936): 456&ndash;460. The Dolch cards and the <a href="word-lists.html">Word lists</a> page.</li>
<li><b>Edward Fry</b>, whose first 100 Instant Words hold the three ELP words that aren&rsquo;t Dolch&rsquo;s: <i>each</i>, <i>other</i> and <i>people</i>.</li>
<li><b>Central Okanagan Public Schools</b>, <i>Early Literacy Profile (ELP) Assessment &amp; Instructional Guide</i> (2025), pp. 16&ndash;17, for the ELP word lists. The cards made from them aren&rsquo;t an SD23 publication.</li>
</ul>
</div></section>

<section class="about" aria-labelledby="sl-h"><div class="wrap prose">
<h2 id="sl-h">Sounds and learning</h2>
<ul class="credits">
<li><b>Daniil Elkonin</b>. Sound circles go back to his boxes, where a child pushes a counter into a box for each sound.</li>
<li>The studies behind marking by hand are cited on <i>Using the operator cards</i>, in the <a href="presentations.html">Session 1 handouts</a>.</li>
</ul>
</div></section>

<section class="about" aria-labelledby="ty-h"><div class="wrap prose">
<h2 id="ty-h">Type and hosting</h2>
<p>Fraunces and Lexend, with Gentium Plus in the deck and handouts, all under the SIL Open Font License. The pages load them from Google Fonts. The site is hosted on GitHub Pages.</p>
</div></section>

<section class="about" id="copyright" aria-labelledby="cr-h"><div class="wrap prose">
<h2 id="cr-h">Copyright</h2>
<p>&copy; 2026 {HOLDER}</p>
<p>The pages, drawings, word cards, handouts and decks on this site are shared under the {LICENCE}. You may copy them, change them and pass them on, as long as you credit the source, don&rsquo;t sell them, and share what you make under the same terms.</p>
<p>The licence covers this site&rsquo;s own work. The works cited above, the ELP and Dolch word lists, and the fonts keep their own terms. Copyright protects the way something is expressed, not the idea or method behind it.</p>
</div></section>

<section class="about" id="copywrite" aria-labelledby="cw-h"><div class="wrap prose">
<h2 id="cw-h">Copywrite</h2>
<p>Children learn language by copying it: the voices around them first, then letters and words, until the copies become something they can write for themselves. Every language user does the same, and so does anyone who builds on a language, whether in a lesson, a book or a notation like this.</p>
<p>Copyright guards a particular way of saying something. Copywrite is the older practice underneath it: taking what others have said and written, and writing it again in your own hand. This site is copywrite too, written in its own marks from what the people above worked out. The licence is meant to keep that open. Copy these cards, mark them, change them, and make them fit your learners.</p>
</div></section>

<section class="about" id="contact-us" aria-labelledby="ct-h"><div class="wrap prose">
<h2 id="ct-h">Contact</h2>
<p>Questions, corrections and suggestions are welcome.</p>
{CONTACT}
</div></section>
</main>
{footer(0)}"""
    (OUT / "credits.html").write_text(page("Credits and copyright · Sound and Word Atlas", credits, 0,
                                           "The writers Legomorphic Notation draws on, the site's copyright and licence, and how to get in touch."),
                                      encoding="utf-8")
    print("wrote about.html, credits.html")
