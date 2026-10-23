# Experiment Notes

A running log of what you tried, on which data, and why. This is the messy, honest
notebook that backs up the tidy numbers in `results.csv` — every row in that CSV should
be traceable to an entry here.

**Nothing in `results.csv` should ever be invented.** If you haven't run an experiment
yet, leave the row out rather than filling in guessed numbers.

## Log format

Copy this block for each new entry:

```
### YYYY-MM-DD — short title

**Dataset file used:**
**What I did:**
**What I observed:**
**Any errors/problems:**
**Next step:**
```

---

## Entries

```
### 4-10-2026

Dataset file used: Wednesday-workingHours
692,703 rows, 79 columns (corrected 23-10-2026: this line first said 18334 rows.
  That can't be right: 81,909 duplicates = 11.82% of all rows implies ~692,700 rows,
  and 610,492 rows were left after removing 1,297 inf rows and duplicates.
  Confirm with df.shape when notebook 1 is re-run.)
Flow Bytes has 1008 missing values
Flow Packets has 1297, Flow Bytes has 289 infinite values
81909 duplicate rows (11.82% of all)
BENIGN and DoS Hulk are the most common (63.5% and 33.3%, respectively)
DoS GoldenEye, DoS slowloris and DoS Slowhttptest are rare (1.49%, 0.84% and 0.79%, respectively)
Heartbleed is the rarest at ~0.00 (only 11 counts)

```

```
### 6-10-2026

0.19% rows dropped for infinite values
11.7% rows dropped for duplicate values
No rows dropped for missing values
No identifier columns removed
X_train: (488393, 78)
X_test:  (122099, 78)
Stratified splitting worked cleanly, equal percentage split for train and test data

```

```
### 22-10-2026 — Stage 5 baseline (untuned decision tree), notebook 4

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
  So the tree was partly relying on lab-specific clues.

Step 3 (testing my keep/remove claims from notebook 3), claims that did not hold:
  - Subflow Bwd Bytes is NOT identical to Total Length of Bwd Packets (34 rows differ)
  - ECE Flag Count is NOT identical to RST Flag Count (1 row differs)
  - Average Packet Size vs Packet Length Mean: Spearman = 0.9976, not exactly 1.0
  - Fwd PSH Flags is non-zero in 4.32% of rows, so it is not "always zero"
  Still to decide: keep these 4 out of list A, or add them back and re-run
  notebooks 3 and 4. Fwd PSH Flags matters most.

Problems:
  - Macro F1 is dominated by Heartbleed (only 2 test rows). C's macro F1 of 0.83 is
    almost entirely from missing both Heartbleed rows; every other class is above
    0.98 recall. Don't compare runs on macro F1 alone. Step 9a in notebook 4 adds
    scores without Heartbleed.
  - ram_mb was not measured. Step 9b in notebook 4 adds it.
  - One day of traffic split at random: near-identical rows from the same attack
    burst can land in both train and test, so these scores are optimistic.

Next step: run Step 9 of notebook 4, decide on the 4 Step 3 columns, then move on to
  making the tree smaller (max_depth / pruning) and measuring the trade-off.
```
