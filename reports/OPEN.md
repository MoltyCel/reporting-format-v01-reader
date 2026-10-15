# Open: what I would have needed from outside the repo

Rule 1 forbids reading anything outside the repo. These are the points where
something outside would have settled a reading. None of them was consulted.

1. The conformance corpus `vectors-w3c-report` at the corpusDigest section 10
   leaves open (O2, lines 693-697, 765). Its members would show how the group
   reads R11 (mismatch), R12 (degrade), R13 (which moved line 164 reads),
   R16 (leaf count), R17 (restated domain), R19 (missing slot), R21 (control
   binding, "proposed corpus row 29", line 753) and R23/R24. The text
   governs where it and the corpus differ (line 756), so the corpus would
   inform readings, not override the text.
2. Message 0038, cited by row 6 as "narrowed 0038" (line 278): what row 6 was
   narrowed to (R05).
3. The CAP-1 draft (draft-hillier-coverage-attestation-00, line 77): whether
   its dispositions include anything like availability-failure (R04).
4. The leaf encoding of a check-set for `flat`, `rfc6962` and
   `RFC9162_SHA256`. The text does not define it, and says flat is not
   defined in its own terms (line 774), so no root is recomputed (R16).
5. A digest serialization for observations: the text names SHA-256 but not
   the bytes it is taken over, so the reader compares the declared digest
   with the store's digest and never re-hashes (R10).
6. A current CPython 3.1x interpreter. Only CPython 3.9.6 was reachable by
   name on this machine; the reader was run under it and its source was
   parsed with the 3.9 grammar. It uses no version-dependent behaviour I
   know of, but the byte-identity claim across versions is untested here.

## Lines that stay shared

None. Every line listed after 0ecc76b was rewritten (see STEPS.md step 6).
New lines may coincide again; that has not been checked yet.
