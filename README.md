# Lightweight Cybersecurity Threat Detector

How small and cheap can a machine-learning model for detecting network attacks be made
before it starts missing attacks? This project trains decision trees on the public
**CICIDS2017** dataset, shrinks them step by step, and measures what each size costs
(nodes, bytes, comparisons per flow, memory) and what it loses, attack by attack.

Every row of the data is one network **flow** (one conversation between two computers),
labelled either `BENIGN` (normal) or one of five attacks: DoS Hulk, DoS GoldenEye,
DoS slowloris, DoS Slowhttptest and Heartbleed.

**Research question:**
> How much detection performance can be retained while reducing the computational,
> memory, and model-size requirements of a machine-learning-based cybersecurity threat
> detector?

Author: Anush Jindal

---

## Pipeline

| Stage | What happens | Where |
|---|---|---|
| 1. Research | Research question, literature review, attack types, and a table explaining all 78 features | `research/` |
| 2. Explore | Load the Wednesday file of CICIDS2017: 692,703 flows, 79 columns. Check size, missing and infinite values, duplicates and class balance | `notebooks/01_dataset_exploration.ipynb` |
| 3. Clean and split | Remove 1,297 rows with infinite values and 80,914 duplicate rows, leaving 610,492. Split 80/20 into a training set (488,393) and a test set (122,099), keeping the same class mix in both | `notebooks/02_preprocessing.ipynb` |
| 4. Choose features | Drop 20 of the 78 features (always zero, or copies of another feature). Build four feature lists: **A (58), B (39), C (15), D (6)** | `notebooks/03_feature_engineering.ipynb`, `research/feature_documentation.md` |
| 5. Baseline model | Train an untuned decision tree on each list. Measure attacks caught, tree size, speed and memory. Then remove possible "shortcut" features and check again | `notebooks/04_baseline_model.ipynb`, `experiments/` |
| 6. Shrink the tree | Limit the tree's depth (1 to 20) and prune it, on lists A-D with and without the shortcut features, on 5 different train/test splits. Record what each class loses at every size. Choose the smallest good tree on a validation set, never on the test set | `notebooks/05_shrinking_the_tree.ipynb`, `notebooks/06_paper_figures.ipynb`, `experiments/` |
| 7. Over-fitting check | Run the Wednesday-trained trees on the **Friday afternoon DDoS** file, which they have never seen | `notebooks/07_friday_overfitting_check.ipynb`, `experiments/` |

---

## Terms

| Term | Meaning here |
|---|---|
| **Feature** | One measured property of a flow, for example its duration or packets per second. The model decides using these. |
| **Decision tree** | A model that asks a chain of yes/no questions about the features ("is Flow Duration > 5,000?") until it reaches an answer. It is small, fast and easy to inspect, which suits a lightweight detector. |
| **Node** | One question (or one final answer) in the tree. More nodes = a bigger tree. |
| **Depth** | The longest chain of questions from the top of the tree to an answer. |
| **Training set / test set** | The model learns only from the training set. The test set is held back and used only to score the model. |
| **Attack recall** | Of all real attacks in the test set, the share the model caught. Missing an attack is the worst mistake, so this is the most important number. |
| **Missed attacks** | Real attacks the model called normal. |
| **False alarms** | Normal flows the model called attacks. |
| **Macro F1** | A score from 0 to 1 that averages all classes equally, so a rare attack counts as much as normal traffic. |
| **Macro F1 without Heartbleed** | The same score, leaving out Heartbleed. Heartbleed has only 2 test rows, so with it included, one lucky or unlucky guess swings the whole score. |
| **Model size** | The size of the saved tree file in KB. |
| **Compact size** | The bytes needed to store the tree as plain arrays, as it would be stored on a small device (9 bytes per node). Much smaller than the saved file, and checked to give exactly the same answers. |
| **Comparisons per flow** | How many yes/no questions the tree asks, on average, before it labels a flow: its real amount of work, whatever the computer. |
| **Memory (RAM)** | The memory needed to hold the tree **plus** classify 1,000 flows at once, in MB. It does not include Python and scikit-learn themselves, which need far more. |
| **Shortcut** | A feature that gives away the answer only because of how the dataset was recorded (for example, attacks in the lab always hit the same port), not because of how attacks behave. A model that relies on shortcuts can fail on a real network. |

---

## Results: Stage 5 baseline (full-size trees)

Untuned decision tree (`random_state=42`), split 42, run in notebook 05 with the
58-feature list A. All numbers come from `experiments/results.csv` and the `S5_*.csv` files.

