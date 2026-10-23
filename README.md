# Lightweight Cybersecurity Threat Detector

**In one sentence:** this project tests how small and cheap a machine-learning model for
spotting network attacks can be made before it starts missing attacks.

It uses the public **CICIDS2017** dataset. Every row is one network **flow** (one
conversation between two computers), labelled either `BENIGN` (normal) or one of five
attacks: DoS Hulk, DoS GoldenEye, DoS slowloris, DoS Slowhttptest and Heartbleed.

**Research question:**
> How much detection performance can be retained while reducing the computational,
> memory, and model-size requirements of a machine-learning-based cybersecurity threat
> detector?

In plain words: *how small and fast can the detector get before it gets noticeably worse?*

Author: Anush Jindal

---

## How the project works, step by step

| Step | What happens | In plain words | Where |
|---|---|---|---|
| 1. Research | Research question, literature review, attack types, a table explaining all 78 features | Understand the problem and the data before touching code | `research/` |
| 2. Explore | Load the Wednesday file of CICIDS2017: 692,703 flows, 79 columns | Look at the data: how big it is, what's broken, which classes are rare | `notebooks/01_dataset_exploration.ipynb` |
| 3. Clean and split | Remove 1,297 rows with infinite values and 80,914 duplicate rows, leaving 610,492. Split 80/20 into a training set (488,393) and a test set (122,099), keeping the same class mix in both | Fix broken rows, then hide 20% of the data as an "exam" the model never studies from | `notebooks/02_preprocessing.ipynb` |
| 4. Choose features | Drop 20 of the 78 features (always zero, or copies of another feature). Build four feature lists: **A (58), B (39), C (15), D (6)** | Decide which clues the model is allowed to look at, from many to very few | `notebooks/03_feature_engineering.ipynb`, `research/feature_documentation_template.md` |
| 5. Baseline model | Train a decision tree on each list with no tuning. Measure how many attacks it catches, how big it is, how fast it is and how much memory it needs. Then remove "shortcut" features and check again | The reference point that later, smaller models are compared against | `notebooks/04_baseline_model.ipynb`, `experiments/` |

**Not started yet:** shrinking the tree on purpose (depth limits, pruning) and the final
write-up.

---

## Words you need to explain the results

| Word | What it means here |
|---|---|
| **Feature** | One measured property of a flow, for example its duration or packets per second. The model decides using these. |
| **Decision tree** | A model that asks a chain of yes/no questions about the features ("is Flow Duration > 5,000?") until it reaches an answer. It is small, fast and easy to inspect, which suits a lightweight detector. |
| **Node** | One question (or one final answer) in the tree. More nodes = a bigger tree. |
| **Depth** | The longest chain of questions from the top of the tree to an answer. |
| **Training set / test set** | The model learns only from the training set. The test set is the exam: it is used only to score the model. |
| **Attack recall** | Of all real attacks in the test set, the share the model caught. Missing an attack is the worst mistake, so this is the most important number. |
| **Missed attacks** | Real attacks the model called normal. |
| **False alarms** | Normal flows the model called attacks. |
| **Macro F1** | A score from 0 to 1 that averages all classes equally, so a rare attack counts as much as normal traffic. |
| **Macro F1 without Heartbleed** | The same score, leaving out Heartbleed. Heartbleed has only 2 test rows, so with it included, one lucky or unlucky guess swings the whole score. |
| **Model size** | The size of the saved tree file in KB. |
| **Memory (RAM)** | The memory needed to hold the tree **plus** classify 1,000 flows at once, in MB. It does not include Python and scikit-learn themselves, which need far more. |
| **Shortcut** | A feature that gives away the answer only because of how the dataset was recorded (for example, attacks in the lab always hit the same port), not because of how attacks behave. A model that relies on shortcuts can fail on a real network. |

---

## Results so far (Stage 5 baseline)

Untuned decision tree (`random_state=42`), one day of traffic, one run.
All numbers come from `experiments/results.csv` and the Step 9 files in `experiments/`.

| Feature list | Features | Attack recall | Missed attacks | False alarms | Macro F1 without Heartbleed | Tree nodes | Model size | Memory |
|---|---|---|---|---|---|---|---|---|
| A (old version) | 57 | 99.90% | 38 | 25 | 0.996 | 825 | 93 KB | 0.75 MB |
| B | 39 | 99.89% | 43 | 26 | 0.996 | 891 | 100 KB | 0.55 MB |
| C | 15 | 99.90% | 38 | 34 | 0.996 | 997 | 111 KB | 0.29 MB |
| D | 6 | 99.82% | 68 | 66 | 0.992 | 1,487 | 164 KB | 0.25 MB |

**Shortcut check** (same lists with the possible shortcut features removed):

