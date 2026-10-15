"""Reader for the Agent Conformance Reporting Format, v0.1.

Written from spec/v01-text.txt alone; the readings it relies on are in
reports/READINGS.md (ids R01..R26).  Usage:

    python3 -I reader.py <directory of member files>

One JSON line per member on stdout, in id order; one summary line on stderr."""

import json, os, sys

SPEC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec", "v01-text.txt")

# Each citation: (first line in spec/v01-text.txt, words quoted from there on).
CITES = {
    "states": (54, "state pass | fail | not-exercised | inconclusive | void"),
    "othervalues": (57, "other-verdict unknown | possible-not-demonstrated |"),
    "discvalues": (60, "discrimination unknown | demonstrated(<evidence ref>)"),
    "freetext": (110, "Free text is refused in place of a disposition"),
    "slots": (152, "Five slots"),
    "fixedslot": (157, "fixed named, not implied: checker identity, constraint set, domain"),
    "pair": (141, "two observations from the same pinned checker"),
    "contained": (164, "an object whose moved is not contained in its declared compared set is rejected"),
    "mismatch": (215, "resolves, digests differ integrity failure"),
    "runlevel": (327, "a report asserting a completeness claim without the count of the population it quantifies over"),
    "claims": (353, "Each claim carries the size of the population it counts over:"),
    "empty": (362, "A claim over an empty population is reported as not claimable, not as satisfied."),
    "novoid": (364, "With a nonempty declared set it is satisfied when the void count is zero and not satisfied otherwise"),
    "aggregate": (343, "An aggregate is computed only over declared, exercised checks"),
    "fillings": (396, "the report says so and names what the producer has instead"),
    "failstate": (405, "\"Fail\" here is the state fail, in all three places. A non-pass is not enough"),
    "controlstate": (416, "control-failed requires the control's state to be fail"),
    "controlpop": (427, "The control is the run's declared checks exercised against an input built to fail them, not a separate check beside them"),
    "binding": (431, "The control runs under the same checker revision and the same relevant configuration and constraints as the declared checks"),
    "silence": (421, "\"Nothing\" is a permitted answer. Silence in that field is not"),
    "leafcount": (229, "A digest match establishes a set only when the count of leaves is bound into what is signed or hashed"),
    "mustshape": (230, "a report MUST declare which tree shape it uses"),
    "closedset": (240, "The declaration is an identifier from a closed, versioned set of tree construction and hash identifiers, not free text"),
    "degrade": (216, "does not resolve unchecked; the rows reading moved degrade"),
    "domain": (171, "The domain is a declared object, declared once at run level. foreclosed and the fixed slot reference it by identifier and no slot restates it"),
    "availability": (89, "integrity-failure kept separate from availability-failure."),
    "row1": (271, "a non-verdict state with no cause"),
    "row2": (272, "void with not_applicable, out_of_scope or withheld"),
    "row3": (273, "not-exercised with integrity-failure"),
    "row4": (274, "cause confinement-failed-during-check with any state but void"),
    "row5": (276, "a declared exclusion with any state but not-exercised"),
    "row6": (278, "a non-verdict state carrying either qualifier"),
    "row7": (279, "a verdict state carrying a cause"),
    "row8": (280, "other-verdict foreclosed with discrimination demonstrated"),
    "row9": (282, "discrimination demonstrated with other-verdict unknown or possible-not-demonstrated"),
    "row10": (284, "foreclosed without a constraint set and a domain"),
    "row12": (288, "discrimination demonstrated citing an evidence object whose changed slot is the checker"),
    "row13": (294, "other-verdict demonstrated citing an evidence object whose moved does not contain the verdict"),
    "row14": (296, "moved asserted on an evidence object that neither carries both observations nor references them with digests"),
    "row11": (286, "an asserted value without its evidence reference, on either field, foreclosed included")}

# Numbered rows of section 4: citation names "row<n>".
ROW_NUMBER = dict((name, int(name[3:])) for name in CITES if name.startswith("row"))


def flatten(text):
    return " ".join(text.split())


def verify_cites():
    """Fail loudly if a quotation does not start on the line it cites."""
    lines = read_text(SPEC).split("\n") if os.path.isfile(SPEC) else []
    for name in sorted(CITES) if lines else []:
        start, words = CITES[name]
        here = flatten(" ".join(lines[start - 1:start + 7]))
        later = flatten(" ".join(lines[start:start + 7]))
        if flatten(words) not in here or flatten(words) in later:
            raise SystemExit("citation %s does not start on line %d" % (name, start))


