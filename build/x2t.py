import json, re, html, sys
raw = json.load(open(sys.argv[1]))
txt = [r["text"] for r in raw if r["text"].lstrip().startswith("{")][0] if isinstance(raw, list) else raw
# the tool text may carry a preamble line before the JSON
i = txt.find("{\"verdict\"")
d = json.loads(txt[i:])
x = d["data"]["xml"]
t = x
t = re.sub(r"<paragraph[^>]*heading='(\d)'[^>]*>", lambda m: "\n\n" + "#" * int(m.group(1)) + " ", t)
t = re.sub(r"<paragraph[^>]*>", "\n", t)
t = re.sub(r"<row[^>]*>", "\n|", t)
t = re.sub(r"</cell>", " |", t)
t = re.sub(r"<listItem[^>]*>", "\n- ", t)
t = re.sub(r"<media [^>]*alt='([^']*)'[^>]*/>", r"[image: \1]", t)
t = re.sub(r"<link[^>]*href='([^']*)'[^>]*>", r"[link: ", t)
t = re.sub(r"</link>", "]", t)
t = re.sub(r"</?italic>", "*", t)
t = re.sub(r"</?bold>", "**", t)
t = re.sub(r"<gap[^>]*/>", " [gap] ", t)
t = re.sub(r"<[^>]+>", "", t)
t = html.unescape(t)
t = re.sub(r"\|\s*\n\s*", "| ", t)
t = re.sub(r"\n{3,}", "\n\n", t)
open(sys.argv[2], "w").write(t)
print(sys.argv[2], len(t), "chars; complete:", d["data"].get("complete"), "next:", d["data"].get("next"))