| Feature list | Features | Attack recall | Missed attacks | False alarms | Macro F1 without Heartbleed | Tree nodes | Model size | Memory |
|---|---|---|---|---|---|---|---|---|
| A | 58 | 99.91% | 36 | 21 | 0.997 | 823 | 93 KB | 0.76 MB |
| B | 39 | 99.89% | 43 | 28 | 0.995 | 891 | 100 KB | 0.55 MB |
| C | 15 | 99.90% | 38 | 34 | 0.996 | 997 | 111 KB | 0.28 MB |
| D | 6 | 99.82% | 68 | 66 | 0.992 | 1,487 | 164 KB | 0.25 MB |

**Shortcut check** (same lists with the possible shortcut features removed):

| Feature list | Features | Attack recall | Missed attacks | False alarms | Macro F1 without Heartbleed | Tree nodes | Model size | Memory |
|---|---|---|---|---|---|---|---|---|
| A without port | 57 | 99.85% | 57 | 46 | 0.992 | 1,143 | 128 KB | 0.78 MB |
| A without port and TCP window | 55 | 99.38% | 240 | 112 | 0.991 | 2,859 | 315 KB | 0.94 MB |
| C without port | 14 | 99.84% | 61 | 70 | 0.993 | 1,603 | 177 KB | 0.34 MB |
| D without port | 5 | 99.65% | 136 | 149 | 0.986 | 2,839 | 312 KB | 0.39 MB |

**Reproducibility:** notebook 05 repeats these runs on one machine (scikit-learn 1.9.1) so
that every number can be compared with Stage 6. Lists C and D gave exactly the same results
as the earlier Colab run of notebook 04. B and the no-port runs differ from it by a few flows
(for example B: 26 -> 28 false alarms), because a newer scikit-learn breaks ties between
equally good splits differently. See `experiments/experiment_notes.md`.

### Findings

1. **Using fewer features barely hurts detection.** Going from 58 features to 6, attack
   recall only drops from 99.91% to 99.82% (36 to 68 missed attacks out of 38,751).
   Lists A, B and C score almost exactly the same.

2. **Fewer features made the tree *bigger*, not smaller.** List D's tree has 1,487 nodes
   against A's 823. With fewer features, each question tells the tree less, so it needs
   more questions to reach the same answers.

3. **But fewer features need *less memory* to run.** A needs 0.76 MB and D needs 0.25 MB.
   Most of the running memory is the input data, so model size and memory move in
   opposite directions, and a fair comparison has to report both.

4. **The model was partly using shortcuts.** Removing destination port and TCP window
   size raised missed attacks from 36 to 240 and made the tree 3.5 times bigger. In this
   dataset all four DoS attacks hit one lab web server from one attacking machine (and
   Heartbleed a second server), so these features partly encode the lab, not the attack.

5. **List C is not really worse.** C's macro F1 with Heartbleed is 0.83, but without
   Heartbleed it is 0.996, almost the same as A's 0.997. C simply missed both of the 2
   Heartbleed test rows. This is why runs are compared without Heartbleed.

## Results: Stage 6 (shrinking the tree)

480 depth-limited trees (8 feature lists x 12 depth limits x 5 splits) plus a pruning sweep.
Numbers are means over the 5 splits unless marked otherwise. Full tables: `experiments/S6_*.csv`.

**The smallest depth chosen on the validation set** (rule: every class except Heartbleed
keeps its recall within 1 point of the full tree), then scored on the test set:

| List | Features | Chosen depth | Nodes (full -> chosen) | Compact size (full -> chosen) | Attack recall (full -> chosen) | Macro F1 without Heartbleed (full -> chosen) |
|---|---|---|---|---|---|---|
| A | 58 | 20 | 808 -> 655 | 7.1 -> 5.8 KB | 99.92% -> 99.93% | 0.996 -> 0.995 |
| B | 39 | 20 | 871 -> 725 | 7.7 -> 6.4 KB | 99.90% -> 99.92% | 0.995 -> 0.995 |
| C | 15 | 12 | 985 -> 419 | 8.7 -> 3.7 KB | 99.90% -> 99.80% | 0.995 -> 0.993 |
| D | 6 | 12 | 1,469 -> 581 | 12.9 -> 5.1 KB | 99.84% -> 99.71% | 0.992 -> 0.986 |
| A-NS | 55 | 20 | 2,849 -> 1,806 | 25.0 -> 15.9 KB | 99.38% -> 99.39% | 0.991 -> 0.991 |
| B-NS | 36 | 15 | 3,413 -> 972 | 30.0 -> 8.5 KB | 99.30% -> 99.23% | 0.990 -> 0.988 |
| C-NS | 13 | 12 | 3,986 -> 608 | 35.0 -> 5.3 KB | 99.22% -> 99.17% | 0.990 -> 0.989 |
| D-NS | 4 | 20 | 16,240 -> 7,264 | 142.7 -> 63.8 KB | 97.11% -> 98.51% | 0.974 -> 0.977 |

