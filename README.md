# Lightweight Cybersecurity Threat Detector

A research project on how small and cheap a machine-learning network threat detector can
be made before its detection quality drops. It classifies network flows from the public
**CICIDS2017** dataset as normal traffic (BENIGN) or one of five attack types (DoS Hulk,
DoS GoldenEye, DoS slowloris, DoS Slowhttptest, Heartbleed).

**Research question:**
> How much detection performance can be retained while reducing the computational,
> memory, and model-size requirements of a machine-learning-based cybersecurity threat
> detector?

Author: Anush Jindal

---

## What has been done

| Stage | What | Where |
|---|---|---|
| 1. Research | Research question, literature review, attack types, documentation of all 78 features | `research/` |
| 2. Dataset | Explored the Wednesday file of CICIDS2017 (692,703 flows, 79 columns) | `notebooks/01_dataset_exploration.ipynb` |
| 3. Preprocessing | Removed rows with infinite values and duplicate rows; stratified 80/20 train/test split (488,393 / 122,099 flows) | `notebooks/02_preprocessing.ipynb` |
| 4. Feature engineering | Grouped all 78 features; built four nested feature sets: A (57), B (39), C (15), D (6) | `notebooks/03_feature_engineering.ipynb` |
| 5. Baseline model | Untuned decision tree on each feature set, scored on detection quality and cost (size, speed); shortcut check without port / TCP window features | `notebooks/04_baseline_model.ipynb`, `experiments/` |

Not started yet: shrinking the model (depth limits, pruning), resource benchmarking, and
the final write-up.

## Baseline results (Stage 5)

Untuned `DecisionTreeClassifier`, one day of traffic, one run. Full numbers in
`experiments/results.csv`; reasoning in `experiments/experiment_notes.md`.

| Feature set | Features | Attack recall | Missed attacks | False alarms | Tree nodes | Model size |
|---|---|---|---|---|---|---|
| A | 57 | 99.90% | 38 | 25 | 825 | 93 KB |
| B | 39 | 99.89% | 43 | 26 | 891 | 100 KB |
| C | 15 | 99.90% | 38 | 34 | 997 | 111 KB |
| D | 6 | 99.82% | 68 | 66 | 1,487 | 164 KB |
| A without port and TCP window | 54 | 99.39% | 235 | 115 | 2,863 | 316 KB |

**Observations so far**

- Detection stays above 99.8% attack recall even with only 6 features.
- Fewer features produced *bigger* trees: each remaining feature carries less
  information, so the tree needs more splits to separate the classes.
- Removing destination port and TCP window size raised missed attacks from 38 to 235
  and tripled the tree size, so the model was partly relying on lab-specific clues
  rather than attack behaviour.

**Limitations**

- Macro F1 is not used for comparison here because Heartbleed has only 2 test rows and
  dominates it. Scores without Heartbleed and memory use are added in Step 9 of
  notebook 4 (not run yet).
- The train/test split is random within one day of traffic, so near-identical flows from
  the same attack can appear in both. These scores are likely optimistic for a new day or
  a new network.
- Four keep/remove decisions from Stage 4 did not fully hold when tested in notebook 4
  (Step 3) and are still to be revisited.

## Repository layout

```
research/      research question, literature review, attack types, feature documentation
notebooks/     01 exploration, 02 preprocessing, 03 feature engineering, 04 baseline model
experiments/   results.csv (one row per experiment) and experiment_notes.md
data/          README on which CICIDS2017 file to download (the CSV is not committed)
models/        trained models are saved here (not committed)
```

## Running it

The notebooks run in Google Colab (free CPU runtime is enough). Download
`Wednesday-workingHours.pcap_ISCX.csv` as described in `data/README.md`, then run
notebooks 01 → 04 in order. Local setup on Windows is covered in `SETUP_GUIDE.md`
(`setup.bat` installs `requirements.txt`).

## Dataset

Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). Toward Generating a New
Intrusion Detection Dataset and Intrusion Traffic Characterization. *ICISSP 2018.*
Canadian Institute for Cybersecurity, University of New Brunswick:
https://www.unb.ca/cic/datasets/ids-2017.html
