"""Coverage (13 November 2026): when each word on the Early Literacy Profile (Central Okanagan) and Dolch lists becomes
decodable on the route, and in UFLI Foundations' sequence.

The question it answers: if two systematic sequences differ in order, which one lets a learner read more of the words
they meet most, sooner? It is a count of words, not a measure of learning. Nobody has compared the two sequences in a
classroom.

How a word gets its place:
  - On the route: the latest step among the things the word needs (its letters, units and marks), or the step whose
    word list has it, whichever is earlier. A kernel word the route teaches with a reason (would, could, should) counts
    from its step.
  - In UFLI: the latest lesson among the things the word needs, or the first lesson whose Roll and Read page uses the
    word, whichever is earlier (UFLI leaves heart words off those pages, so a word there is one UFLI treats as
    decodable). Lessons 1 to 12 have no Roll and Read page, so the concepts place the earliest words. Lesson numbers and concepts
    only: none of UFLI's wording, and no UFLI word list is shown.
  - A word that needs something neither sequence teaches as a pattern (the o of one, the gh of laugh) is by heart in that
    sequence: None.
The Roll and Read first appearances were collected from UFLI's Roll and Read pages for lessons 13 to 128 (12 November
2026) and are kept in data/ufli_first.json for the words this page uses.

Pacing: the route has 32 steps and UFLI 128 lessons, and neither says how long a step or a lesson takes, so the two are
compared at checkpoints where they have taught the same thing (CHECKPOINTS), and across the whole sequence as a share
of its length."""
import json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent

# The single letters. The route uses a letter from the first step whose words have it, and has them all by step 4.
UFLI_LETTER = dict(a=1, m=2, s=3, t=4, p=6, f=7, i=8, n=9, o=12, d=13, c=14, u=15, g=16, b=17, e=18, k=22, h=23, r=24,
                   l=26, w=28, j=29, y=30, x=31, v=33, z=34, q=32)
ROUTE_LETTER = dict(i=1, t=1, n=1, s=1, f=1, a=2, o=2, u=2, m=2, p=2, h=3, e=3, w=3, b=3, y=3, g=3)
SHORT = {"route": dict(i=1, a=2, o=2, u=2, e=4, y=1), "ufli": dict(a=1, i=8, o=12, u=15, e=18, y=8)}
VCE = dict(a=54, i=55, o=56, e=57, u=58, y=55)
S_AS_Z = {"is", "as", "has", "his", "was"}        # s for /z/: UFLI lesson 21

# units: text -> (route step, UFLI lesson); None where the sequence teaches it by heart
UNITS = {
    "sh": (5, 45), "th": (5, 46), "ch": (5, 48), "wh": (5, 50), "ph": (32, 50), "ng": (13, 51), "nk": (13, 52),
    "tch": (6, 69), "dg": (14, 70), "ck": (6, 44), "ll": (6, 42), "ss": (6, 42), "ff": (6, 42), "zz": (6, 42),
    "kn": (25, 98), "wr": (25, 98), "mb": (25, 98), "tw": (25, None), "gh": (None, None), "bu": (None, None),
    "gu": (None, None), "ti": (31, 119), "qu": (4, 32),
    # vowel teams
    "ay": (11, 84), "ai": (20, 84), "ee": (11, 85), "ea": (20, 85), "ey": (20, 114), "oa": (20, 86), "oe": (20, 86),
    "ow": (20, 86), "ie": (20, 87), "igh": (11, 87), "oo": (21, 90), "ew": (21, 91), "ue": (21, 91), "ui": (21, 91),
    "ou": (24, 96), "au": (23, 93), "aw": (23, 93), "al": (23, None), "oi": (24, 95), "oy": (24, 95), "eigh": (20, 114),
    "ough": (None, 116), "augh": (None, 116), "eo": (None, None), "ei": (None, None), "uy": (None, None),
    # r-controlled
    "ar": (12, 77), "or": (12, 78), "ore": (26, 78), "er": (12, 80), "ir": (12, 81), "ur": (12, 81), "ear": (26, 113),
    "air": (26, 112), "are": (26, 112), "ere": (26, 112), "our": (26, None), "eir": (26, None), "oor": (26, None), "our_": (26, None),
}
# a team saying a sound that isn't its usual one: the ai of said and again. UFLI teaches these as heart words.
SECOND_SOUND = {"said": (22, None), "says": (22, None), "again": (22, None), "against": (22, None)}
DIPHTHONG_OW = {"how", "now", "down", "brown", "town", "cow", "owl", "clown", "flower"}
SECOND_OO = {"look", "good", "book", "took", "foot", "stood", "wood", "hook", "cook"}
SHORT_EA = {"head", "bread", "dead", "read_past", "ready", "breakfast"}
YOU_OU = {"you", "your", "soup", "group", "could", "would", "should"}
# a bare (borrowed or weak) vowel: the patterns the route teaches, and where UFLI meets them
O_FOR_U = {"come", "some", "done", "other", "mother", "brother", "love", "from", "month", "son", "won", "nothing",
           "above", "among", "Monday", "another", "front", "none", "money"}
