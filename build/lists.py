"""Spelling lists (lists/<slug>.html), made 10 November 2026: four models, one of each kind. The first was say, pay, lay.

A Legomorphic spelling list is small (six to eight words), states its principle at the top, and holds words that are
all there for the same reason. Each word comes with its word sum, its marking and a sentence. The learner builds each
word from its sum instead of copying it, uses it in a sentence, and is checked with words that were not on the list,
to see whether the convention was learned or only the list.

There are four kinds, by what the words share: one base with many joins (educate, education); one join across many
bases (making, hoping); one analog for several words (say, said; pay, paid), which this first list is; and a closed
set (this, that, these, those). A list is a view of something the site already has: a step's words and contrasts, a
family, or a section of the manual. This one follows the manual's "Say, pay, lay", which cites Brooks.

Each page prints as a learner's sheet; the teacher's notes are left off the print."""
import html

LISTS = [{
    "slug": "say-pay-lay", "title": "say, pay, lay", "kind": "One analog, several words",
    "principle": "At the end of a word this sound is spelled <b>ay</b>. Inside a word it is spelled <b>ai</b>. Three verbs add "
                 "a bare <b>d</b> for the past. The d closes the word, so <b>ay</b> turns to <b>ai</b>.",
    # (word, its sum, a sentence)
    "words": [("say", "say", "I say yes."), ("says", "say + s", "She says yes."), ("said", "sa(y&rarr;i) + d", "He said no."),
              ("pay", "pay", "We pay here."), ("paid", "pa(y&rarr;i) + d", "I paid for it."),
              ("lay", "lay", "Hens lay eggs."), ("laid", "la(y&rarr;i) + d", "The hen laid an egg.")],
    "contrast": ("Most verbs that end in <b>ay</b> keep the y and add <b>ed</b>.",
                 [("play", "play", ""), ("played", "play + ed", ""), ("stay", "stay", ""), ("stayed", "stay + ed", "")]),
    "listen": "<i>Says</i> and <i>said</i> are said with the e of <i>bed</i>. The spelling still shows <i>say</i>.",
    "build": ["say + s", "say + d", "pay + d", "lay + d", "play + ed", "stay + ed"],
    "use": [("Yesterday she", "say", "hello."), ("He", "pay", "for lunch."), ("The hen", "lay", "an egg."), ("We", "play", "outside.")],
    "check": [("re + pay + d", "repaid"), ("mis + lay + d", "mislaid"), ("un + say + d", "unsaid"), ("pray + ed", "prayed"), ("delay + ed", "delayed")],
    "notes": [
        "<i>Said</i>, <i>paid</i> and <i>laid</i> are built the same way: the y becomes i and a bare d is added. That build is "
        "itself the exception. Other verbs in <i>-ay</i> keep the y and add <i>-ed</i>: <i>played</i>, <i>stayed</i>, "
        "<i>prayed</i>, <i>delayed</i>. Brooks calls <i>laid</i> and <i>paid</i> &ldquo;irregularly-spelt (but not "
        "irregularly-pronounced)&rdquo; (p. 196).",
        "A reason for the i still shows. <i>ay</i> is the spelling at the end of a word, and <i>ai</i> never ends a word "
        "(Brooks, p. 191). Once d closes the word, the vowel takes its inside spelling. <i>Daily</i>, <i>gaily</i>, <i>lain</i> "
        "and <i>slain</i> do the same (Brooks, p. 230).",
        "<i>Said</i> and <i>says</i> also shift their vowel. <i>Do</i> does the same in <i>does</i> and <i>done</i>. The spelling "
        "keeps the base and the sound moves, so these are words to spell by their family, not by their sound.",
        "The check uses words that aren&rsquo;t on the list. A learner who writes <i>repaid</i> and <i>mislaid</i> has the "
        "convention; one who writes <i>prayed</i> and <i>delayed</i> has its limit too.",
    ],
    "links": [("Step 22", "steps/22.html", "where <i>said</i> sits on the route"), ("Step 13", "steps/13.html", "<i>played</i>, and a suffix at the seam"),
              ("Sentences", "constructions.html", "frames to say the words in")],
    "source": "Greg Brooks, <i>Dictionary of the British English Spelling System</i> (2015), pp. 191, 196 and 230; the "
              "analysis is from the atlas&rsquo;s manual, &ldquo;Say, pay, lay&rdquo;.",
    "desc": "A spelling list of seven words: say, says, said, pay, paid, lay, laid, with the convention that explains them, words to build, sentences, and a check.",
}, {
    "slug": "hap", "title": "hap: happy, happen, mishap", "kind": "One base, many joins",
    "principle": "<b>Hap</b> is an old word for luck. Before a vowel it is written <b>happ</b>, so the a stays short. Before a "
                 "consonant, or at the end of a word, it is <b>hap</b>.",
    "words": [("happy", "hap + p + y", "I am happy."), ("happier", "hap + p + (y&rarr;i) + er", "She is happier now."),
              ("happily", "hap + p + (y&rarr;i) + ly", "They played happily."), ("unhappy", "un + hap + p + y", "He was unhappy."),
              ("happen", "hap + p + en", "What will happen?"), ("mishap", "mis + hap", "It was a small mishap."),
              ("hapless", "hap + less", "The hapless cat fell in.")],
    "contrast": ("The p doubles only before a vowel.", [("happen", "hap + p + en", ""), ("hapless", "hap + less", ""), ("sunny", "sun + n + y", ""), ("sun", "sun", "")]),
    "build": ["hap + y", "hap + y + er", "un + hap + y", "hap + en", "mis + hap", "hap + less"],
    "use": [("She smiled", "happy + ly", "."), ("He is", "happy + er", "than before."), ("Did anything", "hap + en", "?"), ("It was only a", "mis + hap", ".")],
    "check": [("hap + y + ness", "happiness"), ("hap + en + ed", "happened"), ("per + hap + s", "perhaps"), ("un + hap + y + ly", "unhappily")],
    "notes": [
        "Every word here has the same base, with the same meaning, so the family shows the seam that <i>happy</i> alone hides: "
        "hap + y, having luck. The double p isn&rsquo;t a second sound. It keeps the a short before the vowel that follows.",
        "In <i>mishap</i> the s and the h meet across a seam, so they don&rsquo;t spell <i>sh</i>.",
        "The check asks for the y to turn to i (<i>happiness</i>, <i>unhappily</i>) and for <i>perhaps</i>, where hap is in the "
        "middle with one p.",
    ],
    "links": [("The hap family", "roots/hap.html", "all its words, and why <i>happy</i> has two p&rsquo;s"), ("Step 14", "steps/14.html", "the box blocks the vault"),
              ("Step 29", "steps/29.html", "y turns to i")],
    "source": "Etymonline, <i>hap</i> and <i>happy</i>; Edward Carney, <i>A Survey of English Spelling</i> (1994), pp. 1&ndash;3, on <i>happy</i> among the doubles.",
    "desc": "A spelling list on one base: happy, happier, happily, unhappy, happen, mishap, hapless, with why the p doubles in some and not in others.",
}, {
    "slug": "the-e-drops", "title": "the e drops: making, hoping, icy", "kind": "One join, many bases",
    "principle": "A suffix that starts with a vowel takes the place of a silent <b>e</b>. Out with the old, in with the new: "
                 "the new vowel does the e&rsquo;s job.",
    "words": [("making", "mak(e) + ing", "I am making lunch."), ("taking", "tak(e) + ing", "She is taking a turn."),
              ("giving", "giv(e) + ing", "He is giving it back."), ("having", "hav(e) + ing", "We are having fun."),
              ("racing", "rac(e) + ing", "They are racing home."), ("hoping", "hop(e) + ing", "I am hoping for snow."),
              ("icy", "ic(e) + y", "The road is icy.")],
    "contrast": ("With no e to drop, a short word doubles its last letter instead.", [("hope", "hope", ""), ("hoping", "hop(e) + ing", ""), ("hop", "hop", ""), ("hopping", "hop + p + ing", "")]),
    "build": ["make + ing", "hope + ing", "hop + ing", "race + ing", "ice + y", "give + ing"],
    "use": [("She is", "make + ing", "a card."), ("The frog is", "hop + ing", "away."), ("We are", "hope + ing", "to win."), ("The path was", "ice + y", ".")],
    "check": [("bake + ing", "baking"), ("ride + ing", "riding"), ("shine + y", "shiny"), ("hope + ful", "hopeful"), ("like + ly", "likely")],
    "notes": [
        "The e of <i>make</i> sends the vault that keeps the a long. In <i>making</i> the i stands where the e stood and sends "
        "it. In <i>racing</i> and <i>icy</i> the new vowel also keeps the c soft.",
        "<i>Giving</i> and <i>having</i> drop an e that had a different job: keeping v off the end of the word. Once a suffix "
        "follows, the v isn&rsquo;t at the end.",
        "The check ends with two words where the e stays, <i>hopeful</i> and <i>likely</i>: the suffix starts with a consonant, "
        "so nothing new arrives to do the e&rsquo;s job.",
    ],
    "links": [("Step 15", "steps/15.html", "the e drops, its jobs move"), ("Out with the old, in with the new", "sessions/out-with-the-old.html", "the presentation"),
              ("-ing in Parts", "parts.html#p-suf-ing", "every word with it")],
    "source": "Edward Carney, <i>A Survey of English Spelling</i> (1994): the e drops before an ending that begins with a vowel, p. 130.",
    "desc": "A spelling list on one join: making, taking, giving, having, racing, hoping, icy, with hoping beside hopping.",
}, {
    "slug": "this-that-then", "title": "this, that, these, those, then, there", "kind": "A closed set",
    "principle": "These are the pointing words. Each starts with <b>th</b>, said with a buzz, and each has a partner: one or "
                 "many, near or far, a time or a place.",
    "words": [("this", "", "This one is mine."), ("these", "", "These are mine."), ("that", "", "That one is yours."),
              ("those", "", "Those are yours."), ("then", "", "First we eat, then we play."), ("there", "", "Put it over there.")],
    "contrast": ("Swap <b>th</b> for <b>wh</b> and a pointing word becomes an asking word.", [("then", "then", ""), ("when", "when", ""), ("there", "there", ""), ("where", "where", ""), ("that", "that", ""), ("what", "what", "")]),
    "build_h": "Swap the start",
    "build": ["then, with wh", "there, with wh", "that, with wh", "when, with th", "where, with th", "what, with th"],
    "use": [("I like", "this or these", "apple in my hand."), ("Look at", "that or those", "birds over the hill."), ("We ate, and", "then or there", "we went out."), ("Put the box over", "then or there", ".")],
    "check": [("th + em", "them"), ("th + an", "than"), ("th + ey", "they"), ("wh + ich", "which")],
    "notes": [
        "This is a closed set: a few words that do one job and share a spelling, learned together. There is no join to build, "
        "so the work is the pairs: <i>this</i> and <i>these</i>, <i>that</i> and <i>those</i>, <i>then</i> and <i>there</i>.",
        "The swap with <i>wh</i> is real history as well as a pattern. English built its pointing words on th and its asking "
        "words on wh: <i>then</i> and <i>when</i>, <i>there</i> and <i>where</i>, <i>that</i> and <i>what</i>.",
        "The th in every one of these has its voiced sound, as in <i>the</i>. In most other words th is unvoiced, as in "
        "<i>thin</i>.",
    ],
    "links": [("Step 28", "steps/28.html", "the th and wh family"), ("Sentences", "constructions.html", "where these words work")],
    "source": "Edward Carney, <i>A Survey of English Spelling</i> (1994): the voiced th of <i>the</i>, <i>this</i>, <i>these</i>, <i>that</i>, <i>those</i>, <i>then</i> and <i>there</i>, p. 232.",
    "desc": "A spelling list on a closed set: this, these, that, those, then, there, with their partners in wh.",
}]
PAGES = [(f"lists/{L['slug']}.html", "teachers", f"Spelling list: {L['title']}", L["desc"]) for L in LISTS]


