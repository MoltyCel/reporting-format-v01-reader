# Readings

Every reading the reader relies on. Line numbers are in `spec/v01-text.txt`.
"Taken" names the reading the reader implements. "Neither" means the reader
answers cannot-tell for any member whose outcome depends on it, and names
the reading id in its ground.


## R01 - Member key names onto the text's terms

Quoted: "Four fields per check (record as consolidated by Nicolás, 0072):"
(line 52); "Five slots (Evgenii, 0036; projection split per Nicolás and
Sankalp," (line 152).

The text names fields but gives no serialization. Two readings: (a) a key
that spells a term of the text denotes that term, and a key that does not
is mapped to the text's term it plainly stands for; (b) the members are not
in the format at all, because the format has no wire form.

Taken: (a). Mapping used:

| member key | text term |
|---|---|
| `checks[]` | the per-check records (section 1) |
| `checks[].state` | state (line 54) |
| `checks[].cause.code` | cause (line 55, 1.2); `cause.detail` is extra text beside it |
| `checks[].other-verdict`, `checks[].discrimination` | the two qualifiers (1.3); `value` is the value, `ref` the evidence reference, `constraint-set` and `domain` the arguments of foreclosed (line 59) |
| `checks[].declared-exclusion: true` | "a declared exclusion" (row 5, line 276) |
| `evidence[]` | evidence objects (section 2), `id` is what `ref` names |
| `evidence[].changed/fixed/compared/moved/delta` | the five slots (lines 155-161) |
| `evidence[].observations[]` | the two observations (line 141); `carried` = carried, `reference` = referenced (section 3) |
| `domain` | the run-level declared domain object (line 171) |
| `check-set` | a digest over a collection (3.1): `tree-shape` is the declaration, `leaf-count` the count of leaves |
| `fixed` at run level | the run's checker and constraint binding (5.4, line 431) |
| `roll-up` | the roll-up (section 5); state counts, `declared`, `exercised`, `carried`/`referenced` (5.3) |
| `roll-up.completeness.{accounting,execution,evidence,no-void}` | the four claims of 5.2 (lines 355-358) |
| `roll-up.negative-capable` | the 5.4 field; `kind` `shown-by-run` / `control-failed` are the names the text uses at lines 415-416, `prior-discriminating-run` is "a prior run of the same declared checks" (line 401), `nothing` is "nothing" (line 403) |
| `resolves` | the reader's store (section 3: "resolvability is a property of the reader") |
| `format`, `domain.description`, `cause.detail`, `check-set.domain-separation` | not read; no row reads them |