class Verdict:
    """Collects what the rules found for one member."""

    def __init__(self):
        self.refusals = []   # (sort key, citation name, reason)
        self.unsettled = []  # (reading id, citation name, reason)
        self.notes = []
        self.recount = {}

    def refuse(self, cite, reason):
        # R26: numbered rows first, then the run-level rejection, then sentences.
        rank = (0, ROW_NUMBER[cite]) if cite in ROW_NUMBER else (
            (1, 0) if cite == "runlevel" else (2, CITES[cite][0]))
        self.refusals.append((rank, cite, reason))

    def leave_open(self, reading, cite, reason):
        self.unsettled.append((reading, cite, reason))

    def note(self, text):
        self.notes.append(text)


def describe(cite, reason, reading=None):
    start, words = CITES[cite]
    lead = "line %d" % start
    if cite in ROW_NUMBER:
        lead = "row %d (line %d)" % (ROW_NUMBER[cite], start)
    tail = reason if reading is None else "reading %s: %s" % (reading, reason)
    return '%s: "%s" - %s' % (lead, flatten(words), tail)


STATES = ("pass", "fail", "not-exercised", "inconclusive", "void")
VERDICT_STATES = STATES[:2]  # pass and fail, the two verdict states


def records_of(subject):
    items = subject.get("checks")
    return [r for r in items if isinstance(r, dict)] if isinstance(items, list) else []


def label(record, index):
    return str(record.get("check", "#%d" % index))


# 1.2: the eight CAP-1 dispositions, then the values added on the list.
CAP1_DISPOSITIONS = ("not_applicable disabled_by_policy unsupported_input resource_exhausted"
                     " failed unavailable out_of_scope withheld").split()
LIST_ADDITIONS = ["evidence-does-not-hold", "integrity-failure",
                  "precondition-unsatisfiable", "confinement-failed-during-check"]
CAUSES = tuple(CAP1_DISPOSITIONS + LIST_ADDITIONS)
UNSETTLED_CAUSES = ("availability-failure",)


def cause_code(record):
    """Return (written, code): whether a cause is written, and its value."""
    if "cause" not in record:
        return False, None
    cause = record["cause"]
    if isinstance(cause, dict):
        return True, cause.get("code")
    return True, cause


OTHER_VALUES = ("unknown", "possible-not-demonstrated", "demonstrated", "foreclosed")
DISCRIMINATION_VALUES = ("unknown", "demonstrated")


def qualifier(record, field, allowed, cite, name, found):
    """Return (written, value, body); a qualifier not written is unknown (R03)."""
    if field not in record:
        return False, "unknown", {}
    body = record[field]
    if not isinstance(body, dict):
        body = {"value": body}
    value = body.get("value")
    listed = value in allowed
    if not listed:
        found.leave_open("R25", cite, "%s has %s %s, outside the list" % (
            name, field, json.dumps(value)))
    return True, value, body


def cited(body, run):
    ref = body.get("ref")
    return run.evidence.get(ref) if isinstance(ref, str) else None


