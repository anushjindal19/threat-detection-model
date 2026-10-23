# Experiment Notes

A dated log of each experiment: the data used, what was run, what was observed, any
problems, and the next step. Every row in `results.csv` can be traced to an entry here.

## 2026-10-04 — Dataset exploration (notebook 01)

Numbers re-checked by re-running notebook 1 on 23-10-2026.

```
Dataset file used: Wednesday-workingHours.pcap_ISCX.csv
692,703 rows, 79 columns (78 features + Label), confirmed with df.shape on 23-10-2026.
  This line first said 18334 rows, which was wrong.
Column names have leading spaces in the raw file; stripped with df.columns.str.strip()
Missing values: only Flow Bytes/s, 1,008 rows
Infinite values: Flow Packets/s in 1,297 rows, Flow Bytes/s in 289 rows
  1,008 + 289 = 1,297. This fits the missing Flow Bytes/s rows being the same rows
  as the infinite Flow Packets/s ones (probably zero-duration flows), which would
  explain why notebook 2 dropped no extra rows for missing values. Not checked directly.
81,909 duplicate rows (11.82% of all)
Class counts:
  BENIGN            440,031 (63.52%)
  DoS Hulk          231,073 (33.36%)
  DoS GoldenEye      10,293 (1.49%)
  DoS slowloris       5,796 (0.84%)
  DoS Slowhttptest    5,499 (0.79%)
  Heartbleed             11 (0.0016%)
BENIGN and DoS Hulk make up ~97% of rows; the other DoS types are rare, and
Heartbleed is far too rare to score reliably (all 11 rows survived cleaning:
9 ended up in train, 2 in test).

```

## 2026-10-06 — Preprocessing (notebook 02)

```
0.19% rows dropped for infinite values (1,297 rows)
11.7% rows dropped for duplicate values (80,914 rows; fewer than the 81,909 found in
  notebook 1, probably because some duplicates were among the infinite rows already
  dropped; worked out from the row counts, not printed by notebook 2)
692,703 - 1,297 - 80,914 = 610,492 rows left
No rows dropped for missing values
No identifier columns removed
X_train: (488393, 78)
X_test:  (122099, 78)
Stratified splitting worked cleanly, equal percentage split for train and test data

```

## 2026-10-22 — Stage 5: baseline decision tree (notebook 04)

```
Dataset file used: Wednesday-workingHours, 488393 train + 122099 test rows
What I did: untuned DecisionTreeClassifier(random_state=42) on lists A/B/C/D
  (57/39/15/6 features), plus 4 shortcut-check runs without Destination Port
  (and without Init_Win_bytes_forward/backward for A). Numbers are in results.csv.

What I observed:
  A: macro F1 0.9414, attack recall 0.9990, 825 nodes, 93.0 KB
  D: macro F1 0.9104, attack recall 0.9982, 1487 nodes, 164.5 KB
  Attack recall stays above 99.8% even with 6 features.
  Fewer features gave BIGGER trees (825 -> 1487 nodes): each feature carries less
  information, so the tree needs more splits. One run only, untuned.
  Shortcut check: removing port + TCP window features raised missed attacks from
  38 to 235 and grew the tree from 825 to 2863 nodes (most of the loss is DoS Hulk).
  So the tree was partly relying on lab-specific features.

Step 3 (testing my keep/remove claims from notebook 3), claims that did not hold:
  - Subflow Bwd Bytes is NOT identical to Total Length of Bwd Packets (34 rows differ)
  - ECE Flag Count is NOT identical to RST Flag Count (1 row differs)
  - Average Packet Size vs Packet Length Mean: Spearman = 0.9976, not exactly 1.0
  - Fwd PSH Flags is non-zero in 4.32% of rows, so it is not "always zero"
  Decided 23-10-2026 (see the entry below): Fwd PSH Flags added back to list A;
  the other 3 stay removed as "nearly identical".

Problems:
  - Macro F1 is dominated by Heartbleed (only 2 test rows). C's macro F1 of 0.83 is
    almost entirely from missing both Heartbleed rows; every other class is above
    0.98 recall. Don't compare runs on macro F1 alone. Step 9a in notebook 4 adds
    scores without Heartbleed.
  - ram_mb was not measured. Step 9b in notebook 4 adds it. (Done 23-10-2026.)
  - One day of traffic split at random: near-identical rows from the same attack
    burst can land in both train and test, so these scores are optimistic.

Next step: run Step 9 of notebook 4, decide on the 4 Step 3 columns, then move on to
  making the tree smaller (max_depth / pruning) and measuring the trade-off.
  (Step 9 and the decision were both done on 23-10-2026, see below.)
```

