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


## R04 - The cause vocabulary is closed; free text is not a cause

Quoted: "Its vocabulary is the eight closed dispositions of CAP-1" (line 76),
the eight names (lines 78-79), the added values evidence-does-not-hold
(line 85), integrity-failure (line 89), precondition-unsatisfiable
(line 93), confinement-failed-during-check (line 99); "Free text is refused
in place of a disposition, for CAP-1's reason:" (line 110).

Readings for a `cause.code` outside the vocabulary: (a) it is free text in
place of a disposition, refused by line 110, and on a non-verdict state the
record then has no cause, so row 1 fires as well; (b) it is an unknown
value with no row.

Taken: (a). A `cause.detail` string beside a valid code is not "in place
of" a disposition and is not read.

Sub-reading: line 89 says "integrity-failure kept separate from
availability-failure". Whether availability-failure is a value of its own
or a name for unavailable is not said. Neither: a member using
`availability-failure` would be cannot-tell under R04. (No reading is
needed for integrity-failure: row 3 uses it as a value.)


## R05 - Row 6: what "carrying" a qualifier means

Quoted: "6 a non-verdict state carrying either qualifier narrowed 0038"
(line 278); "Four fields per check" (line 52); "cause required on the three
non-verdict states, absent on the two verdict states" (line 55).

Readings: (a) carrying means the qualifier is written at all, so a
non-verdict record with `other-verdict: {value: unknown}` fires row 6;
(b) carrying means asserting a value other than the default unknown, since
every record has four fields (line 52) and the text states absence only for
cause (line 55). "narrowed 0038" says the row was narrowed but not to what.

Taken: (b) where a non-verdict record carries a non-default value (row 6
fires under both readings). Neither where it writes the qualifier with the
value unknown: such a member is cannot-tell under R05.


## R06 - Row 11: which values need an evidence reference

Quoted: "11 an asserted value without its evidence reference, on either
field, foreclosed included" (line 286); "no value is assertable without the
artifact that carries it" (line 137); the grammar
"other-verdict unknown | possible-not-demonstrated | demonstrated(<ref>) |
foreclosed(<constraint set>, <domain>)" (lines 57-59).

Readings: (a) every value other than the default unknown is asserted and
needs a reference, possible-not-demonstrated included; (b) only values
whose grammar carries a reference, plus foreclosed by the row's own words.

Taken: (a). Line 137 says "no value", with unknown named as the default;
the grammar does not decide it, since foreclosed carries no <ref> in the
grammar and still needs one by row 11.


## R07 - Row 5: what a declared exclusion is

Quoted: "5 a declared exclusion with any state but not-exercised"
(line 276); "\"Declared\" means written by the emitter." (line 45).

Readings: (a) a record carrying `declared-exclusion: true`; (b) also any
record whose cause is out_of_scope.

Taken: (a). out_of_scope is a cause, and causes are read by rows 1 to 4;
nothing says a cause value is an exclusion.

