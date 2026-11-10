#!/usr/bin/env python3
"""ReadTime - reading time, speaking time and a readability estimate.

Reads plain text (from --text or --file) and reports word and sentence
counts, how long the text takes to read silently (200 wpm) or aloud
(150 wpm), and a Flesch Reading Ease estimate.

Python 3, standard library only.
"""

import argparse
import math
import re
import sys

READING_WPM = 200
SPEAKING_WPM = 150

VOWELS = "aeiouy"


def count_syllables(word):
    """Estimate the syllables in one word (a heuristic, not exact).

    Lowercase the word and strip non-letters, count groups of
    consecutive vowels (a e i o u y), subtract 1 if the word ends in
    a silent "e" and the count is over 1, and never return less
    than 1 for a word.
    """
    cleaned = re.sub(r"[^a-z]", "", word.lower())
    if not cleaned:
        return 1
    groups = 0
    prev_was_vowel = False
    for ch in cleaned:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_was_vowel:
            groups += 1
        prev_was_vowel = is_vowel
    if cleaned.endswith("e") and groups > 1:
        groups -= 1
    return max(1, groups)


def count_sentences(text):
    """Count sentences by splitting on . ! ? (non-empty segments)."""
    segments = re.split(r"[.!?]", text)
    return sum(1 for seg in segments if seg.strip())


def format_time(total_seconds):
    minutes, seconds = divmod(total_seconds, 60)
    return "{}:{:02d}".format(minutes, seconds)


def flesch_band(score):
    if score >= 90:
        return "Very easy"
    if score >= 80:
        return "Easy"
    if score >= 70:
        return "Fairly easy"
    if score >= 60:
        return "Standard"
    if score >= 50:
        return "Fairly difficult"
    if score >= 30:
        return "Difficult"
    return "Very confusing"


def analyse(text):
    words = text.split()
    word_count = len(words)
    sentence_count = count_sentences(text)
    if sentence_count == 0 and word_count > 0:
        # Words but no sentence punctuation: treat as one sentence.
        sentence_count = 1
    syllable_count = sum(count_syllables(w) for w in words)

    reading_seconds = math.ceil(word_count / READING_WPM * 60)
    speaking_seconds = math.ceil(word_count / SPEAKING_WPM * 60)

    lines = []
    lines.append("Words: {}".format(word_count))
    lines.append("Sentences: {}".format(sentence_count))
    lines.append(
        "Reading time ({} wpm): {}".format(
            READING_WPM, format_time(reading_seconds)
        )
    )
    lines.append(
        "Speaking time ({} wpm): {}".format(
            SPEAKING_WPM, format_time(speaking_seconds)
        )
    )
    if sentence_count == 0 or word_count == 0:
        lines.append("Flesch Reading Ease: n/a (no sentences)")
    else:
        raw_score = (
            206.875
            - 1.015 * (word_count / sentence_count)
            - 84.6 * (syllable_count / word_count)
        )
        display_score = max(0.0, min(100.0, raw_score))
        lines.append(
            "Flesch Reading Ease: {:.1f} ({})".format(
                display_score, flesch_band(display_score)
            )
        )
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Estimate reading time, speaking time and readability "
            "(Flesch Reading Ease) for a piece of text."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="The text to analyse.")
    group.add_argument("--file", help="Path to a text file to analyse.")
    args = parser.parse_args(argv)

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            parser.error("cannot read file: {}".format(exc))
    else:
        text = args.text

    print(analyse(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