O_FOR_OO = {"to", "do", "who", "two", "into", "today", "together", "whom", "whose", "move", "lose", "prove"}
# a vowel spelling another vowel's short sound: the a of many, the e of pretty. The route teaches many and any at step 22.
BORROWS_OTHER = {"any": 22, "many": 22, "pretty": None}
A_AFTER_W = {"was", "what", "want", "wash", "water", "watch", "wasp", "swan", "swap", "wand", "warm"}

# (milestone, route step, UFLI lesson): the point where each sequence finishes the same thing. What else each has taught
# by then is the difference in order.
CHECKPOINTS = [
    ("Single letters and short vowels done", 4, 34),
    ("Silent e done", 9, 62),
    ("The first r-controlled units done", 12, 83),
    ("All the r-controlled units done", 26, 113),
]


def _needs(word, p, side):
    """What the word needs on one side ('route' or 'ufli'): a list of step or lesson numbers, or None if by heart."""
    k = 0 if side == "route" else 1
    out = []
    units, sylls = p["units"], p["syllables"]
    seams = [m["after"] for m in p["marks"] if m["type"] == "seam"]
    text = "".join(l["ch"] for l in p["letters"])
    n_syll = len(sylls)
    for i, u in enumerate(units):
        kind, s, c0 = u["kind"], u["text"], u["cols"][0]
        low = s.lower()
        if kind == "c":
            for ch in low:
                out.append(ROUTE_LETTER.get(ch, 4) if side == "route" else UFLI_LETTER[ch])
            if len(low) > 1:                                  # a cluster: UFLI brings r and l blends in at 25 and 27, others with their letters
                out.append(6 if side == "route" else (25 if "r" in low[1:2] else 27 if "l" in low[1:2] else 0))
        elif kind in ("k", "g", "x", "q"):
            key = low
            if kind == "x" and low not in UNITS:              # a medial double (better, little): two closed syllables
                out.append(14 if side == "route" else 67)
                continue
            if key not in UNITS: return None
            v = UNITS[key][k]
            if v is None: return None
            out.append(v)
        elif kind == "s":
            out.append(SHORT[side][low])
            for ch in low: pass
        elif kind == "l":
            syl = next(j for j, (a, b) in enumerate(sylls) if a <= c0 <= b)
            a, b = sylls[syl]
            after = [x for x in units if x["cols"][0] > c0 and x["cols"][0] <= b]
            vaulted = any(x["kind"] == "e>" for x in after)
            if vaulted:
                out.append(9 if side == "route" else VCE[low])
            elif after and any(x["kind"] in ("c", "k", "g", "x") for x in after) and not any(x["kind"] in ("e>", "e0") for x in after):
                out.append(18 if side == "route" else 72)     # long before two consonants: old, find, both
            elif n_syll > 1 and syl < n_syll - 1 and not any(sylls[syl][1] == sm for sm in seams):
                out.append(16 if side == "route" else 68)     # open, in a longer word: o|pen
            elif low == "y":
                out.append(3 if side == "route" else 73)
            else:
                out.append((1 if low == "i" else 3) if side == "route" else 66)
        elif kind == "b":
            w = word
            if low == "y": out.append(14 if side == "route" else 74)
            elif w in BORROWS_OTHER: out.append(BORROWS_OTHER[w] if side == "route" else None)
            elif w in O_FOR_U: out.append(19 if side == "route" else None)
            elif w in O_FOR_OO: out.append(19 if side == "route" else None)
            elif w in A_AFTER_W: out.append((19 if w in {"was", "what"} else 23) if side == "route" else 94)
            elif low == "u" and w in {"put", "pull", "full", "push", "bush"}: out.append(22 if side == "route" else 89)
            elif low == "a" and "ll" in text[c0:c0 + 3].lower() or (low == "a" and text[c0:c0 + 2].lower() == "al"):
                out.append(23 if side == "route" else 43)
            elif n_syll > 1: out.append(16 if side == "route" else 68)   # a weak vowel in a longer word
            else: return None
            if out[-1] is None: return None
        elif kind == "t":
            key = low
            if word in SECOND_SOUND:
                v = SECOND_SOUND[word]
                if v[k] is None: return None
                out.append(v[k]); continue
            if low == "ow" and word in DIPHTHONG_OW: v = (24, 96)
            elif low == "oo" and word in SECOND_OO: v = (22, 89)
            elif low == "ea" and word in SHORT_EA: v = (22, 94)
            elif low == "ou" and word in YOU_OU: v = (21, None) if word in {"you", "soup", "group"} else (7, None)
            elif low == "oul": v = (7, None)
            else:
                v = UNITS.get(key)
                if v is None: return None
            if v[k] is None: return None
            out.append(v[k])
        elif kind == "r":
            nxt = units[i + 1]["kind"] if i + 1 < len(units) else ""
            if nxt == "e0" and word != "were" and low + "e" in UNITS: low = low + "e"   # ore, are, ere: more, care, there
            v = UNITS.get(low)
            if v is None or v[k] is None: return None
            out.append(v[k])
        elif kind == "le":
            out.append(17 if side == "route" else 75)
        elif kind == "e0":
            prev = units[i - 1]["text"].lower() if i else ""
            out.append((8 if prev.endswith("v") else 9) if side == "route" else 62)
        elif kind == "e>":
            pass
        elif kind == "z":
            out.append(25 if side == "route" else 98)
        elif kind == "ap":
            out.append(27 if side == "route" else None)
            if out[-1] is None: return None
        elif kind == "w":
            return None
        else:
            return None
    # marks that bring their own step
    for m in p["marks"]:
        if m["type"] == "nudge": out.append(10 if side == "route" else 60)
        if m["type"] == "blockedvault": out.append(14 if side == "route" else 67)
    # endings and joins at a seam
    for sm in seams:
        rest = text[sm + 1:].lower().replace("’", "")
        head = text[:sm + 1].lower()
        if rest in ("s",): out.append(13 if side == "route" else (21 if word in S_AS_Z or head[-1] in "aeiouglmnrvwdb" else 20))
        elif rest == "es": out.append(13 if side == "route" else 63)
        elif rest == "ed": out.append(13 if side == "route" else 64)
        elif rest == "ing": out.append(13 if side == "route" else 65)
        elif rest == "y": out.append(14 if side == "route" else 74)
        elif rest == "ly": out.append(29 if side == "route" else 101)
        elif rest in ("er", "est"): out.append(14 if side == "route" else 100)
        elif head in ("un",): out.append(30 if side == "route" else 103)
        elif head in ("re", "pre"): out.append(30 if side == "route" else 104)
        else: out.append(16 if side == "route" else 67)               # two words join: into, myself
    low_text = text.lower()
    if "nk" in low_text: out.append(13 if side == "route" else 52)        # nk is written as two letters: drink, think
    if re.search(r"[aou]ll\b", low_text) and not seams and n_syll == 1:   # all, oll and ull: ball, roll, full
        out.append(23 if side == "route" else 43)
    if n_syll > 1 and not seams:
        out.append(16 if side == "route" else 67)
    if side == "ufli" and word in S_AS_Z: out.append(21)
    return out


