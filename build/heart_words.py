"""Words with a heart (13 November 2026): lists/hearts.html, on Legomorphic spelling.

A heart word is one with a part a learner can't yet decode, or can't ever decode by the usual sounds. A heart over that
part says "learn this by heart". The notation can usually say why instead, so the words here are sorted by how much
of the heart a learner can lose:
  1. none of it once the step comes: the word is regular on the route (could, both, talk, learn, into);
  2. some of it, given a reason they can use: a word it comes from (said, say), a pattern with a history (o for the
     vowel of up beside m, n, v and th), or a letter doing a job (the u that keeps g hard in guess);
  3. the rest, by heart, with a story at most (of, eye, women).
The words are irregular words common in early reading: the Early Literacy Profile (Central Okanagan), Dolch, the
route, and the words early-reading programs teach as heart words. Codes for the ones the site hadn't marked are below.

Ruled 13 November 2026: gu is a bonded unit (guess, guide), as bu is in buy; the teacher's note says why the u is
there. two keeps tw bonded and people keeps eo as a team, though twin and popular say the letters: the cone stays for
forms of the same word. The silent h of hour, honest and honour joins the vowel unit after it (ruled 13 November 2026):
h is a breath shaped by the vowel that follows it, so where it isn't said it belongs with that vowel."""
import html

CODES = {
    "talk": "c.t t.al c.k", "friend": "c.fr t.ie c.nd ; cup 3", "woman": "c.w b.o | c.m b.a c.n", "women": "c.w b.o | c.m b.e c.n",
    "move": "c.m b.o c.v e0", "four": "c.f r.our", "fourth": "c.f r.our g.th", "nothing": "c.n b.o + | g.th s.i k.ng",
    "another": "b.a | c.n + b.o g.th | r.er", "above": "b.a | c.b b.o c.v e0", "among": "b.a | c.m b.o k.ng",
    "against": "b.a | c.g t.ai c.nst", "almost": "b.a c.l | c.m l.o c.st", "poor": "c.p r.oor", "won": "c.w b.o c.n",
    "son": "c.s b.o c.n", "month": "c.m b.o c.n g.th", "hour": "t.hou c.r", "minute": "c.m s.i | c.n b.u c.t e0",
    "Monday": "c.M b.o c.n | c.d t.ay", "Wednesday": "c.W s.e k.dn e0 c.s | c.d t.ay", "heart": "c.h r.ear c.t",
    "about": "b.a | c.b t.ou c.t", "answer": "s.a c.n | k.sw r.er", "honest": "t.ho | c.n b.e c.st ; cup 1", "honour": "t.ho | c.n r.our ; cup 1",
    "truth": "c.tr l.u g.th", "truly": "c.tr l.u + | c.l b.y", "busy": "c.b b.u | c.s b.y", "build": "k.bu s.i c.ld",
    "built": "k.bu s.i c.lt", "sure": "c.s r.ur e0", "whom": "k.wh b.o c.m", "whose": "k.wh b.o c.s e0",
    "toward": "c.t b.o + | c.w r.ar c.d", "through": "g.th c.r t.ough", "learn": "c.l r.ear c.n", "earth": "r.ear g.th",
    "early": "r.ear | c.l b.y", "guy": "k.gu l.y", "guess": "k.gu s.e k.ss", "guest": "k.gu s.e c.st", "guide": "k.gu l.i c.d e>",
    "young": "c.y t.ou k.ng ; cup 2", "touch": "c.t t.ou g.ch ; cup 2", "enough": "b.e | c.n t.ou k.gh", "tough": "c.t t.ou k.gh",
    "rough": "c.r t.ou k.gh", "love": "c.l b.o c.v e0",
}

