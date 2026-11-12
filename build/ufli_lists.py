"""Spelling lists lined up with UFLI Foundations, by lesson number (12 November 2026): lists/ufli-NN.html.

UFLI's copyright statement says Toolbox items that carry its copyright notice can't be altered, reposted or used to make
other materials, so none of these words is taken from UFLI's materials. Each list has a lesson number and our own
description of what the lesson adds; the words are ours. They were found by a script (not part of the build) that ran
through common English words (wordfreq) and kept those that CMUdict says are spoken sound for sound as spelled with
only the spellings UFLI has taught by that lesson, and that use the lesson's new one. The lists below were then chosen
by hand from what it found: one-syllable words until the syllable lessons, no names, nothing a learner shouldn't say
in class. Review lessons have no list of their own.

So far these cover the kindergarten lessons (to 68). The grade 1 and 2 lessons follow the same way.

(lesson, our description, list words, check words, optional sums {word: sum})"""
import html, json, pathlib, re
import ufli_lessons
HERE = pathlib.Path(__file__).resolve().parent
UFLI_HOME = "https://ufli.education.ufl.edu/foundations/home/"

LESSONS = [
    (4, "<b>t</b> spells /t/", ["at", "sat", "mat", "mast"], []),
    (6, "<b>p</b> spells /p/", ["map", "tap", "pat", "past", "stamp", "spat"], ["sap", "amp"]),
    (7, "<b>f</b> spells /f/", ["fat", "fast", "fats"], []),
    (8, "<b>i</b> spells its short sound, as in <i>it</i>", ["it", "if", "sit", "fit", "tip", "pit", "mist", "fist"], ["sip", "spit", "tips"]),
    (9, "<b>n</b> spells /n/", ["in", "pin", "tin", "fin", "nap", "snap", "spin", "mint"], ["nip", "snip", "tint"]),
    (11, "<b>a</b> before <b>m</b> or <b>n</b>, where the vowel takes a nasal sound", ["am", "an", "man", "fan", "pan", "tan", "ant", "pants"], ["span", "stamp"]),
    (12, "<b>o</b> spells its short sound, as in <i>on</i>", ["on", "not", "top", "stop", "spot", "pop", "pot", "mop"], ["soft", "stomp", "tot"]),
    (13, "<b>d</b> spells /d/", ["and", "did", "dad", "sad", "mad", "dot", "pod", "dip"], ["sand", "pond", "damp"]),
    (14, "<b>c</b> spells /k/", ["can", "cat", "cap", "cot", "cop", "camp", "cast", "act"], ["scan", "cost", "fact"]),
    (15, "<b>u</b> spells its short sound, as in <i>up</i>", ["up", "us", "fun", "cut", "cup", "sun", "mud", "nut"], ["dust", "pup", "stunt"]),
    (16, "<b>g</b> spells /g/", ["got", "dog", "gas", "gap", "dig", "pig", "gum", "fog"], ["tug", "gift", "snag"]),
    (17, "<b>b</b> spells /b/", ["but", "big", "bad", "bit", "bus", "bag", "cab", "tub"], ["bud", "stab", "bump"]),
    (18, "<b>e</b> spells its short sound, as in <i>bed</i>", ["get", "set", "men", "ten", "bed", "pet", "net", "pen"], ["test", "nest", "spend"]),
    (20, "<b>-s</b> at the end of a word, said /s/", ["cats", "caps", "cups", "tips", "pots", "nuts", "pets", "gets"], ["maps", "dots", "fits"],
     {"cats": "cat + s", "caps": "cap + s", "cups": "cup + s", "tips": "tip + s", "pots": "pot + s", "nuts": "nut + s", "pets": "pet + s", "gets": "get + s"}),
    (21, "<b>-s</b> at the end of a word, said /z/: the same spelling", ["bags", "beds", "dogs", "pigs", "bugs", "bins", "cabs", "digs"], ["tubs", "pens", "mugs"],
     {"bags": "bag + s", "beds": "bed + s", "dogs": "dog + s", "pigs": "pig + s", "bugs": "bug + s", "bins": "bin + s", "cabs": "cab + s", "digs": "dig + s"}),
    (22, "<b>k</b> spells /k/, mostly before e and i, and in <b>sk</b>", ["kid", "kit", "skin", "skip", "desk", "mask", "ask", "task"], ["dusk", "skid", "kept"]),
    (23, "<b>h</b> spells /h/", ["had", "him", "hand", "hit", "hot", "hat", "hug", "hen"], ["hip", "hum", "hunt"]),
    (24, "<b>r</b> spells /r/ at the start of a word", ["run", "red", "rest", "rat", "rip", "rug", "rod", "rub"], ["rag", "rent", "rim"]),
    (25, "<b>r</b> after another consonant at the start: <b>cr</b>, <b>dr</b>, <b>fr</b>, <b>gr</b>, <b>tr</b>", ["drop", "trip", "grab", "crab", "drum", "frog", "grin", "crop"], ["trap", "drip", "grip"]),
    (26, "<b>l</b> spells /l/", ["let", "lot", "leg", "lip", "lid", "lap", "lost", "last"], ["lamp", "log", "left"]),
    (27, "<b>l</b> after another consonant (<b>bl</b>, <b>cl</b>, <b>fl</b>, <b>pl</b>, <b>sl</b>), and <b>lt</b> at the end", ["flag", "clap", "slip", "plan", "club", "belt", "flat", "plug"], ["clip", "sled", "melt"]),
    (28, "<b>w</b> spells /w/", ["win", "wet", "web", "wig", "wag", "swim", "twin", "went"], ["west", "swam", "twig"]),
    (29, "<b>j</b> spells /j/", ["jet", "jam", "job", "jog", "jug", "jump", "just", "jig"], ["jab", "jot", "jest"]),
    (30, "<b>y</b> spells /y/ at the start of a word", ["yes", "yet", "yum", "yam", "yak", "yelp"], ["yap", "yip"]),
    (31, "<b>x</b> spells two sounds, /ks/", ["six", "box", "fox", "fix", "mix", "wax", "tax", "next"], ["ox", "flex", "text"]),
    (32, "<b>qu</b> spells /kw/", ["quit", "quest", "quilt", "squid"], ["quits", "quilts"]),
    (33, "<b>v</b> spells /v/", ["van", "vet", "vest", "vast", "vent"], ["vat", "vents"]),
    (34, "<b>z</b> spells /z/", ["zip", "zap", "zest", "quiz"], ["zips", "zaps"]),
    (42, "<b>ff</b>, <b>ll</b>, <b>ss</b> and <b>zz</b> at the end, after a short vowel", ["off", "will", "tell", "miss", "kiss", "stuff", "buzz", "fell"], ["hill", "dress", "fizz"]),
    (43, "<b>all</b>, <b>oll</b> and <b>ull</b>: the vowel changes before ll", ["all", "call", "ball", "fall", "small", "roll", "full", "pull"], ["tall", "wall", "troll"]),
    (44, "<b>ck</b> after a short vowel", ["back", "sick", "rock", "duck", "neck", "kick", "lock", "truck"], ["stick", "black", "clock"]),
    (45, "<b>sh</b> spells one sound", ["ship", "fish", "shop", "wish", "shut", "cash", "dish", "shell"], ["shed", "rush", "fresh"]),
    (46, "<b>th</b> with a buzz, as in <i>this</i>", ["that", "this", "them", "then", "than"], ["thus"]),
    (47, "<b>th</b> without a buzz, as in <i>thin</i>", ["thin", "thick", "bath", "math", "path", "moth", "cloth", "fifth"], ["sixth", "tenth", "broth"]),
    (48, "<b>ch</b> spells one sound", ["much", "such", "rich", "lunch", "chip", "chin", "chop", "inch"], ["bench", "chest", "punch"]),
    (50, "<b>wh</b> for /w/, and <b>ph</b> for /f/", ["when", "which", "whip", "whisk", "graph"], ["whiff", "whim"]),
    (51, "<b>ng</b> spells one sound", ["long", "song", "sing", "king", "ring", "wing", "hang", "bring"], ["strong", "swing", "gong"]),
    (52, "<b>nk</b>: the n says the sound of ng before k", ["think", "thank", "bank", "drink", "pink", "sink", "ink", "junk"], ["trunk", "blink", "honk"]),
    (54, "<b>a</b>, a consonant, then <b>e</b>: the a says its name", ["make", "made", "take", "came", "game", "name", "cake", "gate"], ["plate", "shape", "wave"]),
    (55, "<b>i</b>, a consonant, then <b>e</b>: the i says its name", ["like", "time", "five", "bike", "ride", "kite", "mine", "smile"], ["hide", "white", "dime"]),
    (56, "<b>o</b>, a consonant, then <b>e</b>: the o says its name", ["home", "hope", "note", "joke", "bone", "stone", "rope", "hole"], ["woke", "smoke", "globe"]),
    (57, "<b>e</b>, a consonant, then <b>e</b>: the e says its name. Few words use it", ["eve", "here", "theme"], []),
    (58, "<b>u</b>, a consonant, then <b>e</b>: the u says its name, or /oo/", ["cute", "mule", "tube", "rule", "flute", "cube", "use", "dune"], ["prune", "fume"]),
    (63, "<b>-es</b> after s, x, sh and ch", ["boxes", "dishes", "wishes", "foxes", "buses", "benches", "glasses", "lunches"], ["fixes", "dresses", "inches"],
     {"boxes": "box + es", "dishes": "dish + es", "wishes": "wish + es", "foxes": "fox + es", "buses": "bus + es", "benches": "bench + es", "glasses": "glass + es", "lunches": "lunch + es"}),
    (64, "<b>-ed</b>, said three ways and spelled one", ["jumped", "asked", "fished", "yelled", "filled", "ended", "landed", "rested"], ["kicked", "smelled", "melted"],
     {"jumped": "jump + ed", "asked": "ask + ed", "fished": "fish + ed", "yelled": "yell + ed", "filled": "fill + ed", "ended": "end + ed", "landed": "land + ed", "rested": "rest + ed"}),
    (65, "<b>-ing</b> added to a word", ["jumping", "fishing", "helping", "asking", "ending", "sending", "resting", "kicking"], ["falling", "standing", "melting"],
     {"jumping": "jump + ing", "fishing": "fish + ing", "helping": "help + ing", "asking": "ask + ing", "ending": "end + ing", "sending": "send + ing", "resting": "rest + ing", "kicking": "kick + ing"}),
    (66, "Open and closed: a vowel at the end says its name, a consonant after it closes it", ["he", "me", "we", "she", "no", "go", "so", "hi"], ["be"]),
    (67, "Two closed syllables, and compound words", ["sunset", "laptop", "napkin", "basket", "picnic", "magnet", "bathtub", "backpack"], ["contest", "pigpen", "handstand"]),
    (68, "An open syllable, then a closed one", ["robot", "pupil", "even", "hotel", "open", "human", "bonus", "basic"], ["silent", "total", "pilot"]),
]


