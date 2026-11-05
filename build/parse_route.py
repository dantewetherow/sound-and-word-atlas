"""Parse the manual's route section (converted text) into route.json: bands, steps, words, marks, kernel, Carney."""
import re, json, sys
src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8").read()
intro = re.search(r"## The route\n(.+?)\n", t).group(1).replace("[link: orientation map]", "orientation map")
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
car = re.search(r"### Carney's pages for each step\n(.+?)\n\| Step \| What the route teaches \| Carney \(1994\) \|(.+)$", t, re.S)
carney_intro = car.group(1).strip()
cells = [c.strip() for c in car.group(2).split("|")]; cells = [c for c in cells if c != ""]
for i in range(0, len(cells) - len(cells) % 3, 3):
    n, _, pages = cells[i:i + 3]
    steps[int(n)]["carney"] = pages
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
           "carney_intro": carney_intro, "open": open_items,
           "note_16_32": ("Steps 16 to 32" + notes.group(1)).strip() if notes else ""},
          open(out, "w"), ensure_ascii=False, indent=1)
print(len(steps), "steps;", [ (b["name"], b["steps"]) for b in bands ])
print("open items:", len(open_items))
