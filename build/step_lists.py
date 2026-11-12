"""A spelling list for every step and every family (12 November 2026), in the shape of the model lists in lists.py.

A step's list holds the step's words, or its pattern's commonest words where the step has few, each with a sentence; the
step's contrast; a column to build the words (from sounds, or from a sum where the step has parts); sentences to
complete; and a check of words that aren't on the list, the last of them where the step's idea stops. A family's list
takes its word sums from the family itself (roots.py), so they can't drift apart. The Carney references come from the
step (route.json), the family's sources from the family.

Steps 1, 15 and 28 already had lists (open-or-closed, the-e-drops, this-that-then), and the hap family had one: those
stay in lists.py and are counted in. Sentences are short and use words learners already say."""
import html, json, pathlib, re

ROUTE = json.loads((pathlib.Path(__file__).parent / "data" / "route.json").read_text())
STEPS = {s["n"]: s for s in ROUTE["steps"]}
HAVE = {1: "open-or-closed", 15: "the-e-drops", 28: "this-that-then"}      # steps whose list is a model in lists.py


def _md(s):
    return re.sub(r"\*([^*]+)\*", r"<i>\1</i>", s or "")


def S(n, principle, words, contrast, build, use, check, notes, build_h="Build it", listen=None, more_links=()):
    st = STEPS[n]
    title = st["title"].replace("*", "")
    ws = [w for w, _, _ in words]
    return {
        "slug": f"step-{n:02d}", "group": "step", "n": n,
        "title": f"Step {n}: {title}", "kind": "A step&rsquo;s pattern",
        "principle": principle, "words": words, "contrast": contrast, "listen": listen, "build_h": build_h,
        "build": build, "use": use, "check": check, "notes": notes,
        "links": [(f"Step {n}", f"steps/{n:02d}.html", _md(st["title"]).lower() + ", on the route")] + list(more_links),
        "source": "Edward Carney, <i>A Survey of English Spelling</i> (1994): " + _md(st.get("carney", "")) + ".",
        "desc": html.unescape(f"A spelling list for step {n}, {title}: {', '.join(ws)}, with a contrast, words to build, sentences and a check."),
    }


L = []

L.append(S(2, "A short vowel needs a consonant after it. In a two-letter word that one consonant closes it: <b>at</b>, <b>on</b>, <b>up</b>.",
    [("at", "", "Look at me."), ("an", "", "I have an apple."), ("am", "", "I am six."), ("as", "", "Run as fast as you can."),
     ("on", "", "Turn on the light."), ("up", "", "Get up."), ("us", "", "Come with us.")],
    ("The same two letters, open and closed: <i>no</i> says o&rsquo;s name, <i>on</i> is short.", [("no", "no", ""), ("on", "on", "")]),
    ["a, closed with t", "a, closed with n", "a, closed with m", "o, closed with n", "u, closed with p", "u, closed with s"],
    [("Look", "at or an", "the dog."), ("I", "am or an", "seven."), ("Get", "up or us", "now."), ("Put it", "on or an", "the box.")],
    [("o + x", "ox"), ("i + f", "if"), ("i + t", "it"), ("o + f", "of")],
    ["These are almost all small words. Carney&rsquo;s short word rule: words that carry meaning have at least three "
     "letters, and small words like these can have two (pp. 131&ndash;133). A content word with the same sounds adds a "
     "letter: <i>inn</i> beside <i>in</i>, <i>add</i> beside <i>ad</i>.",
     "The check ends with <i>of</i>, where the idea stops: its o borrows the sound of <i>up</i> and its f says /v/."],
    build_h="Close it", listen="The s of <i>as</i> says /z/; the s of <i>us</i> says /s/. Either way it closes the word.",
    more_links=[("Step 6", "steps/06.html", "closed words in the kernel")]))

L.append(S(3, "At the end of a short word the vowel is open and says its name: <b>he</b>, <b>so</b>. At the end, <b>y</b> says the name of i: <b>my</b>.",
    [("he", "", "He can swim."), ("me", "", "Look at me."), ("we", "", "We are here."), ("my", "", "My cat is black."),
     ("by", "", "Sit by me."), ("so", "", "I am so glad."), ("no", "", "No, thank you."), ("go", "", "Go to bed.")],
    ("Some open vowels borrow another sound: <i>do</i> and <i>to</i> don&rsquo;t say o&rsquo;s name.", [("go", "go", ""), ("do", "do", ""), ("so", "so", ""), ("to", "to", "")]),
    ["h + e", "m + y", "s + o", "w + e", "b + y", "n + o"],
    [("Can", "he or me", "come too?"), ("This is", "my or by", "hat."), ("I said", "no or so", "."), ("Let&rsquo;s", "go or so", "!")],
    [("sh + e", "she"), ("fl + y", "fly"), ("b + e", "be"), ("d + o", "do")],
    ["<i>Be</i> and <i>bee</i> sound the same. <i>Be</i> is a small word, so two letters will do; <i>bee</i> is a "
     "content word and takes three (Carney, p. 133).",
     "The check ends with <i>do</i>, an open o that borrows a sound. That waits for step 19."],
    more_links=[("Step 19", "steps/19.html", "a vowel that borrows a sound")]))

L.append(S(4, "Add one consonant to an open word and it closes: the vowel goes short. <b>be</b>, <b>bed</b>; <b>go</b>, <b>got</b>.",
    [("bed", "", "Go to bed."), ("met", "", "We met at the park."), ("wet", "", "My socks are wet."), ("got", "", "I got a new hat."),
     ("not", "", "It is not hot."), ("him", "", "Give it to him."), ("hit", "", "She hit the ball.")],
    ("Open, then closed: the vowel says its name, then goes short.", [("be", "be", ""), ("bed", "bed", ""), ("no", "no", ""), ("not", "not", "")]),
    ["be, closed with d", "we, closed with t", "go, closed with t", "no, closed with t", "hi, closed with m", "me, closed with t"],
    [("Is your hair", "wet or met", "?"), ("Time for", "bed or be", "."), ("I am", "not or got", "sleepy."), ("Throw it to", "him or hit", ".")],
    [("so + b", "sob"), ("he + n", "hen"), ("pi + n", "pin"), ("no + t + e", "note")],
    ["Every word here is an open word with one consonant added. The vowel letter stays the same; only its sound changes.",
     "The check ends with <i>note</i>: a silent e after the consonant reaches back and makes the o long again. That is "
     "step 9."],
    build_h="Close it", more_links=[("Step 9", "steps/09.html", "the vault")]))

