# Sound and Word Atlas

A route through English spelling for teachers: 32 steps in eight bands, with every word drawn in legomorphic notation. Each step has its own page with its words marked, the marks it brings in, its kernel words and contrasts, and the pages in Edward Carney's *A Survey of English Spelling* (Routledge, 1994) that back it.

The site is at https://dantewetherow.github.io/sound-and-word-atlas/.

## What's where

- `docs/` is the site itself. GitHub Pages publishes this folder as it is.
- `build/` has what makes it:
  - `build_site.py` writes the pages from `data/route.json`.
  - `parse_route.py` turns the manual's route section (`data/route_section.md`) into `data/route.json`.
  - `x2t.py` converts a read of the manual from the Claude Docs connector into markdown.
  - `legomorphic_words.py` draws the marked words.
  - `known_codes.py` and `deck_codes.json` hold the codes the session decks already use, and `site_codes.py` holds the codes written for route words that had none.
  - `site.css` is the stylesheet.

## The manual stays the source

The route and its notes come from the *Legomorphic notation* manual. To change what the site says, change the manual, then rebuild. Choices about how a word is marked wait for a ruling in the manual's Marking calls tab, under "From the atlas site", and `site_codes.py` changes to match once they're ruled.

## Rebuilding

1. Read the manual's route section (from "The route" to "The operator system") with the Claude Docs connector, save the result, and convert it with `build/x2t.py`. Keep the part before "## The operator system" as `build/data/route_section.md`.
2. `python3 build/parse_route.py build/data/route_section.md build/data/route.json`
3. To rebuild the word cards, run `npm install @fontsource-variable/lexend` somewhere outside the repository, then `python3 build/build_elp_cards.py <that folder>/node_modules docs/cards <a scratch folder>`. The words come from `build/data/elp_hfw.json`, taken from the SD23 ELP guide (pp. 16–17).
4. `python3 build/build_site.py build/data/route.json docs --standalone`. It writes the Word cards page when the card PDFs are in `docs/cards`.
5. Commit and push. Pages republishes the site within a few minutes.

To refresh the deck codes from a copy of the atlas folder, run `python3 build/known_codes.py --refresh /path/to/atlas`.

Without `--standalone`, the home page is written with no doctype or head, which is what the claude.ai artifact version of the site needs.
