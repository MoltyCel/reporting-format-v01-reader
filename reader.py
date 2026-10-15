"""Reader for the Agent Conformance Reporting Format, v0.1.

Written from spec/v01-text.txt alone; the readings it relies on are in
reports/READINGS.md (ids R01..R26).  Usage:

    python3 -I reader.py <directory of member files>

One JSON line per member on stdout, in id order; one summary line on stderr.
"""

import json
import os
import sys

SPEC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec", "v01-text.txt")

# Each citation: (first line in spec/v01-text.txt, words quoted from there on).
CITES = {
    "states": (54, "state pass | fail | not-exercised | inconclusive | void"),
    "freetext": (110, "Free text is refused in place of a disposition"),
    "availability": (89, "integrity-failure kept separate from availability-failure."),
    "row1": (271, "a non-verdict state with no cause"),
    "row2": (272, "void with not_applicable, out_of_scope or withheld"),
}

# Numbered rows of section 4: citation names "row<n>".
ROW_NUMBER = dict((name, int(name[3:])) for name in CITES if name.startswith("row"))


def flatten(text):
    return " ".join(text.split())


def verify_cites():
    """Fail loudly if a quotation does not start on the line it cites."""
    if not os.path.isfile(SPEC):
        return
    with open(SPEC, encoding="utf-8") as handle:
        lines = handle.read().split("\n")
    for name in sorted(CITES):
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

    def refuse(self, cite, reason):
        if cite in ROW_NUMBER:
            key = (0, ROW_NUMBER[cite])
        elif cite == "runlevel":
            key = (1, 0)
        else:
            key = (2, CITES[cite][0])
        self.refusals.append((key, cite, reason))

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
VERDICT_STATES = ("pass", "fail")


def records_of(subject):
    items = subject.get("checks")
    if not isinstance(items, list):
        return []
    return [r for r in items if isinstance(r, dict)]


def label(record, index):
    return str(record.get("check", "#%d" % index))


# 1.2: the eight CAP-1 dispositions, then the values added on the list.
CAUSES = (
    "not_applicable", "disabled_by_policy", "unsupported_input",
    "resource_exhausted", "failed", "unavailable", "out_of_scope", "withheld",
    "evidence-does-not-hold", "integrity-failure", "precondition-unsatisfiable",
    "confinement-failed-during-check",
)
UNSETTLED_CAUSES = ("availability-failure",)


def cause_code(record):
    """Return (written, code): whether a cause is written, and its value."""
    if "cause" not in record:
        return False, None
    cause = record["cause"]
    if isinstance(cause, dict):
        return True, cause.get("code")
    return True, cause


def read_record(record, name, found):
    state = record.get("state")
    if state not in STATES:
        found.leave_open("R25", "states", "%s has state %s, outside the list" % (
            name, json.dumps(state)))
    written, code = cause_code(record)
    if written and code in UNSETTLED_CAUSES:
        found.leave_open("R04", "availability", "%s gives cause %s" % (name, code))
    elif written and code not in CAUSES:
        found.refuse("freetext", "%s gives cause %s, not a disposition" % (
            name, json.dumps(code)))
    has_cause = written and (code in CAUSES or code in UNSETTLED_CAUSES)
    resting = state in STATES and state not in VERDICT_STATES
    if resting and not has_cause:
        found.refuse("row1", "%s is %s with no cause from the vocabulary" % (name, state))
    if state == "void" and code in ("not_applicable", "out_of_scope", "withheld"):
        found.refuse("row2", "%s is void with cause %s" % (name, code))


def judge(member):
    found = Verdict()
    subject = member.get("subject")
    store = member.get("resolves")
    if not isinstance(subject, dict):
        subject = {}
    if not isinstance(store, dict):
        store = {}
    for index, record in enumerate(records_of(subject)):
        read_record(record, label(record, index), found)
    return found


def render(member_id, found):
    refusals = sorted(set(found.refusals))
    unsettled = sorted(set(found.unsettled))
    line = {
        "id": member_id,
        "grounds": [describe(c, r) for _, c, r in refusals],
        "open": sorted(set(r for r, _, _ in unsettled)),
        "notes": sorted(set(found.notes)),
    }
    if refusals:
        _, cite, reason = refusals[0]
        line["verdict"] = "reject"
        line["ground"] = describe(cite, reason)
    elif unsettled:
        reading, cite, reason = unsettled[0]
        line["verdict"] = "cannot-tell"
        line["ground"] = describe(cite, reason, reading)
    else:
        line["verdict"] = "accept"
        line["ground"] = "; ".join(line["notes"])
    return line


def load(directory):
    members = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(directory, name), encoding="utf-8") as handle:
            members.append(json.load(handle))
    members.sort(key=lambda m: str(m.get("id")))
    return members


def run(argv):
    if len(argv) != 1:
        sys.stderr.write("usage: python3 -I reader.py <members directory>\n")
        return 2
    verify_cites()
    tally = {"accept": 0, "reject": 0, "cannot-tell": 0}
    members = load(argv[0])
    for member in members:
        line = render(str(member.get("id")), judge(member))
        tally[line["verdict"]] += 1
        sys.stdout.write(json.dumps(line, sort_keys=True, ensure_ascii=True) + "\n")
    sys.stderr.write("members=%d accept=%d reject=%d cannot-tell=%d\n" % (
        len(members), tally["accept"], tally["reject"], tally["cannot-tell"]))
    return 0


sys.exit(run(sys.argv[1:]))
