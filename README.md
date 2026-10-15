# Reader for the Agent Conformance Reporting Format v0.1

A reader of report objects written in the "Agent Conformance Reporting
Format", v0.1 (W3C Agent Conformance and Benchmarking Community Group, list
message of 30 September 2026), built from the specification text alone.

## Purpose

For each member file the reader decides whether a conforming validator
refuses the report object (`reject`), does not (`accept`), or whether the
text leaves the outcome open (`cannot-tell`). A reject names the row or
sentence of the text that refuses the object, with its line number in
`spec/v01-text.txt`; a cannot-tell names the sentence that leaves it open
and the reading id from `reports/READINGS.md`.

## Command

    python3 -I reader.py members

Writes one JSON line per member to stdout, in id order, keys sorted:
`id`, `verdict`, `ground`, `grounds` (every refusal found), `open`
(reading ids left open for this member), `notes`, and `recount` (the
reader's own count of carried and referenced observations). One summary
line goes to stderr.

For a reproducible run:

    PYTHONHASHSEED=0 python3 -I reader.py members > out/run.jsonl 2> out/run.err

## Requirements

CPython 3.9 or later, standard library only. No network, no packages.
The reader checks at start that every line number it cites still carries
the quoted words in `spec/v01-text.txt`, and stops if one does not.

## Source restriction

The only source of rules is `spec/v01-text.txt`, the v0.1 text as posted to
the list. Nothing outside this repository was read while building it: not
the conformance corpus the text points to, not the list archive, not any
other implementation, not package documentation. General knowledge is used
only where the text names it (SHA-256, RFC 6962); where that was not enough,
the gap is in `reports/OPEN.md`. Every interpretation is in
`reports/READINGS.md`, and the build log is in `reports/STEPS.md`.

## Layout

- `reader.py` - the reader
- `spec/v01-text.txt` - the text (input, unchanged)
- `members/` - the 165 member files (input, unchanged)
- `reports/READINGS.md` - readings R01-R26, quoted and line-numbered
- `reports/STEPS.md` - steps, files opened, decisions
- `reports/OPEN.md` - what would have needed a source outside the repo
- `out/` - the recorded run