def route_step(word, p, listed):
    need = _needs(word, p, "route")
    by_concept = max(need) if need else None
    if word in listed and (by_concept is None or listed[word] <= by_concept): return listed[word], "listed"
    return by_concept, "concept"


def ufli_lesson(word, p, first):
    need = _needs(word, p, "ufli")
    by_concept = max(need) if need else None
    if word in first and (by_concept is None or first[word] <= by_concept): return first[word], "roll and read"
    return by_concept, "concept"


def listed_steps(route):
    """word -> the first step whose word list has it. Contrast words don't count: they are shown to be set apart."""
    out = {}
    for st in route["steps"]:
        for w in st.get("words") or []:
            out.setdefault(w, st["n"])
    return out


def table(LW, route):
    """[(word, lists it's on, route step, how, UFLI lesson, how)] for every ELP and Dolch word."""
    elp = json.load(open(HERE / "data" / "elp_hfw.json", encoding="utf-8"))
    dolch = json.load(open(HERE / "data" / "dolch.json", encoding="utf-8"))
    first = json.load(open(HERE / "data" / "ufli_first.json", encoding="utf-8"))
    listed = listed_steps(route)
    where = {}
    for k, v in elp["lists"].items():
        for w in v["words"]: where.setdefault(w, []).append(("elp", k, v["grade"]))
    for lv in dolch["levels"]:
        for w in lv["words"]: where.setdefault(w, []).append(("dolch", lv["key"], lv["name"]))
    rows = []
    for w, on in where.items():
        p = LW.parse(w)
        rs, rh = route_step(w, p, listed)
        ul, uh = ufli_lesson(w, p, first)
        rows.append({"word": w, "on": on, "step": rs, "step_how": rh, "lesson": ul, "lesson_how": uh})
    return rows