def read_qualifiers(record, name, state, run, found):
    other = qualifier(record, "other-verdict", OTHER_VALUES, "othervalues", name, found)
    disc = qualifier(record, "discrimination", DISCRIMINATION_VALUES, "discvalues", name, found)
    if state in STATES and state not in VERDICT_STATES:
        for field, (written, value, _) in (("other-verdict", other), ("discrimination", disc)):
            if written and value != "unknown":
                found.refuse("row6", "%s is %s and carries %s %s" % (name, state, field, value))
            elif written:
                found.leave_open("R05", "row6", "%s is %s and writes %s as unknown" % (
                    name, state, field))
    if other[1] == "foreclosed" and disc[1] == "demonstrated":
        found.refuse("row8", "%s: other-verdict foreclosed beside discrimination demonstrated" % name)
    if disc[1] == "demonstrated" and other[1] in ("unknown", "possible-not-demonstrated"):
        found.refuse("row9", "%s: discrimination demonstrated, other-verdict %s" % (name, other[1]))
    if other[1] == "foreclosed":
        missing = [k for k in ("constraint-set", "domain") if not other[2].get(k)]
        if missing:
            found.refuse("row10", "%s: foreclosed without %s" % (name, " and ".join(missing)))
        if "domain" in other[2]:
            domain_slot(other[2]["domain"], "%s other-verdict" % name, run, found)
    for field, (written, value, body), allowed in (
            ("other-verdict", other, OTHER_VALUES), ("discrimination", disc, DISCRIMINATION_VALUES)):
        if value in allowed and value != "unknown" and not body.get("ref"):
            found.refuse("row11", "%s: %s %s names no evidence reference" % (name, field, value))
    for field, body, cite in (("other-verdict", other[2], "othervalues"),
                              ("discrimination", disc[2], "discvalues")):
        if "ref" in body and cited(body, run) is None:
            found.leave_open("R25", cite, "%s: %s cites %s, no evidence object of the report" % (
                name, field, json.dumps(body["ref"])))
    target = cited(disc[2], run)
    if disc[1] == "demonstrated" and target is not None and target.get("changed") == "checker rule":
        found.refuse("row12", "%s: discrimination cites evidence %s, whose changed slot is the checker rule" % (
            name, target.get("id")))
    target = cited(other[2], run)
    if other[1] == "demonstrated" and target is not None:
        status, moved = recompute(target, run.store)
        declared = target.get("moved")
        if status == "read" and "verdict" not in moved:
            found.refuse("row13", "%s: evidence %s recomputes moved as %s, without the verdict" % (
                name, target.get("id"), json.dumps(sorted(moved))))
        elif status == "unresolved" and isinstance(declared, list) and "verdict" not in declared:
            found.leave_open("R12", "degrade", "%s: evidence %s does not resolve and declares moved %s" % (
                name, target.get("id"), json.dumps(declared)))
    return other, disc


class Run:
    """What the rules need from the whole report."""

    def __init__(self, subject, store):
        self.subject = subject
        self.store = store
        self.records = records_of(subject)
        domain = subject.get("domain")
        self.domain = domain.get("id") if isinstance(domain, dict) else None
        self.evidence = {}
        items = subject.get("evidence")
        for item in items if isinstance(items, list) else []:
            if isinstance(item, dict) and item.get("id") not in self.evidence:
                self.evidence[item.get("id")] = item


def look(observation, store):
    """Section 3 table for one observation: ("read", content), "unresolved" or "mismatch"."""
    side = "carried" if "carried" in observation else "reference"
    if side == "carried":
        content = observation["carried"]
        return ("read", content) if isinstance(content, dict) else ("unresolved", None)
    ref = observation.get("reference")
    if not isinstance(ref, dict):
        return "unresolved", None
    where = ref.get("vector")
    held = store.get(where) if isinstance(where, str) else None
    if not isinstance(held, dict) or not ref.get("sha256"):
        return "unresolved", None
    if held.get("sha256") != ref.get("sha256"):
        return "mismatch", None
    return "read", held


def recompute(item, store):
    """Return (status, moved) where moved is the recomputed set, or None."""
    seen = item.get("observations")
    if not (isinstance(seen, list) and len(seen) == 2 and all(isinstance(o, dict) for o in seen)):
        return "malformed", None
    looked = [look(o, store) for o in seen]
    outcomes = [kind for kind, _ in looked]
    if "mismatch" in outcomes:
        return "mismatch", None
    if "unresolved" in outcomes:
        return "unresolved", None
    first, second = looked[0][1], looked[1][1]
    # R09: compared names for the two things an observation holds
    terms = (("verdict", "verdict"), ("fired-rule list", "rules"))
    return "read", set(term for term, key in terms if first.get(key) != second.get(key))


def domain_slot(value, where, run, found):
    identifier = isinstance(value, str)
    if not identifier:
        found.leave_open("R17", "domain", "%s writes the domain as %s, not an identifier" % (
            where, json.dumps(value, sort_keys=True)))
    if identifier and value != run.domain:
        found.leave_open("R17", "domain", "%s names domain %s, the run's is %s" % (
            where, value, json.dumps(run.domain)))


CHANGED_VALUES = ("input artifact", "checker rule", "constraint")
FIXED_NAMES = ("checker", "constraint-set", "domain")