## 2026-10-23 — Notebook 04 Step 9, and the decision on the 4 Step 3 columns

```
Dataset file used: Wednesday-workingHours, same 488393 train + 122099 test rows
What I did:
  1. Re-ran notebook 4 Steps 1-8 and ran Step 9 for the first time.
     This run still used the OLD list A (57 features).
     Step 9a: scores without Heartbleed. Step 9b: memory needed by each tree.
     Results.csv now has this run's rows, with ram_mb filled in.
  2. Decided what to do with the 4 Step 3 claims that did not hold:
     - Fwd PSH Flags: ADDED BACK to list A (A: 57 -> 58 features). It is non-zero in
       4.32% of rows, so "always zero" was simply wrong, and it could help tell
       attacks apart. Kept out of B (B already has PSH Flag Count, which counts PSH
       in both directions), so B, C and D did not change.
     - Subflow Bwd Bytes, ECE Flag Count, Average Packet Size: still removed. They
       are nearly identical to a kept column (34 rows differ / 1 row differs /
       Spearman 0.9976), so a tree would gain almost nothing from them. Their reason
       in the feature table now says "nearly identical" instead of "identical".

What I observed:
  Step 9a (macro F1 over the 5 classes that are not Heartbleed):
    A 0.9963 | B 0.9957 | C 0.9958 | D 0.9924
    A_no_port 0.9917 | A_no_port_no_window 0.9919 | C_no_port 0.9930 | D_no_port 0.9861
    -> Without Heartbleed, A, B and C are basically tied. C looked much worse before
       (0.83) only because it missed both Heartbleed test rows. D is a little lower.
    -> Heartbleed caught (out of 2): 1 for every run except C and C_no_port (0).
  Step 9b (memory, MB = tree in memory + extra memory to classify 1,000 flows):
    A 0.75 | B 0.55 | C 0.29 | D 0.25
    A_no_port 0.77 | A_no_port_no_window 0.93 | C_no_port 0.34 | D_no_port 0.39
    -> Every model needs under 1 MB.
    -> Fewer features = LESS memory to run (A 0.75 MB -> D 0.25 MB), even though the
       tree itself gets BIGGER (0.09 MB -> 0.16 MB). Most of the running memory is
       the input data, and fewer features means less data per flow.
       So model file size and memory to run move in opposite directions.
       Both need to be reported.
    -> Removing the shortcut features also costs memory: A_no_port_no_window's tree
       is 0.31 MB, 3.5x the size of A's.
  Accuracy, F1, nodes, depth and model size were EXACTLY the same as on 22-10
  (same data, same random_state, so the tree is the same).

Any errors/problems:
  - Timings were very different from 22-10: A trained in 38.4 s (was 27.4 s) and
    predicted at 0.41 ms per 1000 rows (was 0.19). The tree and data were identical,
    so this is Colab's machine speed changing between sessions. Timings can only be
    compared within the same session, never across sessions.
  - The memory numbers do not include Python, pandas and scikit-learn themselves,
    which need far more memory (100+ MB) than the tree. They measure what the MODEL
    needs, not the whole program.
  - Results.csv rows for A, A_no_port and A_no_port_no_window are marked "-v1"
    (the old 57-feature list A). They must be replaced after the re-run below.

Next step:
  1. Re-run notebook 3 so feature_sets.json in Drive has the new list A (58).
  2. Re-run notebook 4 top to bottom including Step 9, and replace all rows in
     results.csv with the ones Step 9b prints. Only the A rows should change
     (B, C and D use the same features as before).
  3. Then move on to making the tree smaller (max_depth / pruning).
```
