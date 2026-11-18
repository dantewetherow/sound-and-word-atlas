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
NT = {"is": "isn’t", "are": "aren’t", "did": "didn’t", "can": "can’t", "will": "won’t"}


def words():
    """Every word a round can put on the board."""
    out = set()
    for st in STEPS.values():
        for r in st["levels"]:
            for k in ("actor", "adet", "op", "act", "where", "what", "wdet"):
                out.update(w for w in r.get(k, []) if w and w != "=")
            if "=" in r.get("op", []): out.update(FIT.get(a) or ("are" if a == "men" else "is") for a in r["actor"])
            if r.get("not"):
                out.add("not"); out.update(NT[o] for o in out.copy() if o in NT); out.add("aren’t")
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
           .replace("/*STEPS*/", json.dumps(STEPS, ensure_ascii=False)).replace("/*FIT*/", json.dumps(FIT, ensure_ascii=False)))
    door_page("gym", "The gymnasium · A Legend for English Words",
              "A gym for each step on the path: build sentences from the step's words on a balance, tip them into questions, and unlock a round at a time.",
              f"""<section class="hero door-hero"><div class="wrap">
<p class="eyebrow t-only"><a href="constructions.html">Sentences</a> · a trial</p>
<h1>The gymnasium</h1>
<p class="lead t-only">A gym for each step on the path. Build sentences from the step&rsquo;s words on a balance, tip them from a claim to a question, and unlock a round at a time as a learner decodes. Tap any word to walk it.</p>
</div></section>
<section class="gym-sec"><div class="wrap">
{gym}
</div></section>""")
    print(f"wrote gym.html | {len(STEPS)} steps, {sum(len(s['levels']) for s in STEPS.values())} rounds, {len(SVG)} words")
    return list(STEPS)
