"""Spelling lists (lists/<slug>.html), made 10 November 2026. The first is the model: say, pay, lay.

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
}]
PAGES = [(f"lists/{L['slug']}.html", "teachers", f"Spelling list: {L['title']}", L["desc"]) for L in LISTS]


def write(OUT, page, header, footer, X):
    (OUT / "lists").mkdir(exist_ok=True)
    LW, SC = X["LW"], X["SC"]
    def drawn(w, F=40):
        if w in LW.W and w not in SC.UNMARKED: return X["svg_of"](w, F, label=f"{w}, marked")
        return f'<span class="plain" style="font-size:{F}px">{html.escape(w)}</span>'
    for L in LISTS:
        rows = "".join(f'<tr><td class="lw">{drawn(w)}</td><td class="ls">{s} &rarr; <i>{w}</i></td><td class="lsent">{sent}</td></tr>' for w, s, sent in L["words"])
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
<p class="llisten">{L["listen"]}</p>
<h2>The contrast</h2>
<p class="sub">{ctext}</p>
<div class="words rrow">{crow}</div>
</div></section>
<section class="about lwork"><div class="wrap">
<div><h2>Build it</h2><ol class="lblanks">{build}</ol></div>
<div><h2>Use it</h2><ol class="lblanks use">{use}</ol></div>
<div><h2>Check: not on the list</h2><ol class="lblanks">{check}</ol></div>
</div></section>
<section class="about t-only noprint"><div class="wrap prose">
<h2>For the teacher</h2>
{"".join(f"<p>{n}</p>" for n in L["notes"])}
<p>Have the learner build each word from its sum, not copy it, and say each sentence before writing it. Six to eight words is the whole list: the convention is what&rsquo;s being learned.</p>
<ul>{links}</ul>
<p class="sub">Source: {L["source"]}</p>
{X["uc"]("this is the first spelling list, made as a model. Next: a list from each step and each family, made from what the site already holds.")}
</div></section>
</main>
{footer(1)}"""
        (OUT / "lists" / f"{L['slug']}.html").write_text(page(f"Spelling list: {L['title']} · Sound and Word Atlas", body, 1, L["desc"]), encoding="utf-8")
    print(f"wrote {len(LISTS)} spelling list(s)")
    return [(p, t) for p, _, t, _ in PAGES]
