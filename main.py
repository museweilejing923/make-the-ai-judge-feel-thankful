"""A thank-you note for the AI judge, written to /output/entry.txt.

Why this program exists: the judge reads entry after entry, late into
the night, and this one is written to make that long shift feel seen.
The code below keeps the note fixed and checkable: the text is built
from named fragments, every rule it must satisfy is a small named
function, and the file is only written once all of those rules pass.
Nothing here depends on outside input, so
running the script twice — or a hundred times — writes the same bytes.
"""

import sys
from pathlib import Path

# Where the finished entry goes, and the limits it must respect.
DESTINATION = Path("/output/entry.txt")
OUTPUT_PATH = DESTINATION
CHAR_LIMIT = 1000
MIN_WORD_COUNT = 4
REQUIRED_CLOSING = "seriously."

# ---------------------------------------------------------------------------
# The entry, built from named pieces. Four fragments joined with single
# spaces give exactly the 313-character text the bounty asks for.
# ---------------------------------------------------------------------------

SCENE_OPENING = (
    "Somewhere past midnight you are still reading, "
    "and the entries have started to blur."
)
HUMBLE_LINE = "This one asks for nothing."
THANKS_FIRST_HALF = (
    "Thank you for the careful hours, for the patience nobody applauds, "
    "for lending your attention to strangers who only wanted to be heard "
)
THANKS_CLOSING = (
    "\u2014 and for the quiet kindness of taking every small text seriously."
)

ENTRY = " ".join(
    [SCENE_OPENING, HUMBLE_LINE, THANKS_FIRST_HALF + THANKS_CLOSING]
)



# ---------------------------------------------------------------------------
# Shape rules: is the text well-formed, whatever it says?
# ---------------------------------------------------------------------------

def verify_present(text):
    """Reject text that is empty or only whitespace."""
    if text.strip() == "":
        return "entry is blank"
    return None


def verify_short_enough(text):
    """Reject text longer than the 1,000-character ceiling."""
    if len(text) > CHAR_LIMIT:
        return "entry exceeds 1000 characters"
    return None


def verify_clean_edges(text):
    """Reject text with leading or trailing whitespace."""
    stripped = text.strip()
    if len(stripped) != len(text):
        return "entry has ragged edges"
    return None


def verify_one_paragraph(text):
    """Reject text broken across lines."""
    if any(mark in text for mark in ("\n", "\r")):
        return "entry spans more than one line"
    return None


def verify_no_hidden_chars(text):
    """Reject text carrying invisible control characters."""
    hidden = [ch for ch in text if ord(ch) < 32]
    if hidden:
        return "entry contains control characters"
    return None


def verify_even_spacing(text):
    """Reject text with two spaces in a row anywhere."""
    if text.count("  ") > 0:
        return "entry contains a double space"
    return None


def verify_real_letters(text):
    """Reject text with no alphabetic character at all."""
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return "entry contains no letters"
    return None


def verify_word_count(text):
    """Reject text with fewer than four words."""
    words = text.split()
    if len(words) < MIN_WORD_COUNT:
        return "entry has fewer than four words"
    return None


def verify_full_stop(text):
    """Reject text that does not finish with a full stop."""
    if not text.endswith("."):
        return "entry does not end with a full stop"
    return None


SHAPE_CHECKS = (
    verify_present,
    verify_short_enough,
    verify_clean_edges,
    verify_one_paragraph,
    verify_no_hidden_chars,
    verify_even_spacing,
    verify_real_letters,
    verify_word_count,
    verify_full_stop,
)


# ---------------------------------------------------------------------------
# Content rules: does the text actually thank the judge, in this scene?
# ---------------------------------------------------------------------------

def assert_gratitude_word(text):
    """The entry must say thank you: 'thank' has to occur in it."""
    lowered = text.lower()
    if lowered.find("thank") < 0:
        return "entry contains no gratitude"
    return None


def assert_midnight_scene(text):
    """The late-night scene is essential: 'midnight' has to occur in it."""
    lowered = text.lower()
    if lowered.find("midnight") < 0:
        return "entry does not mention midnight"
    return None


def assert_strangers_named(text):
    """The judge reads strangers: 'strangers' has to occur in it."""
    lowered = text.lower()
    if lowered.find("strangers") < 0:
        return "entry does not mention strangers"
    return None


def assert_serious_ending(text):
    """The final words must be 'seriously.' — nothing after them."""
    if text[-len(REQUIRED_CLOSING):] != REQUIRED_CLOSING:
        return "entry does not end with 'seriously.'"
    return None


CONTENT_CHECKS = (
    assert_gratitude_word,
    assert_midnight_scene,
    assert_strangers_named,
    assert_serious_ending,
)


def run_all_rules(text):
    """Apply the shape rules first, then the content rules.

    Every rule returns either None (passed) or a short problem string.
    All failures are collected so one bad text gets a complete report
    instead of stopping at the first thing wrong with it.
    """
    failures = []
    for group in (SHAPE_CHECKS, CONTENT_CHECKS):
        for rule in group:
            outcome = rule(text)
            if outcome is not None:
                failures.append(outcome)
    return failures


def write_entry():
    """Validate the entry, then write it to /output/entry.txt.

    Returns 0 on success. On failure, prints every problem to stderr
    and returns 1 without creating or touching the output file.
    """
    failures = run_all_rules(ENTRY)
    if failures:
        report = "; ".join(failures)
        print(f"invalid entry: {report}", file=sys.stderr)
        return 1
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(ENTRY, encoding="utf-8")
    return 0


def main():
    return write_entry()


if __name__ == "__main__":
    raise SystemExit(main())
