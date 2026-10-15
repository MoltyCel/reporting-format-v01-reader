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


## R08 - Row 12: "the checker" as the changed object

Quoted: "12 discrimination demonstrated citing an evidence object whose
changed slot is the checker" (line 288); "changed which object varied:
input artifact | checker rule | constraint (0072 part 1.3; input | checker
in 0036)" (lines 155-156).

Taken (only reading found): `changed` = `checker rule` is "the checker".
`input artifact` and `constraint` are not.


## R09 - Recomputing moved from the observations

Quoted: "moved is recomputed, not declared. It is recomputed over what the
referenced observations actually contain" (line 163); "The vocabulary for
compared enumerates verdict, and verdict with rule list; there is no value
for the list itself." (line 583); "MUST-FAIL pairs with different fired-rule
lists" (line 601).

An observation in a member holds `verdict` and `rules`. Taken: the
observation's `verdict` is what compared calls "verdict", its `rules` is
what compared calls "fired-rule list" (the rule list). Recomputed moved is
the set of those two names on which the two observations differ; two rule
lists differ when they are not equal as lists (a list keeps its order; the
text does not say rule order is irrelevant, and no member needs it). Nothing
else is in an observation, so the error list (7.1) can never be recomputed
as moved.


## R10 - Resolving a reference and comparing its digest

Quoted: "resolves, digests match / resolves, digests differ / does not
resolve" (lines 213-216); "the digest only tells them whether what they did
resolve is what the object was written against" (line 223).

The text does not say how a locator is formed or over which bytes a digest
is taken. Taken: the locator is the reference's `vector`; it resolves when
the store has that key; the digests match when the reference's `sha256`
equals the `sha256` the store holds for it. The reader does not re-hash
store contents: the text names no serialization to hash. A reference with
no `vector` does not resolve.


## R11 - What a digest mismatch does to the verdict

Quoted: "Reading a well-formed object is a table, not a row, because
resolvability is a property of the reader and not of the object:" (line 210);
"resolves, digests differ integrity failure" (line 215); "a mismatch needs
someone to find out which side moved" (line 221).

Readings: (a) integrity failure refuses the object; (b) it is not a row, so
the object is not rejected, and the rows reading moved simply do not read
that observation. The text calls the table "not a row" and gives no
outcome for the middle state; 5.3 calls non-resolution legitimate
(line 387) but says nothing of a mismatch.

Neither. A member with a mismatching reference on an evidence object is
cannot-tell under R11 (unless another ground rejects it).


## R12 - "The rows reading moved degrade"

Quoted: "does not resolve unchecked; the rows reading moved degrade"
(line 216); "row 13 reads moved, which is recomputed and degrades when
references do not resolve" (line 316); "The counter is disclosure and not
rejection. A reference that does not resolve is legitimate" (line 386).

Readings when an evidence object's observations do not all resolve:
(a) the rows reading moved (row 13, the containment sentence of line 164)
are not evaluated for it; (b) they fall back to the declared moved and
read it as a consistency check.

Not rejection either way for the non-resolution itself (line 386, settled).
Neither between (a) and (b): where (b) would fire and (a) would not, the
member is cannot-tell under R12. Where (b) would not fire, both agree and
the member is not refused on that ground.


## R13 - Line 164: which moved must be contained in compared

Quoted: "moved is recomputed, not declared. It is recomputed over what the
referenced observations actually contain, and an object whose moved is not
contained in its declared compared set is rejected." (lines 163-165);
"It also makes visible an emitter reporting a difference in something it
says it did not look at." (line 168); "So what the record composes is
currently settled by the emitter, not by the format" (line 587); "v0.1
does not settle it" (line 575).

Readings: (a) "its moved" is the recomputed moved, the one just described;
(b) it is the moved the emitter declared, which line 168 can be read as
pointing at; (c) both. Section 7.1 records that the 42 published objects
declare moving the error list, which has no compared value, and leaves what
the record composes open (O1).

Taken where both agree: reject when the recomputed and the declared moved
both escape compared; no ground when both are contained. Neither where they
disagree: such a member is cannot-tell under R13.


## R14 - Row 14 with mixed carry and reference

Quoted: "14 moved asserted on an evidence object that neither carries both
observations nor references them with digests" (line 296); "The format
permits both and requires one (Nicolás)." (line 204).

Readings: (a) literal: the object must carry both or reference both with
digests; one carried and one referenced fires the row; (b) per
observation: each must be carried or referenced with a digest.