def write(OUT, page, header, footer, X):
    (OUT / "lists").mkdir(exist_ok=True)
    LW, SC = X["LW"], X["SC"]
    def drawn(w, F=40):
        if w in LW.W and w not in SC.UNMARKED: return X["svg_of"](w, F, label=f"{w}, marked")
        return f'<span class="plain" style="font-size:{F}px">{html.escape(w)}</span>'
    for L in LISTS:
        rows = "".join(f'<tr><td class="lw">{drawn(w)}</td>' + (f'<td class="ls">{s} &rarr; <i>{w}</i></td>' if s else "") + f'<td class="lsent">{sent}</td></tr>' for w, s, sent in L["words"])
        ctext, cwords = L["contrast"]
        crow = "".join(f'<figure class="word">{drawn(w, 36)}<figcaption>{s}</figcaption></figure>' for w, s, _ in cwords)
        build = "".join(f'<li><span>{b} &rarr;</span><span class="blank"></span></li>' for b in L["build"])
        use = "".join(f'<li>{a} <span class="blank short"></span> <span class="hint">({v})</span> {z}</li>' for a, v, z in L["use"])
        check = "".join(f'<li><span>{b} &rarr;</span><span class="blank"></span><span class="ans t-only">{html.escape(a)}</span></li>' for b, a in L["check"])
        links = "".join(f'<li><a href="../{u}">{t}</a>: {what}</li>' for t, u, what in L["links"])
        body = f"""{header(1)}
<main class="list-page">
<section class="hero"><div class="wrap">
<p class="eyebrow t-only">Spelling list &middot; {L["kind"]}</p>
<h1>{L["title"]}</h1>
<p class="lprinciple">{L["principle"]}</p>
<p class="board t-only noprint"><a href="#" onclick="window.print(); return false;">Print this list</a>: the teacher&rsquo;s notes are left off.</p>
</div></section>
<section class="about"><div class="wrap">
<h2>The words</h2>
<table class="ltable"><tbody>{rows}</tbody></table>
{f'<p class="llisten">{L["listen"]}</p>' if L.get("listen") else ""}
<h2>The contrast</h2>
<p class="sub">{ctext}</p>
<div class="words rrow">{crow}</div>
</div></section>
<section class="about lwork"><div class="wrap">
<div><h2>{L.get("build_h", "Build it")}</h2><ol class="lblanks">{build}</ol></div>
<div><h2>Use it</h2><ol class="lblanks use">{use}</ol></div>
<div><h2>Check: not on the list</h2><ol class="lblanks">{check}</ol></div>
</div></section>
<section class="about t-only noprint"><div class="wrap prose">
<h2>For the teacher</h2>
{"".join(f"<p>{n}</p>" for n in L["notes"])}
<p>{"Have the learner build each word from its sum, not copy it, and say" if any(s for _, s, _ in L["words"]) else "Have the learner say"} each sentence before writing it. Six to eight words is the whole list: the convention is what&rsquo;s being learned.</p>
<ul>{links}</ul>
<p class="sub">Source: {L["source"]}</p>
{X["uc"]("the first four spelling lists are models, one of each kind. Next: a list from each step and each family, made from what the site already holds.")}
</div></section>
</main>
{footer(1)}"""
        (OUT / "lists" / f"{L['slug']}.html").write_text(page(f"Spelling list: {L['title']} · Sound and Word Atlas", body, 1, L["desc"]), encoding="utf-8")
    print(f"wrote {len(LISTS)} spelling list(s)")
    return [(p, t) for p, _, t, _ in PAGES]
