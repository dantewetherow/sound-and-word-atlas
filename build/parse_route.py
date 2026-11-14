"""Parse the manual's route section (converted text) into route.json: bands, steps, words, marks, kernel, Carney, and
the move and its research for the steps that teach one (the manual's "Moves and research", added 10 November 2026),
and the affixes and roots placed at each step (its "Parts on the steps", added the same day)."""
import re, json, sys
src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8").read()
intro = re.search(r"## The (?:route|path)\n(.+?)\n", t).group(1).replace("[link: orientation map]", "orientation map")
bands, steps = [], {}
for m in re.finditer(r"### ([^\n|]+?)\n\| Step \| Words \| New marks \| Kernel words \|(.+?)(?=### |Steps 16 to 32|$)", t, re.S):
    band = m.group(1).strip(); body = m.group(2)
    cells = [c.strip() for c in body.split("|")]
    cells = [c for c in cells if c != ""]
    rows = [cells[i:i + 4] for i in range(0, len(cells) - len(cells) % 4, 4)]
    nums = []
    for step, words, marks, kernel in rows:
        n, title = re.match(r"(\d+)\.\s*(.+)", step).groups()
        steps[int(n)] = {"n": int(n), "title": title, "band": band, "words_md": words, "marks": marks, "kernel_md": kernel}
        nums.append(int(n))
    bands.append({"name": band, "steps": nums})
def table3(heading, columns):
    """A three-column table under its own heading, to the next heading or the end: (intro, rows)."""
    m = re.search(rf"### {re.escape(heading)}\n(.+?)\n\| Step \| {re.escape(columns)} \|(.+?)(?=\n### |\Z)", t, re.S)
    if not m: return "", []
    cells = [c.strip() for c in m.group(2).split("|")]; cells = [c for c in cells if c != ""]
    return m.group(1).strip(), [cells[i:i + 3] for i in range(0, len(cells) - len(cells) % 3, 3)]
carney_intro, rows = table3("Carney's pages for each step", "What the path teaches | Carney (1994)")
for n, _, pages in rows:
    steps[int(n)]["carney"] = pages
moves_intro, rows = table3("Moves and research", "The move | Research")
for n, move, research in rows:
    steps[int(n)]["move"], steps[int(n)]["research"] = move, research
parts_intro, rows = table3("Parts on the steps", "Affixes and roots | Why here")
for n, ps, why in rows:
    steps[int(n)]["parts"], steps[int(n)]["parts_why"] = [x.strip() for x in ps.replace("*", "").split(",") if x.strip()], why
open_m = re.search(r"Open on these steps:\n(.+?)\n\n### Carney", t, re.S)
open_items = [re.sub(r"\s+", " ", x).strip() for x in open_m.group(1).split("- ") if x.strip()]
notes = re.search(r"\| Steps 16 to 32(.+?)\nOpen on these steps", t, re.S)
def words_of(md):
    md = md.replace("**", "")
    main = md.split("; contrast")[0]
    out = []
    for w in re.findall(r"\*([^*]+)\*", main):
        for part in re.split(r"[,/→]| and ", w):
            p = part.strip().strip("*").strip()
            if p and p not in out: out.append(p)
    return out
for s in steps.values():
    s["words"] = words_of(s["words_md"])
    c = re.search(r"; contrast (.+)$", s["words_md"])
    s["contrast_md"] = c.group(1) if c else ""
json.dump({"intro": intro, "bands": bands, "steps": [steps[k] for k in sorted(steps)],
           "carney_intro": carney_intro, "moves_intro": moves_intro, "parts_intro": parts_intro, "open": open_items,
           "note_16_32": ("Steps 16 to 32" + notes.group(1)).strip() if notes else ""},
          open(out, "w"), ensure_ascii=False, indent=1)
print(len(steps), "steps;", [ (b["name"], b["steps"]) for b in bands ])
print("open items:", len(open_items), "· moves:", [s["n"] for s in steps.values() if s.get("move")])