L.append(S(5, "Some sounds are spelled with two letters: <b>th</b>, <b>sh</b>, <b>ch</b>, <b>wh</b>. The two letters make one sound, under one circle.",
    [("the", "", "The sun is hot."), ("she", "", "She can read."), ("this", "", "This is my book."), ("that", "", "That dog is big."),
     ("with", "", "Come with me."), ("much", "", "Thank you so much."), ("such", "", "It was such fun."), ("which", "", "Which one is yours?")],
    ("<i>She</i> is open and long. Add a d and it closes: <i>shed</i>.", [("she", "she", ""), ("shed", "shed", "")]),
    ["th + e", "sh + e", "th + i + s", "w + i + th", "m + u + ch", "wh + i + ch"],
    [("Can I come", "with or which", "you?"), ("Thank you very", "much or such", "!"), ("", "She or The", "is my sister."), ("", "Which or With", "way is home?")],
    [("sh + i + p", "ship"), ("ch + i + n", "chin"), ("th + i + n", "thin"), ("mis + hap", "mishap")],
    ["The h in th, sh and ch is a helper: it changes the letter before it instead of saying its own sound (Carney, p. 39).",
     "The th of <i>the</i>, <i>this</i> and <i>that</i> buzzes; the th of <i>thin</i> doesn&rsquo;t. Same spelling, two sounds.",
     "The check ends with <i>mishap</i>, where s and h meet across a seam and don&rsquo;t spell sh."],
    more_links=[("The hap family", "roots/hap.html", "why <i>mishap</i> has no sh")]))

L.append(S(6, "Most short words are closed: a short vowel with a consonant after it. At the end of a word, <b>l</b>, <b>s</b> and <b>f</b> often double after a short vowel: <b>will</b>, <b>spell</b>.",
    [("has", "", "She has a cat."), ("had", "", "We had fun."), ("did", "", "Did you see it?"), ("can", "", "I can swim."),
     ("will", "", "I will help."), ("must", "", "You must stop."), ("went", "", "He went home."), ("spell", "", "Can you spell it?")],
    ("After a short vowel at the end, l doubles: <i>will</i>, <i>spell</i>, <i>shall</i>. <i>Has</i> keeps one s, which says /z/.", [("will", "will", ""), ("spell", "spell", ""), ("shall", "shall", ""), ("has", "has", "")]),
    ["w + i + ll", "sp + e + ll", "m + u + st", "w + e + nt", "c + a + n", "d + i + d"],
    [("We", "had or has", "lunch at noon."), ("You", "must or much", "wash your hands."), ("She", "went or want", "to the park."), ("I", "will or well", "be there.")],
    [("b + e + ll", "bell"), ("m + e + ss", "mess"), ("o + ff", "off"), ("b + u + s", "bus")],
    ["At the end of a word, doubling is mostly limited to ff, ss, ll and the doubled spellings ck, tch and dge (Carney&rsquo;s rule #D5, p. 123).",
     "The check ends with <i>bus</i>, a short vowel with one s. A few words keep one: <i>bus</i>, <i>gas</i>, <i>yes</i>."],
    more_links=[("Step 14", "steps/14.html", "the box blocks the vault")]))

L.append(S(7, "Learn one, spell three. <b>would</b>, <b>could</b> and <b>should</b> share <b>ould</b>: the ou says the vowel of <i>book</i> and the l is silent.",
    [("would", "", "Would you like a snack?"), ("could", "", "I could see the moon."), ("should", "", "You should rest.")],
    ("The analog is the spelling, not the sound: <i>wood</i> sounds like <i>would</i> and is spelled another way.", [("would", "would", ""), ("wood", "wood", "")]),
    ["w + ould", "c + ould", "sh + ould", "would + n&rsquo;t", "could + n&rsquo;t", "should + n&rsquo;t"],
    [("", "Would or Wood", "you help me?"), ("I", "could or cold", "not find it."), ("We", "should or shoulder", "go now."), ("The fire needs more", "wood or would", ".")],
    [("would + n&rsquo;t", "wouldn&rsquo;t"), ("could + n&rsquo;t", "couldn&rsquo;t"), ("should + n&rsquo;t", "shouldn&rsquo;t"), ("sh + oulder", "shoulder")],
    ["Three words, one spelling to learn. The l in ould is empty: it has no sound (Carney, p. 249), and nothing in the "
     "family brings it back, so it stays in the unit.",
     "The check ends with <i>shoulder</i>, where ould says its letters&rsquo; own sounds: the analog stops there."],
    build_h="Build it", more_links=[("Step 27", "steps/27.html", "two words join: <i>wouldn&rsquo;t</i>")]))

L.append(S(8, "English words don&rsquo;t end in v. A silent <b>e</b> comes after it: <b>have</b>, <b>give</b>, <b>live</b>. In <b>gave</b> the e also makes the a long.",
    [("have", "", "I have a dog."), ("give", "", "Give me the ball."), ("live", "", "Where do you live?"), ("gave", "", "She gave me a hug."),
     ("save", "", "Save some for me."), ("five", "", "I am five.")],
    ("The e after v can be silent, or send a vault: <i>live</i> is short, <i>five</i> is long.", [("have", "have", ""), ("gave", "gave", ""), ("live", "live", ""), ("five", "five", "")]),
    ["hav, add e", "giv, add e", "liv, add e", "gav, add e", "sav, add e", "fiv, add e"],
    [("We", "have or gave", "two cats."), ("Please", "give or live", "it back."), ("She", "gave or give", "it to me yesterday."), ("I can count to", "five or fine", ".")],
    [("dr + i + ve", "drive"), ("s + o + l + ve", "solve"), ("gl + o + ve", "glove"), ("r + e + v", "rev")],
    ["The e in <i>have</i> and <i>give</i> is there for the v, not the vowel: the vowel stays short (Carney, p. 13). In "
     "<i>gave</i> and <i>five</i> the same e also sends a vault.",
     "The check ends with <i>rev</i>: short forms and slang can end in v (<i>rev</i>, <i>gov</i>; Carney, p. 231)."],
    build_h="Add the e", more_links=[("Step 9", "steps/09.html", "the vault")]))

L.append(S(9, "A silent <b>e</b> at the end reaches back over one consonant and makes the vowel say its name: <b>mad</b>, <b>made</b>.",
    [("make", "", "Let&rsquo;s make a cake."), ("like", "", "I like apples."), ("time", "", "What time is it?"), ("home", "", "Go home."),
     ("name", "", "What is your name?"), ("made", "", "I made it myself."), ("hope", "", "I hope it snows."), ("note", "", "Read the note.")],
    ("Add the e and the vowel says its name.", [("mad", "mad", ""), ("made", "made", ""), ("hop", "hop", ""), ("hope", "hope", ""), ("cub", "cub", ""), ("cube", "cube", "")]),
    ["mad, add e", "dim, add e", "hop, add e", "not, add e", "cub, add e", "pin, add e"],
    [("I", "hope or hop", "you can come."), ("Write me a", "note or not", "."), ("Cut the cheese into a", "cube or cub", "."), ("I", "made or mad", "a card.")],
    [("t + a + p + e", "tape"), ("k + i + t + e", "kite"), ("r + o + b + e", "robe"), ("h + a + v + e", "have")],
    ["The vault reaches over one consonant only. Two consonants stop it: that is step 14.",
     "The check ends with <i>have</i>: its e keeps v off the end and sends no vault, so the a stays short (step 8)."],
    build_h="Add the e", more_links=[("Step 14", "steps/14.html", "the box blocks the vault")]))

