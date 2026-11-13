"""Marking by rule (13 November 2026): a first pass of Legomorphic Notation codes from a word's spelling and its
pronunciation in CMUdict, for words nobody has marked by hand yet. Its output is data/auto_codes.json, which the Word walk
and the site search use, each word labelled "marked by rule, not yet checked". Nothing else on the site draws them.

The words are the common words of K-2 decoding practice, kept as a plain alphabetical list. Seams for endings other than
-s, -es, -ed and -ing are only drawn where the word was met in practice on that ending.

How it marks: letters are matched to sounds (consonant units, sh/th/ch, vowel teams, r-controlled units, -le, silent e);
a vowel is short, long (its name) or bare by its sound; syllables break before one consonant after a long or weak vowel
and after it otherwise, between two consonants, and at a seam; a doubled pair, ck, tch or dge after a short vowel is
boxed when a vowel follows, with the blocked vault; a silent e after one consonant and a long vowel sends the vault, and
so does a vowel one consonant after a long vowel (making, table); e, i or y after a c or g said soft gets the nudge.
Words whose letters it can't match to their sounds (silent t, ough, borrowed spellings) are left unmarked.

Checked against the 366 hand-marked words it overlaps: 343 come out the same (94%). Most of the rest are seams the hand
marking draws by meaning (happy, music) and vaults the hand marking leaves out (baby, open).

auto_mark.py WORDS.json HEADINGS.json OUT.json
"""
import json, re, sys, itertools
import cmudict
CMU = cmudict.dict()
VOW = set("aeiouy")
SHORT = {"a": {"AE"}, "e": {"EH"}, "i": {"IH"}, "o": {"AA", "AO"}, "u": {"AH"}, "y": {"IH"}}
LONG = {"a": {"EY"}, "e": {"IY"}, "i": {"AY"}, "o": {"OW"}, "u": {"UW", "Y UW"}, "y": {"AY"}}
VOWEL_PH = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"}

# consonant graphemes: letters -> (phoneme options, token kind)
CONS = [
    ("tch", ["CH"], "g"), ("dge", None, None), ("ti", ["SH"], "g"), ("si", ["ZH", "SH"], "k"), ("ci", ["SH"], "k"),
    ("sh", ["SH"], "g"), ("th", ["TH", "DH"], "g"), ("ch", ["CH"], "g"), ("ch", ["K"], "k"),
    ("ck", ["K"], "k"), ("wh", ["W", "HH"], "k"), ("ph", ["F"], "k"), ("ng", ["NG"], "k"), ("kn", ["N"], "k"), ("wr", ["R"], "k"),
    ("mb", ["M"], "k"), ("gn", ["N"], "k"), ("gh", ["G"], "k"), ("qu", ["K W"], "q"), ("dg", ["JH"], "k"),
    ("ff", ["F"], "k"), ("ll", ["L"], "k"), ("ss", ["S", "Z"], "k"), ("zz", ["Z"], "k"), ("bb", ["B"], "k"), ("dd", ["D"], "k"),
    ("gg", ["G"], "k"), ("mm", ["M"], "k"), ("nn", ["N"], "k"), ("pp", ["P"], "k"), ("rr", ["R"], "k"), ("tt", ["T"], "k"), ("cc", ["K"], "k"),
    ("b", ["B"], "c"), ("c", ["K", "S"], "c"), ("d", ["D", "T"], "c"), ("f", ["F"], "c"), ("g", ["G", "JH"], "c"), ("h", ["HH"], "c"),
    ("j", ["JH"], "c"), ("k", ["K"], "c"), ("l", ["L"], "c"), ("m", ["M"], "c"), ("n", ["N", "NG"], "c"), ("p", ["P"], "c"),
    ("r", ["R"], "c"), ("s", ["S", "Z"], "c"), ("t", ["T", "CH"], "c"), ("v", ["V"], "c"), ("w", ["W"], "c"), ("x", ["K S", "G Z"], "c"),
    ("y", ["Y"], "c"), ("z", ["Z"], "c"),
]
TEAMS = ["eigh", "augh", "ough", "igh", "ai", "ay", "ee", "ea", "ey", "ei", "ie", "oa", "oe", "oo", "ow", "ou", "oi", "oy", "ew", "ue", "ui", "au", "aw", "eu"]
RUNITS = ["ear", "air", "our", "eir", "oar", "eer", "oor", "ar", "or", "er", "ir", "ur"]


