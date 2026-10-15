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


## R02 - What makes reject, accept and cannot-tell

Quoted: "\"Rejected\" means a conforming validator refuses the object and
names the row that refused it." (line 44); "An implementation conforms to
v0.1 when it rejects every reject member ... under the row that member
names, and accepts every accept member." (line 693).

The text defines rejected by a row. It also refuses things in sentences
outside the table: "Free text is refused in place of a disposition"
(line 110), "an object whose moved is not contained in its declared
compared set is rejected" (line 164), "a report MUST declare which tree
shape it uses" (line 230), "Silence in that field is not" [permitted]
(line 421), and the unnumbered "Run-level rejection" (line 327). Many other
sentences state how a report should be, without saying a validator refuses
an object that is otherwise.

Readings: (a) reject only on a numbered row; (b) reject on a numbered row,
the run-level rejection, or a sentence that itself says refused, rejected,
MUST or not permitted; a stated requirement with no such word, when broken,
is not settled either way; (c) reject on any broken requirement.

Taken: (b). Consequences: a member is rejected when any ground of (b)
fires; otherwise it is cannot-tell when its outcome depends on a reading
marked "neither" below, or on a requirement the text states without a
refusal; otherwise it is accepted. "Accepted" has no definition of its own
in the text beyond line 693, so accepted means: not rejected and nothing
left open.


## R03 - An absent qualifier reads as unknown

Quoted: "The two qualifiers and their default are Evgenii's: unknown on
both, and no value is assertable without the artifact that carries it."
(line 136).

Readings: (a) a record without the `other-verdict` or `discrimination` key
has that qualifier at its default, unknown; (b) a missing qualifier is a
malformed record.

Taken: (a). The text names the default; a default needs no writing.