L.append(S(10, "An <b>e</b>, <b>i</b> or <b>y</b> right after a <b>c</b> or <b>g</b> nudges it soft: c says /s/, g says /j/. <i>The gentle giant went to the gym by cycling to the city centre.</i>",
    [("nice", "", "That is nice."), ("face", "", "Wash your face."), ("age", "", "What is your age?"), ("page", "", "Turn the page."),
     ("city", "", "We live in a city."), ("gym", "", "We play in the gym."), ("giant", "", "The giant was tall."), ("cent", "", "It costs one cent.")],
    ("Hard before a, o and u; soft before e, i and y.", [("cat", "cat", ""), ("cent", "cent", ""), ("got", "got", ""), ("gym", "gym", "")]),
    ["pl + a + ce", "r + a + ge", "c + e + ll", "g + e + m", "c + i + t + y", "h + u + ge"],
    [("A", "giant or gate", "lives in the castle."), ("Wash your", "face or fact", "."), ("We live in a big", "city or kitty", "."), ("Turn the", "page or pack", ".")],
    [("r + i + ce", "rice"), ("c + i + r + c + le", "circle"), ("g + e + m", "gem"), ("g + e + t", "get")],
    ["For c it nearly always holds (Carney&rsquo;s rule C.8, p. 303). For g it usually does, but some old English words "
     "keep a hard g before e or i: <i>get</i>, <i>give</i>, <i>girl</i>, <i>begin</i>. Try soft first, then hard.",
     "The check ends with <i>get</i>, where the nudge doesn&rsquo;t take."]))

L.append(S(11, "Two vowel letters can spell one vowel sound together, as a team: <b>ay</b> in <b>day</b>, <b>ee</b> in <b>see</b>, <b>igh</b> in <b>night</b>.",
    [("may", "", "May I go?"), ("day", "", "It is a sunny day."), ("play", "", "Let&rsquo;s play."), ("see", "", "I see a bird."),
     ("tree", "", "Climb the tree."), ("been", "", "Where have you been?"), ("might", "", "It might rain."), ("night", "", "Good night.")],
    ("A team says the vowel&rsquo;s name; one vowel with a consonant after it is short.", [("may", "may", ""), ("man", "man", ""), ("see", "see", ""), ("set", "set", "")]),
    ["d + ay", "s + ee", "n + igh + t", "pl + ay", "tr + ee", "l + igh + t"],
    [("It is a sunny", "day or did", "."), ("Climb the", "tree or try", "."), ("Turn on the", "light or lit", "."), ("It", "might or night", "snow.")],
    [("w + ay", "way"), ("f + ee + t", "feet"), ("r + igh + t", "right"), ("s + ai + d", "said")],
    ["<i>Been</i> is said with the vowel of <i>bin</i> in many places, and with the vowel of <i>bean</i> in others.",
     "The check ends with <i>said</i>, where a team says another sound. That is step 22."],
    more_links=[("Step 20", "steps/20.html", "teams for the long vowels")]))

L.append(S(12, "When <b>r</b> follows a vowel it changes the vowel&rsquo;s sound. The vowel and the r work as one unit: <b>ar</b>, <b>or</b>, <b>er</b>, <b>ir</b>, <b>ur</b>.",
    [("car", "", "Get in the car."), ("for", "", "This is for you."), ("her", "", "I like her hat."), ("bird", "", "A bird can fly."),
     ("turn", "", "It&rsquo;s your turn."), ("are", "", "We are friends."), ("were", "", "They were late."), ("or", "", "Tea or milk?")],
    ("<i>er</i>, <i>ir</i> and <i>ur</i> spell the same sound.", [("her", "her", ""), ("bird", "bird", ""), ("turn", "turn", "")]),
    ["c + ar", "f + or", "h + er", "b + ir + d", "t + ur + n", "st + ar"],
    [("A", "bird or bed", "sat on the fence."), ("It&rsquo;s my", "turn or ten", "."), ("Is this", "for or far", "me?"), ("They", "were or where", "here.")],
    [("st + ar", "star"), ("sh + or + t", "short"), ("g + ir + l", "girl"), ("w + or + d", "word")],
    ["Three spellings for one sound (er, ir, ur) means these are learned word by word, by their families.",
     "The check ends with <i>word</i>: after a w, or says the sound of <i>her</i>."],
    more_links=[("Step 26", "steps/26.html", "more r-controlled units")]))

L.append(S(13, "A suffix joins at the seam and the base keeps its spelling: <b>go + ing</b>, <b>play + ed</b>. <b>-ed</b> and <b>-s</b> keep one spelling whatever they sound like.",
    [("gets", "get + s", "He gets up early."), ("sees", "see + s", "She sees the bus."), ("going", "go + ing", "We are going home."),
     ("doing", "do + ing", "What are you doing?"), ("being", "be + ing", "Thank you for being kind."), ("played", "play + ed", "We played tag."),
     ("jumped", "jump + ed", "The frog jumped."), ("wanted", "want + ed", "I wanted a turn.")],
    ("<i>-ed</i> says three things and is spelled one way.", [("played", "play + ed", ""), ("jumped", "jump + ed", ""), ("wanted", "want + ed", "")]),
    ["jump + ed", "play + s", "go + ing", "see + ing", "want + ed", "look + ing"],
    [("Yesterday we", "play", "outside."), ("She", "see", "the moon every night."), ("We are", "go", "to school."), ("He", "get", "the mail every day.")],
    [("look + ed", "looked"), ("fix + ed", "fixed"), ("rain + ing", "raining"), ("hop + ing", "hopping")],
    ["Learners who spell <i>jumped</i> as <i>jumpt</i> are spelling the sound. The seam shows the suffix: one spelling, "
     "three sounds (Carney, pp. 18&ndash;19).",
     "The check ends with <i>hopping</i>: a short word doubles its last letter before the suffix. That is step 14."],
    more_links=[("Step 14", "steps/14.html", "the box blocks the vault"), ("Parts", "parts.html", "the suffixes")]))