def phones(word):
    out = []
    for pr in CMU.get(word.lower(), []):
        out.append([(re.sub(r"\d", "", p), (int(p[-1]) if p[-1].isdigit() else None)) for p in pr])
    return out


def align(w, ph, seams, ed_es):
    """Letters to sounds. Returns a list of (letters, kind, phonemes, stress) or None. seams: letter indices after which a
    seam falls. ed_es: index where an -ed/-es suffix's e starts (that e may be silent)."""
    n, m = len(w), len(ph)
    best = []

    def silent_e_ok(i):
        return w[i] == "e" and (i == n - 1 or i in seams or i == ed_es)

    def go(i, j, acc):
        if best: return
        if i == n:
            if j == m: best.append(list(acc))
            return
        rest = w[i:]
        opts = []
        if rest.startswith("le") and (i + 2 == n or (i + 1) in seams) and j + 1 < m and ph[j][0] == "AH" and ph[j + 1][0] == "L":
            opts.append(("le", "le", 2, 2))
        for r in RUNITS:
            if rest.startswith(r) and j < m:
                if len(r) == 2 and w[i + 2:] == "e" and j < m and " ".join(x[0] for x in ph[j:j + 1]) in LONG.get(r[0], ()): continue
                if ph[j][0] == "ER" and not (i + len(r) < n and w[i + len(r)] in VOW and w[i + len(r)] != "e"): opts.append((r, "r", 1, len(r)))
                elif j + 1 < m and ph[j][0] in VOWEL_PH and ph[j + 1][0] == "R" and not (i + len(r) < n and w[i + len(r)] in VOW and w[i + len(r)] != "e"):
                    opts.append((r, "r", 2, len(r)))
        for t in TEAMS:
            if rest.startswith(t) and j < m and ph[j][0] in VOWEL_PH:
                opts.append((t, "t", 1, len(t)))
            if t in ("ew", "ue", "eu") and rest.startswith(t) and j + 1 < m and ph[j][0] == "Y" and ph[j + 1][0] == "UW":
                opts.append((t, "t", 2, len(t)))
        if w[i] in VOW and not (w[i] == "y" and i == 0):
            if j < m and ph[j][0] in VOWEL_PH:
                opts.append((w[i], "v", 1, 1))
            if j + 1 < m and ph[j][0] == "Y" and ph[j + 1][0] == "UW" and w[i] == "u":
                opts.append((w[i], "v", 2, 1))
            if silent_e_ok(i): opts.append(("e", "e", 0, 1))
        for g, pos, kind in CONS:
            if pos is None or not rest.startswith(g): continue
            for p in pos:
                ps = p.split()
                if [x[0] for x in ph[j:j + len(ps)]] == ps: opts.append((g, kind, len(ps), len(g)))
        for g, kind, k, L in opts:
            # a doubled letter or digraph may not straddle a seam
            if any(i <= s < i + L - 1 for s in seams): continue
            acc.append((g, kind, ph[j:j + k])); go(i + L, j + k, acc); acc.pop()
            if best: return
    go(0, 0, [])
    return best[0] if best else None


SUFFIXES = {"s": "-s", "es": "-es", "ed": "-ed", "ing": "-ing", "er": "-er", "est": "-est", "ly": "-ly", "less": "-less", "ful": "-ful",
            "ness": "-ness", "ment": "-ment", "y": "-y", "able": "-able", "ible": "-ible", "ist": "-ist", "ish": "-ish", "ion": "-ion"}
PREFIXES = ["un", "re", "pre", "dis", "mis", "uni", "bi", "tri"]


