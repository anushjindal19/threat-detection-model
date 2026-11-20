# Lightweight Cybersecurity Threat Detector

How small and cheap can a machine-learning model for detecting network attacks be made
before it starts missing attacks? This project trains decision trees on the public
**CICIDS2017** dataset, shrinks them step by step, and measures what each size costs and
what it loses, attack by attack.

**Research question:**
> How much detection performance can be retained while reducing the computational,
> memory, and model-size requirements of a machine-learning-based cybersecurity threat
> detector?

Author: Anush Jindal

---

## Two versions

The project has been done twice. The first version scored about 99.9%, which was too good
to be true, so the second version answers the same question again, testing the trees on traffic they
have not seen. Both are
kept here, each in its own folder.

| | [v1: random split](v1_random_split/) | [v2: unseen data](v2_unseen_data/) |
|---|---|---|
| Data | Wednesday only (610,492 flows, 5 attack types) | All five days (2,572,640 flows, 14 attack types) |
| What the tree learns | The name of each attack tool | Attack or normal |
| Features | Lists A-D (58 to 6 features), with and without 3 shortcut features | The shortcut-free lists only (55 to 4 features) |
| Test set | A random 20% of the same day | Later traffic, an attack type never seen, a day never seen |
| Attack flows caught | **99.9%** | **94.7%** later traffic, **55.7%** unseen attack type, **7.2%** unseen day |
| Smallest good tree | 3.7 KB (list C, depth 12) | 8.0 KB (list A-NS, pruned) |
| Status | Kept as it was, for comparison | Current |

## Why v1's 99.9% could not be trusted

1. **Random split of one day.** Each attack is one long burst of similar flows. Shuffling
   them puts near-copies of the training flows in the test set. With only the split changed
   to "train on the earlier part, test on the later part", DoS slowloris recall falls from
   99.1% to 59.1%.
2. **Shortcut features.** Destination port and TCP window size identify the lab's server,
   not the attack.
3. **Only attacks the tree had trained on.** The test set held the same five attack tools,
   from the same session. Kept out of training, an attack type is caught 32% of the time on
   average, and a port scan almost never.

## Answer to the research question

![Recall per attack type against model size, depth limits vs pruning](v2_unseen_data/results/figures/fig5_depth_vs_pruning.png)

Measured on traffic recorded after the training data (v2, 55-feature list):

| Tree | Size | Comparisons per flow | Attack flows caught | Per attack type |
|---|---|---|---|---|
| Full tree, 4,043 nodes | 35.5 KB | 17.6 | 94.7% | 82.3% |
| Pruned, 913 nodes (chosen on validation data) | 8.0 KB | 14.7 | 94.7% | 80.2% |
| Pruned, 265 nodes | 2.3 KB | 11.6 | 91.0% | 73.3% |
| Pruned, 111 nodes | 1.0 KB | 10.6 | 86.1% | 64.3% |
| One question | 0.03 KB | 1.0 | 44.4% | 21.3% |

1. **Model size can be cut by about three quarters with no loss** in the share of attack
   flows caught, if the tree is pruned. The pruned tree (8.0 KB) fits the 32 KB of an
   ATmega328P microcontroller; the full tree (35.5 KB) does not.
2. **Below that, the rarest attacks are forgotten first** while overall recall stays high.
   The 2.3 KB tree misses every Infiltration and SQL-injection flow. A depth-8 tree still
   catches 84.6% of attack flows but none of the web attacks.
3. **Depth limits are the wrong way to shrink.** No depth limit passed the validation check;
   pruning did for every feature list.
4. **Computation falls much less than size** (17% fewer comparisons for a 77% smaller tree).
   **Memory** follows both the tree and the number of features: fewer features save input
   memory (52 bytes for 13 features against 220 for 55) but do not make the tree smaller,
   and they cost detection on the less common attacks.
5. **What can be retained is detection of known attacks.** On attack types left out of
   training, trees of every size caught at most 33% per type, and on whole days left out at
   most 22%. v1's random split hid this and made shrinking look free.

None of the warnings about testing is new on its own (see
[`research/literature_review.md`](research/literature_review.md), entries 8 to 13). What the
project adds is the size axis: the size-versus-detection curve measured attack by attack on
traffic the tree has not seen.

Full tables, per-attack results and limitations: [v2 README](v2_unseen_data/README.md).
v1's results (which attacks a smaller tree forgets first, the shortcut check, memory and
speed): [v1 README](v1_random_split/README.md).

---

## Repository layout

```
README.md              this file
research/              research question, literature review, references, attack types and
                       the table explaining all 78 features (shared by both versions)
data/                  where to download the CICIDS2017 files (the data is not committed)

v1_random_split/       FIRST VERSION, unchanged
  notebooks/           01-07: explore, clean, features, baseline, shrinking, figures,
                       Friday check
  experiments/         result files, figures and the dated log
  README.md            v1's full results

v2_unseen_data/        CURRENT VERSION
  notebooks/           01 why v1 scored so high, 02 prepare all days,
                       03 train and test, 04 results
  results/             one set of files per notebook (01_*, 02_*, 03_*, 04_*) and figures/
  helpers.py           code shared by the v2 notebooks
  notes.md             dated log
  README.md            v2's full results and a guide to every result file
```

The repository exactly as it was when v1 was finished is commit `e75145f`.

## How to run

```
pip install -r requirements.txt
```

Download the data as described in [`data/README.md`](data/README.md), then follow "How to
run" in the README of the version you want.

## Limitations

- All five days come from one lab network in one week. A new day in v2 is still the same
  network, so a different network is likely to be harder.
- CICIDS2017 has known labelling and flow-construction errors (Engelen et al., 2021;
  Lanvin et al., 2023), which these results inherit.
- Three attack types have fewer than 40 flows and cannot be scored reliably.
- Tree sizes are calculated and checked in software, not measured on a device.

Each version's README lists its own limitations in full.

## Next steps

- **Test on a different network:** CSE-CIC-IDS2018 has the same four DoS tools on another
  network (15 and 16 February 2018).
- **Compare with an anomaly detector** trained on normal traffic only, the usual approach
  to attacks nobody has seen.
- **Repeat tests 1 and 2 of v2 on several splits,** as v1 did.
- **Run the tree on a microcontroller:** export the pruned tree to C (for example with
  emlearn) and benchmark it on an ATmega328P and an STM32F401.
- **Use the corrected CICIDS2017** (Engelen et al., 2021) to check how much the dataset's
  labelling errors change the results.

## Dataset

Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). Toward Generating a New
Intrusion Detection Dataset and Intrusion Traffic Characterization. *ICISSP 2018.*
Canadian Institute for Cybersecurity, University of New Brunswick:
https://www.unb.ca/cic/datasets/ids-2017.html