L.append(S(14, "Two consonants between vowels block the vault, so the first vowel stays short. A short word doubles its last consonant to build the block: <b>get</b>, <b>getting</b>.",
    [("spelling", "spell + ing", "We have spelling today."), ("getting", "get + t + ing", "It is getting late."), ("helped", "help + ed", "She helped me."),
     ("sunny", "sun + n + y", "It is a sunny day."), ("happy", "hap + p + y", "I am happy."), ("hopping", "hop + p + ing", "The frog is hopping."),
     ("running", "run + n + ing", "Stop running."), ("sitting", "sit + t + ing", "We are sitting on the mat.")],
    ("One consonant lets the vault through; two block it.", [("hoping", "hop(e) + ing", ""), ("hopping", "hop + p + ing", "")]),
    ["get + ing", "sun + y", "hop + ing", "run + ing", "help + ed", "spell + ing"],
    [("We are", "sit", "on the mat."), ("Look at the frog", "hop", "."), ("It is a", "sun", "day."), ("She", "help", "me yesterday.")],
    [("swim + ing", "swimming"), ("fun + y", "funny"), ("jump + ing", "jumping"), ("fix + ing", "fixing")],
    ["<i>Help</i> and <i>spell</i> already end in two consonants, so nothing doubles: the block is there already.",
     "The check ends with <i>fixing</i>: x never doubles, because it already spells two sounds."],
    more_links=[("Step 15", "steps/15.html", "the e drops")]))

L.append(S(16, "In a two-syllable word with one consonant between the vowels, try the first vowel long, then short: <b>ti-ger</b>, but <b>sev-en</b>. Keep the one that makes a word you know.",
    [("tiger", "", "The tiger is asleep."), ("paper", "", "Fold the paper."), ("robot", "", "The robot can walk."), ("seven", "", "I am seven."),
     ("lemon", "", "Squeeze the lemon."), ("robin", "", "A robin sang."), ("music", "", "Turn up the music."), ("river", "", "We swam in the river.")],
    ("The same pattern, different vowels: you have to try.", [("robot", "robot", ""), ("robin", "robin", ""), ("tiger", "tiger", ""), ("river", "river", "")]),
    ["ti + ger", "sev + en", "pa + per", "lem + on", "ro + bot", "riv + er"],
    [("A", "robin or robot", "built a nest."), ("I have", "seven or even", "pencils."), ("Write on the", "paper or pepper", "."), ("We fished in the", "river or rider", ".")],
    [("pi + lot", "pilot"), ("cab + in", "cabin"), ("ze + ro", "zero"), ("sil + ly", "silly")],
    ["Kearns (2020) counted words like these: the first vowel was long 47% of the time, short 25% and weak 21%. So try "
     "long first, but expect to try again.",
     "The check ends with <i>silly</i>, where a double consonant settles it: no trying needed."],
    build_h="Say it in syllables"))

L.append(S(17, "A final <b>le</b> is a syllable of its own. A short vowel before it needs two consonants to block the vault (<b>apple</b>); a long one has one (<b>table</b>).",
    [("table", "", "Set the table."), ("title", "", "Read the title."), ("bugle", "", "He played the bugle."), ("little", "", "A little bird sang."),
     ("apple", "", "Eat an apple."), ("middle", "", "Stand in the middle."), ("bubble", "", "Blow a bubble.")],
    ("One consonant before le: long. Two: short.", [("title", "title", ""), ("little", "little", ""), ("table", "table", ""), ("apple", "apple", "")]),
    ["ta + ble", "ap + ple", "lit + tle", "ti + tle", "bub + ble", "mid + dle"],
    [("She ate an", "apple or able", "."), ("A", "little or title", "puppy."), ("Pop the", "bubble or bugle", "."), ("Write the", "title or little", "at the top.")],
    [("bot + tle", "bottle"), ("noo + dle", "noodle"), ("cra + dle", "cradle"), ("han + dle", "handle")],
    ["The le is a vowel and a consonant with the letters switched round (Carney, p. 129). It takes one red circle.",
     "The check ends with <i>handle</i>: n and d already make two consonants, so nothing doubles."],
    build_h="Say it in syllables"))

L.append(S(18, "Before <b>ld</b>, <b>nd</b> and a few other pairs, i and o often say their names though nothing sends a vault: <b>find</b>, <b>old</b>.",
    [("old", "", "My dog is old."), ("cold", "", "It is cold outside."), ("both", "", "Both of us came."), ("most", "", "Most cats like milk."),
     ("find", "", "I can&rsquo;t find my shoe."), ("kind", "", "Be kind."), ("child", "", "The child is happy."), ("wild", "", "A wild horse ran.")],
    ("The same shape, a different sound: i is long before nd, short before nt.", [("mind", "mind", ""), ("mint", "mint", ""), ("most", "most", ""), ("cost", "cost", "")]),
    ["f + i + nd", "c + o + ld", "ch + i + ld", "m + o + st", "w + i + ld", "b + o + th"],
    [("Be", "kind or kid", "to others."), ("Wear a coat, it&rsquo;s", "cold or cot", "."), ("Can you", "find or fin", "it?"), ("", "Most or Must", "of the cake is gone.")],
    [("be + hind", "behind"), ("g + o + ld", "gold"), ("p + o + st", "post"), ("w + i + nd", "wind")],
    ["Carney lists these as long before nd, ld and lt (p. 129; rules I.11 and I.12, pp. 332&ndash;333). It is a "
     "tendency, not a rule: <i>cost</i> and <i>mint</i> are short.",
     "The check ends with <i>wind</i>, which is long in <i>wind the clock</i> and short in <i>the wind blows</i>."]))

L.append(S(19, "Some vowels borrow another vowel&rsquo;s sound: the o of <b>come</b> says the u of <i>up</i>, the a of <b>was</b> says the o of <i>on</i>. Spell them by the word, not the sound.",
    [("come", "", "Come here."), ("some", "", "Have some juice."), ("done", "", "I am done."), ("from", "", "A card from Gran."),
     ("was", "", "It was fun."), ("what", "", "What is that?"), ("do", "", "Do you want it?"), ("who", "", "Who is there?")],
    ("The same letters, a borrowed sound.", [("home", "home", ""), ("come", "come", ""), ("bone", "bone", ""), ("done", "done", "")]),
    ["s + o + me", "d + o + ne", "fr + o + m", "w + a + s", "wh + a + t", "t + o"],
    [("Can you", "come or comb", "over?"), ("I want", "some or sum", "milk."), ("This is", "from or form", "my mom."), ("", "Who or How", "ate my sandwich?")],
    [("l + o + ve", "love"), ("m + o + n + ey", "money"), ("n + o + ne", "none"), ("h + o + me", "home")],
    ["Next to m and n, old handwriting ran u into its neighbours, so scribes wrote o instead: <i>come</i>, <i>some</i>, "
     "<i>money</i> (Carney, p. 69).",
     "The check ends with <i>home</i>, which keeps o&rsquo;s own sound: the borrowing isn&rsquo;t a rule to apply to every o."]))

