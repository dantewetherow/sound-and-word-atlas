"""Every word code the site draws with: the codes in legomorphic_words.py, plus a snapshot of the codes the
deck tools add.

The deck tools (legend_rules.py, flsz_family.py and th_family.py) live outside this repository, so
deck_codes.json keeps the codes they add and the site builds without them. To refresh the snapshot from a
copy of the atlas folder:

    python3 known_codes.py --refresh /path/to/atlas
"""
import ast, json, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import legomorphic_words as LW
SNAPSHOT = HERE / "deck_codes.json"


def dict_literals(path, names=None, inline_for=False):
    """Dictionary literals in a deck tool, read without running it."""
    tree = ast.parse(pathlib.Path(path).read_text(encoding="utf-8"))
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
            tgt = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if names and not set(tgt) & set(names): continue
            try: out.update(ast.literal_eval(node.value))
            except Exception: pass
        if inline_for and isinstance(node, ast.For) and isinstance(node.iter, ast.Call):
            f = node.iter.func
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Dict):
                try: out.update(ast.literal_eval(f.value))
                except Exception: pass
    return out


def is_code(word, c):
    """True when the string parses as a code for that word (so stray labels in a tool are left out)."""
    had, old = word in LW.W, LW.W.get(word)
    LW.W[word] = c
    try:
        LW.parse(word); return True
    except Exception:
        return False
    finally:
        if had: LW.W[word] = old
        else: LW.W.pop(word, None)


def deck_codes(atlas):
    atlas = pathlib.Path(atlas); out = {}
    for path, names, inline in [(atlas / "tools/legend_rules.py", ["LOCAL"], False),
                                (atlas / "tools/flsz_family.py", ["NEW"], False),
                                (atlas / "tools/th_family.py", None, True)]:
        for w, c in dict_literals(path, names, inline).items():
            if isinstance(w, str) and isinstance(c, str) and is_code(w, c):
                out.setdefault(w, {"code": c, "from": path.name})
    return out


def all_codes():
    codes = dict(LW.W); codes.update({k: v for k, v in LW.KEY_ONLY.items() if k not in codes})
    sources = {w: "legomorphic_words.py" for w in codes}
    for w, rec in json.loads(SNAPSHOT.read_text(encoding="utf-8")).items():
        if w not in codes:
            codes[w] = rec["code"]; sources[w] = rec["from"]
    return codes, sources


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--refresh":
        snap = deck_codes(sys.argv[2])
        SNAPSHOT.write_text(json.dumps(snap, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(len(snap), "deck codes written to", SNAPSHOT.name)
    else:
        codes, _ = all_codes()
        print(len(codes), "codes")