def split(word, heads, lexicon):
    """Seams from the lesson headings the word sits under: a suffix or prefix is only split off where a heading names it,
    and the base (after undoing doubling, the dropped e and y to i) is a word. Returns letter indices of seams."""
    H = " ".join(heads).lower()
    seams = []
    w = word
    # prefixes
    for p in PREFIXES:
        if (p + "-" in H or (p == "re" and "re" in H.split()) or p + "la" in H) and w.startswith(p) and w[len(p):] in lexicon and len(w) - len(p) >= 2:
            seams.append(len(p) - 1); break
    if "compound" in H:
        for k in range(3, len(w) - 2):
            if w[:k] in lexicon and w[k:] in lexicon and len(w[:k]) >= 3 and len(w[k:]) >= 3:
                seams.append(k - 1); break
    for suf in sorted(SUFFIXES, key=len, reverse=True):
        tag = SUFFIXES[suf]
        hit = suf in ("s", "es", "ing", "ed") or tag in H or (suf in ("s", "es") and ("-s" in H or "-es" in H)) or (suf in ("er", "est") and ("-er" in H or "-est" in H)) \
            or (suf in ("ing", "ed") and ("double" in H or "drop" in H or "-ing" in H or "-ed" in H)) or (suf in ("ed", "es", "er", "est") and "y to i" in H)
        if not hit or not w.endswith(suf) or len(w) - len(suf) < 2: continue
        stem = w[:-len(suf)]
        if suf == "s" and stem.endswith("s"): continue
        if not any(ch in VOW for ch in stem): break
        if suf == "es" and w[:-1] in lexicon and w[-2] == "e" and len(w) > 4 and not re.search(r"(s|x|z|sh|ch)$", w[:-2]):
            seams.append(len(w) - 2); return sorted(set(seams)), "s"
        cands = [(stem, len(stem) - 1)]
        if len(stem) >= 2 and stem[-1] == stem[-2]: cands.append((stem[:-1], len(stem) - 1))       # hop + p + ing: seam after the double
        cands.append((stem + "e", len(stem) - 1))                                                     # mak(e) + ing
        if stem.endswith("i"): cands.insert(0, (stem[:-1] + "y", len(stem) - 1))       # tr(y>i) + ed
        for base, s in cands:
            if base.endswith("e") and base != stem and (len(base) < 2 or base[-2] in VOW): continue
            if suf == "y" and stem[-1] in VOW: continue
            if not any(ch in VOW for ch in base): continue
            pre = w[:seams[0] + 1] if seams else ""
            if (base in lexicon or (pre and base[len(pre):] in lexicon)) and (len(base) >= 3 or (len(base) == 2 and suf in ("ing", "es"))):
                seams.append(s); return sorted(set(seams)), suf
        break
    return sorted(set(seams)), None