L.append(S(20, "Each long vowel has its teams: <b>ai</b> and <b>ay</b> for a, <b>ea</b> and <b>ee</b> for e, <b>oa</b> and <b>ow</b> for o, <b>ie</b> and <b>igh</b> for i.",
    [("rain", "", "The rain stopped."), ("paid", "", "I paid for lunch."), ("eat", "", "Let&rsquo;s eat."), ("read", "", "I like to read."),
     ("boat", "", "We rode in a boat."), ("show", "", "Show me."), ("pie", "", "Have some pie."), ("they", "", "They are here.")],
    ("<i>ai</i> and <i>oa</i> inside a word; <i>ay</i> and <i>ow</i> at the end.", [("paid", "paid", ""), ("play", "play", ""), ("boat", "boat", ""), ("show", "show", "")]),
    ["r + ai + n", "b + oa + t", "sh + ow", "p + ie", "th + ey", "r + ea + d"],
    [("We sailed in a", "boat or bowl", "."), ("Please", "show or shoe", "me."), ("I", "read or red", "a book every night."), ("", "They or Then", "are my cousins.")],
    [("tr + ai + n", "train"), ("s + oa + p", "soap"), ("b + ea + ch", "beach"), ("eigh + t", "eight")],
    ["Where a team sits in a word helps decide it: ai and oa inside, ay and ow at the end. The spelling list "
     "<a href=\"say-pay-lay.html\">say, pay, lay</a> builds on that.",
     "The check ends with <i>eight</i>, where eigh spells the long a."],
    more_links=[("say, pay, lay", "lists/say-pay-lay.html", "ay at the end, ai inside")]))

L.append(S(21, "The long u sound has many spellings: <b>oo</b>, <b>ew</b>, <b>ue</b>, <b>ou</b>. Learn each word with its spelling.",
    [("too", "", "Me too!"), ("moon", "", "Look at the moon."), ("food", "", "We need food."), ("new", "", "I have new shoes."),
     ("grew", "", "The plant grew."), ("blue", "", "The sky is blue."), ("true", "", "Is it true?"), ("soup", "", "Hot soup.")],
    ("Three spellings, one sound.", [("do", "do", ""), ("due", "due", ""), ("dew", "dew", "")]),
    ["m + oo + n", "n + ew", "bl + ue", "s + ou + p", "f + oo + d", "gr + ew"],
    [("The sky is", "blue or blew", "."), ("The wind", "blew or blue", "hard."), ("I want", "two or too", "cookies."), ("Can I come", "too or two", "?")],
    [("sp + oo + n", "spoon"), ("fl + ew", "flew"), ("gl + ue", "glue"), ("b + oo + k", "book")],
    ["<i>Blue</i> and <i>blew</i>, <i>too</i> and <i>two</i>: the sentence chooses the spelling.",
     "The check ends with <i>book</i>, where oo says its other sound. That is step 22."]))

L.append(S(22, "A team can say a second sound: <b>oo</b> in <b>book</b>, not <i>moon</i>; <b>ea</b> in <b>head</b>, not <i>eat</i>.",
    [("look", "", "Look up."), ("good", "", "That was good."), ("book", "", "Read a book."), ("head", "", "My head hurts."),
     ("bread", "", "Bread and butter."), ("put", "", "Put it here."), ("pull", "", "Pull the rope."), ("said", "", "She said yes.")],
    ("A team can say two sounds.", [("moon", "moon", ""), ("book", "book", ""), ("eat", "eat", ""), ("head", "head", "")]),
    ["l + oo + k", "h + ea + d", "br + ea + d", "p + u + t", "p + u + ll", "g + oo + d"],
    [("Wear a hat on your", "head or heed", "."), ("Can you", "pull or pool", "the wagon?"), ("Please", "put or putt", "it away."), ("What a good", "book or boot", "!")],
    [("f + oo + t", "foot"), ("br + ea + th", "breath"), ("p + u + sh", "push"), ("f + oo + d", "food")],
    ["<i>Said</i> keeps the spelling of <i>say</i> and shifts its vowel. The list <a href=\"say-pay-lay.html\">say, pay, lay</a> explains it.",
     "The check ends with <i>food</i>, where oo says its first sound."],
    more_links=[("say, pay, lay", "lists/say-pay-lay.html", "why <i>said</i> has ai")]))

L.append(S(23, "The sound in <b>saw</b> is spelled <b>aw</b>, <b>au</b>, or <b>a</b> before l (<b>all</b>, <b>walk</b>). After a w, a often says it too (<b>want</b>, <b>wash</b>).",
    [("saw", "", "I saw a fox."), ("draw", "", "Draw a cat."), ("all", "", "That&rsquo;s all."), ("small", "", "A small mouse."),
     ("walk", "", "Let&rsquo;s walk."), ("want", "", "I want a turn."), ("wash", "", "Wash your hands."), ("because", "", "I&rsquo;m late because I slept in.")],
    ("Before ll, a says the sound of <i>saw</i>.", [("call", "call", ""), ("cat", "cat", ""), ("all", "all", ""), ("at", "at", "")]),
    ["s + aw", "dr + aw", "b + all", "t + alk", "w + a + nt", "sm + all"],
    [("I", "saw or sew", "a rainbow."), ("Let&rsquo;s", "walk or wake", "to school."), ("Can I", "draw or drew", "you a picture?"), ("The bug is very", "small or smell", ".")],
    [("cr + aw + l", "crawl"), ("t + all", "tall"), ("t + alk", "talk"), ("sh + all", "shall")],
    ["The l in <i>walk</i> and <i>talk</i> is silent and joins the unit; nothing in the family says it (Carney, pp. 181&ndash;184).",
     "The check ends with <i>shall</i>, where a before ll is short."]))

L.append(S(24, "The sound of <b>ouch</b> is spelled <b>ou</b> or <b>ow</b>; the sound of <b>oil</b> is <b>oi</b> or <b>oy</b>. Inside a word, usually ou and oi; at the end, ow and oy.",
    [("out", "", "Go out."), ("round", "", "The ball is round."), ("found", "", "I found it!"), ("how", "", "How are you?"),
     ("down", "", "Sit down."), ("coin", "", "A shiny coin."), ("boy", "", "The boy ran."), ("toy", "", "My toy car.")],
    ("<i>ow</i> can say two sounds.", [("now", "now", ""), ("snow", "snow", "")]),
    ["r + ou + nd", "d + ow + n", "c + oi + n", "b + oy", "p + oi + nt", "c + ow"],
    [("I", "found or fond", "my hat!"), ("Sit", "down or done", "."), ("Flip a", "coin or corn", "."), ("Which", "toy or tie", "do you want?")],
    [("cl + ou + d", "cloud"), ("c + ow", "cow"), ("j + oi + n", "join"), ("gr + ow", "grow")],
    ["<i>Down</i> and <i>town</i> have ow inside a word; the inside-and-end tendency is a help, not a rule (Carney, pp. 169, 202).",
     "The check ends with <i>grow</i>, where ow says the long o."]))