def read_evidence(item, run, found):
    where = "evidence %s" % item.get("id")
    absent = [k for k in ("changed", "fixed", "compared", "delta") if k not in item]
    if absent:
        found.leave_open("R19", "slots", "%s lacks %s" % (where, ", ".join(absent)))
    if "changed" in item and item["changed"] not in CHANGED_VALUES:
        found.leave_open("R19", "slots", "%s has changed %s" % (where, json.dumps(item["changed"])))
    fixed = item.get("fixed")
    names_all = isinstance(fixed, dict) and all(k in fixed for k in FIXED_NAMES)
    if "fixed" in item and not names_all:
        found.leave_open("R19", "fixedslot", "%s does not name checker, constraint set and domain" % where)
    if names_all:
        domain_slot(fixed["domain"], "%s fixed slot" % where, run, found)
    if "compared" in item and not isinstance(item["compared"], list):
        found.leave_open("R19", "slots", "%s has no compared list" % where)
    delta = item.get("delta")
    if "delta" in item and not (isinstance(delta, dict) and isinstance(delta.get("changes"), list)):
        found.leave_open("R19", "slots", "%s has no list of changes in its delta" % where)
    elif "delta" in item and "arity" in delta:
        found.note("%s: declared arity %s not read, recomputed %d from the delta (R18)" % (
            where, json.dumps(delta["arity"]), len(delta["changes"])))
    seen = item.get("observations")
    if not (isinstance(seen, list) and len(seen) == 2 and all(
            isinstance(o, dict) and ("carried" in o or "reference" in o) for o in seen)):
        found.leave_open("R19", "pair", "%s does not hold two observations" % where)
    if "moved" in item and isinstance(seen, list):
        carries = bool(seen) and all(isinstance(o, dict) and "carried" in o for o in seen)
        references = bool(seen) and all(
            isinstance(o, dict) and isinstance(o.get("reference"), dict) and o["reference"].get("sha256")
            for o in seen)
        if not carries and not references:
            found.refuse("row14", "%s asserts moved but neither carries both observations nor references both with digests" % where)
    status, moved = recompute(item, run.store)
    compared = item.get("compared")
    declared = item.get("moved")
    if isinstance(compared, list):
        declared_inside = not isinstance(declared, list) or all(x in compared for x in declared)
        if status == "read":
            recomputed_inside = all(x in compared for x in moved)
            if not recomputed_inside and not declared_inside:
                found.refuse("contained", "%s: moved %s escapes compared %s" % (
                    where, json.dumps(sorted(moved)), json.dumps(compared)))
            elif recomputed_inside != declared_inside:
                found.leave_open("R13", "contained", "%s: recomputed moved %s and declared moved %s disagree on compared %s" % (
                    where, json.dumps(sorted(moved)), json.dumps(declared), json.dumps(compared)))
        elif status == "unresolved" and not declared_inside:
            found.leave_open("R12", "degrade", "%s does not resolve and declares moved %s outside compared %s" % (
                where, json.dumps(declared), json.dumps(compared)))
    if status == "mismatch":
        found.leave_open("R11", "mismatch", "%s: a referenced observation resolves with a different digest" % where)
    elif status == "unresolved":
        found.note("%s: observations do not all resolve, read as unchecked" % where)


TREE_SHAPES = ("flat", "rfc6962", "RFC9162_SHA256")


def read_collection(run, found):
    collection = run.subject.get("check-set")
    if isinstance(collection, dict):
        read_tree(collection, run, found)


def read_tree(collection, run, found):
    shape = collection.get("tree-shape")
    if "tree-shape" not in collection:
        found.refuse("mustshape", "the check-set digest declares no tree shape")
    elif shape not in TREE_SHAPES:
        found.refuse("closedset", "the check-set declares tree shape %s, not an identifier of the set" % json.dumps(shape))
    count = collection.get("leaf-count")
    if "leaf-count" not in collection:
        found.leave_open("R16", "leafcount", "the check-set states no leaf count")
    elif count != len(run.records) or isinstance(count, bool):
        found.leave_open("R16", "leafcount", "the check-set states %s leaves over %d check records" % (
            json.dumps(count), len(run.records)))


# 5.2: which population each claim counts over.
CLAIM_POPULATIONS = {
    "accounting": "declared checks",
    "execution": "declared checks",
    "evidence": "verdict records",
    "no-void": "declared checks"}