def code(word, heads=(), lexicon=frozenset()):
    if not re.fullmatch(r"[a-z]+", word): return None, "not lower-case letters"
    seams, suf = split(word, heads, lexicon)
    ed_es = len(word) - 2 if suf in ("ed", "es") else -1
    for ph in phones(word):
        units = align(word, ph, set(seams), ed_es)
        if units: break
    else:
        return None, "no alignment"
    align_units = units
    # unit kinds: vowels
    toks = []          # [kind, letters, start]
    pos = 0
    nvow = sum(1 for g, k, p in units if k in ("v", "t", "r", "le"))
    for idx, (g, k, p) in enumerate(units):
        if k == "v":
            names = " ".join(x[0] for x in p)
            stress = p[0][1] if p else None
            L = g
            if names in LONG.get(L, ()) : kind = "l"
            elif names in SHORT.get(L, ()) and not (L in "aeo" and names == "AH"): kind = "s"
            elif L == "i" and names == "IH": kind = "s"
            else: kind = "b"
            if L == "y" and names == "IY": kind = "b"
            if L == "e" and names in ("IH", "IY", "AH") and ((pos in seams) or (pos == 1 and word.startswith("be") and nvow > 1)): kind = "l"
            if kind == "s" and stress == 0 and L in "aeu" and nvow > 1: kind = "b"
            if L == "i" and names in ("AH", "IH") and stress == 0: kind = "s"
            if seams and pos < seams[0] and re.match(r"(un|dis|mis|in|im)", word) and names in ("AH", "IH") and L in "ui": kind = "s"
            toks.append([kind, g, pos, stress])
        elif k == "e":
            toks.append(["e", g, pos, None])
        else:
            toks.append([k, g, pos, (p[0][1] if p and k in ("t", "r") else None)])
        pos += len(g)
    # silent e: e> or e0
    for i, t in enumerate(toks):
        if t[0] != "e": continue
        prev_v = [j for j in range(i) if toks[j][0] in ("s", "l", "b", "t", "r", "le")]
        between = [toks[j] for j in range(prev_v[-1] + 1, i)] if prev_v else []
        if prev_v and toks[prev_v[-1]][0] == "l" and len(between) == 1 and between[0][0] in ("c", "k", "g") and len(between[0][1]) <= 2 \
                and not (len(between[0][1]) == 2 and between[0][0] == "c"):
            t[0] = "e>"
        else:
            t[0] = "e0"
    # merge runs of plain consonants into one c. token, later split by syllables
    # syllable breaks: between consecutive sounded vowel units
    vidx = [i for i, t in enumerate(toks) if t[0] in ("s", "l", "b", "t", "r", "le")]
    seam_after_tok = set()
    for s in seams:
        for i, t in enumerate(toks):
            if t[2] + len(t[1]) - 1 == s: seam_after_tok.add(i)
    if any(s not in {toks[i][2] + len(toks[i][1]) - 1 for i in seam_after_tok} for s in seams):
        return None, "seam inside a unit"
    breaks = set()          # break after token index
    for a, b in zip(vidx, vidx[1:]):
        mid = list(range(a + 1, b))
        cons = [i for i in mid if toks[i][0] in ("c", "k", "g", "q")]
        sm = [i for i in range(a, b) if i in seam_after_tok]
        if toks[b][0] == "le":
            # ta|ble, can|dle, ap|ple: the consonant before le goes with it, unless it is a double
            if cons and toks[cons[-1]][0] == "k" and len(toks[cons[-1]][1]) == 2 and toks[cons[-1]][1][0] == toks[cons[-1]][1][1]:
                breaks.add(cons[-1])
            elif cons: breaks.add(("split", cons[-1]))
            else: breaks.add(a)
            continue
        if sm:
            s = sm[0]
            # mak(e) + ing: a long vowel then one consonant before the seam: break before the consonant
            if toks[a][0] == "l" and len([i for i in mid if i <= s and toks[i][0] in ("c", "k", "g", "q")]) == 1 and \
                    sum(len(toks[i][1]) for i in mid if i <= s and toks[i][0] == "c") <= 1 and not any(toks[i][0].startswith("e") for i in mid if i <= s):
                breaks.add(a)
            else:
                breaks.add(s)
            continue
        if not cons:
            breaks.add(a); continue
        letters = "".join(toks[i][1] for i in cons)
        if len(cons) == 1 and len(toks[cons[0]][1]) == 1 or (len(cons) == 1 and toks[cons[0]][0] in ("g", "q", "k") and not (len(toks[cons[0]][1]) == 2 and toks[cons[0]][1][0] == toks[cons[0]][1][1]) and toks[cons[0]][1] != "ck"):
            # one consonant unit: open if the first vowel is long, closed otherwise
            if toks[a][0] in ("l", "t", "r") or (toks[a][0] == "b" and toks[a][3] == 0): breaks.add(a)
            else: breaks.add(cons[0])
        else:
            first = cons[0]
            if toks[first][0] == "k" and (toks[first][1][0] == toks[first][1][1] if len(toks[first][1]) == 2 else False) or toks[first][1] in ("ck",):
                breaks.add(first)
            elif len(cons) == 1:
                breaks.add(("split1", first))
            else:
                breaks.add(first)
    # build the code: plain consonant letters group into c. tokens, split at breaks
    out = []          # list of strings
    units = []        # unit kinds for annotation numbering: (kind, letters)
    buf = ""

    def flush():
        nonlocal buf
        if buf: out.append("c." + buf); units.append(("c", buf)); buf = ""

    split_points = {}
    for b in breaks:
        if isinstance(b, tuple):
            i = b[1]; L = toks[i][1]
            split_points[i] = 1 if b[0] == "split1" else (len(L) - 1 if len(L) > 1 else 0)
    for i, t in enumerate(toks):
        kind, g = t[0], t[1]
        if kind == "c":
            if i in split_points:
                k = split_points[i]
                if k == 0:
                    flush(); out.append("|"); buf += g
                else:
                    buf += g[:k]; flush(); out.append("|"); buf += g[k:]
            else:
                buf += g
        else:
            flush()
            if kind in ("s", "l", "b", "t", "r"): out.append(f"{kind}.{g}")
            elif kind == "le": out.append("le")
            elif kind in ("e0", "e>"): out.append(kind)
            elif kind == "g": out.append(f"g.{g}")
            elif kind == "q": out.append(f"q.{g}")
            else: out.append(f"k.{g}")
            units.append((kind, g))
        if i in seam_after_tok:
            flush(); out.append("+")
        if i in breaks:
            flush(); out.append("|")
    flush()
    # tidy: "+ |" order, no doubled bars
    s = " ".join(out)
    s = re.sub(r"\| \+", "+ |", s)
    s = re.sub(r"(\| )+", "| ", s).strip(" |")
    # recompute units from the final string
    U = [tk for tk in s.split() if tk not in ("|", "+")]
    kinds = [("le" if tk == "le" else tk if tk in ("e0", "e>") else tk.split(".")[0]) for tk in U]
    text = ["le" if tk == "le" else "e" if tk in ("e0", "e>") else tk.split(".", 1)[1] for tk in U]
    ann = []
    # doubled pairs followed later by a vowel letter: box them
    for i, (k, g) in enumerate(zip(kinds, text)):
        if k == "k" and (g in ("ck", "tch", "dg") or (len(g) == 2 and g[0] == g[1])) and i > 0 and kinds[i - 1] == "s":
            later = [j for j in range(i + 1, len(kinds)) if kinds[j] in ("s", "l", "b", "t", "r", "le", "e0", "e>")]
            if later:
                U[i] = "x." + g; kinds[i] = "x"
                v = later[0]
                if kinds[v] in ("s", "l", "b", "r", "e0"): ann.append(f"bv {v}>{i}")
        if k == "g" and g in ("tch", "sh", "th") and i > 0 and kinds[i - 1] == "s":
            later = [j for j in range(i + 1, len(kinds)) if kinds[j] in ("s", "l", "b", "t", "r", "le", "e0", "e>")]
            if later and (g == "tch" or kinds[later[0]] in ("s", "l", "r")):
                U[i] = "x." + g; kinds[i] = "x"
                v = later[0]
                if kinds[v] in ("s", "l", "b", "r", "e0"): ann.append(f"bv {v}>{i}")
    # a cluster after a short vowel at a seam before a suffix that starts with a vowel: box it (helped, jumping)
    toks2 = s.split()
    ui = -1
    for p, tk in enumerate(toks2):
        if tk in ("|", "+"): continue
        ui += 1
        if kinds[ui] == "c" and len(text[ui]) >= 2 and ui > 0 and kinds[ui - 1] == "s":
            nxt = [x for x in toks2[p + 1:p + 3]]
            if nxt and nxt[0] == "+" and ui + 1 < len(kinds) and kinds[ui + 1] in ("s", "b", "e0", "l"):
                ann.append(f"box {ui}"); ann.append(f"bv {ui + 1}>{ui}")
    seam_after_unit, ui = {}, -1
    for tk in toks2:
        if tk == "+": seam_after_unit[ui] = True
        elif tk != "|": ui += 1
    # vaults: a long single vowel, one consonant unit, then a vowel that can send
    for i, k in enumerate(kinds):
        if k != "l" or i + 2 >= len(kinds): continue
        if seam_after_unit.get(i): continue
        if kinds[i + 1] in ("c", "k", "g") and (len(text[i + 1]) == 1 or kinds[i + 1] in ("k", "g")) and kinds[i + 2] in ("s", "l", "b", "r", "le"):
            ann.append(f"vault {i + 2}>{i}")
        elif kinds[i + 1] == "g" and text[i + 1] == "ti":
            ann.append(f"vault {i + 1}>{i}")
    # nudges: a c or g said soft (/s/, /j/) by the vowel letter after it
    softpos, p0 = set(), 0
    for g, k, p in align_units:
        if g in ("c", "g", "dg") and p and p[0][0] in ("S", "JH"): softpos.add(p0 + len(g) - 1)
        p0 += len(g)
    starts, p0 = [], 0
    for t in text:
        starts.append(p0); p0 += len(t)
    for i, (k, g) in enumerate(zip(kinds, text)):
        last = starts[i] + len(g) - 1
        if last in softpos and i + 1 < len(kinds) and kinds[i + 1] in ("s", "l", "b", "e0", "e>", "t") and text[i + 1][0] in "eiy":
            ann.append(f"nudge {i + 1}>{i}")
    U2 = []
    ui = -1
    for tk in toks2:
        if tk in ("|", "+"): U2.append(tk); continue
        ui += 1; U2.append(U[ui])
    s = " ".join(U2)
    if word.endswith("tion") and (word[:-3] in lexicon or word[:-3] + "e" in lexicon) and len(word) > 5:
        ann.append(f"seam {len(word) - 4}")
    if ann: s += " ; " + " ; ".join(dict.fromkeys(ann))
    return s, None


if __name__ == "__main__":
    words = json.load(open(sys.argv[1]))
    heads = json.load(open(sys.argv[2]))
    lex = set(w.lower() for w in words) | set(k for k in CMU if len(k) > 1)
    out, fail = {}, {}
    for w in words:
        c, why = code(w, heads.get(w, ()), lex)
        if c: out[w] = c
        else: fail[w] = why
    json.dump(out, open(sys.argv[3], "w"), indent=0, sort_keys=True)
    print(len(out), "coded", len(fail), "not")