def at_checkpoints(rows, which):
    ws = [r for r in rows if any(o[0] == which for o in r["on"])]
    out = []
    for name, step, lesson in CHECKPOINTS:
        a = sum(1 for r in ws if r["step"] is not None and r["step"] <= step)
        b = sum(1 for r in ws if r["lesson"] is not None and r["lesson"] <= lesson)
        out.append((name, step, lesson, a, b, len(ws)))
    return out


def curve(rows, which, side, n, of):
    ws = [r for r in rows if any(o[0] == which for o in r["on"])]
    key = "step" if side == "route" else "lesson"
    return [sum(1 for r in ws if r[key] is not None and r[key] <= x) for x in range(1, of + 1)], len(ws)


def section(rows):
    """The section on ufli.html: the counts at each milestone, what they show, the limits, and every ELP word."""
    import html as H
    elp = json.load(open(HERE / "data" / "elp_hfw.json", encoding="utf-8"))
    E_, D_ = at_checkpoints(rows, "elp"), at_checkpoints(rows, "dolch")
    tr = "".join(f'<tr><th scope="row">{n}</th><td><a href="steps/{s:02d}.html">step {s}</a></td><td>lesson {l}</td>'
                 f'<td class="num">{a}</td><td class="num">{b}</td><td class="num">{c}</td><td class="num">{d}</td></tr>'
                 for (n, s, l, a, b, ne), (_, _, _, c, d, nd) in zip(E_, D_))
    ne, nd = E_[0][5], D_[0][5]
    table_ = (f'<div class="tablewrap"><table class="cw-table cov-table"><thead>'
              f'<tr><th scope="col" rowspan="2">When both have finished</th><th scope="col" rowspan="2">Route</th><th scope="col" rowspan="2">UFLI</th>'
              f'<th scope="colgroup" colspan="2">ELP words (of {ne})</th><th scope="colgroup" colspan="2">Dolch words (of {nd})</th></tr>'
              f'<tr><th scope="col">route</th><th scope="col">UFLI</th><th scope="col">route</th><th scope="col">UFLI</th></tr></thead>'
              f'<tbody>{tr}</tbody></table></div>')
    by = {r["word"]: r for r in rows}
    def i(ws): return ", ".join(f"<i>{H.escape(w)}</i>" for w in ws)
    s0, l0 = CHECKPOINTS[0][1], CHECKPOINTS[0][2]
    elp_rows = [r for r in rows if any(o[0] == "elp" for o in r["on"])]
    early_r = [r["word"] for r in elp_rows if r["step"] is not None and r["step"] <= s0 and not (r["lesson"] is not None and r["lesson"] <= l0)]
    early_u = [r["word"] for r in elp_rows if r["lesson"] is not None and r["lesson"] <= l0 and not (r["step"] is not None and r["step"] <= s0)]
    only_r = [r["word"] for r in elp_rows if r["step"] is not None and r["lesson"] is None]
    neither = [r["word"] for r in elp_rows if r["step"] is None and r["lesson"] is None]
    s2, l2 = CHECKPOINTS[2][1], CHECKPOINTS[2][2]
    mid_u = [r["word"] for r in elp_rows if r["lesson"] is not None and r["lesson"] <= l2 and not (r["step"] is not None and r["step"] <= s2)]
    lists = []
    for k, v in elp["lists"].items():
        cells = []
        for w in v["words"]:
            r = by[w]
            st = f'<a href="steps/{r["step"]:02d}.html">{r["step"]}</a>' if r["step"] is not None else '<span class="none">by heart</span>'
            le = (f'<span class="{"cpt" if r["lesson_how"] == "concept" else ""}">{r["lesson"]}</span>' if r["lesson"] is not None else '<span class="none">by heart</span>')
            cells.append(f'<tr><th scope="row"><i>{H.escape(w)}</i></th><td>{st}</td><td>{le}</td></tr>')
        lists.append(f'<div class="cov-list"><h3>{"Kindergarten" if v["grade"] == "K" else "Grade " + v["grade"] + ": " + H.escape(v["label"])}</h3>'
                     f'<table class="cov-words"><thead><tr><th scope="col">Word</th><th scope="col">Step</th><th scope="col">Lesson</th></tr></thead><tbody>{"".join(cells)}</tbody></table></div>')
    return f"""<section class="about" id="coverage" aria-labelledby="cov-h"><div class="wrap prose">
<h2 id="cov-h">Which words, how soon</h2>
<p>Both orders are systematic, and research doesn&rsquo;t favour one systematic order over another: the National Reading Panel&rsquo;s 38 phonics studies used about 19 different sequences, and they all worked. Nobody has compared these two in a classroom. What can be counted is which of the words learners meet most each order lets them decode, and when: the 148 high-frequency words of the Early Literacy Profile (Central Okanagan) and Dolch&rsquo;s 220.</p>
<p>The two can&rsquo;t be lined up step for lesson, because neither says how long a step or a lesson takes. So the count is made at the points where both have finished the same thing. What else each has taught by then is the difference in order.</p>
</div><div class="wrap">
{table_}
</div><div class="wrap prose">
<p><b>At the start, the route is ahead on the ELP&rsquo;s first lists.</b> Once the single letters and short vowels are in, the route reads {len(early_r)} words UFLI doesn&rsquo;t yet: {i(early_r)}. UFLI reads {i(early_u)}. These are the pronouns and small words of the kindergarten and CV lists. On Dolch&rsquo;s lists the two are even at that point: his first lists have many closed words (<i>big, can, red, run</i>) that UFLI&rsquo;s letter-by-letter order reaches as fast.</p>
<p><b>At silent e, the route is a little ahead on the ELP&rsquo;s words, and the two are even on Dolch&rsquo;s.</b></p>
<p><b>In the middle, UFLI is ahead.</b> By the time it finishes the first r-controlled units, UFLI has also taught open syllables in longer words, endings, consonant + le and long vowels before two consonants. The route teaches those after its r-controlled step (steps 13 to 18), so at that point UFLI reads {len(mid_u)} ELP words the route doesn&rsquo;t yet, among them {i(mid_u[:10])}.</p>
<p><b>By the end, the route reads more.</b> The difference is no longer order: it is the words the route teaches with a reason and UFLI teaches as heart words: {i(only_r)}. Neither decodes {i(neither)}.</p>
<p>So the case for the route&rsquo;s order is real but narrow: it is the first few weeks, and the small grammar words. The case for UFLI&rsquo;s order is the middle. The route&rsquo;s bigger difference is that it explains its kernel words, and that would hold in either order.</p>
<p class="sub"><b>How the counts were made.</b> A word counts on the route from the step whose list has it, or from the latest step among the things it needs (its letters, units and marks), whichever is earlier. In UFLI it counts from the first lesson whose Roll and Read page uses it (UFLI leaves heart words off those pages), or from the latest lesson among the things it needs, whichever is earlier. Lessons 1 to 12 have no Roll and Read page, so those lessons are placed by what they teach. On 1,907 words of five letters or fewer from the Roll and Read pages, placing by what a word needs gave the lesson UFLI first uses it in 88% of words, and within three lessons in 91%. This counts words, not learning: it says what a learner could decode, not what they will.</p>
</div><div class="wrap">
<details class="ufli-more"><summary><h3 class="cov-sum">Every ELP word: the step and the lesson</h3></summary>
<p class="sub">A lesson in grey was placed by what the word needs: no Roll and Read page uses the word. <i>By heart</i>: the sequence teaches it as a heart word, or doesn&rsquo;t teach it.</p>
<div class="cov-lists">{"".join(lists)}</div>
</details>
</div></section>"""
