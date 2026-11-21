"""The gymnasium (gym.html), 17 November 2026: a gym for each step on the path, built for the board at the front of the room.

Each step's gym has rounds. A round frees one more piece: a slot, a word, or the operator coming loose from the actor.
The actor sits on the fulcrum of a beam; the operator (am, is, are, did, can, will) tips it from a claim to a question;
the rest of the sentence runs left to right below. A teacher unlocks the next round when a learner decodes the last.
Four verdicts: Works, Almost (one word changes it to standard English), Missing a piece, and Crash. Some sentences
never come up (data/gym.json says which rounds; the engine's giggle screen says which sentences).

The rounds live in data/gym.json; the engine and the page live in gym_template.html. Here the words are drawn with the
site's own code, with layer classes so the board can turn marks on and off, and the word walk's drawings
(docs/walk, written by walk.py) are copied in so a tapped word walks as it does on the Word walk page. Step pages link
here with ?step=N. The word cards are build_gym_word_cards.py."""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
DATA = json.loads((HERE / "data" / "gym.json").read_text(encoding="utf-8"))
STEPS, FIT = DATA["STEPS"], DATA["FIT"]
NT = {"is": "isn’t", "are": "aren’t", "did": "didn’t", "can": "can’t", "will": "won’t", "could": "couldn’t", "would": "wouldn’t", "should": "shouldn’t", "have": "haven’t", "has": "hasn’t", "had": "hadn’t"}

# Squeezes the gym needs that contractions.py doesn't draw yet; spelled as build_verb_cards.py has them.
GYM_CODES = {"hadn’t": "c.h s.a c.d + | c.n ap c.t", "haven’t": "c.h s.a c.v | b.e + c.n ap c.t ; schwa 3"}   # haven't as seven: the e is said weakly


SLOTS = ("actor", "adet", "op", "act", "rec", "where", "what", "wdet")
ACTIONS = {"go", "went", "get", "got", "hit", "met", "be", "spell", "has", "had", "have", "give", "gave", "live"}
PERF, BE = {"have", "has", "had"}, {"am", "is", "are"}


def kit(STEPS):
    """The lexicon builds up (18 November 2026): a round never takes a word away. Each slot holds the round's own words
    first, in the order gym.json gives them, then every word the slot has had in earlier rounds and steps, the most
    recent first, so the arrows reach the new words before the old ones. The round's own lists are kept as "own",
    for the teacher's list of sentences.

    Two things are a round's scaffold rather than its words, and the round keeps its own: "=" (the operator goes with
    the actor) stays only where the round has it, and then the loose am/is/are wait; and in steps 3 and 4 an action
    rides in the operator slot, so once a round has an action slot of its own, those actions move down into it."""
    order = [(n, i) for n in STEPS for i in range(len(STEPS[n]["levels"]))]
    out = json.loads(json.dumps(STEPS))
    for k, (n, i) in enumerate(order):
        own = STEPS[n]["levels"][i]
        back = [STEPS[m]["levels"][j] for m, j in reversed(order[:k])]
        lists = {s: list(own.get(s, [])) for s in SLOTS}
        has_act = "act" in own
        linked = "=" in lists["op"]

        def add(slot, w):
            if w not in lists[slot]: lists[slot].append(w)
        for r in back:
            for s in SLOTS:
                for w in r.get(s, []):
                    if s == "op":
                        if w == "=": continue
                        if w in ACTIONS and not (w in PERF and "act" in r):                # an action riding in the operator slot
                            if has_act: add("act", w); w = ""                          # it moves down, and the beam can be empty
                        if w in BE and linked: continue
                        if w == "" and not has_act: continue
                    add(s, w)
        if has_act and lists["op"] and any(o in BE for o in lists["op"]) and "" not in lists["act"]: lists["act"].append("")   # am/is/are take no action
        if has_act and "" in lists["act"] and "" not in lists["op"] and any(a in ACTIONS for a in lists["act"]): lists["op"].append("")
        lv = out[n]["levels"][i]
        for s in SLOTS:
            if lists[s] and lists[s] != [""]: lv[s] = lists[s]
            elif s in own: lv[s] = own[s]
        for flag in ("not", "tip"):
            if own.get(flag) or any(r.get(flag) for r in back): lv[flag] = True
        lv["own"] = {s: own[s] for s in SLOTS if s in own} | {f: own[f] for f in ("not", "tip") if f in own}
    # What each round brings that the round before it didn't have, slot by slot: the words a sentence must use to count
    # towards unlocking the next round (gym_template.html, "five that work").
    for k, (n, i) in enumerate(order):
        lv, prev = out[n]["levels"][i], (out[order[k - 1][0]]["levels"][order[k - 1][1]] if k else {})
        had = {s: set(prev.get(s, [])) for s in SLOTS}
        had["act"] |= {o for o in prev.get("op", []) if o in ACTIONS and o not in PERF}   # go and hit rode in the operator slot: not new as actions
        fresh = {s: [w for w in lv["own"].get(s, []) if w and w != "=" and w not in had[s]] for s in SLOTS}
        lv["fresh"] = {s: v for s, v in fresh.items() if v}
        if lv.get("not") and not prev.get("not"): lv["fresh"]["not"] = True
    return out


