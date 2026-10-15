# Steps

Repo paths only. One entry per step: files opened, what was decided.

## Step 1 - read the text

Opened: `spec/v01-text.txt` (all 967 lines).

Decided: the text is the only rule source. It gives the record vocabulary
(section 1), the evidence object (2), carry-or-reference and the reading
table (3), tree-shape declaration (3.1), the rejection table (4), the
roll-up (5), and the conformance appendix (10). It gives no JSON
serialization, so every mapping from a member's key names onto the text's
terms is a reading (READINGS.md R01).

## Step 2 - survey the member encoding

Opened: `members/*.json` (all 165), through throw-away survey scripts that
listed every key path and the distinct values under it, printed a compact
one-line form of the 81 members whose run domain is `d-run`, and grouped
the 84 members whose run domain is `d-disensor` by structure (state,
qualifier values, evidence slots, digest match against the member's own
`resolves`). The survey scripts lived in the session scratchpad outside the
repo; they were written by me, read only repo files, and are not part of
the build. No other path was read.

Decided: the members use key names that are partly the text's own (`state`,
`cause`, `other-verdict`, `discrimination`, `changed`, `fixed`, `compared`,
`moved`, `delta`) and partly not (`check-set`, `leaf-count`, `tree-shape`,
`negative-capable`, `kind`, `declared-exclusion`, `completeness`,
`carried`/`reference` per observation). Each needs a reading before code.

Honesty note: the agent harness placed two documents into my context before
I started (the operator's global instruction file and a memory index). Both
concern unrelated projects; neither mentions this format, its rows or its
corpus. I did not open them; they were supplied. The harness also saved one
long tool output of mine to a file outside the repo; I did not read that
file back, I re-ran the survey with shorter output instead.

## Step 3 - write the readings down

Opened: `spec/v01-text.txt` (to quote and line-number each reading).

Decided: readings R01-R26 in `reports/READINGS.md`, committed one per
commit before any rule was coded, plus two refinements (R26 ground order,
R09 list comparison). Readings where the reader takes neither side and
answers cannot-tell: R04 (availability-failure only), R05 (unknown written
on a non-verdict record), R11, R12 (where the fallback would fire), R13
(where declared and recomputed moved disagree), R16, R17, R19, R20 (unknown
filling only), R21, R23 (claim values), R24 (state counts), R25.

## Step 4 - code the rules

Opened: `reader.py` (my own file), `spec/v01-text.txt` (through the
reader's citation check), `members/` (through the reader's output).

Decided: one rule per commit, in this order: record walk and state list;
cause vocabulary and line 110; rows 1, 2, 3, 4, 5, 7; qualifier parsing;
rows 6, 8, 9, 10, 11; run context and domain slots; evidence slots; declared
arity; dangling references; row 12; observation resolution and moved
recompute; row 13; line 164 containment; row 14; tree shape; leaf count;
5.4 silence, shown-by-run, control-failed, control binding, prior run;
run-level rejection; claim values; roll-up counts; the recounted counter.
Code written from the text; no code from any other implementation was
reproduced or consulted.

## Step 5 - check and run

Opened: `reader.py`, `out/run.jsonl`, `out/run.err`.

Decided: the reader's source parses under the CPython 3.9 grammar, and four
runs (PYTHONHASHSEED 0, 0, 1, 12345) gave byte-identical output under
CPython 3.9.6, the only interpreter reachable by name here. No 3.1x
interpreter was found by trying `python3.10` to `python3.14`; that gap is in
`reports/OPEN.md`. I did not judge whether the verdicts are right.

## Step 6 - rewrite the lines that coincide with other implementations

Input: the coordinator's list of 40 line numbers of `reader.py` at 0ecc76b
whose whitespace-stripped text occurs in at least one implementation I have
not seen. I was told only the line numbers, not the other code.

Opened: `reader.py` (at 0ecc76b and the working copy), `out/run.jsonl`.

Decided: every listed line was rewritten by changing the structure, not by
renaming: the three imports became one line; the docstring closes on its
text line; dict and tuple literals close on their last entry; bare
`return`, `else:` and `continue` were removed by wrapping or by splitting
functions (`read_tree`, `count_sides`, `read_json`); the cause vocabulary is
built from the CAP-1 list plus the list's additions; rows 2 and 3 are a
table (`STATE_CAUSE_ROWS`); moved is recomputed from a table of compared
names; the 5.4 fillings dispatch through `FILLINGS`; the roll-up check moved
into `judge`; the verdict is set accept-first and overridden; `run` raises
SystemExit for usage and returns nothing. One new line repeated a listed
line (`if "carried" in observation:` in `count_sides`) and was rewritten
again. A check script confirms no listed line text remains in `reader.py`.
No line had to stay shared, so OPEN.md lists none.

Behaviour change outside the verdicts: a wrong argument count now exits
with status 1 (SystemExit message) instead of 2.

Result: `out/run.jsonl` is byte-identical to the one at 0ecc76b (sha256
505dfb71a640e7ef0eceb7f2d859e5cf08dac4c81bed80672135e0eb51b92130), also
with PYTHONHASHSEED 1 and 777; the source still parses under the 3.9
grammar.

## Step 7 - second line check

Input: the coordinator's second list for `reader.py` at 966c10f: lines 67,
520, 556. Only line numbers were given.

Opened: `reader.py` (at 966c10f and the working copy), `out/run.jsonl`.

Decided: both file reads (the spec in `verify_cites`, the members in
`load`) now go through one helper `read_text`, which opens in binary and
decodes UTF-8; members are parsed with `json.loads`. This removes the
`lines = []` initialiser (now one conditional expression) and the
text-mode `open(..., encoding=...)` line. In `count_sides` the observation
is no longer replaced when it is not a dict; its keys are read through a
guarded view instead. A check script confirms none of the three line
texts remains. No line had to stay shared.

Result: `out/run.jsonl` byte-identical, sha256
505dfb71a640e7ef0eceb7f2d859e5cf08dac4c81bed80672135e0eb51b92130; the
source parses under the 3.9 grammar.