| Feature list | Features | Attack recall | Missed attacks | False alarms | Macro F1 without Heartbleed | Tree nodes | Model size | Memory |
|---|---|---|---|---|---|---|---|---|
| A without port | 56 | 99.85% | 58 | 47 | 0.992 | 1,139 | 127 KB | 0.77 MB |
| A without port and TCP window | 54 | 99.39% | 235 | 115 | 0.992 | 2,863 | 316 KB | 0.93 MB |
| C without port | 14 | 99.85% | 60 | 67 | 0.993 | 1,607 | 178 KB | 0.34 MB |
| D without port | 5 | 99.65% | 136 | 154 | 0.986 | 2,837 | 312 KB | 0.39 MB |

**About list A:** on 23-10-2026 the feature `Fwd PSH Flags` was put back into list A,
which is now 58 features. The A rows above are from the old 57-feature list. They are
marked `-v1` in `results.csv` and will be replaced once notebooks 3 and 4 are re-run.
Lists B, C and D did not change.

### What the results mean

1. **Using fewer features barely hurts detection.** Going from 57 features to 6, attack
   recall only drops from 99.90% to 99.82% (38 to 68 missed attacks out of about 38,700).
   Lists A, B and C score almost exactly the same.

2. **Fewer features made the tree *bigger*, not smaller.** List D's tree has 1,487 nodes
   against A's 825. With fewer clues, each question tells the tree less, so it needs more
   questions to reach the same answers. Shrinking the feature list does not shrink the
   model file.

3. **But fewer features need *less memory* to run.** A needs 0.75 MB and D needs 0.25 MB.
   Most of the running memory is the input data. With fewer features, each flow is
   smaller, and that saving outweighs the bigger tree. So **model size and memory move in
   opposite directions**, and a fair comparison has to report both.

4. **The model was partly using shortcuts.** Removing destination port and TCP window
   size raised missed attacks from 38 to 235 and made the tree 3.5 times bigger. Most of
   the extra misses were DoS Hulk. In this dataset, attacks came from a fixed lab setup,
   so these features partly encode the lab, not the attack.

5. **Earlier "list C is much worse" was a false alarm.** C's macro F1 with Heartbleed was
   0.83, but without Heartbleed it is 0.996, the same as A. C simply missed both of the 2
   Heartbleed test rows. This is why runs are compared without Heartbleed.

6. **Everything is already tiny.** Every model needs under 1 MB and well under 1 ms per
   1,000 flows. So the interesting question is not *"does it fit?"* but *"what does it
   get wrong as it shrinks, and is it relying on shortcuts?"*

### Limitations (be upfront about these)

- **The scores are probably too optimistic.** One day of traffic was split at random, so
  almost identical flows from the same attack burst can end up in both the training and
  the test set. That makes the test easier than a new day or a new network would be.
- **Heartbleed cannot be scored reliably.** It has only 11 rows in the whole file and 2 in
  the test set.
- **Timings are noisy.** The same tree trained in 27.4 s one day and 38.4 s the next on
  Colab. Timings are only compared within one session.
- **Memory is the model's share only.** It does not include Python and scikit-learn
  (100+ MB). A real small device would need the tree converted to something like C.
- **One run, one random seed, no tuning.** These are baseline numbers, not final ones.

---

## How every feature decision was checked

The feature table (`research/feature_documentation_template.md`) gives a reason for
keeping or removing each of the 78 features. In notebook 4, Step 3, every
"remove" reason was **tested on the real data** rather than taken from other papers:

- 17 of the 21 claims held (the column really was always zero, an exact copy, or in
  the same order as a kept column).
- 3 were *nearly* true (for example, two columns differed in 34 rows out of 488,393).
  Those columns stay removed, and the table now says "nearly identical".
- 1 was wrong: `Fwd PSH Flags` is non-zero in 4.32% of rows, not "always zero". It was
  put back into list A.

---

## What is in this repository

```
research/      research question, literature review, attack types, and the
               feature table (feature_documentation_template.md)
notebooks/     01 explore, 02 clean and split, 03 choose features, 04 baseline model
experiments/   results.csv (one row per experiment), experiment_notes.md (dated log of
               what was done and why), feature_sets.json (lists A-D), Step 9 result
               files. See experiments/README.md for what every file and column means.
data/          how to download the CICIDS2017 file (the data itself is not uploaded)
models/        trained trees are saved here (not uploaded; re-run notebook 4 to recreate)
```

## Running it

The notebooks run in Google Colab (the free CPU runtime is enough). Download
`Wednesday-workingHours.pcap_ISCX.csv` as described in `data/README.md`, then run
notebooks 01 → 04 in order. Local setup on Windows is covered in `SETUP_GUIDE.md`.

## Dataset

Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). Toward Generating a New
Intrusion Detection Dataset and Intrusion Traffic Characterization. *ICISSP 2018.*
Canadian Institute for Cybersecurity, University of New Brunswick:
https://www.unb.ca/cic/datasets/ids-2017.html