L.append(S(25, "Some letters are silent and join their unit: <b>kn</b> in <b>knee</b>, <b>wr</b> in <b>write</b>, <b>mb</b> in <b>lamb</b>. A silent letter that another form of the word says stands in a cone: the g of <b>sign</b>.",
    [("know", "", "I know the way."), ("knee", "", "I hurt my knee."), ("knife", "", "Use a knife and fork."), ("write", "", "Write your name."),
     ("wrong", "", "That&rsquo;s the wrong way."), ("lamb", "", "A baby lamb."), ("climb", "", "Climb the hill."), ("two", "", "I have two pets.")],
    ("The g of <i>sign</i> is said in <i>signal</i>, so it gets a cone, not a bond.", [("knot", "knot", ""), ("not", "not", ""), ("sign", "sign", ""), ("signal", "sign + al", "")]),
    ["kn + ee", "wr + i + te", "l + a + mb", "cl + i + mb", "kn + o + t", "wr + a + p"],
    [("Please", "write or right", "your name."), ("I", "know or no", "the answer."), ("Tie a", "knot or not", "."), ("I have", "two or too", "sisters.")],
    [("kn + ee + l", "kneel"), ("wr + i + st", "wrist"), ("th + u + mb", "thumb"), ("si + gn", "sign")],
    ["Silent letters are inert or empty: inert if another form of the word says them (<i>sign</i>, <i>signal</i>), "
     "empty if none does (<i>knife</i>) (Carney, pp. 41&ndash;42). The notation bonds the empty ones and cones the inert.",
     "The check ends with <i>sign</i>: ask the learner which word says its g."]))

L.append(S(26, "More vowels change before <b>r</b>: <b>air</b>, <b>ear</b>, <b>ore</b>, <b>are</b>, <b>ere</b>. The vowel letters and the r work as one unit.",
    [("hair", "", "Brush your hair."), ("hear", "", "I can hear you."), ("more", "", "Can I have more?"), ("before", "", "Wash before lunch."),
     ("care", "", "Take care."), ("there", "", "Put it there."), ("where", "", "Where is my hat?"), ("your", "", "Is this your coat?")],
    ("The same letters, different sounds.", [("were", "were", ""), ("there", "there", ""), ("are", "are", ""), ("care", "care", "")]),
    ["h + air", "h + ear", "m + ore", "c + are", "th + ere", "wh + ere"],
    [("I can", "hear or here", "a bird."), ("Put it over", "there or their", "."), ("I want", "more or mare", "."), ("Is that", "your or you", "dog?")],
    [("ch + air", "chair"), ("st + ore", "store"), ("n + ear", "near"), ("b + ear", "bear")],
    ["<i>Here</i> goes with <i>there</i> and <i>where</i>, the place words. <i>Hear</i> has <i>ear</i> in it: a "
     "reminder, not a reason, since the two words aren&rsquo;t related.", "The check ends with <i>bear</i>, where ear says the sound of <i>air</i>."]))

L.append(S(27, "Two words can join into one, with an apostrophe where letters are left out: <b>I + am</b> is <b>I&rsquo;m</b>, <b>do + not</b> is <b>don&rsquo;t</b>.",
    [("I&rsquo;m", "I + am", "I&rsquo;m here."), ("it&rsquo;s", "it + is", "It&rsquo;s late."), ("isn&rsquo;t", "is + not", "It isn&rsquo;t fair."),
     ("don&rsquo;t", "do + not", "Don&rsquo;t run."), ("can&rsquo;t", "can + not", "I can&rsquo;t see."), ("we&rsquo;re", "we + are", "We&rsquo;re ready.")],
    ("<i>It&rsquo;s</i> is <i>it is</i>; <i>its</i> means belonging to it.", [("it&rsquo;s", "it + is", ""), ("its", "its", "")]),
    ["I + am", "it + is", "do + not", "is + not", "we + are", "can + not"],
    [("", "it is", "raining."), ("I", "do not", "know."), ("She", "is not", "home."), ("", "we are", "late!")],
    [("you + are", "you&rsquo;re"), ("did + not", "didn&rsquo;t"), ("he + is", "he&rsquo;s"), ("will + not", "won&rsquo;t")],
    ["The apostrophe stands where letters were left out: one mark, wherever the gap is (Carney, p. 50).",
     "The check ends with <i>won&rsquo;t</i>, which changes its first word: <i>will</i> becomes <i>wo</i>. Learn it as a word."],
    build_h="Join them", more_links=[("Step 7", "steps/07.html", "would, could, should")]))

L.append(S(29, "A <b>y</b> at the end of a base turns to <b>i</b> before most suffixes when a consonant comes before it: <b>try</b>, <b>tried</b>. After a vowel it stays: <b>play</b>, <b>played</b>.",
    [("sadly", "sad + ly", "He waved sadly."), ("slowly", "slow + ly", "The snail moved slowly."), ("happily", "happ(y&rarr;i) + ly", "They played happily."),
     ("happier", "happ(y&rarr;i) + er", "She is happier now."), ("tried", "tr(y&rarr;i) + ed", "I tried my best."), ("carries", "carr(y&rarr;i) + es", "He carries the bag."),
     ("cried", "cr(y&rarr;i) + ed", "The baby cried."), ("babies", "bab(y&rarr;i) + es", "The babies slept.")],
    ("After a consonant, y turns to i; after a vowel, it stays.", [("try", "try", ""), ("tried", "tr(y&rarr;i) + ed", ""), ("play", "play", ""), ("played", "play + ed", "")]),
    ["try + ed", "cry + es", "happy + ly", "baby + es", "slow + ly", "carry + ed"],
    [("She", "try", "again yesterday."), ("He", "carry", "the box every day."), ("Walk", "slow", "."), ("We are", "happy", "than before.")],
    [("fly + es", "flies"), ("funny + er", "funnier"), ("stay + ed", "stayed"), ("dry + ing", "drying")],
    ["The y turns to i because English doesn&rsquo;t like y in the middle of a word; it stays before <i>-ing</i> so that "
     "two i&rsquo;s don&rsquo;t meet (Carney, pp. 70, 135&ndash;136).",
     "The check ends with <i>drying</i>, where the y stays."],
    more_links=[("The hap family", "roots/hap.html", "happy, happier, happily")]))

