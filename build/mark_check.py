"""The marking rules, in one place, and a check that holds every code on the site to them (20 November 2026).

Written while marking the 153 family words that had no marks. Each rule was either already ruled (the date says when)
or had to be settled to mark those words; Dante confirmed rules 3 and 16 and the act and create marks on 21 November;
rules 4, 5, 8, 10, 13 (the e sender) and the long u with no vault in lunar and ducal wait on him.

Units
  1. The units spell the word, letter for letter, in order.
  2. A silent consonant bonds into its unit (kn, wr, mb; ps in psychology; ch said k is k.ch) and takes a cone only
     when another form of the word says it (sign, signal). Ruled 12 November.
  3. gu before e, i or y, where the u only keeps the g hard, is one consonant unit, k.gu (guess, guide). So -logue is
     k.gu and a silent e in its cone (dialogue, catalogue): the u guards the g, and the e finishes the word. Confirmed 21 November.
  4. gi before a vowel, said j, is one consonant unit, k.gi (legion), as ti said sh is g.ti (nation). The seam falls
     inside it (leg + ion), and its i sends the vault.
  5. -ous is a vowel unit and s, said weakly: a ə over the ou (famous, luminous). 21 November: the ə replaces the cup
     these took from young, whose ou is stressed and keeps its cup.
  6. -re said er is an r unit (centre, lustre).

Vowels
  7. A vowel is short (cup), long (bar), weak (a small ə over it) or borrowed (the sound it borrows, small over it: oo
     over the o of do, u over the o of come, ah over the a of want, ee over the y of happy). 21 November 2026: the two
     new marks split what bare used to hold. The ə is Johann Andreas Schmeller's symbol (1820s); writing a vowel's
     other sound over it follows Romalda Spalding's numbered markings (The Writing Road to Reading, 1957). A vowel
     left bare is one not yet decided (carry, where Canadian speech varies). Gone takes a short o: ruled 21 November.
  8. An unstressed i is weak in the middle of a word, with a ə (similar, commodity), and keeps its cup in a
     last, closed syllable (logic, visit, lucid, active). The ə stands for the weak vowel whether a speaker says it
     as uh or as a quick i: in much Canadian and American speech the two have merged, and the mark doesn't take sides.
     21 November: Dante ruled that legible (and illegible) read better with a short mark; whether that holds for every
     -ible, and for the other mid-word i's, is open.
  9. So -ic at the end of a word is s.i c.c (logic), and -ic before another ending is a weak i | c.c + (logical, medical).
 10. An i that says e's name, in words from French (elite, expertise, machine), takes a small ee over it; its final e
     sits in a cone with no vault, since a vault is for a vowel that says its own name.
 11. A final e that is said says its name: l.e (simile).
 12. A family keeps its parts and lets the vowel marks move with the beat: product, produce, productivity.

Vaults (ruled 10 and 20 November)
 13. A vault needs a sender the spelling gives: a silent e; a y; a vowel that takes a dropped e's place across a seam
     (making, producer); an i before another vowel (experience, notation, legion), or an e doing the same (simultaneous).
     A long vowel no letter causes (over, tiger, lunar) has its bar and no vault.
 17. Word sums follow structured word inquiry (Melvyn Ramsden's Real Spelling, and Pete Bowers, who brought it into
     classrooms): a sum holds when its words share meaning and history, and it shows how the modern family is built,
     whatever road a word took into English. So a vowel suffix that replaces the family's final e sends the vault:
     mode/+al is modal, lune/+ar is lunar, pole/+ar is polar, reduce/+ible is reducible, as produce/+er is producer.
     Where no e-word is in the family, there is no e to replace and no vault: sol + ar is solar (sole is another
     word). How a word came into English goes in its note: modal was borrowed whole from Latin modalis. Ruled 21
     November, replacing the same morning's ruling by history.

Nudges
 14. A c before e, i or y is soft and takes a nudge from that letter (lucid, medicine, produce). A g takes one where
     it is said soft (legend, logic), and none where it stays hard (elegant, give).

Parts
 15. A seam goes where the word sum puts it. Where a syllable break falls one letter earlier, the break comes first
     and the seam after the letter (lec | t + ure, collec | t + ive).
 16. A prefix that changes its last letter to match the base keeps that letter: the double is two units with the seam
     between them, never a boxed double (col + lect, il + legible, as + sign, ac + com + modate). A doubled letter
     inside one part is a box (happen, lesson). Confirmed 21 November.

What the check does. Rules 1, 5, 13 and 14 (for c) are tested on every code. Rules 15 and 16 are tested wherever a
family page gives the word sum. A hand-checked code that breaks one stops the build. Rule-made codes (auto_codes.json)
are counted and listed in docs/mark-audit.json, since they are labelled "not yet checked" and are fixed by hand-marking
them. Rules 7 to 12 need an ear, and are the reviewer's."""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
VOWEL_KINDS = ("s", "l", "b", "t", "r", "w")
STILL_BARE = {"carry", "carries", "carried", "en"}            # not yet decided: carry varies most in Canadian speech


def units(code):
    main = code.split(";")[0].split()
    return [t for t in main if t not in ("|", "+")], main


def letters(tok):
    if tok == "le": return "le"
    if tok in ("e0", "e>"): return "e"
    if tok == "ap": return "’"
    return tok.split(".", 1)[1] if "." in tok else tok


def kind(tok):
    return tok.split(".", 1)[0] if "." in tok else tok


def anns(code):
    out = []
    for a in [p.strip() for p in code.split(";")[1:]]:
        m = re.fullmatch(r"(vault|bv|nudge|box|seam|cup) (\d+)(?:>(\d+)(?:-(\d+))?|-(\d+))?", a)
        if m: out.append((m.group(1), int(m.group(2)), int(m.group(3)) if m.group(3) else None))
    return out


