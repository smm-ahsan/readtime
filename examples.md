# Examples

Real output from ReadTime, captured from an actual run.

## A 400-word file of simple sentences

The test file was built by repeating one simple 10-word sentence
("The quick brown fox jumps over the lazy dog today.") 40 times,
giving exactly 400 words in 40 sentences.

Command:

```bash
python3 readtime.py --file readtime_test.txt
```

Output:

```
Words: 400
Sentences: 40
Reading time (200 wpm): 2:00
Speaking time (150 wpm): 2:40
Flesch Reading Ease: 86.7 (Easy)
```

## A single word with no sentence punctuation

Text with words but no sentence punctuation counts as one sentence,
so a lone word still gets a full report instead of an error.

Command:

```bash
python3 readtime.py --text "Hello"
```

Output:

```
Words: 1
Sentences: 1
Reading time (200 wpm): 0:01
Speaking time (150 wpm): 0:01
Flesch Reading Ease: 36.7 (Difficult)
```
