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