def read_claims(run, rollup, found):
    claims = rollup.get("completeness")
    claims = claims if isinstance(claims, dict) else {}
    sizes = {"declared checks": len(run.records),
             "verdict records": sum(1 for r in run.records if r.get("state") in VERDICT_STATES)}
    for name in sorted(set(claims) - set(CLAIM_POPULATIONS)):
        found.leave_open("R23", "claims", "the roll-up makes a claim %s the text does not name" % json.dumps(name))
    for name in sorted(set(claims) & set(CLAIM_POPULATIONS)):
        claim = claims[name] if isinstance(claims[name], dict) else {}
        size = sizes[CLAIM_POPULATIONS[name]]
        count = claim.get("population")
        if not isinstance(count, int) or isinstance(count, bool):
            found.refuse("runlevel", "the %s claim carries no population count" % name)
        elif count != size:
            found.refuse("runlevel", "the %s claim counts %d, its population (%s) is %d" % (
                name, count, CLAIM_POPULATIONS[name], size))
        value = claim.get("claim")
        if size == 0 and value != "not-claimable":
            found.leave_open("R23", "empty", "the %s claim is %s over an empty population" % (name, json.dumps(value)))
        if name == "no-void" and size > 0:
            voids = sum(1 for r in run.records if r.get("state") == "void")
            wanted = "satisfied" if voids == 0 else "not-satisfied"
            if value != wanted:
                found.leave_open("R23", "novoid", "the no-void claim is %s with %d void records" % (json.dumps(value), voids))


def read_counts(run, rollup, found):
    states = [r.get("state") for r in run.records]
    recount = dict((s, states.count(s)) for s in STATES)
    recount["declared"] = len(states)
    recount["exercised"] = sum(recount[s] for s in ("pass", "fail", "inconclusive", "void"))
    for key in sorted(recount):
        if key in rollup and rollup[key] != recount[key]:
            found.leave_open("R24", "aggregate", "the roll-up gives %s %s, the records give %d" % (
                key, json.dumps(rollup[key]), recount[key]))


def by_run(run, field, found):
    if not any(r.get("state") == "fail" for r in run.records):
        found.refuse("failstate", "the roll-up claims shown-by-run but no check record is in state fail")


def by_control(run, field, found):
    control = field.get("control")
    if not isinstance(control, dict):
        control = {}
    if control.get("state") != "fail":
        found.refuse("controlstate", "the control's state is %s, not fail" % json.dumps(control.get("state")))
    named = control.get("checks")
    declared = [r.get("check") for r in run.records]
    if isinstance(named, list) and any(c not in declared for c in named):
        found.leave_open("R21", "controlpop", "the control names a check that is not a declared check")
    ours, theirs = run.subject.get("fixed"), control.get("fixed")
    if isinstance(ours, dict) and isinstance(theirs, dict):
        for key in sorted(set(ours) & set(theirs)):
            if ours[key] != theirs[key]:
                found.leave_open("R21", "binding", "the control ran under %s %s, the run under %s" % (
                    key, json.dumps(theirs[key]), json.dumps(ours[key])))


PRIOR_NOTES = {
    "unresolved": "prior run does not resolve: unchecked, not discriminating power, not a refusal (R22)",
    "read": "prior run resolves with a matching digest; its content is not read (R22)"}


def by_prior(run, field, found):
    outcome, _ = look({"reference": field.get("reference")}, run.store)
    if outcome == "mismatch":
        found.leave_open("R11", "mismatch", "the prior run's reference resolves with a different digest")
    if outcome in PRIOR_NOTES:
        found.note(PRIOR_NOTES[outcome])


# 5.4: the fillings the text names (R01, R20); "nothing" needs no check.
FILLINGS = {
    "nothing": None,
    "shown-by-run": by_run,
    "control-failed": by_control,
    "prior-discriminating-run": by_prior}


def read_negative(run, rollup, found):
    read_claims(run, rollup, found)
    read_counts(run, rollup, found)
    field = rollup.get("negative-capable")
    kind = field.get("kind") if isinstance(field, dict) else None
    if kind is None:
        found.refuse("silence", "the roll-up does not say whether its checks could produce a negative verdict")
    elif kind not in FILLINGS:
        found.leave_open("R20", "fillings", "the roll-up names %s, not one of the fillings" % json.dumps(kind))
    elif FILLINGS[kind] is not None:
        FILLINGS[kind](run, field, found)


# Rows 2 and 3: a state written with a cause it may not carry.
STATE_CAUSE_ROWS = (
    ("row2", "void", ("not_applicable", "out_of_scope", "withheld"), "%(name)s is void with cause %(code)s"),
    ("row3", "not-exercised", ("integrity-failure",), "%(name)s is not-exercised with integrity-failure"))