(`-NS` = without `Destination Port`, `Init_Win_bytes_forward` and `Init_Win_bytes_backward`.)

### Findings

1. **The overall score hides what a smaller tree forgets.** List A at depth 8 still catches
   98.4% of attacks, but only 81.8% of DoS Slowhttptest and 88.5% of DoS slowloris (the two
   rarest DoS attacks), while DoS Hulk stays at 99.4%. In lists A, B and C, from depth 3
   upward, DoS Hulk never falls below 98.7%: the losses land on the smaller attacks.
2. **Shrinking the shortcut-free trees is almost free.** Without the shortcut features the
   full trees are 3.5 to 11 times bigger and partly memorise the training data. C-NS keeps
   its score (about 0.1 points lower at most) with 85% fewer nodes, and D-NS at depth 20
   catches *more* attacks than its full tree.
3. **How the tree is shrunk matters more than how much.** On split 42, pruning list A to
   217 nodes kept macro F1 at 0.996 (full tree: 0.997), while a depth-limited tree of
   similar size (293 nodes) scored 0.978.
4. **In Python, memory and speed depend on the number of features, not the size of the
   tree.** For list A, classifying a batch of 1,000 flows needs about 0.67 MB at every depth,
   but only 0.09 MB with the 6 features of list D, because scikit-learn copies the whole
   batch of features before classifying it. A small device that checks one flow at a time
   would need only 4 bytes per feature (232 bytes for list A), so there the tree itself
   would be the main memory cost. Compact trees are tiny either way: every full tree with the
   shortcut features is 13.1 KB or less, well inside the 32 KB flash of an ATmega328P or
   the 512 KB of an STM32F401.

## Results: Stage 7 (over-fitting check on a new day: Friday afternoon)

The Wednesday scores (99.9% accuracy) come from a test set cut from the **same day** as the
training set, so they may be too optimistic. Here the same trees (trained on the Wednesday
training set, split 42) were run on the **Friday afternoon DDoS** file: 223,082 flows after
the same cleaning as notebook 2, of which 95,068 are normal and 128,014 are a DDoS attack.

**Why Friday afternoon:** it is the best over-fitting check in CICIDS2017. It has plenty of
normal traffic, and its attack is a DDoS HTTP flood against port 80 of the **same web
server** (192.168.10.50) that Wednesday's four DoS attacks hit, which makes it the closest
relative of Wednesday's attacks on any other day. It was sent with a different tool (LOIT)
from three different attacking machines. No other CICIDS2017 day contains Wednesday's exact
attacks. The trees never saw the label "DDoS", so they cannot name it; what matters is
whether they call it *an* attack.

Unlimited trees (full table, every depth: `experiments/S7_friday_test.csv`):

| List | Accuracy (exact label) | Accuracy (attack vs normal) | False alarms on normal traffic: Friday (Wednesday) | DDoS flows flagged as an attack |
|---|---|---|---|---|
| A (58) | 42.60% | 59.67% | 0.025% (0.025%) | 38,059 of 128,014 (29.7%) |
| B (39) | 42.60% | 64.94% | 0.041% (0.034%) | 49,848 (38.9%) |
| C (15) | 42.58% | 53.03% | 0.084% (0.041%) | 23,305 (18.2%) |
| D (6) | 42.56% | 53.37% | 0.135% (0.079%) | 24,121 (18.8%) |
| A-NS (55) | 42.53% | 64.89% | 0.191% (0.134%) | 49,863 (39.0%) |
| B-NS (36) | 42.51% | 59.36% | 0.248% (0.181%) | 37,590 (29.4%) |
| C-NS (13) | 42.46% | 77.86% | 0.361% (0.221%) | 78,961 (61.7%) |
| D-NS (4) | 38.99% | 60.60% | 8.515% (1.167%) | 48,214 (37.7%) |
| Always "normal" | 42.62% | 42.62% | 0% | 0 |

### Findings

1. **The 99.9% does not carry over to a new day.** On Wednesday, list A catches 99.9% of
   attacks. On Friday it catches only 29.7% of a flood attack on the same web server, and
   calls the other 70.3% normal traffic (most of the flows it does catch are called
   "DoS Hulk"). The trees learned Wednesday's specific attack tools and recording, not a
   general idea of "flood attack".
2. **Normal traffic is not the problem.** List A's false-alarm rate is 0.025% on both days,
   and lists B-D and A-NS to C-NS stay below 0.4%. So the trees did not memorise Wednesday's
   normal traffic. The exception is D-NS (4 features): 8.5% false alarms on Friday.