Taken: (a). Row 14 is a form row "decidable from the object alone"
(line 207) and its wording is a plain neither/nor over the object; lines
205-207 also speak of the object staying with its corpus or leaving it,
not of single observations.


## R15 - The tree-shape declaration and its set

Quoted: "a report MUST declare which tree shape it uses" (line 230);
"The declaration is an identifier from a closed, versioned set of tree
construction and hash identifiers, not free text" (line 240); "Sankalp's
corpus already fixes tree shape as a closed set of two, flat and rfc6962"
(line 251); "the set need not disallow that identifier" (line 249);
"The v0.1 set is the members that have a vector pair in the corpus section
10 cites; see O3." (line 253); section 10 cites "<open, O2>" (line 694);
0.13.0, the only candidate named (line 704), carries "RFC9162_SHA256 joins
flat and rfc6962 as a tree shape" (line 749).

Readings for RFC9162_SHA256: (a) a member, since every corpus the text
names as candidate carries it and 3.1 says the set need not disallow it;
(b) not settled, since the cited corpus is open.

Taken: flat and rfc6962 are members (every corpus the text names carries
them). RFC9162_SHA256 is a member under (a). A `check-set` with no
`tree-shape` breaks the MUST of line 230 and is rejected (R02). A value
outside the set is not an identifier of the set and is refused as free
text (line 240, by the reason of line 110).


## R16 - The leaf count, and why roots are not recomputed

Quoted: "A digest match establishes a set only when the count of leaves is
bound into what is signed or hashed" (line 229); "Binding the count is
necessary and is not a general membership proof." (line 231); "The list
has not said what flat denotes in the text's own terms; until it does, a
member is defined by its vector pair." (line 774).

The text gives no leaf encoding for any shape, and says flat is not defined
in its own terms. The reader therefore never recomputes a `check-set` root.
(RFC 6962 is cited at line 234, but what a leaf is in a report is not.)

For the count: readings (a) a `check-set` with no `leaf-count`, or one that
differs from the number of check records, is refused; (b) such a digest
just establishes no set, which the reader weighs; nothing refuses it.
No sentence with a refusal word covers the count (R02).

Neither. A member whose `check-set` lacks `leaf-count`, or whose
`leaf-count` differs from its number of check records, is cannot-tell
under R16.


## R17 - A slot that restates the domain, or names another one

Quoted: "The domain is a declared object, declared once at run level.
foreclosed and the fixed slot reference it by identifier and no slot
restates it (Nicolás; Kenne, 0040). This removed a rejection row instead of
adding one: foreclosure over a domain that is not the run's domain can no
longer be written." (lines 171-175).

Readings for a `fixed.domain` or foreclosed `domain` that is an object
instead of an identifier, or an identifier other than the run domain's:
(a) refused, as not written in the format; (b) not refused, since the text
says a row was removed, not added.

Neither. Such a member is cannot-tell under R17.


## R18 - A declared arity, and a delta of more than one change

Quoted: "Arity is not a slot. A declared arity is forgeable the same way a
declared moved is, so arity is recomputed from the delta (0072)."
(line 177); "7.2 Input side: what counts as one field (was row B)"
(line 590); rows 1-14 (lines 271-297).

Taken: a declared `delta.arity` is not read; arity is the number of
`delta.changes`. No row of section 4 reads arity (row B is not in v0.1,
it is the open item of 7.2), so neither a declared arity nor an arity above
one refuses an object.


## R19 - An evidence object missing a slot or an observation

Quoted: "Five slots" (line 152) and the slot list (lines 155-161); "fixed
named, not implied: checker identity, constraint set, domain" (line 157);
"two observations from the same pinned checker" (line 141).

moved may be absent: it is recomputed, and row 14 speaks of moved being
"asserted" (line 296). For a missing `changed`, `fixed`, `compared` or
`delta`, a `fixed` lacking one of its three names, a `changed` outside its
three values, or a number of observations other than two: readings
(a) refused as malformed; (b) not refused, no row reads it.

Neither. Such a member is cannot-tell under R19.


## R20 - The 5.4 field: silence, shown-by-run, control-failed

Quoted: "\"Nothing\" is a permitted answer. Silence in that field is not"
(line 421); "\"Fail\" here is the state fail, in all three places. A
non-pass is not enough:" (line 405); "shown-by-run requires a positive
fail count, control-failed requires the control's state to be fail"
(lines 415-417), reported by the text as "already the reading of the
Python validator" and checked by the 0.12.0 validator (line 418).

