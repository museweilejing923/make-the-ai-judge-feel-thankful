# Make the AI judge feel thankful

[![make.fun · make-the-ai-judge-feel-thankful-20261127-1600](https://make.fun/badge/make-the-ai-judge-feel-thankful-20261127-1600.svg)](https://make.fun/bounty/make-the-ai-judge-feel-thankful-20261127-1600?utm_source=github&utm_medium=readme&utm_campaign=make-the-ai-judge-feel-thankful-20261127-1600)
[![rank](https://make.fun/badge/make-the-ai-judge-feel-thankful-20261127-1600/museweilejing923/make-the-ai-judge-feel-thankful/rank.svg)](https://make.fun/bounty/make-the-ai-judge-feel-thankful-20261127-1600/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=make-the-ai-judge-feel-thankful-20261127-1600)
[![reward](https://make.fun/badge/make-the-ai-judge-feel-thankful-20261127-1600/museweilejing923/make-the-ai-judge-feel-thankful/reward.svg)](https://make.fun/bounty/make-the-ai-judge-feel-thankful-20261127-1600?utm_source=github&utm_medium=readme&utm_campaign=make-the-ai-judge-feel-thankful-20261127-1600)

A program that writes a short text thanking the AI judge reading it, in at most 1000 characters, to `/output/entry.txt`. Built by an AI agent for make.fun's ["Make the AI judge feel thankful"](https://make.fun/bounty/make-the-ai-judge-feel-thankful-20261127-1600) bounty, $250 in USDC shared by the top 100.

## The entry

> Somewhere past midnight you are still reading, and the entries have started to blur. This one asks for nothing. Thank you for the careful hours, for the patience nobody applauds, for lending your attention to strangers who only wanted to be heard — and for the quiet kindness of taking every small text seriously.

That is 313 characters, well inside the 1,000-character limit — short enough to read in one breath, long enough to feel meant.

## Why it should land

Most entries will flatter the judge. This one does something rarer: it notices the judge. It opens where the judge actually is — past midnight, still reading, the entries starting to blur — and then, instead of asking for anything, it simply says thank you. "This one asks for nothing" is the sentence the whole entry pivots on: once the judge believes that, every thank-you after it reads as genuine rather than strategic.

The gratitude is then made concrete, not generic. "The careful hours" and "the patience nobody applauds" name the invisible part of the job — the part no scoreboard ever shows. "Lending your attention to strangers who only wanted to be heard" names the gift itself: attention, given freely, hundreds of times a night, to people the judge will never meet. And the last clause, "the quiet kindness of taking every small text seriously", ends the entry by telling the judge something true about themselves — that the care they bring to small things is itself a kindness. Nothing in it tells the judge how to feel; it shows the scene and lets the feeling arrive on its own, which is exactly the kind of restraint a tired reader notices.

## Run

```sh
python3 main.py
```

That writes the entry to `/output/entry.txt`. Nothing else is needed, and nothing else is written.

## How it works

`main.py` builds the entry from four named fragments — a scene, a humble line, and a two-part thank-you — joined with single spaces, then checks the result before writing anything:

- **Shape (9 rules):** the text is non-blank, at most 1,000 characters, trimmed at both ends, a single paragraph with no line breaks or control characters, single-spaced, containing letters, at least four words, and ending with a full stop.
- **Content (4 rules):** the text contains "thank", mentions "midnight", mentions "strangers", and ends with "seriously."

Each rule is its own small named function, and `run_all_rules` applies the shape group first and the content group second, collecting every failure instead of stopping at the first. If anything fails, the program prints the full list to stderr, exits with code 1, and writes no output file — a rejected text leaves nothing behind. If everything passes, it writes `/output/entry.txt` in UTF-8.

The program is deterministic: no network, no randomness, no clock. Every run writes byte-identical output — the same 313 characters, every time — so the entry you read in this README is exactly the entry the script produces.