L.append(S(30, "<b>un-</b> and <b>re-</b> join at the front, and neither the prefix nor the base changes: <b>un + do</b>, <b>re + fill</b>.",
    [("undo", "un + do", "Undo the knot."), ("untie", "un + tie", "Untie your shoes."), ("unhappy", "un + hap + p + y", "He felt unhappy."),
     ("unlock", "un + lock", "Unlock the door."), ("redo", "re + do", "Redo the page."), ("replay", "re + play", "Replay the song."),
     ("refill", "re + fill", "Refill my cup."), ("reread", "re + read", "Reread the story.")],
    ("The prefix joins before the base; the base keeps its spelling.", [("happy", "hap + p + y", ""), ("unhappy", "un + hap + p + y", ""), ("play", "play", ""), ("replay", "re + play", "")]),
    ["un + do", "re + do", "un + lock", "re + fill", "un + tie", "re + read"],
    [("Please", "un + tie", "your shoes."), ("Let&rsquo;s", "re + play", "the game."), ("Can you", "re + fill", "the jug?"), ("I am", "un + happy", "about it.")],
    [("un + kind", "unkind"), ("re + build", "rebuild"), ("un + pack", "unpack"), ("re + enter", "re-enter")],
    ["Nothing drops or doubles at the front of a word in these: the prefix and the base each keep their letters, which "
     "is why <i>unnatural</i> has two n&rsquo;s.",
     "The check ends with <i>re-enter</i>, where the hyphen keeps two e&rsquo;s apart (Carney, p. 48)."]))

L.append(S(31, "A Latin base keeps its spelling through its family: <b>act</b>, <b>act + ion</b>, <b>act + or</b>. It&rsquo;s <b>-ion</b>, not <i>-tion</i>: the t belongs to <i>act</i>.",
    [("act", "act", "Act it out."), ("action", "act + ion", "Lights, camera, action!"), ("actor", "act + or", "She is an actor."),
     ("active", "act + ive", "Stay active."), ("react", "re + act", "How did he react?"), ("create", "create", "Create a picture."),
     ("creation", "creat(e) + ion", "What a creation!"), ("creator", "creat(e) + or", "Meet the creator of the game.")],
    ("The suffix is <i>-ion</i>; the t comes with the base.", [("act", "act", ""), ("action", "act + ion", ""), ("create", "create", ""), ("creation", "creat(e) + ion", "")]),
    ["act + ion", "act + or", "act + ive", "re + act", "create + ion", "create + or"],
    [("The", "act + or", "took a bow."), ("Watch the", "act + ion", "!"), ("Let&rsquo;s", "create", "a story."), ("He", "re + act + ed", "fast.")],
    [("direct + ion", "direction"), ("invent + or", "inventor"), ("educate + ion", "education"), ("act + ual", "actual")],
    ["Spelling <i>-tion</i> as one suffix hides the base. With <i>-ion</i>, <i>action</i> is <i>act</i> + <i>ion</i> and "
     "the t was there all along.",
     "The check ends with <i>actual</i>, where the t of act says /ch/: the base keeps its spelling, not its sound."],
    more_links=[("Parts", "parts.html#lessons", "it&rsquo;s -ion, not -tion"), ("The *deuk- family", "roots/deuk.html", "produce, production")]))

L.append(S(32, "Words from Greek spell /f/ with <b>ph</b>, and are built from Greek parts: <b>photo</b> (light), <b>phone</b> (sound), <b>graph</b> (writing).",
    [("photo", "photo", "Take a photo."), ("phone", "phone", "Answer the phone."), ("graph", "graph", "Read the graph."),
     ("telephone", "tele + phone", "The telephone rang."), ("photograph", "photo + graph", "A photograph of my dog."),
     ("alphabet", "alpha + bet", "Sing the alphabet."), ("photographer", "photo + graph + er", "The photographer smiled.")],
    ("<i>ph</i> in words from Greek, <i>f</i> in English&rsquo;s own words.", [("phone", "phone", ""), ("fun", "fun", "")]),
    ["tele + phone", "photo + graph", "photo + graph + er", "auto + graph", "para + graph", "micro + phone"],
    [("The", "photo + graph + er", "took our picture."), ("Pick up the", "tele + phone", "."), ("Say the", "alpha + bet", "."), ("Draw a", "graph", "of the results.")],
    [("graph + ic", "graphic"), ("micro + phone", "microphone"), ("para + graph", "paragraph"), ("f + i + sh", "fish")],
    ["<i>Alphabet</i> is named for the first two Greek letters, alpha and beta. Words from Greek keep ph for /f/ (Carney, p. 228).",
     "The check ends with <i>fish</i>: an English word, so its /f/ is f."],
    build_h="Build it", more_links=[("The *sem- family", "roots/sem.html", "homophone, homograph")]))


# ------------------------------------------------------------------ the families
def _sums(slug):
    """Each word of a family (not its debated words), with its parts as a sum, from roots.py."""
    import roots
    R = next(r for r in roots.ROOTS if r["slug"] == slug)
    out = {}
    for c in R["clusters"]:
        for g in c["groups"]:
            for w, parts, *_ in g:
                out[w] = " + ".join(p.strip("-") for p in parts) if parts else ""
    return R, out


def F(slug, principle, words, contrast, build, use, check, notes):
    R, sums = _sums(slug)
    for w, _ in words:
        assert w in sums, (slug, w)                         # a family's list holds the family's own words
    rows = [(w, sums[w], sent) for w, sent in words]
    cw = [(w, sums.get(w, ""), "") for w in contrast[1]]
    return {
        "slug": f"family-{slug}", "group": "family", "root": R["root"],
        "title": f"The {R['root']} family: " + ", ".join(w for w, _ in words[:4]), "kind": "One root, many words",
        "principle": principle, "words": rows, "contrast": (contrast[0], cw), "listen": None, "build_h": "Build it",
        "build": build, "use": use, "check": check, "notes": notes,
        "links": [(f"The {R['root']} family", f"roots/{slug}.html", "every word, the roads in, and the lessons")],
        "source": "; ".join(f'<a href="{u}">{t}</a>' for t, u in R["sources"][:3]) + ".",
        "desc": f"A spelling list for the {R['root']} family: " + ", ".join(w for w, _ in words) + ".",
    }


L.append(F("leg", "One root, three spellings: <b>leg</b> (<i>legend</i>), <b>lect</b> (<i>collect</i>) and <b>lig</b> (<i>eligible</i>). Each means to gather, to choose or to read.",
    [("legend", "We read a legend about a dragon."), ("legible", "Make your writing legible."), ("collect", "I collect stamps."), ("select", "Select a book."),
     ("election", "The class held an election."), ("lecture", "The scientist gave a lecture."), ("eligible", "Who is eligible to play?"), ("intelligent", "Dogs are intelligent.")],
    ("The base keeps its spelling when <i>-ion</i> joins: lect + ion.", ["collect", "collection", "select", "selection"]),
    ["col + lect + ion", "se + lect + ive", "e + lect + or", "il + leg + ible", "neg + lect", "dia + logue"],
    [("I keep my rocks in a", "col + lect + ion", "."), ("Please", "se + lect", "a colour."), ("Who won the", "e + lect + ion", "?"), ("Neat writing is", "leg + ible", ".")],
    [("re + col + lect", "recollect"), ("neg + lect + ful", "neglectful"), ("dia + lect", "dialect"), ("log + ic", "logic")],
    ["Collect has two l&rsquo;s because the prefix <i>con-</i> became <i>col-</i> before the l of lect. Each part brings its own.",
     "The check ends with <i>logic</i>: the same root by its Greek road, spelled log."]))