3. **What gets caught is close to luck.** The share of DDoS flows caught jumps between about
   17%, 29%, 39% and 63% depending on the list and depth, with no clear pattern. A depth-1
   tree (one question) catches 62.7%, more than list A's full tree. Catching this attack
   hangs on one or two thresholds.
4. **Exact-label accuracy is meaningless here.** Every tree scores about 42.6%, the share
   of normal flows. "Always normal" scores the same.
5. **What this cannot separate:** DDoS is a different tool from more machines, so some drop
   is expected even for a model that is not over-fitted. Testing the same attacks on new
   data needs the CSE-CIC-IDS2018 DoS days (15 and 16 February 2018), which use the same
   four DoS tools.

## Limitations

- **The scores are too optimistic.** One day of traffic was split at random, so almost
  identical flows from the same attack burst can end up in both the training and the test
  set. Stage 7 confirms this matters: on a related attack from another day (Friday DDoS),
  list A catches 29.7% instead of 99.9%.
- **Heartbleed cannot be scored reliably.** It has only 11 rows in the whole file and 2 in
  the test set.
- **Timings are noisy.** The same tree trained in 27.4 s one day and 38.4 s the next on
  Colab. Timings are only compared within one session.
- **Memory is the model's share only.** It does not include Python and scikit-learn
  (100+ MB). A real small device would need the tree converted to something like C.
- **Stage 5 is one run on one split.** Stage 6 repeats every depth on 5 splits; the pruning
  sweep and the time/memory measurements are from split 42 only.
- **The comparisons in Stage 6 are on test data.** Only the "chosen depth" table uses a rule
  fixed on the validation set; the curves describe the test results at every size.
- **The dataset has known errors.** CICIDS2017 contains flow-construction and labelling
  errors (Engelen et al., 2021; Lanvin et al., 2023), which these results inherit.

---

## How every feature decision was checked

The feature table (`research/feature_documentation.md`) gives a reason for keeping or
removing each of the 78 features. In notebook 4, Step 3, every "remove" reason was
**tested on the real data** rather than taken from other papers:

- 17 of the 21 claims held (the column really was always zero, an exact copy, or in
  the same order as a kept column).
- 3 were *nearly* true (for example, two columns differed in 34 rows out of 488,393).
  Those columns stay removed, and the table says "nearly identical".
- 1 was wrong: `Fwd PSH Flags` is non-zero in 4.32% of rows, not "always zero". It was
  put back into list A.

---

## Repository layout

```
research/      research question, literature review, references, attack types, and the
               feature table (feature_documentation.md)
notebooks/     01 explore, 02 clean and split, 03 choose features, 04 baseline model,
               05 shrinking the tree (Stage 6, also re-runs Stage 5), 06 paper figures,
               07 over-fitting check on Friday afternoon (Stage 7)
experiments/   results.csv (one row per experiment), experiment_notes.md (dated log of
               what was done and why), feature_sets.json (lists A-D), the S5_*/S6_*/S7_*
               result files and figures/. See experiments/README.md for every file and column.
data/          how to download the CICIDS2017 files (the data itself is not committed)
models/        trained trees are saved here (not committed; re-run notebook 4 to recreate)
```

## How to run

The notebooks run in Google Colab (the free CPU runtime is enough) or locally:

```
pip install -r requirements.txt
```

1. Download `Wednesday-workingHours.pcap_ISCX.csv` as described in `data/README.md` and put
   it in `data/` (local) or the Drive data folder (Colab).
2. Run notebooks 01 → 04 in order. Notebook 02 writes the train/test files that
   notebooks 03 and 04 read.
3. Notebook 05 needs only the raw CSV (it repeats the cleaning and split itself) and takes
   about 1.5 hours on a 2-core CPU. Notebook 06 builds the figures from the saved CSVs in
   seconds.
4. Notebook 07 also needs `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` and takes
   about 10 minutes.

## Next steps

- **Test the same attacks on new data:** the CSE-CIC-IDS2018 DoS days (15 and 16 February
  2018) use the same four DoS tools as Wednesday.
- **Validate the pruning choice:** choose `ccp_alpha` on the validation set and repeat it on
  several splits, as was done for depth.
- **Run the tree on a microcontroller:** export the compact tree to C (for example with
  emlearn) and benchmark it on an ATmega328P (32 KB flash / 2 KB SRAM) and an STM32F401
  (512 KB flash / 96 KB RAM).
- **Use the corrected CICIDS2017** (Engelen et al., 2021) to check how much the dataset's
  labelling errors change the results.

## Dataset

Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). Toward Generating a New
Intrusion Detection Dataset and Intrusion Traffic Characterization. *ICISSP 2018.*
Canadian Institute for Cybersecurity, University of New Brunswick:
https://www.unb.ca/cic/datasets/ids-2017.html
