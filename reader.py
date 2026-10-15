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
}

# Numbered rows of section 4, keyed by citation name.
ROW_NUMBER = {
}


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


def judge(member):
    found = Verdict()
    subject = member.get("subject")
    store = member.get("resolves")
    if not isinstance(subject, dict):
        subject = {}
    if not isinstance(store, dict):
        store = {}
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
