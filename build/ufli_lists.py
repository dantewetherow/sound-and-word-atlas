"""Spelling lists lined up with UFLI Foundations, by lesson number (12 November 2026): lists/ufli-NN.html.

UFLI's copyright statement says Toolbox items that carry its copyright notice can't be altered, reposted or used to make
other materials, so none of these words is taken from UFLI's materials. Each list has a lesson number and our own
description of what the lesson adds; the words are ours. They were found by a script (not part of the build) that ran
through common English words (wordfreq) and kept those that CMUdict says are spoken sound for sound as spelled with
only the spellings UFLI has taught by that lesson, and that use the lesson's new one. The lists below were then chosen
by hand from what it found: one-syllable words until the syllable lessons, no names, nothing a learner shouldn't say
in class. Review lessons have no list of their own.

So far these cover the kindergarten and grade 1 lessons (to 110). The grade 2 lessons follow the same way.

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
    # grade 1 (12 November 2026)
    (60, "<b>c</b> before <b>e</b> says /s/, as in <i>face</i> and <i>dance</i>", ["face", "race", "nice", "rice", "ice", "place", "dance", "fence"], ["space", "prince", "slice"]),
    (61, "<b>g</b> before <b>e</b> says /j/, as in <i>age</i> and <i>hinge</i>", ["age", "page", "cage", "stage", "huge", "hinge", "plunge", "fringe"], ["wage", "bulge", "lunge"]),
    (62, "A final <b>e</b> that sends no vault: <i>have</i>, <i>give</i>, <i>come</i>", ["have", "give", "live", "love", "come", "some", "done", "none"], ["glove", "shove"]),
    (69, "<b>tch</b> after a short vowel", ["catch", "match", "patch", "pitch", "itch", "ditch", "fetch", "sketch"], ["hatch", "stitch", "clutch"]),
    (70, "<b>dge</b> after a short vowel", ["edge", "badge", "bridge", "fudge", "ridge", "judge", "hedge", "wedge"], ["lodge", "nudge", "smudge"]),
    (72, "<b>i</b> and <b>o</b> say their names before <b>ld</b>, <b>nd</b> and <b>st</b>", ["find", "kind", "mind", "wild", "child", "old", "cold", "most"], ["gold", "blind", "post"]),
    (73, "<b>y</b> at the end says the name of i", ["my", "by", "why", "try", "fly", "dry", "sky", "cry"], ["shy", "spy", "fry"]),
    (74, "<b>y</b> at the end of a longer word says the name of e", ["candy", "lucky", "empty", "sandy", "handy", "dusty", "rusty", "silly"], ["messy", "windy", "fifty"]),
    (75, "A consonant and <b>le</b> make the last syllable", ["candle", "handle", "simple", "puzzle", "tickle", "bubble", "apple", "little"], ["pickle", "wiggle", "bundle"]),
    (77, "<b>ar</b>: the vowel and its r as one unit", ["car", "star", "park", "dark", "farm", "arm", "yard", "sharp"], ["chart", "smart", "barn"]),
    (78, "<b>or</b> and <b>ore</b>", ["for", "short", "fork", "born", "storm", "more", "store", "score"], ["north", "horn", "shore"]),
    (80, "<b>er</b>", ["her", "fern", "herd", "term", "sister", "winter", "under", "river"], ["perch", "silver", "number"]),
    (81, "<b>ir</b> and <b>ur</b>: the same sound as er", ["bird", "girl", "first", "shirt", "dirt", "turn", "hurt", "burn"], ["third", "curl", "church"]),
    (82, "<b>or</b> after <b>w</b> says the sound of <i>her</i>", ["work", "word", "worm", "world", "worst", "worth"], ["worker", "worthy"]),
    (84, "<b>ai</b> inside a word and <b>ay</b> at the end", ["rain", "train", "paint", "wait", "tail", "day", "play", "stay"], ["snail", "chain", "tray"]),
    (85, "<b>ee</b>, <b>ea</b> and <b>ey</b> for the name of e", ["see", "tree", "feet", "green", "eat", "sea", "read", "key"], ["sheep", "team", "valley"]),
    (86, "<b>oa</b>, <b>ow</b> and <b>oe</b> for the name of o", ["boat", "road", "coat", "goat", "snow", "grow", "show", "toe"], ["soap", "throw", "slow"]),
    (87, "<b>ie</b> and <b>igh</b> for the name of i", ["pie", "tie", "high", "night", "light", "right", "bright", "fight"], ["lie", "sight", "flight"]),
    (89, "<b>oo</b> and <b>u</b> for the vowel of <i>book</i> and <i>put</i>", ["book", "look", "good", "foot", "wood", "cook", "put", "push"], ["hook", "stood", "bush"]),
    (90, "<b>oo</b> for the vowel of <i>moon</i>", ["moon", "food", "room", "zoo", "soon", "pool", "tooth", "spoon"], ["boot", "roof", "broom"]),
    (91, "<b>ew</b>, <b>ui</b> and <b>ue</b> for the vowel of <i>moon</i>", ["new", "grew", "blew", "few", "blue", "true", "glue", "fruit"], ["chew", "suit", "clue"]),
    (93, "<b>au</b>, <b>aw</b> and <b>augh</b> for the vowel of <i>saw</i>", ["saw", "draw", "straw", "paw", "crawl", "haul", "launch", "caught"], ["claw", "taught", "fault"]),
    (94, "<b>ea</b> for short e (<i>head</i>), and <b>a</b> after w for short o (<i>want</i>)", ["head", "bread", "ready", "heavy", "breath", "want", "wash", "watch"], ["thread", "spread", "wand"]),
    (95, "<b>oi</b> inside a word and <b>oy</b> at the end", ["oil", "coin", "boil", "join", "point", "boy", "toy", "joy"], ["soil", "voice", "enjoy"]),
    (96, "<b>ou</b> and <b>ow</b> for the vowel of <i>out</i>", ["out", "loud", "cloud", "round", "mouth", "cow", "now", "down"], ["shout", "crown", "owl"]),
    (98, "<b>kn</b>, <b>wr</b> and <b>mb</b>: a silent letter in the unit", ["knee", "knock", "knot", "write", "wrap", "wrong", "lamb", "thumb"], ["knife", "wrist", "numb"]),
    (99, "<b>-s</b> and <b>-es</b> on words that name and words that do", ["toys", "plays", "runs", "jumps", "foxes", "wishes", "glasses", "fixes"], ["brushes", "bunches", "keys"],
     {"toys": "toy + s", "plays": "play + s", "runs": "run + s", "jumps": "jump + s", "foxes": "fox + es", "wishes": "wish + es", "glasses": "glass + es", "fixes": "fix + es"}),
    (100, "<b>-er</b> and <b>-est</b> to compare", ["taller", "tallest", "faster", "fastest", "longer", "longest", "smaller", "smallest"], ["colder", "softest", "darker"],
     {"taller": "tall + er", "tallest": "tall + est", "faster": "fast + er", "fastest": "fast + est", "longer": "long + er", "longest": "long + est", "smaller": "small + er", "smallest": "small + est"}),
    (101, "<b>-ly</b>: how something is done", ["sadly", "softly", "quickly", "slowly", "kindly", "badly", "loudly", "neatly"], ["gladly", "boldly", "safely"],
     {"sadly": "sad + ly", "softly": "soft + ly", "quickly": "quick + ly", "slowly": "slow + ly", "kindly": "kind + ly", "badly": "bad + ly", "loudly": "loud + ly", "neatly": "neat + ly"}),
    (102, "<b>-less</b> and <b>-ful</b>", ["helpful", "useful", "thankful", "hopeful", "endless", "homeless", "helpless", "painless"], ["restful", "sleepless", "fearless"],
     {"helpful": "help + ful", "useful": "use + ful", "thankful": "thank + ful", "hopeful": "hope + ful", "endless": "end + less", "homeless": "home + less", "helpless": "help + less", "painless": "pain + less"}),
    (103, "<b>un-</b> at the front", ["undo", "unlock", "unpack", "untie", "unfold", "unzip", "unkind", "unfair"], ["unplug", "unwrap", "unsafe"],
     {"undo": "un + do", "unlock": "un + lock", "unpack": "un + pack", "untie": "un + tie", "unfold": "un + fold", "unzip": "un + zip", "unkind": "un + kind", "unfair": "un + fair"}),
    (104, "<b>pre-</b> and <b>re-</b> at the front", ["redo", "reread", "refill", "replay", "rewind", "preheat", "preschool", "pretest"], ["recheck", "retell", "prepay"],
     {"redo": "re + do", "reread": "re + read", "refill": "re + fill", "replay": "re + play", "rewind": "re + wind", "preheat": "pre + heat", "preschool": "pre + school", "pretest": "pre + test"}),
    (105, "<b>dis-</b> at the front", ["dislike", "disagree", "disobey", "dishonest", "distrust", "disown", "discount", "dismiss"], ["disarm", "displease", "disconnect"],
     {"dislike": "dis + like", "disagree": "dis + agree", "disobey": "dis + obey", "dishonest": "dis + honest", "distrust": "dis + trust", "disown": "dis + own", "discount": "dis + count", "dismiss": "dis + miss"}),
    (107, "A short word doubles its last consonant before <b>-ing</b> and <b>-ed</b>", ["running", "hopping", "sitting", "swimming", "stopped", "hugged", "planned", "clapped"], ["shopping", "grabbed", "chatting"],
     {"running": "run + n + ing", "hopping": "hop + p + ing", "sitting": "sit + t + ing", "swimming": "swim + m + ing", "stopped": "stop + p + ed", "hugged": "hug + g + ed", "planned": "plan + n + ed", "clapped": "clap + p + ed"}),
    (108, "Doubling before <b>-er</b> and <b>-est</b>", ["bigger", "biggest", "hotter", "hottest", "sadder", "flatter", "thinnest", "wettest"], ["fatter", "dimmest", "reddest"],
     {"bigger": "big + g + er", "biggest": "big + g + est", "hotter": "hot + t + er", "hottest": "hot + t + est", "sadder": "sad + d + er", "flatter": "flat + t + er", "thinnest": "thin + n + est", "wettest": "wet + t + est"}),
    (109, "The <b>e</b> drops before a suffix that starts with a vowel", ["making", "baking", "hoping", "riding", "smiling", "liked", "hoped", "used"], ["shining", "saved", "wider"],
     {"making": "mak(e) + ing", "baking": "bak(e) + ing", "hoping": "hop(e) + ing", "riding": "rid(e) + ing", "smiling": "smil(e) + ing", "liked": "lik(e) + ed", "hoped": "hop(e) + ed", "used": "us(e) + ed"}),
    (110, "<b>y</b> turns to <b>i</b> before a suffix", ["tried", "cried", "flies", "babies", "happier", "funniest", "carried", "puppies"], ["dried", "spies", "sunnier"],
     {"tried": "tr(y&rarr;i) + ed", "cried": "cr(y&rarr;i) + ed", "flies": "fl(y&rarr;i) + es", "babies": "bab(y&rarr;i) + es", "happier": "happ(y&rarr;i) + er", "funniest": "funn(y&rarr;i) + est", "carried": "carr(y&rarr;i) + ed", "puppies": "pupp(y&rarr;i) + es"}),
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
<p class="eyebrow t-only"><a href="../ufli.html#lists">UFLI Foundations</a> &middot; Spelling list</p>
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
<p class="sub">Lined up with <a href="{UFLI_HOME}">UFLI Foundations</a> by lesson number. UFLI didn&rsquo;t make this list and hasn&rsquo;t endorsed it. Lesson descriptions are ours. See <a href="../ufli.html">UFLI Foundations</a> for every lesson and where each meets the route.</p>
{X["uc"]("lists for the kindergarten and grade 1 lessons, 4 to 110, since 12 November 2026. The grade 2 lessons are next.")}
</div></section>
</main>
{footer(1)}"""
        (OUT / "lists" / f"{e['slug']}.html").write_text(page(f"Spelling list: UFLI lesson {e['n']} · A Legend for English Words", body, 1, PAGES[k][3]), encoding="utf-8")
    return E
