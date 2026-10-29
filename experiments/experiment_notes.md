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

## 2026-10-29 — Stage 6: shrinking the tree (notebook 05), and the Stage 5 re-run with list A (58)

```
Dataset file used: Wednesday-workingHours.pcap_ISCX.csv (raw file; notebook 05 repeats the
  notebook 2 cleaning and split). Split 42 checked against y_train.csv / y_test.csv from
  notebook 2: identical, row for row. 610,492 rows, 488,393 train + 122,099 test.
Machine: one 2-core CPU, scikit-learn 1.9.1 (Colab used an older version).

What I did:
  1. Part 1: re-ran the 8 Stage 5 runs with the new 58-feature list A, so all results come
     from the same machine and library version. Replaced every row of results.csv (the -v1
     rows are gone) and the three S5_*.csv files.
  2. Part 2: "always BENIGN" baseline on 5 splits.
  3. Part 3: depth sweep. max_depth 1,2,3,4,5,6,8,10,12,15,20,unlimited x 8 feature lists
     (A, B, C, D and A-NS, B-NS, C-NS, D-NS = without Destination Port and both
     Init_Win_bytes features) x 5 splits (seeds 42-46) = 480 trees.
  4. Part 4: cost-complexity pruning, 13 ccp_alpha values from 0 to 0.03, split 42 only.
  5. Part 5: chose the smallest depth on a VALIDATION set (20% of the training set):
     every class except Heartbleed within 1 point of the unlimited tree (also a 0.1-point
     version). Rule written into the notebook before the full run (a 2-minute code test
     had only shown test scores for 2 depths on 2 lists).
  6. New measures: compact size (9 bytes per node) and average comparisons per flow.
     A classifier using only the compact arrays gave exactly the same predictions as
     scikit-learn for all 480 + 104 trees.

What I observed:
  Stage 5 re-run (split 42): A 58 features: attack recall 99.91%, 36 missed, 21 false
    alarms, 823 nodes, 0.76 MB. C and D: exactly the same as the 23-10 Colab run. B and the
    no-port runs differ by a few flows (B false alarms 26 -> 28; C_no_port 1607 -> 1603
    nodes), because the newer scikit-learn breaks ties between equal splits differently.
  Depth sweep (means over 5 splits):
    - Rare attacks are lost first. A at depth 8: attack recall 98.4% but Slowhttptest
      81.8%, slowloris 88.5%, Hulk 99.4%. A at depth 4: attack recall 93.3%, Slowhttptest
      18.2%, slowloris 32.9%.
    - Attack recall is not a safe summary: A at depth 3 flags 97.8% of attacks but raises
      false alarms from 0.03% to 4.3% of benign flows.
    - Without the shortcut features the unlimited trees are 3.5x (A-NS) to 11x (D-NS)
      bigger and overfit: D-NS at depth 15-20 catches more attacks (98.5-98.7%) than its
      unlimited tree (97.1%). C-NS at depth 12 keeps its score with 85% fewer nodes.
    - Results barely move between splits: unlimited-tree attack recall varies by at most
      0.3 points within any list.
    - Heartbleed: no tree of depth 4 or less caught a Heartbleed flow on any split.
  Validation choice (1-point rule): A 20, B 20, C 12, D 12, A-NS 20, B-NS 15, C-NS 12,
    D-NS 20. Strict 0.1-point rule: A, B, A-NS, D-NS need the unlimited tree.
  Pruning (split 42): much better than depth limits at the same size. A pruned to 217
    nodes: macro F1 (no Heartbleed) 0.996 vs 0.997 full; depth 12 (293 nodes): 0.978.
  Costs: memory to classify a batch of 1,000 flows depends on the number of features, not
    the tree: 0.67 MB for list A at every depth, 0.09 MB for list D (scikit-learn copies
    the batch). One flow at a time would need only 4 bytes per feature. Prediction time 0.05-0.37 ms
    per 1,000 flows for every tree, too small and noisy to compare.

Any errors/problems:
  - First launch of the long run failed because the notebook file did not exist yet when
    nbconvert started; re-launched, then ran without errors (about 1.5 hours).
  - Pruning was only run on split 42 and was not chosen on the validation set, so its
    advantage is a test-set comparison, not a validated choice.

Next step: write the paper. Figures for it are made by notebook 06 from the saved CSVs.
```