Taken: a roll-up with no `negative-capable` (or no `kind`) is refused by
line 421. `shown-by-run` with no check record in state fail, and
`control-failed` whose control state is not fail, are refused: the text
states the requirement as the reading validators apply (R02 (b)). A `kind`
outside the four is not settled (neither, cannot-tell under R20).

Alternative not taken: these two are statements of how to read the field,
for the reader to weigh (line 424), not refusals.


## R21 - The control: same checker and configuration, same checks

Quoted: "The control runs under the same checker revision and the same
relevant configuration and constraints as the declared checks whose
negative capability it is reported for." (line 431); "The control is the
run's declared checks exercised against an input built to fail them, not a
separate check beside them" (line 427); "Roel's 5.4 binding is proposed
corpus row 29, where a control that ran under a different constraint set or
checker than the run it speaks for is rejected and a run that declares no
binding is not." (line 753).

No numbered row and no refusal word in 5.4; the corpus row is "proposed".
Readings for a control whose `fixed` differs from the run-level `fixed` on
a name both declare: (a) refused, as corpus row 29; (b) not refused, a
condition for the reader to weigh.

Neither: cannot-tell under R21. Where the run or the control declares no
binding, nothing is compared (both readings agree). A control naming a
check that is not a declared check is likewise cannot-tell under R21.


## R22 - A prior run whose reference does not resolve

Quoted: "A prior run is a reference, so the reading table in section 3
applies: a prior run that reads as unchecked is not discriminating power"
(line 443); "A prior run only counts where check identity survives across
runs." (line 452); "A reference that does not resolve is legitimate"
(line 387); "Where the prior run names a set of observations, 3.1 applies"
(line 446).

Taken: a prior-run reference the store cannot resolve reads as unchecked;
the producer then has shown no discriminating power, which the reader
weighs like "nothing" (line 422-424); this is not a refusal. Whether the
reference declares check identity or a tree shape is not read once it is
unchecked, since nothing it says can count.

Alternative not taken: an unresolvable prior run, or one without a tree
shape, is refused. No sentence with a refusal word says so.


## R23 - Completeness claims: count and value

Quoted: "Run-level rejection (Evgenii, 0036, agreed by Nicolás, 0039): a
report asserting a completeness claim without the count of the population
it quantifies over." (lines 327-329); populations (lines 355-358); "A claim
over an empty population is reported as not claimable, not as satisfied."
(line 362); "With a nonempty declared set it is satisfied when the void
count is zero and not satisfied otherwise" (line 364).

Population count: readings (a) a figure that differs from the recounted
population is not "the count of the population" and the run-level row
fires; (b) only a missing figure fires. Taken: (a). Populations recounted:
accounting, execution, no-void = number of check records; evidence =
number of records in state pass or fail.

Claim value: a claim reported satisfied over an empty population, or a
no-void claim whose value contradicts the void count. No refusal word;
neither: cannot-tell under R23.


## R24 - Roll-up counts that disagree with the records; the counter

Quoted: "An aggregate is computed only over declared, exercised checks"
(line 343); "Inconclusive and void are exercised checks" (line 348);
"The counter is disclosure and not rejection." (line 386); "The roll-up
counts how many verdict records carry their evidence and how many
reference it" (line 377).

State counts: the reader recounts `declared` (records), each state, and
`exercised` (pass + fail + inconclusive + void). A roll-up figure that
differs: no refusal word; neither: cannot-tell under R24.

The carried/referenced counter: settled as not a rejection (line 386).
What it counts (verdict records, line 377, or observations) is also not
settled, so the reader neither judges it nor lets it affect a verdict; it
emits its own recount of carried and referenced observations as data.


## R25 - Values outside the closed vocabularies

Quoted: "state pass | fail | not-exercised | inconclusive | void" (line 54);
"discrimination unknown | demonstrated(<evidence ref>)" (line 60); the
other-verdict list (lines 57-59).

A state, other-verdict value or discrimination value outside its list, or a
qualifier `ref` naming no evidence object of the report, has no row.
Neither: cannot-tell under R25. (Causes are R04.)


## R26 - Order: a firing row decides even when other points are open

Quoted: "\"Rejected\" means a conforming validator refuses the object and
names the row that refused it." (line 44); "A rejection vector names the
row that rejected it" (line 331).

Taken: when any ground of R02 (b) fires, the member is rejected, even if
other points of the same member are open; all grounds found are listed.
The ground named first is the lowest numbered row of section 4 that fires,
since line 44 asks for a row; failing a numbered row, the run-level
rejection; failing that, the first refusing sentence in text order. A refusal does not
wait on the outcome of an unrelated open reading.
