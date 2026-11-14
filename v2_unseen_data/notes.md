# v2 notes

Dated log of what was done in v2, what was seen and what was decided. v1's log is
`../v1_random_split/experiments/experiment_notes.md`.

## 2026-11-12 — Why v1 scored 99.9%, and the v2 redesign

```
Why: v1's trees score about 99.9% on Wednesday. A score that high usually means the test is
  too easy. v1's own Friday check (notebook 07) already found only 29.7% of a related DDoS
  attack caught.

What was wrong in v1 (three things):
  1. Random split of one day. Each attack is one long burst, so the test set is full of
     flows that sit between two training flows of the same burst.
  2. Shortcut features (Destination Port, the two Init_Win_bytes columns) describe the lab.
     Lists C and D kept them.
  3. The trees learned the name of each attack tool, and the test set contained only those
     same tools, recorded in the same session.

Check (notebook 01): Wednesday, v1's model, only the split changed (random -> by time):
  - List A: attack recall 99.91% -> 99.07%, macro F1 0.997 -> 0.841,
    DoS slowloris 99.1% -> 59.1%.
  - List A-NS: attack recall 99.38% -> 90.60%, DoS Hulk 99.4% -> 90.0%.
  - Exact copies are not the cause (list A: 0.01% of test flows have an identical training
    flow). The leak is near-copies.
  So the split explains part of the 99.9%. The rest is point 3, measured below.

Decisions for v2:
  - Keep decision trees, so the research question does not change.
  - All eight CICIDS2017 files: 2,830,743 rows -> 2,572,640 after the same cleaning as v1
    (2,867 infinite, 255,236 duplicates). 2,146,899 normal, 425,741 attack, 14 attack types.
  - Trees learn attack / normal. Attack names are kept only for scoring.
  - Only the shortcut-free lists: A-NS 55, B-NS 36, C-NS 13, D-NS 4.
  - Train / validation / test by time order (first 60% / next 20% / last 20% of each
    attack and of normal traffic in each file). The files have no timestamp column, so
    file order is used as the clock.
  - Four tests: random split (for comparison), later traffic, new attack (14 runs),
    new day (5 runs).
  - Tree size chosen on validation rows only (the rule itself was revised once, see the
    next entry).
```

## 2026-11-12 — The v2 run (notebooks 02-04)

```
Run: notebook 03, 21 runs x 4 lists = 84 full trees, each scored at 12 depth limits and
  12 pruning strengths = 2,016 rows. 29.7 minutes, scikit-learn 1.9.1, 2-core CPU.

To save time each tree is grown once and read at every size:
  - Depth limits: the full tree is cut at depth d. Checked against re-training with
    max_depth=d (list C-NS): identical answers at depths 1, 3 and 6, 99.998% agreement at
    depth 10, 99.949% at depth 15. The differences are ties between equally good questions,
    which scikit-learn breaks at random.
  - Pruning: pruning the grown tree gives the identical tree to training with ccp_alpha
    (checked at two strengths).

What I observed (full-size trees, list A-NS):
  - Attack flows caught: 99.2% random split, 94.7% later traffic, 55.7% unseen attack
    type, 7.2% unseen day. Per attack type: 86.0%, 82.3%, 32.3%, 16.4%.
  - (Reading corrected on 14 Nov, see the next entry.) Unseen attacks caught in test 3,
    which I first read as "a relative stays in training": DoS Hulk 85.8%,
    XSS 92.9%, Web Brute Force 82.5%, slowloris 70.9%, DDoS 63.0%. PortScan 0.2%,
    FTP-Patator 0.0%, SSH-Patator 0.1%, Bot 0.0%, Heartbleed 0 of 11.
  - Bot: 190 of 390 caught with a random split; 0 of 389 on later traffic, and that 0 is
    the same on every list.
  - False alarms on a new day: Monday 0.10%, Tuesday 0.26%, Wednesday 0.04%,
    Thursday 3.38%, Friday 2.14% (0.08% on later traffic from seen days).
  - Depth: seen attacks per type 21.3% (depth 1) -> 82.3% (no limit). Unseen attack types
    11-23% up to depth 10, 31-33% from depth 12.
  - Validation rule: no depth limit passed for any list in test 2. Pruning passed with
    913 nodes for A-NS (-77%, 8.0 KB) and 1,475 for C-NS (-74%, 13.0 KB).
  - Pruning matched or beat the depth-limited tree of at least the same size in 77 of 96
    comparisons on seen attacks and 656 of 864 on unseen ones.

Any errors/problems:
  - First version of the depth check assumed the cut tree and the re-trained tree were
    identical. They are not always (ties), so the check now measures agreement.
  - First full run scored validation only as one pooled number. Three attack types have
    2 to 7 validation flows, which made a per-type rule jump around, so the run was
    restarted to save validation recall for every attack type; the rule uses only attack
    types with at least 100 validation flows.
  - Tests 1 and 2 are one split each (v1 used five random splits).

Next step: update the paper. v1 becomes the naive baseline, v2 the main result.
```

## 2026-11-14 — Review of the repo and paper

```
Why: a last check of every number and every claim before the paper goes to Viraj sir.

What was wrong and what changed:
  1. Finding 2 claimed too much. It said unseen attacks are caught "only when a close
     relative was in training". The data do not show that. Comparing test 3 (attack type
     held out) with test 4 (whole day held out) for list A-NS:
       DoS Hulk 85.8% -> 14.1%, DDoS 63.0% -> 0.0% (6 of 128,014),
       DoS slowloris 70.9% -> 53.8%, DoS Slowhttptest 36.6% -> 21.6%,
       Web Brute Force 82.5% -> 80.4%, Web XSS 92.9% -> 91.3% (A-NS only; B-NS and C-NS
       fall below 5%).
     DoS Hulk stays in training in test 4 and DDoS is still missed, so "a similar attack"
     is not the explanation for DDoS. Related attacks share a day in this dataset, so the
     two explanations cannot be separated. Finding 2 now says what the data show: test 3
     is optimistic, test 4 is the stricter test. Notebook 04, both READMEs and the paper
     were changed, and 04_recall_by_attack.csv has a "day unseen" column.
  2. "Rule fixed before looking at test scores" was not true. The first version of the
     validation rule used one pooled number; it was changed to "every attack type with at
     least 100 validation flows" after the first run. The wording is corrected everywhere
     and listed as a limitation.
  3. "Time order" was assumed. Notebook 02 now checks it against the published attack
     schedule: in every file the attacks first appear in schedule order. The order is not
     exact (half of DoS GoldenEye's rows are in the last 15% of the Wednesday file).
  4. Rounding: three figures had been rounded twice. DoS Slowhttptest unseen is 36.6%
     (not 36.5%), list B-NS random-split recall per type is 86.8% (not 86.9%), and the
     pruning comparison is now given as counts (77 of 96, 656 of 864).
  5. Earlier work was missing from the write-up: time-aware splits (Pendlebury 2019),
     random vs leakage-free splits on this dataset (Moczkodan and Ragab 2026), Destination
     Port as a shortcut (D'hooge 2022), dataset design flaws (Flood 2024), zero-day
     evaluation with anomaly detectors (Hindy 2020) and Sommer and Paxson (2010). Added
     to the paper and to research/literature_review.md. The random-split result is
     therefore not new; what is new here is the size axis.

Not done (possible follow-ups):
  - Hold out DDoS together with PortScan, to see which part of Friday's traffic the trees
    used to catch DDoS in test 3.
  - An anomaly detector trained on normal traffic only, as a baseline for unseen attacks.
  - Tests 1 and 2 on several splits.
```