L.append(F("deuk", "One root, to lead, with two spellings: <b>duce</b> for the verb (<i>produce</i>) and <b>duct</b> before an ending (<i>production</i>).",
    [("produce", "Farms produce food."), ("product", "This product is new."), ("production", "The school play was a big production."), ("reduce", "Reduce your speed."),
     ("reduction", "The price had a reduction."), ("introduce", "Introduce your friend."), ("introduction", "Read the introduction."), ("conductor", "The conductor waved.")],
    ("<i>duce</i> for the verb, <i>duct</i> before <i>-ion</i>.", ["reduce", "reduction", "introduce", "introduction"]),
    ["pro + duce", "pro + duct + ion", "re + duce", "re + duct + ion", "con + duct + or", "e + duc + ate"],
    [("Bees", "pro + duce", "honey."), ("Read the", "intro + duct + ion", "first."), ("The", "con + duct + or", "led the band."), ("We need to", "re + duce", "waste.")],
    [("de + duct", "deduct"), ("pro + duc(e) + er", "producer"), ("e + duc + at(e) + ion", "education"), ("con + duct", "conduct")],
    ["The verb drops its e before <i>-er</i> (<i>producer</i>) and takes <i>duct</i> before <i>-ion</i> (<i>production</i>).",
     "The check ends with <i>conduct</i>, a noun and a verb with one spelling: CONduct, conDUCT. The stress moves; the spelling doesn&rsquo;t."]))

L.append(F("sem", "<b>*sem-</b> means one, as one, together. Its Latin spellings are <b>simil</b> (like), <b>semble</b> (together) and <b>sim</b> (<i>simple</i>); its Greek one is <b>homo</b> (the same).",
    [("similar", "Your hats are similar."), ("similarity", "There is a similarity between them."), ("assemble", "Assemble the robot."), ("resemble", "You resemble your dad."),
     ("resemblance", "I see the resemblance."), ("simple", "The game is simple."), ("homophone", "<i>Two</i> and <i>too</i> are homophones."), ("assimilate", "Some prefixes assimilate to the letter after them.")],
    ("<i>as-</i> before s doubles the s: as + semble, as + simil + ate.", ["assemble", "resemble"]),
    ["as + semble", "re + semble", "simil + ar + ity", "dis + simil + ar", "homo + phone", "as + simil + ate"],
    [("Your bikes look", "simil + ar", "."), ("Let&rsquo;s", "as + semble", "the puzzle."), ("Twins", "re + semble", "each other."), ("It&rsquo;s a", "sim + ple", "recipe.")],
    [("en + semble", "ensemble"), ("simul + at(e) + ion", "simulation"), ("homo + graph", "homograph"), ("homo + nym", "homonym")],
    ["<i>Assimilate</i> names the very thing its spelling shows: <i>ad-</i> became <i>as-</i> to match the s after it.",
     "The check ends with <i>homonym</i>: Greek <i>homo</i>, the same, with <i>nym</i>, a name. English&rsquo;s own words from the root, <i>same</i> and <i>some</i>, have no parts to build."]))

L.append(F("med", "<b>*med-</b> means to measure, to take fitting steps. Its spellings are <b>mod</b> (a measure, a manner: <i>mode</i>, <i>accommodate</i>) and <b>med</b> (to treat: <i>medical</i>).",
    [("mode", "Put the phone in quiet mode."), ("model", "We built a model plane."), ("modern", "A modern house."), ("module", "Finish the first module."),
     ("medical", "She needs medical help."), ("medicine", "Take your medicine."), ("accommodate", "The cabin can accommodate six people."), ("accommodation", "We found accommodation by the lake.")],
    ("Two c&rsquo;s and two m&rsquo;s: ac + com + mod. Each prefix brings its own.", ["accommodate", "accommodation"]),
    ["ac + com + mod + ate", "mod + ule", "med + ic + al", "com + mod + ity", "com + mode", "med + ic + ate"],
    [("Can the van", "ac + com + mod + ate", "us all?"), ("See a doctor for", "med + ic + al", "help."), ("We finished the last", "mod + ule", "."), ("Switch to night", "mode", ".")],
    [("mod(e) + al", "modal"), ("med + ic + at(e) + ion", "medication"), ("mod + ul(e) + ate", "modulate"), ("mod + ul(e) + ar", "modular")],
    ["<i>Accommodate</i> is one of the most misspelled words in English. Its sum fixes it: ac + com + mod + ate, so two c&rsquo;s and two m&rsquo;s.",
     "The check ends with <i>modular</i>: the e of <i>module</i> drops before <i>-ar</i>, as it does before <i>-ate</i>. English&rsquo;s own word from the root, <i>must</i>, has no parts to build."]))

L.append(F("leuk", "<b>*leuk-</b> means light. Latin made it <b>lustr</b> (<i>illustrate</i>), <b>lumin</b> (<i>illuminate</i>), <b>luc</b> (<i>lucid</i>) and <b>lun</b> (<i>lunar</i>); English kept <b>light</b>.",
    [("illustrate", "Illustrate your story."), ("illustration", "Look at the illustration."), ("illuminate", "Lamps illuminate the street."), ("lucid", "Give a lucid answer."),
     ("translucent", "The glass is translucent."), ("lunar", "We watched a lunar eclipse."), ("light", "Turn on the light."), ("lighten", "Lighten the colour.")],
    ("Two l&rsquo;s in both: il + lustr, il + lumin.", ["illustrate", "illuminate"]),
    ["il + lustr + ate", "il + lustr + at(e) + ion", "il + lumin + ate", "trans + luc + ent", "il + lustr + ious", "light + en"],
    [("Can you", "il + lustr + ate", "the poem?"), ("A", "lun + ar", "rover drove on the moon."), ("Candles", "il + lumin + ate", "the room."), ("Frosted glass is", "trans + luc + ent", ".")],
    [("lumin + ous", "luminous"), ("e + luc + id + ate", "elucidate"), ("il + lumin + at(e) + ion", "illumination"), ("light + en + ing", "lightening")],
    ["In <i>illustrate</i> the prefix is <i>in-</i>, in, into, written <i>il-</i> before l; in <i>illegal</i> it means not. Two prefixes, spelled alike.",
     "The check ends with <i>lightening</i>, making lighter. <i>Lightning</i>, the flash, is the same family with no e. The <i>light</i> that means not heavy sounds the same and comes from another root."]))

STEP_LISTS = L
