# Known limitations of the frozen run

The findings below come from an outside audit of this reader:
James Siyuan He, `moltrust-reader-audit-001`, in
[Silentpartnercoding/agent-security-verifier-matrix](https://github.com/Silentpartnercoding/agent-security-verifier-matrix/tree/635f3d57eb6f90fdf4c6945778020c34521be0a1/experiments/moltrust-reader-audit-001)
at commit `635f3d57eb6f90fdf4c6945778020c34521be0a1`. The mutation results
are in `artifacts/mutation-results.json` and `artifacts/mutation-results-more.json`
there; the author's response is
[issue #8](https://github.com/Silentpartnercoding/agent-security-verifier-matrix/issues/8).

They hold against commit `6d8ee54b01d20a819869ceb9fcea096d59251f8c`, the tag
`frozen-run-1`, whose recorded output is `out/run.jsonl` (sha256
`505dfb71a640e7ef0eceb7f2d859e5cf08dac4c81bed80672135e0eb51b92130`). That
commit stays unchanged: the audit and the list post both point to it. A reader
that fixes any of this would be a different run under its own commit.

The reader reads whatever `.json` files are in the directory it is given. It
has no manifest, no expected member count and no digest of the member set, so
a complete and unaltered input is the caller's job. The checks under "How to
see it" are what a caller can do without changing the reader.

## Changed member set, exit 0

| Input | What happens | How to see it |
|---|---|---|
| One member file omitted | 164 lines, exit 0; omitting a rejected member gives `reject=27` | stderr summary says `members=164`, not 165 |
| One member file duplicated | 166 lines, exit 0, the member's line appears twice | `members=166`; the same `id` on two stdout lines |
| One member file renamed | output identical to the recorded run, exit 0 | not visible in the output; `git diff --stat frozen-run-1 -- members` lists the rename |
| One member file renamed to `.JSON` | the file is not read: 164 lines, `reject=27`, exit 0 | `members=164` |
| Empty directory | no lines, `members=0`, exit 0 | `members=0` |

## Reject turns into accept

| Input | What happens | How to see it |
|---|---|---|
| A duplicate JSON key whose second value overwrites the operative one | `v0e286b53de78162a` turns from reject into accept, exit 0 | not visible in the output; Python's `json` keeps the last value without a warning. Parse the members with an `object_pairs_hook` that refuses repeated keys, or compare against the tag |
| A rejected member's content replaced by an accepting body under the same `id` | `v0e286b53de78162a` turns from reject into accept, exit 0 | not visible in the output; `git diff frozen-run-1 -- members` shows the change |

## Duplicate evidence: the first occurrence wins

When a member carries two evidence objects with the same id, the reader uses
the first one and ignores the second. The verdict then depends on the order
inside the file: in the audit, `vf9b5623144960dda` stays accept when the
duplicate is appended and becomes reject (row 12) when it is prepended or the
pair is reversed. Nothing in the output shows that a duplicate was present; a
caller has to check that evidence ids are unique within each member.

## Five inputs crash the reader

| Input | Error | stdout before the crash |
|---|---|---|
| An evidence id that is a list | `TypeError: unhashable type: 'list'` | 160 lines |
| `observations` that is an integer | `TypeError: 'int' object is not iterable` | 160 lines |
| A negative `kind` that is a list | `TypeError: unhashable type: 'list'` | none |
| A member file that is not valid JSON | `json.decoder.JSONDecodeError` | none |
| A member file whose top level is an array | `AttributeError: 'list' object has no attribute 'get'` | none |

Each crash exits 1 with a traceback on stderr and no summary line. In the
first two, 160 complete lines are already on stdout when the process stops,
so a caller that reads stdout without checking the exit status takes a partial
result for a whole one. Check the exit status, and check that the last stderr
line is the `members=` summary.

## What the reader does not establish

The audit also records what the reader was never built to do, and these hold
for the frozen run as well. It does not run the checker a report names, does
not load or hash the artifacts a report refers to, and compares digest strings
supplied inside the report without showing that they describe any bytes. A
matching output reproduces this reader's reading of the reports; it does not
verify the claims inside them.

Two smaller points from the same audit: when `spec/v01-text.txt` is missing,
the citation check at start is skipped instead of failing; and the documented
`PYTHONHASHSEED=0 python3 -I ...` command does not set the seed, because `-I`
makes Python ignore `PYTHON*` environment variables.