# (group, [(what the heart part has, the words, a note for the teacher)])
GROUPS = [
    ("The heart goes away on the route", "These are regular once their step comes. A heart on them would teach that something regular is odd.", [
        ("ould, one spelling for three words (step 7)", ["could", "would", "should"], "Learn one and spell three."),
        ("A long vowel before two consonants (step 18)", ["both", "almost"], "Like <i>most</i>, <i>old</i> and <i>find</i>."),
        ("al for the vowel of <i>saw</i> (step 23)", ["talk", "walk"], "The l is silent and joins the vowel."),
        ("An r-controlled unit (steps 12 and 26)", ["are", "were", "there", "where", "their", "your", "four", "fourth", "door", "floor", "poor", "learn", "earth", "early", "heart"],
         "The unit spells the sound; several units spell more than one."),
        ("Parts that keep their spelling (seams)", ["into", "today", "nothing", "another", "toward"], "Each part is a word the learner knows."),
        ("Nothing irregular at all", ["very", "been"], "<i>Very</i> is closed, short e, then y. <i>Been</i> is a team, said with the vowel of <i>bin</i> in many places."),
    ]),
    ("The heart part has a reason", "A word it comes from, a pattern with a history, or a letter doing a job for another letter.", [
        ("From a word the learner knows", ["said", "says", "does", "goes", "truth", "truly", "built"],
         "<i>Say</i>, <i>do</i>, <i>go</i>, <i>true</i>, <i>build</i>: the spelling keeps the word, and the sound moves."),
        ("o for the vowel of <i>up</i>, beside m, n, v and th (step 19)", ["son", "won", "month", "Monday", "among", "above", "mother", "brother", "other", "come", "some", "done", "love"],
         "Old handwriting ran u into m, n and v, so scribes wrote o (Carney 1994: 69). One pattern, not thirteen hearts."),
        ("o for the vowel of <i>moon</i>, and a after w (step 19)", ["to", "do", "who", "whom", "whose", "move", "two", "was", "what", "want"],
         "<i>Two</i> keeps the w that <i>twin</i>, <i>twelve</i> and <i>twenty</i> say."),
        ("gu keeps g hard", ["guess", "guest", "guide", "guy"],
         "Without the u, <i>gide</i> would read as <i>jide</i>: g before e, i or y is often soft (step 10). The bond bar shows the u working with the g. Before a, o or u the g is hard anyway, so <i>guard</i> doesn&rsquo;t need its u; it came with the word from French."),
        ("A team saying another of its sounds (step 22)", ["friend", "young", "touch"], "The bar stays: the spelling is the unit. Where the unit says the short sound of one of its letters, that letter carries the cup: the e of <i>friend</i>, the u of <i>young</i> and <i>touch</i>."),
    ]),
    ("By heart", "The heart is honest here. A story helps the word stick, but it won&rsquo;t help a learner read the next one.", [
        ("A letter saying another letter&rsquo;s sound", ["of", "busy", "build", "pretty", "any", "many", "women", "woman", "minute", "sure"],
         "<i>Of</i> and <i>off</i> were once one word; the f stayed. <i>Busy</i> is spelled with u and said with short i; in <i>build</i>, as in <i>buy</i>, the u is silent beside the b. <i>Woman</i> was Old English <i>wifman</i>, wife-man, then <i>wimman</i>; the o didn&rsquo;t come in until the 13th century (Upward and Davidson 2011: 186). <i>Women</i> is still said with the old i, and spelled with the o of <i>woman</i>."),
        ("One and once", ["one", "once"], "<i>Alone</i> and <i>only</i> keep the old sound of <i>one</i>: <i>all one</i>, <i>one-ly</i>."),
        ("A silent letter", ["hour", "honest", "honour", "answer", "Wednesday"],
         "The h of <i>hour</i> and <i>honest</i> was silent in the French they came from. It joins the vowel after it under one bar: h is only a breath shaped like the vowel that follows it, and here not even that. <i>Answer</i> is <i>and</i> + <i>swear</i> in Old English. <i>Wednesday</i> is Woden&rsquo;s day."),
        ("ough and augh", ["laugh", "enough", "tough", "rough", "through"], "Learned by family: <i>tough</i>, <i>rough</i>, <i>enough</i> rhyme."),
        ("Others", ["eye", "people", "again", "against", "because", "about", "always"], "<i>Again</i>, <i>about</i> and <i>always</i> start with a weak a; past it, they are regular. <i>People</i> keeps an o that <i>popular</i> says."),
    ]),
]


def write(OUT, page, header, footer, X):
    LW = X["LW"]
    from noun_codes import NOUN_CODES
    def drawn(w):
        if w in LW.W: return X["svg_of"](w, 36, label=f"{w}, marked")
        if w in NOUN_CODES: return X["svg_of"](w, 36, code=NOUN_CODES[w], label=f"{w}, marked")
        return f'<span class="plain" style="font-size:36px">{html.escape(w)}</span>'
    secs = []
    for k, (h, sub, rows) in enumerate(GROUPS, 1):
        items = "".join(f'<div class="hw-row"><h3>{what}</h3><div class="words rrow">{"".join(f"<figure class=word>{drawn(w)}</figure>" for w in ws)}</div>'
                        f'<p class="sub t-only">{note}</p></div>' for what, ws, note in rows)
        secs.append(f'<section class="about hw-group hw-{k}"><div class="wrap"><h2>{k}. {h}</h2><p class="sub">{sub}</p>{items}</div></section>')
    body = f"""{header(1)}
<main class="hearts-page">
<section class="hero"><div class="wrap">
<p class="eyebrow t-only"><a href="index.html">Legomorphic spelling</a> &middot; Words with a heart</p>
<h1>Words with a heart</h1>
<p class="lead">A heart word has a part a learner can&rsquo;t decode yet, or can&rsquo;t decode by the usual sounds at all. A heart over that part says <i>learn this by heart</i>. The notation can usually say why instead. Most heart words are regular once their step comes, or have a reason a learner can use; only a few have to be learned by heart.</p>
<p class="sub t-only">Map every heart word sound by sound, as with any word: a circle for each sound, then find the part that doesn&rsquo;t say what the letters usually say. Then ask which group it&rsquo;s in. Every word here can be looked up in <a href="../walk.html">Words</a>.</p>
</div></section>
{"".join(secs)}
<section class="about t-only"><div class="wrap prose">
<p class="sub">Most of these words are on the Early Literacy Profile (Central Okanagan) and Dolch lists. Programs such as UFLI Foundations teach them as heart words, with a heart over the part to learn by heart; the notation shows the reason where there is one. Carney, <i>A Survey of English Spelling</i> (1994): o for u beside m, n and v, p. 69; the vowel of <i>book</i> in <i>could</i>, p. 146.</p>
{X["uc"]("ruled 13 November 2026: gu bonded, as bu is in buy; a silent h joins the vowel after it, as in hour and honest.")}
</div></section>
</main>
{footer(1)}"""
    (OUT / "lists" / "hearts.html").write_text(page("Words with a heart · A Legend for English Words", body, 1,
        "Heart words sorted by how much of the heart a learner can lose: regular on the route, a reason to use, or by heart."), encoding="utf-8")
    return sorted({w for _, _, rows in GROUPS for _, ws, _ in rows for w in ws})
