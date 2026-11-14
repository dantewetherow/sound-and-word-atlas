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
import html, re

LISTS = [{
    "slug": "open-or-closed", "group": "step", "n": 1, "title": "open or closed: I, it, in, is, if", "kind": "A step&rsquo;s pattern",
    "principle": "A vowel at the end of a syllable is <b>open</b>: it says its name, as <b>I</b> does. A consonant after it "
                 "<b>closes</b> it, and it says its short sound: <b>it</b>, <b>in</b>, <b>is</b>, <b>if</b>.",
    "words": [("I", "", "I can run."), ("hi", "", "Say hi to Sam."), ("it", "", "It is red."), ("in", "", "Come in."),
              ("is", "", "She is here."), ("if", "", "Ask if you can go."), ("him", "", "Give it to him."), ("his", "", "That is his hat.")],
    "contrast": ("Open, the i says its name. Close it with a consonant and it goes short.",
                 [("I", "I", ""), ("it", "it", ""), ("hi", "hi", ""), ("hit", "hit", "")]),
    "listen": "In <i>is</i> and <i>his</i> the s says /z/. It still closes the syllable.",
    "build_h": "Close it",
    "build": ["I, closed with t", "I, closed with n", "I, closed with f", "hi, closed with t", "hi, closed with m", "hi, closed with s"],
    "use": [("Come", "in or it", "and sit down."), ("Ask", "if or is", "you can play."), ("That is", "him or his", "bike."), ("Say", "hi or him", "to Mom.")],
    "check": [("s + i + t", "sit"), ("w + i + n", "win"), ("k + i + d", "kid"), ("f + i + nd", "find")],
    "notes": [
        "Step 1 has one vowel and one idea. At the end of a syllable the vowel is open and says its name; a consonant after "
        "it closes it and it says its short sound. <i>I</i> is open; <i>it</i>, <i>in</i>, <i>is</i> and <i>if</i> are closed.",
        "<i>Hi</i> is the same open i with a consonant in front. Closing it gives <i>hit</i>, <i>him</i> and <i>his</i>: the "
        "same move as <i>I</i> to <i>it</i>, so the Close it column is the step&rsquo;s whole lesson in six words.",
        "<i>I</i> is the one word that is always a capital, wherever it falls in a sentence.",
        "The check uses words that aren&rsquo;t on the list. <i>Sit</i>, <i>win</i> and <i>kid</i> are closed the same way. "
        "<i>Find</i> is where the idea stops: before <i>nd</i> the i stays long though the syllable is closed. That waits for "
        "step 18, and a learner who writes it correctly has met it somewhere else.",
    ],
    "links": [("Step 1", "steps/01.html", "open or closed, on the path"), ("Step 4", "steps/04.html", "one consonant closes it"),
              ("Step 18", "steps/18.html", "long before two consonants: <i>find</i>")],
    "source": "Edward Carney, <i>A Survey of English Spelling</i> (1994): short vowels can&rsquo;t end an open syllable and long "
              "vowels can, p. 134; short i, p. 135; long i, p. 151; s for /z/, p. 238; <i>find</i> and <i>kind</i>, pp. 332&ndash;333.",
    "desc": "A spelling list for step 1: I, hi, it, in, is, if, him, his, open against closed, with words to close, sentences and a check.",
}, {
    "slug": "say-pay-lay", "pattern": 1, "title": "say, pay, lay", "kind": "One analog, several words",
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
    "links": [("Step 22", "steps/22.html", "where <i>said</i> sits on the path"), ("Step 13", "steps/13.html", "<i>played</i>, and a suffix at the seam"),
              ("Sentences", "constructions.html", "frames to say the words in")],
    "source": "Greg Brooks, <i>Dictionary of the British English Spelling System</i> (2015), pp. 191, 196 and 230; the "
              "analysis is from the manual, &ldquo;Say, pay, lay&rdquo;.",
    "desc": "A spelling list of seven words: say, says, said, pay, paid, lay, laid, with the convention that explains them, words to build, sentences, and a check.",
}, {
    "slug": "hap", "group": "family", "root": "hap", "pattern": 2, "title": "hap: happy, happen, mishap", "kind": "One base, many joins",
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
    "slug": "the-e-drops", "group": "step", "n": 15, "pattern": 3, "title": "the e drops: making, hoping, icy", "kind": "One join, many bases",
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
    "slug": "this-that-then", "group": "step", "n": 28, "pattern": 4, "title": "this, that, these, those, then, there", "kind": "A closed set",
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
import step_lists                 # a list for every other step and family (12 November 2026)
LISTS += step_lists.STEP_LISTS
# The kinds of list, four of them; each model list stands for one.
KINDS = [(1, "One analog, several words", "One word&rsquo;s spelling carries to others that rhyme with it, letter for letter."),
         (2, "One base, many joins", "One base and the prefixes and suffixes that join it."),
         (3, "One join, many bases", "One way that a suffix joins, tried on many bases."),
         (4, "A closed set", "A small set of words that work together and change together.")]
INDEX_DESC = "Spelling lists that follow the path: one for each step and each word family, each with a check, and the four kinds of list they are made from."
PAGES = [("lists/index.html", "teachers", "Legomorphic spelling", INDEX_DESC),
         ("lists/hearts.html", "teachers", "Spelling list: Words with a heart", "Heart words sorted by how much of the heart a learner can lose: regular on the path, a reason to use, or by heart."),
         ("lists/apart.html", "teachers", "Spelling list: Spelled apart", "Words that sound the same and are spelled differently, marked side by side and sorted by why the spelling keeps them apart.")]
PAGES += [(f"lists/{L['slug']}.html", "teachers", f"Spelling list: {L['title']}", L["desc"]) for L in LISTS]
HAS_CHECK = " It comes with a check to give before and after the lesson."


# A generalization check for a list (lists/<slug>-check.html): words to dictate before the lesson, after it, and a few
# weeks later. Four groups: taught words (was the list learned?), transfer words that were never on the list (did the
# convention generalize, and does the learner know where it stops?), invented words (which nobody can have seen), and
# control words that have nothing to do with the lesson (these shouldn't improve; if they do as much as the transfer
# words, something other than the lesson is at work). Each word is scored twice: the whole word, and the target feature.
# (word, group, sentence, the feature to look for)
CHECKS = {
    "the-e-drops": {
        "title": "the e drops",
        "feature": "Is the silent e gone before a vowel suffix, and kept before a consonant suffix?",
        "items": [
            ("baking", "transfer", "We are baking bread.", "no e before ing: not <i>bakeing</i>"),
            ("cabin", "control", "They stayed in a cabin.", ""),
            ("making", "taught", "I am making lunch.", "no e before ing"),
            ("hopeful", "limit", "She felt hopeful.", "the e is kept: not <i>hopful</i>"),
            ("shiny", "transfer", "The coin is shiny.", "no e before y: not <i>shiney</i>"),
            ("lemon", "control", "He cut a lemon.", ""),
            ("racing", "taught", "They are racing home.", "no e before ing"),
            ("riding", "transfer", "He is riding a bike.", "no e, and one d: not <i>rideing</i> or <i>ridding</i>"),
            ("river", "control", "The river is cold.", ""),
            ("hoping", "taught", "I am hoping for snow.", "no e, and one p: not <i>hopeing</i> or <i>hopping</i>"),
            ("safely", "limit", "We got home safely.", "the e is kept: not <i>safly</i>"),
            ("smiling", "transfer", "The baby is smiling.", "no e before ing: not <i>smileing</i>"),
            ("seven", "control", "I have seven cards.", ""),
            ("icy", "taught", "The road is icy.", "no e before y: not <i>icey</i>"),
        ],
        # invented words: the base is printed on the sheet, so only the join is being tested
        "invented": [("zake + ing", "zaking", "no e before ing", None), ("plome + ing", "ploming", "no e before ing", None)],
        "score_eg": "A learner who writes <i>bakin</i> has the feature and not the word.",
        "desc": "A check for the list 'the e drops': fourteen words to dictate and two invented ones, before and after the lesson, with a scoring key.",
    },
}
GROUPS = [("taught", "Taught", "On the list. Was the list learned?"),
          ("transfer", "Transfer", "Not on the list, same convention. Did it generalize?"),
          ("limit", "Limit", "Not on the list, where the convention stops. Was it over-learned?"),
          ("invented", "Invented", "Made-up words nobody has seen. Only the convention can get these right."),
          ("control", "Control", "Nothing to do with the lesson. These shouldn&rsquo;t change much.")]
import checks                     # a check for every other list (12 November 2026)
CHECKS.update(checks.build(LISTS))
# A check belongs to its list: the list's page leads to it, and the shelf shows only the lists.
PAGES[:] = [(p, d, t_, s + (HAS_CHECK if p[6:-5] in CHECKS else "")) for p, d, t_, s in PAGES]
PAGES += [(f"lists/{s}-check.html", "teachers", f"Check: {C['title']}", C["desc"]) for s, C in CHECKS.items()]
import ufli_lists                 # lined up with UFLI Foundations by lesson number (12 November 2026)
PAGES += ufli_lists.PAGES


def home_link(L, what="list"):
    """The list's home, from its first link: the step it belongs to, with the step's title, or its family's page."""
    t, u, _ = L["links"][0]
    if u.startswith("steps/"):
        st = step_lists.STEPS[int(u[6:8])]
        t = f"Step {st['n']}: " + re.sub(r"\*([^*]+)\*", r"<i>\1</i>", st["title"])
    return f'This {what} goes with <a href="../{u}">{t}</a>.'


def write_check(OUT, page, header, footer, X, slug, C):
    n = len(C["items"])
    blanks = "".join(f'<li><span class="blank long"></span></li>' for _ in C["items"])
    inv = "".join(f'<li><span>{p} &rarr;</span><span class="blank long"></span></li>' if p else '<li><span class="blank long"></span></li>' for p, *_ in C["invented"])
    printed = any(p for p, *_ in C["invented"])
    label = {g: l for g, l, _ in GROUPS}
    key = "".join(f'<tr><td>{k + 1}</td><td><b>{w}</b></td><td>{sent}</td><td>{label[g]}</td><td>{f or "whole word only"}</td></tr>' for k, (w, g, sent, f) in enumerate(C["items"]))
    key += "".join(f'<tr><td>{n + k + 1}</td><td><b>{a}</b></td><td>{f"(printed: {p})" if p else f"Say: {say}"}</td><td>Invented</td><td>{f}</td></tr>' for k, (p, a, f, say) in enumerate(C["invented"]))
    count = {g: sum(1 for it in C["items"] if it[1] == g) for g, _, _ in GROUPS}; count["invented"] = len(C["invented"])
    tally = "".join(f'<tr><td><b>{l}</b> <span class="of">of {count[g]}</span><span class="why">{why}</span></td>' + "<td></td>" * 6 + "</tr>" for g, l, why in GROUPS if count[g])
    body = f"""{header(1)}
<main class="list-page check-page">
<section class="hero noprint"><div class="wrap">
<p class="eyebrow"><a href="{slug}.html">&larr; The spelling list: {C["title"]}</a></p>
<p class="lhome">{home_link(next(L for L in LISTS if L["slug"] == slug), "check")}</p>
<h1>Check: {C["title"]}</h1>
<p class="lprinciple">{C["feature"]}</p>
<p class="board"><a href="#" onclick="window.print(); return false;">Print the check</a>: a sheet for the learner, then the words to say and the key.</p>
</div></section>
<section class="about csheet"><div class="wrap">
<h2>Spelling check <span class="cname">Name <span class="blank long"></span> Date <span class="blank"></span></span></h2>
<p class="sub">Write each word you hear.</p>
<ol class="lblanks ccols">{blanks}</ol>
{f"""<p class="sub">{"These are made-up words. Add the ending." if printed else "These are made-up words. Write each one you hear."}</p>
<ol class="lblanks" start="{n + 1}">{inv}</ol>""" if C["invented"] else ""}
</div></section>
<section class="about cteach"><div class="wrap">
<h2>To say, and the key</h2>
<p class="sub">Say the word, then the sentence, then the word again.{(" For the made-up words, say: &ldquo;These are made-up words. The first part is printed for you. Add the ending and write the whole word.&rdquo;" if printed else " For the made-up words, say: &ldquo;These are made-up words. Write each one the way you think it&rsquo;s spelled.&rdquo; Say each once more if asked.") if C["invented"] else ""} Don&rsquo;t teach these words between checks.</p>
<p class="sub">Score each word twice: the whole word right, and the feature right. {C.get("score_eg", "A learner can have the feature right and the word wrong, or the other way round.")}{"" if C["invented"] else C.get("no_inv", "")}</p>
<div class="cscroll"><table class="ctable ckey"><thead><tr><th></th><th>Word</th><th>Sentence</th><th>Group</th><th>The feature to look for</th></tr></thead><tbody>{key}</tbody></table></div>
<h2>The tally</h2>
<div class="cscroll"><table class="ctable ctally"><thead><tr><th rowspan="2">Group</th><th colspan="2">Before</th><th colspan="2">After</th><th colspan="2">Weeks later</th></tr>
<tr><th>word</th><th>feature</th><th>word</th><th>feature</th><th>word</th><th>feature</th></tr></thead><tbody>{tally}</tbody></table></div>
</div></section>
<section class="about noprint"><div class="wrap prose">
<h2>Reading the result</h2>
<p>Give the check before the lesson, after it, and again a few weeks later. The lesson worked if the transfer and invented words rise and the control words don&rsquo;t rise as much. If everything rises together, something other than the lesson did it. If the limit words fall, the convention was over-learned: it is being used where it doesn&rsquo;t belong.</p>
<p>Use words the learners already say. If most can spell a word beforehand, it can&rsquo;t show anything; swap it for another of the same kind.</p>
<p>With two classes, compare the gain on transfer words against the gain on control words in each. That is suggestive, not proof: the classes differ in more than the lesson. A stronger design needs only one class: teach three lessons in turn, give all three checks each time, and see whether each set of transfer words rises only after its own lesson.</p>
<p>Keep learners&rsquo; results in the school&rsquo;s own records. Nothing here collects them.</p>
{X["uc"]("the check for &lsquo;the e drops&rsquo; was made first, as a model; since 12 November 2026 every list has one, made the same way. None has been tried in a class yet. The control words come from three small sets by level and haven&rsquo;t been matched to the others for how common they are.")}
</div></section>
</main>
{footer(1)}"""
    (OUT / "lists" / f"{slug}-check.html").write_text(page(f"Check: {C['title']} · A Legend for English Words", body, 1, C["desc"]), encoding="utf-8")


def write(OUT, page, header, footer, X):
    (OUT / "lists").mkdir(exist_ok=True)
    LW, SC = X["LW"], X["SC"]
    def drawn(w, F=40):
        if "&" in w and html.unescape(w) in LW.W: w = html.unescape(w)      # I&rsquo;m: the contractions are coded with ’
        if w in LW.W and w not in SC.UNMARKED: return X["svg_of"](w, F, label=f"{w}, marked")
        return f'<span class="plain" style="font-size:{F}px">{w if "&" in w else html.escape(w)}</span>'
    for L in LISTS:
        sums = any(s and s != w for w, s, _ in L["words"])
        rows = "".join(f'<tr><td class="lw">{drawn(w)}</td>' + ((f'<td class="ls">{s} &rarr; <i>{w}</i></td>' if s and s != w else '<td class="ls"></td>') if sums else "") + f'<td class="lsent">{sent}</td></tr>' for w, s, sent in L["words"])
        ctext, cwords = L["contrast"]
        crow = "".join(f'<figure class="word">{drawn(w, 36)}<figcaption>{s if s != w else ""}</figcaption></figure>' for w, s, _ in cwords)
        build = "".join(f'<li><span>{b} &rarr;</span><span class="blank"></span></li>' for b in L["build"])
        use = "".join(f'<li>{a} <span class="blank short"></span> <span class="hint">({v})</span> {z}</li>' for a, v, z in L["use"])
        check = "".join(f'<li><span>{b} &rarr;</span><span class="blank"></span><span class="ans t-only">{a}</span></li>' for b, a in L["check"])
        links = "".join(f'<li><a href="../{u}">{t}</a>: {what}</li>' for t, u, what in L["links"])
        body = f"""{header(1)}
<main class="list-page">
<section class="hero"><div class="wrap">
<p class="eyebrow t-only"><a href="index.html">Legomorphic spelling</a> &middot; {L["kind"]}</p>
<h1>{L["title"]}</h1>
<p class="lprinciple">{L["principle"]}</p>
<p class="lhome noprint">{home_link(L)}</p>
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
{f"""<section class="about t-only noprint lcheck"><div class="wrap">
<h2>Did it generalize?</h2>
<p class="sub">This list has a check: {len(CHECKS[L["slug"]]["items"]) + len(CHECKS[L["slug"]]["invented"])} words to give before the lesson, after it, and a few weeks later. Most of them aren&rsquo;t on the list, so it shows whether the convention was learned or only the words.</p>
<p><a class="btn" href="{L["slug"]}-check.html">Open the check</a></p>
</div></section>""" if L["slug"] in CHECKS else ""}
<section class="about t-only noprint"><div class="wrap prose">
<h2>For the teacher</h2>
{"".join(f"<p>{n}</p>" for n in L["notes"])}
<p>{"Have the learner build each word from its sum, not copy it, and say" if sums else "Have the learner say"} each sentence before writing it. Six to eight words is the whole list: the convention is what&rsquo;s being learned.</p>
<ul>{links}</ul>
<p class="sub">Source: {L["source"]}</p>
{X["uc"]("since 12 November 2026 every step and every family has a list. The four model lists were made first, one of each kind; the rest follow them and haven&rsquo;t been tried in a class yet. Each has a generalization check, also untried.")}
</div></section>
</main>
{footer(1)}"""
        (OUT / "lists" / f"{L['slug']}.html").write_text(page(f"Spelling list: {L['title']} · A Legend for English Words", body, 1, L["desc"]), encoding="utf-8")
    for slug, C in CHECKS.items(): write_check(OUT, page, header, footer, X, slug, C)
    X["ufli_lists"] = ufli_lists.write(OUT, page, header, footer, X)
    import heart_words
    X["heart_words"] = heart_words.write(OUT, page, header, footer, X)
    import apart
    X["heart_words"] = sorted(set(X["heart_words"]) | set(apart.write(OUT, page, header, footer, X)))
    write_index(OUT, page, header, footer, X)
    print(f"wrote {len(LISTS)} spelling list(s), {len(CHECKS)} check(s)")
    return [(p, t) for p, _, t, _ in PAGES]


def write_index(OUT, page, header, footer, X):
    """lists/index.html: the one door to the lists. Steps by number, families by root, and the four kinds of list."""
    md = lambda t: re.sub(r"\*([^*]+)\*", r"<i>\1</i>", t)
    by_n = {L["n"]: L for L in LISTS if L.get("group") == "step"}
    steps = "".join(f'<a class="sbtn" href="{by_n[st["n"]]["slug"]}.html"><b>Step {st["n"]}</b><span>{md(st["title"])}</span></a>'
                    for st in step_lists.ROUTE["steps"] if st["n"] in by_n)
    fams = "".join(f'<a class="dtile" href="{L["slug"]}.html"><b>{L["root"]}</b><span>{", ".join(w for w, _, _ in L["words"][:5])}</span></a>'
                   for L in LISTS if L.get("group") == "family")
    model = {L["pattern"]: L for L in LISTS if L.get("pattern")}
    kinds = "".join(f'<a class="dtile" href="{model[k]["slug"]}.html"><b>{name}</b><span>{why} The model: <i>{model[k]["title"]}</i>.</span></a>'
                    for k, name, why in KINDS)
    body = f"""{header(1)}
<main class="lists-index">
<section class="hero"><div class="wrap">
<h1>Legomorphic spelling</h1>
<p class="lead">Spelling lists that follow the path: one for every step and every word family. Each has six to eight words with sentences, a contrast, words to build, sentences to finish, and a check of words that aren&rsquo;t on the list. Print one and the teacher&rsquo;s notes are left off. Each list also has a generalization check, to give before the lesson, after it and a few weeks later: its list&rsquo;s page leads to it.</p>
</div></section>
<section class="about"><div class="wrap">
<h2>Steps</h2>
<p class="sub">The list for each step on the path, in order.</p>
<div class="step-btns">{steps}</div>
</div></section>
<section class="about" id="ufli"><div class="wrap">
<h2>Lined up with UFLI Foundations</h2>
<p class="sub">For schools that run UFLI: where its lessons meet the path, the mark to draw alongside each part of UFLI, and short word lists by lesson number. They live with everything else for UFLI.</p>
<div class="door-tiles"><a class="dtile" href="../ufli.html"><b>UFLI Foundations</b><span>UFLI&rsquo;s lessons in sixteen bands, each with the mark to add and an example or two marked, and why the two orders differ.</span></a></div>
</div></section>
<section class="about" id="hearts"><div class="wrap">
<h2>Words with a heart, and words spelled apart</h2>
<p class="sub">The words programs teach as heart words, sorted by how much of the heart a learner can lose; and words that sound the same and are spelled differently, sorted by why.</p>
<div class="door-tiles"><a class="dtile" href="hearts.html"><b>Words with a heart</b><span>Regular on the path, a reason to use, or by heart: each word marked so the reason shows.</span></a>
<a class="dtile" href="apart.html"><b>Spelled apart</b><span>Words that sound the same and are spelled differently, side by side: a short word and a long one, a letter kept from the family, or history.</span></a></div>
</div></section>
<section class="about" id="families"><div class="wrap">
<h2>Families</h2>
<p class="sub">Extension work, for intermediate and middle school: one root, many words. Each list takes its word sums from the family&rsquo;s page. The <a href="../tents.html">affix tent cards</a> go with them.</p>
<div class="door-tiles">{fams}</div>
</div></section>
<section class="about"><div class="wrap">
<h2>Patterns</h2>
<p class="sub">Every list is one of four kinds. The first lists were made as models, one of each.</p>
<div class="door-tiles">{kinds}</div>
<p class="sub">The steps and families mix the kinds: a step about a suffix is one join, many bases; a family is one base, many joins.</p>
<p class="sub">Keep learners&rsquo; results in the school&rsquo;s own records. Nothing here collects them.</p>
</div></section>
</main>
{footer(1)}"""
    (OUT / "lists" / "index.html").write_text(page("Legomorphic spelling · A Legend for English Words", body, 1, INDEX_DESC), encoding="utf-8")