def seam_letters(code):
    """Letter indices after which a seam falls: from + between units, and from seam N inside one."""
    us, main = units(code)
    out, n = set(), 0
    for t in main:
        if t == "+": out.add(n - 1)
        elif t != "|": n += len(letters(t))
    out |= {a for k, a, _ in anns(code) if k == "seam"}
    return out


def sum_seams(word, sum_parts):
    """Letter indices after which the word sum puts a seam, or None where the sum doesn't spell the word plainly."""
    parts = [re.sub(r"\(.*?\)", "", p.strip("-")) for p in sum_parts]
    if "".join(parts) != word: return None
    out, n = set(), 0
    for p in parts[:-1]: n += len(p); out.add(n - 1)
    return out


def check(word, code, sum_parts=None):
    bad = []
    us, main = units(code)
    spelt = "".join(letters(t) for t in us)
    if spelt.lower() != word.lower().replace("'", "’"): return [f"rule 1: the units spell “{spelt}”"]
    A = anns(code)
    pos = [i for i, t in enumerate(main) if t not in ("|", "+")]
    # rule 5: -ous
    weak = {int(a.split()[1]) for a in [p.strip() for p in code.split(";")[1:]] if a.startswith(("schwa ", "says "))}
    if word.endswith("ous") and len(us) >= 2 and us[-2] == "t.ou" and (len(us) - 2) not in weak:
        bad.append("rule 5: -ous without its ə")
    # rule 7: a bare vowel is weak or borrowed, and says which; the few left bare are listed
    for i, t in enumerate(us):
        if kind(t) == "b" and i not in weak and word not in STILL_BARE:
            bad.append(f"rule 7: the {letters(t)} is bare: give it a ə or the sound it borrows")
    # rule 13: a vault's sender
    for k, a, b in A:
        if k != "vault" or b is None or a >= len(us) or b >= len(us): continue
        lo, hi = min(a, b), max(a, b)
        snd, L = us[a], letters(us[a])
        nxt = us[a + 1] if a + 1 < len(us) else ""
        after = main[pos[a] + 1] if pos[a] + 1 < len(main) else ""
        seam = "+" in main[pos[lo]:pos[hi]] or any(k2 == "seam" for k2, _, _ in A)
        glide = (L[-1] in "ie" and kind(nxt) in VOWEL_KINDS) or any(letters(u)[-1] == "i" for u in us[lo + 1:hi]) or kind(snd) in ("g", "k") and L[-1] == "i"
        y = L.endswith("y") or (L == "i" and after == "+")
        r_drop = kind(snd) == "r" or kind(snd) in ("s", "l", "b") and False
        base_e = L == "e" and after == "+"
        if not (seam or glide or y or base_e or kind(snd) == "r"):
            bad.append(f"rule 13: the vault from {L} to {letters(us[b])} has no sender the spelling gives")
    # rule 14: c before e, i, y
    nudged = {b for k, a, b in A if k == "nudge"}
    for i, t in enumerate(us[:-1]):
        if kind(t) in ("c", "k") and letters(t).endswith("c") and letters(t) not in ("sc",) and letters(us[i + 1])[0] in "eiy" and kind(us[i + 1]) != "ap":
            if i not in nudged and not (letters(t).endswith("cc")):
                bad.append(f"rule 14: the c before {letters(us[i + 1])} has no nudge")
    # rules 15 and 16: seams against the word sum
    if sum_parts:
        want = sum_seams(word, sum_parts)
        if want is not None:
            have = seam_letters(code)
            if want - have: bad.append(f"rule 15: the sum {' + '.join(sum_parts)} puts a seam after letter {sorted(want - have)}, and the marks have none there")
            for i in want:
                if any(kind(t) in ("x", "k") and len(letters(t)) == 2 and letters(t)[0] == letters(t)[1] and sum(len(letters(u)) for u in us[:j]) == i for j, t in enumerate(us)):
                    bad.append("rule 16: a double across a seam is drawn as one unit")
    return bad


def run(OUT):
    import gym, parts, roots
    auto = json.loads((HERE / "data" / "auto_codes.json").read_text(encoding="utf-8"))
    codes = gym.codes()
    for f in ("more_codes.json", "family_codes.json"): codes.update(json.loads((HERE / "data" / f).read_text(encoding="utf-8")))
    sums = {}
    for R in roots.ROOTS:
        for c in R.get("clusters", []):
            for g in c["groups"]:
                for e in g:
                    if e[1]: sums[e[0]] = e[1]
    hand_bad, auto_bad = {}, {}
    for w, c in sorted(codes.items()):
        if not re.fullmatch(r"[A-Za-z’']+", w): continue
        b = check(w, c, sums.get(w))
        if b: (auto_bad if auto.get(w) == c else hand_bad)[w] = b
    n_auto = sum(1 for w, c in codes.items() if auto.get(w) == c)
    (OUT / "mark-audit.json").write_text(json.dumps({"hand": hand_bad, "rule_made": auto_bad}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"mark check | {len(codes) - n_auto} hand-checked codes, {len(hand_bad)} to look at | {n_auto} rule-made, {len(auto_bad)} to look at | {len(sums)} checked against word sums")
    return hand_bad, auto_bad


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(HERE))
    h, a = run(HERE.parent / "docs")
    from collections import Counter
    for name, d in (("hand", h), ("rule-made", a)):
        print(name, Counter(x.split(":")[0] for v in d.values() for x in v))
        for w, v in list(d.items())[:60 if name == "hand" else 12]: print("  ", w, "|", "; ".join(v))