def words():
    """Every word a round can put on the board."""
    out = set()
    for st in kit(STEPS).values():
        for r in st["levels"]:
            for k in ("actor", "adet", "op", "act", "rec", "where", "what", "wdet"):
                out.update(w for w in r.get(k, []) if w and w != "=")
            if "=" in r.get("op", []): out.update(FIT.get(a) or ("are" if a == "men" else "is") for a in r["actor"])
            if r.get("not"):
                out.add("not"); out.update(NT[o] for o in out.copy() if o in NT); out.add("aren’t")
    out |= {"yes", "no", "they", "not"}                         # a ladder's answers: Yes, it is. No, they didn't.
    return sorted(out)


def cap_code(code):
    toks = code.split(" ")
    for i, t in enumerate(toks):
        if "." in t:
            k, v = t.split(".", 1); toks[i] = f"{k}.{v[0].upper()}{v[1:]}"; break
    return " ".join(toks)


def codes():
    from known_codes import all_codes
    import site_codes as SC, heart_words, apart, ablaut, contractions, builder
    from dolch_codes import DOLCH_CODES
    from noun_codes import NOUN_CODES
    c, _ = all_codes()
    for src in [SC.SITE_CODES, heart_words.CODES, apart.CODES, ablaut.CODES, contractions.CODES, DOLCH_CODES, builder.CODES, NOUN_CODES]:
        for w, x in src.items(): c.setdefault(w, x)
    c.update(SC.SITE_RULED)
    for w, x in GYM_CODES.items(): c.setdefault(w, x)
    for w, x in json.loads((HERE / "data" / "auto_codes.json").read_text(encoding="utf-8")).items(): c.setdefault(w, x)
    return c


def write(OUT, door_page, LW):
    c = codes()

    def draw(word, code):
        had, old = word in LW.W, LW.W.get(word)
        LW.W[word] = code
        try: svg, _, _ = LW.svg_strip([word], F=56, cls=True, label=word)    # layer classes: the board turns marks on and off
        finally:
            if had: LW.W[word] = old
            else: LW.W.pop(word, None)
        return svg

    SVG, WALK = {}, {}
    ix = dict(json.loads((OUT / "walk" / "index.json").read_text(encoding="utf-8")))
    for w in words():
        code = c.get(w); assert code, f"gym: no code for {w}"
        lo = draw(w, code)
        SVG[w] = [lo, lo if w in ("I", "I’m") else draw(w[0].upper() + w[1:], cap_code(code))]
        f = json.loads((OUT / "walk" / f"{ix[w]}.json").read_text(encoding="utf-8"))["forms"][0]
        WALK[w] = {k: f[k] for k in ("svg", "W", "H", "units", "bars", "sounds", "sylls", "short", "long", "jobs", "parts")}
    gym = ((HERE / "gym_template.html").read_text(encoding="utf-8")
           .replace("/*SVG*/", json.dumps(SVG, ensure_ascii=False)).replace("/*WALK*/", json.dumps(WALK, ensure_ascii=False))
           .replace("/*STEPS*/", json.dumps(kit(STEPS), ensure_ascii=False)).replace("/*FIT*/", json.dumps(FIT, ensure_ascii=False))
           .replace("<!--GYMCARDS-->", ", ".join(f'<a href="cards/gym-word-cards-step-{n}.pdf">step {n}</a>' for n in STEPS)))
    door_page("gym", "The gymnasium · Sounds and Words, Assembled",
              "A gym for each step on the path: build sentences from the step's words on a balance, tip them into questions, and unlock a round at a time.",
              f"""<section class="hero door-hero"><div class="wrap">
<p class="eyebrow t-only"><a href="constructions.html">Sentences</a> · a trial</p>
<h1>The gymnasium</h1>
<p class="lead t-only">A gym for each step on the path. Climb a ladder of sentences built from the step&rsquo;s words, a word at a time, or build your own on a balance. Tip each one from a claim to a question, answer yes or no, and unlock a round at a time. Tap any word to walk it.</p>
</div></section>
<section class="gym-sec"><div class="wrap">
{gym}
</div></section>""")
    from doors import UNLISTED
    if "gym.html" in UNLISTED:                               # unlisted: keep it out of search engines too
        f = OUT / "gym.html"; s = f.read_text(encoding="utf-8")
        f.write_text(s.replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1), encoding="utf-8")
    print(f"wrote gym.html | {len(STEPS)} steps, {sum(len(s['levels']) for s in STEPS.values())} rounds, {len(SVG)} words")
    return list(STEPS)
