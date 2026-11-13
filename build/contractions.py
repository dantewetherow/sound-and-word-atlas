"""Squeezed into oblivion (13 November 2026): contractions.html, behind Words, beside the ablaut page.

In a contraction a small, unstressed word loses its vowel, and sometimes more, and the apostrophe stands where the
letters were (Carney 1994: 50). The notation draws the apostrophe red, in the vowel's colour, with no circle: it holds
the vowel's place and says nothing. A seam stands between the two words. The squeeze itself is the apostrophe
catastrophe (ruled 13 November 2026). Pairs that sound alike (its and it's, your and you're) live on Spelled apart;
the possessive 's isn't treated: it isn't a squeeze, and the history it rests on is too fine a point for learners.
These are the first contractions the site draws."""
import html

CODES = {
    "isn’t": "s.i c.s + | c.n ap c.t", "wasn’t": "c.w b.a c.s + | c.n ap c.t", "aren’t": "r.ar e0 + c.n ap c.t",
    "weren’t": "c.w r.er e0 + c.n ap c.t", "doesn’t": "c.d b.o + e0 c.s + | c.n ap c.t", "didn’t": "c.d s.i c.d + | c.n ap c.t",
    "hasn’t": "c.h s.a c.s + | c.n ap c.t", "couldn’t": "c.c t.oul c.d + | c.n ap c.t", "wouldn’t": "c.w t.oul c.d + | c.n ap c.t",
    "shouldn’t": "g.sh t.oul c.d + | c.n ap c.t",
    "I’m": "l.I + ap c.m", "it’s": "s.i c.t + ap c.s", "he’s": "c.h l.e + ap c.s", "she’s": "g.sh l.e + ap c.s",
    "you’re": "c.y t.ou + ap c.r e0", "we’re": "c.w l.e + ap c.r e0", "they’re": "g.th t.ey + ap c.r e0", "let’s": "c.l s.e c.t + ap c.s",
    "I’ll": "l.I + ap k.ll", "I’ve": "l.I + ap c.v e0", "I’d": "l.I + ap c.d", "can’t": "c.c s.a c.n + ap c.t",
    "won’t": "c.w l.o + c.n ap c.t", "don’t": "c.d l.o + c.n ap c.t",
    "its": "s.i c.t c.s", "who’s": "k.wh b.o + ap c.s",
}

# (heading, what happened, [(contraction, the two words, a sentence)])
GROUPS = [
    ("not loses its o", "The o of <i>not</i> is squeezed out and the apostrophe takes its place. In <i>aren&rsquo;t</i> and "
     "<i>weren&rsquo;t</i> the silent e of <i>are</i> and <i>were</i> stays: the first word keeps its whole spelling, and only <i>not</i> is squeezed.", [
        ("isn’t", "is + not", "It isn&rsquo;t fair."), ("wasn’t", "was + not", "It wasn&rsquo;t me."), ("aren’t", "are + not", "We aren&rsquo;t late."),
        ("weren’t", "were + not", "They weren&rsquo;t home."), ("doesn’t", "does + not", "It doesn&rsquo;t fit."), ("didn’t", "did + not", "I didn&rsquo;t see."),
        ("hasn’t", "has + not", "She hasn&rsquo;t come."), ("couldn’t", "could + not", "I couldn&rsquo;t reach."),
        ("wouldn’t", "would + not", "He wouldn&rsquo;t stop."), ("shouldn’t", "should + not", "You shouldn&rsquo;t run.")]),
    ("The operator loses its vowel", "After a pronoun, <i>am</i>, <i>is</i>, <i>are</i> and <i>us</i> lose their vowels. What&rsquo;s "
     "left is a consonant, and sometimes a silent e, leaning on the word before it.", [
        ("I’m", "I + am", "I&rsquo;m here."), ("it’s", "it + is", "It&rsquo;s late."), ("he’s", "he + is", "He&rsquo;s tall."),
        ("she’s", "she + is", "She&rsquo;s ready."), ("you’re", "you + are", "You&rsquo;re next."), ("we’re", "we + are", "We&rsquo;re ready."),
        ("they’re", "they + are", "They&rsquo;re here."), ("let’s", "let + us", "Let&rsquo;s go.")]),
    ("More than the vowel goes", "Some lose a whole first part. One apostrophe stands for all of it.", [
        ("I’ll", "I + will", "I&rsquo;ll help."), ("I’ve", "I + have", "I&rsquo;ve got it."), ("I’d", "I + would", "I&rsquo;d like that."),
        ("can’t", "can + not", "I can&rsquo;t see."), ("don’t", "do + not", "Don&rsquo;t run."), ("won’t", "will + not", "I won&rsquo;t go.")]),
]


def write(OUT, door_page, X):
    LW = X["LW"]
    from noun_codes import NOUN_CODES
    def fig(w, sub, F):
        code = None if w in LW.W else (CODES.get(w) or NOUN_CODES.get(w) or X["auto_codes"][w])
        return f'<figure class="word">{X["svg_of"](w, F, code=code, label=f"{w}, marked")}<figcaption>{sub}</figcaption></figure>'
    secs = []
    for h, sub, rows in GROUPS:
        figs = "".join(fig(w, f"<span class=ws>{s}</span><span class=t-only>{sent}</span>", 40) for w, s, sent in rows)
        secs.append(f'<section class="about ct-group"><div class="wrap"><h2>{h}</h2><p class="sub t-only">{sub}</p><div class="words rrow">{figs}</div></div></section>')
    body = f"""<section class="hero"><div class="wrap">
<p class="eyebrow t-only">Explorations</p>
<h1>Squeezed into oblivion</h1>
<p class="lead">In a contraction, two words join and the second one, small and quick, loses its vowel. The vowel is squeezed into oblivion, and an apostrophe lands where it was: an apostrophe catastrophe. The apostrophe is drawn red, in the vowel&rsquo;s colour, with no circle: it holds the vowel&rsquo;s place and says nothing.</p>
</div></section>
{"".join(secs)}
<section class="about t-only"><div class="wrap prose">
<p><i>Won&rsquo;t</i> keeps an old form of <i>will</i>, <i>wol</i>, so it changes more than the others. <i>Don&rsquo;t</i> changes its vowel: <i>do</i> says the vowel of <i>moon</i>, <i>don&rsquo;t</i> the name of o. Both are worth saying aloud beside the two words they come from.</p>
<p class="sub">Edward Carney, <i>A Survey of English Spelling</i> (1994): the apostrophe, p. 50. These are on the route at <a href="steps/27.html">step 27</a>, and the ones that sound like another word (<i>it&rsquo;s</i> and <i>its</i>, <i>you&rsquo;re</i> and <i>your</i>) are on <a href="lists/apart.html#squeeze">Spelled apart</a>. Every word here can be looked up in <a href="walk.html">Words</a>.</p>
{X["uc"]("the first contractions the site draws, since 13 November 2026.")}
</div></section>"""
    door_page("contractions", "Squeezed into oblivion · A Legend for English Words", "Contractions: the vowel squeezed out, the apostrophe in its place, and the apostrophe catastrophes.", body)
    return sorted({w for _, _, rows in GROUPS for w, _, _ in rows} | {"its", "who’s"})