def read_record(record, name, run, found):
    state = record.get("state")
    known_state = state in STATES
    if not known_state:
        found.leave_open("R25", "states", "%s has state %s, outside the list" % (
            name, json.dumps(state)))
    written, code = cause_code(record)
    if written and code in UNSETTLED_CAUSES:
        found.leave_open("R04", "availability", "%s gives cause %s" % (name, code))
    elif written and code not in CAUSES:
        found.refuse("freetext", "%s gives cause %s, not a disposition" % (
            name, json.dumps(code)))
    has_cause = written and (code in CAUSES or code in UNSETTLED_CAUSES)
    resting = known_state and state not in VERDICT_STATES
    if resting and not has_cause:
        found.refuse("row1", "%s is %s with no cause from the vocabulary" % (name, state))
    for row, bad_state, bad_codes, wording in STATE_CAUSE_ROWS:
        if state == bad_state and code in bad_codes:
            found.refuse(row, wording % {"name": name, "code": code})
    if code == "confinement-failed-during-check" and state != "void":
        found.refuse("row4", "%s is %s with confinement-failed-during-check" % (name, state))
    if record.get("declared-exclusion") is True and state != "not-exercised":
        found.refuse("row5", "%s is a declared exclusion in state %s" % (name, state))
    if state in VERDICT_STATES and written:
        found.refuse("row7", "%s is %s and carries a cause" % (name, state))
    read_qualifiers(record, name, state, run, found)


def judge(member):
    found = Verdict()
    subject = member.get("subject")
    store = member.get("resolves")
    if not isinstance(subject, dict):
        subject = {}
    if not isinstance(store, dict):
        store = {}
    run = Run(subject, store)
    if run.domain is None:
        found.leave_open("R17", "domain", "the report declares no run-level domain")
    for index, record in enumerate(run.records):
        read_record(record, label(record, index), run, found)
    for key in sorted(run.evidence, key=str):
        read_evidence(run.evidence[key], run, found)
    found.recount = count_sides(run)
    read_collection(run, found)
    rollup = run.subject.get("roll-up")
    if isinstance(rollup, dict):
        read_negative(run, rollup, found)
    if not isinstance(rollup, dict):
        found.leave_open("R24", "aggregate", "the report has no roll-up")
    return found


def count_sides(run):
    """R24: the reader's own count of carried and referenced observations."""
    sides = {"carried": 0, "referenced": 0}
    for item in run.evidence.values():
        for observation in item.get("observations") or []:
            keys = observation if isinstance(observation, dict) else {}
            side = "carried" if "carried" in keys else (
                "referenced" if "reference" in keys else None)
            if side is not None:
                sides[side] += 1
    return sides


def render(member_id, found):
    refusals = sorted(set(found.refusals))
    unsettled = sorted(set(found.unsettled))
    line = {
        "id": member_id,
        "grounds": [describe(c, r) for _, c, r in refusals],
        "open": sorted(set(r for r, _, _ in unsettled)),
        "notes": sorted(set(found.notes)),
        "recount": found.recount}
    # R02, R26: a refusal decides; else an open reading; else accept.
    line["verdict"], line["ground"] = "accept", "; ".join(line["notes"])
    if unsettled and not refusals:
        reading, cite, reason = unsettled[0]
        line["verdict"], line["ground"] = "cannot-tell", describe(cite, reason, reading)
    if refusals:
        _, cite, reason = refusals[0]
        line["verdict"], line["ground"] = "reject", describe(cite, reason)
    return line


def load(directory):
    files = sorted(n for n in os.listdir(directory) if n.endswith(".json"))
    parsed = [json.loads(read_text(os.path.join(directory, n))) for n in files]
    return sorted(parsed, key=lambda m: str(m.get("id")))


def read_text(path):
    """The file's bytes decoded as UTF-8 (spec text and member files alike)."""
    with open(path, "rb") as source:
        return source.read().decode("utf-8")


def run(argv):
    if len(argv) != 1:
        raise SystemExit("usage: python3 -I reader.py <members directory>")
    verify_cites()
    tally = {"accept": 0, "reject": 0, "cannot-tell": 0}
    for member in load(argv[0]):
        line = render(str(member.get("id")), judge(member))
        tally[line["verdict"]] += 1
        sys.stdout.write(json.dumps(line, sort_keys=True, ensure_ascii=True) + "\n")
    sys.stderr.write("members=%d accept=%d reject=%d cannot-tell=%d\n" % (
        sum(tally.values()), tally["accept"], tally["reject"], tally["cannot-tell"]))


run(sys.argv[1:])
