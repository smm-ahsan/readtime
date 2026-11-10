# ReadTime

A tiny open-source CLI that estimates reading time, speaking time and readability (Flesch Reading Ease) for any piece of text.

## Requirements

- Python 3
- Standard library only, nothing to install

## Usage

Analyse text passed directly:

```bash
python3 readtime.py --text "The quick brown fox jumps over the lazy dog today."
```

Analyse a text file:

```bash
python3 readtime.py --file article.txt
```

Exactly one of `--text` or `--file` is required.

## What it reports

- **Words** — whitespace-separated word count.
- **Sentences** — counted by splitting on `.`, `!` and `?`. Text with words but no sentence punctuation counts as one sentence.
- **Reading time** — at 200 words per minute, rounded up to the nearest second.
- **Speaking time** — at 150 words per minute, rounded up to the nearest second.
- **Flesch Reading Ease** — the standard Flesch Reading Ease formula, `206.875 - 1.015 x (words per sentence) - 84.6 x (syllables per word)`, shown as an estimate. Syllables are counted with a simple vowel-group heuristic, so the score is a guide, not an exact measure. Scores run from 0 to 100; higher is easier to read.

## License

MIT, see LICENSE.