def _steps_of(D):
    inv = {}
    for s, v in D["map"].items():
        for l in v["lessons"]: inv.setdefault(l, []).append(int(s))
    return {l: sorted(v) for l, v in inv.items()}


def entries():
    D = json.loads((HERE / "data" / "ufli_crosswalk.json").read_text(encoding="utf-8"))
    st = _steps_of(D)
    out = []
    for row in LESSONS:
        n, what, words, check = row[:4]
        out.append({"n": n, "slug": f"ufli-{n:03d}", "what": what, "words": words, "check": check, "sums": row[4] if len(row) > 4 else {},
                    "steps": st.get(n, [])})
    return out


PAGES = [(f"lists/{e['slug']}.html", "teachers", f"Spelling list: UFLI lesson {e['n']}", re.sub(r"<[^>]+>", "", f"A spelling list lined up with UFLI Foundations lesson {e['n']}: {e['what']}. Words: {', '.join(e['words'])}.")) for e in entries()]


def write(OUT, page, header, footer, X):
    LW, SC, STEPS = X["LW"], X["SC"], {s["n"]: s for s in X["STEPS"]}
    md = lambda t: re.sub(r"\*([^*]+)\*", r"<i>\1</i>", t)
    def drawn(w, F=40):
        if w in LW.W and w not in SC.UNMARKED: return X["svg_of"](w, F, label=f"{w}, marked")
        return f'<span class="plain" style="font-size:{F}px">{html.escape(w)}</span>'
    E = entries()
    for k, e in enumerate(E):
        sums = e["sums"]
        rows = "".join(f'<figure class="word">{drawn(w)}<figcaption>{sums.get(w, "")}</figcaption></figure>' for w in e["words"])
        check = "".join(f'<li><span class="blank"></span><span class="ans t-only">{html.escape(w)}</span></li>' for w in e["check"])
        steps = " and ".join(f'<a href="../steps/{s:02d}.html">Step {s}: {md(STEPS[s]["title"])}</a>' for s in e["steps"])
        prev = f'<a href="{E[k - 1]["slug"]}.html">&larr; Lesson {E[k - 1]["n"]}</a>' if k else ""
        nxt = f'<a href="{E[k + 1]["slug"]}.html">Lesson {E[k + 1]["n"]} &rarr;</a>' if k + 1 < len(E) else ""
        body = f"""{header(1)}
<main class="list-page">
<section class="hero"><div class="wrap">
<p class="eyebrow t-only"><a href="index.html#ufli">Spelling lists</a> &middot; Lined up with UFLI Foundations</p>
<h1>UFLI lesson {e["n"]}</h1>
<p class="lprinciple">{e["what"]}.</p>
{f'<p class="lhome noprint">This lesson meets the route at {steps}.</p>' if steps else ""}
{f'<p class="ladds t-only noprint"><b>What the notation adds:</b> {ufli_lessons.L[e["n"]][1]} <a href="../ufli.html#lessons">Every lesson</a>.</p>' if ufli_lessons.L.get(e["n"]) else ""}
<p class="board t-only noprint"><a href="#" onclick="window.print(); return false;">Print this list</a>: the teacher&rsquo;s notes are left off.</p>
</div></section>
<section class="about"><div class="wrap">
<h2>The words</h2>
<div class="words rrow ugrid">{rows}</div>
</div></section>
{f'''<section class="about lwork"><div class="wrap">
<div><h2>Check: not on the list</h2><p class="sub">Words that use the same spelling. Say each one; the learner writes it.</p><ol class="lblanks">{check}</ol></div>
</div></section>''' if check else ""}
<section class="about t-only noprint"><div class="wrap prose">
<h2>For the teacher</h2>
<p>Every word here uses only spellings that UFLI Foundations has taught by lesson {e["n"]}, and each uses the one this lesson adds. The words are ours: none is taken from UFLI&rsquo;s materials. Say each word, use it in a sentence, and say it again.</p>
<p class="ulnav">{prev}{" &middot; " if prev and nxt else ""}{nxt}</p>
<p class="sub">Lined up with <a href="{UFLI_HOME}">UFLI Foundations</a> by lesson number. UFLI didn&rsquo;t make this list and hasn&rsquo;t endorsed it. Lesson descriptions are ours. See <a href="../ufli.html">the route and UFLI Foundations</a> for where each lesson meets the route.</p>
{X["uc"]("lists for the kindergarten lessons, 4 to 68, since 12 November 2026. The grade 1 and 2 lessons are next.")}
</div></section>
</main>
{footer(1)}"""
        (OUT / "lists" / f"{e['slug']}.html").write_text(page(f"Spelling list: UFLI lesson {e['n']} · A Legend for English Words", body, 1, PAGES[k][3]), encoding="utf-8")
    return E
