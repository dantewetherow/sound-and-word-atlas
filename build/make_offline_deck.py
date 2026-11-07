"""An offline copy of a deck: the Google Fonts links are replaced by the same fonts, embedded, so the file runs
from a USB stick or a laptop with no network and no sign-in.

Run:  python3 make_offline_deck.py <deck.html> <node_modules with the @fontsource packages> <out.html>
"""
import base64, pathlib, re, sys
deck, fonts, out = (pathlib.Path(a) for a in sys.argv[1:4])
LATIN = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
LATIN_EXT = "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF"
GREEK = "U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF"
def face(family, rel, style, weight, rng):
    data = base64.b64encode((fonts / rel).read_bytes()).decode()
    return f'@font-face{{font-family:"{family}";font-style:{style};font-weight:{weight};font-display:block;src:url(data:font/woff2;base64,{data}) format("woff2");unicode-range:{rng};}}'
V, G = "@fontsource-variable", "@fontsource/gentium-plus/files"
rules = [
 face("Fraunces", f"{V}/fraunces/files/fraunces-latin-opsz-normal.woff2", "normal", "100 900", LATIN),
 face("Fraunces", f"{V}/fraunces/files/fraunces-latin-ext-opsz-normal.woff2", "normal", "100 900", LATIN_EXT),
 face("Fraunces", f"{V}/fraunces/files/fraunces-latin-opsz-italic.woff2", "italic", "100 900", LATIN),
 face("Fraunces", f"{V}/fraunces/files/fraunces-latin-ext-opsz-italic.woff2", "italic", "100 900", LATIN_EXT),
 face("Lexend", f"{V}/lexend/files/lexend-latin-wght-normal.woff2", "normal", "100 900", LATIN),
 face("Lexend", f"{V}/lexend/files/lexend-latin-ext-wght-normal.woff2", "normal", "100 900", LATIN_EXT),
 face("Gentium Plus", f"{G}/gentium-plus-latin-400-normal.woff2", "normal", "400", LATIN),
 face("Gentium Plus", f"{G}/gentium-plus-latin-ext-400-normal.woff2", "normal", "400", LATIN_EXT),
 face("Gentium Plus", f"{G}/gentium-plus-greek-400-normal.woff2", "normal", "400", GREEK),
 face("Gentium Plus", f"{G}/gentium-plus-latin-400-italic.woff2", "italic", "400", LATIN),
 face("Gentium Plus", f"{G}/gentium-plus-latin-ext-400-italic.woff2", "italic", "400", LATIN_EXT),
]
s = deck.read_text(encoding="utf-8")
links = re.findall(r'<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>\n?', s)
assert len(links) == 3, links
for l in links: s = s.replace(l, "")
s = s.replace("</title>", "</title>\n<style>/* fonts built in, so this copy runs offline */\n" + "\n".join(rules) + "\n</style>", 1)
assert "googleapis" not in s and "gstatic" not in s
out.write_text(s, encoding="utf-8"); print("wrote", out, f"{out.stat().st_size / 1e6:.2f} MB")
