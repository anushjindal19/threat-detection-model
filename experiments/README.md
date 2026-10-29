# What is in `experiments/`

Every number in this folder came from actually running a notebook. Nothing is estimated
or typed in by hand. If a number is not measured yet, the cell is left empty.

All result files (`results.csv`, `S5_*.csv`, `S6_*.csv` and `figures/fig1_*`, `fig2_*`)
were made by **one run of `notebooks/05_shrinking_the_tree.ipynb`** (29-10-2026,
scikit-learn 1.9.1, 2-core CPU), so every number can be compared with every other. The
paper figures were drawn from those files by notebook 06. That run also re-did the Stage 5 baseline (notebook 4, Steps 4-9) with the new
58-feature list A, which replaced the old `-v1` rows.

| File | What it is | Made by |
|---|---|---|
| `results.csv` | One row per headline experiment (see the column guide below): the 8 Stage 5 baseline runs (`S5-*`) and the 8 smallest trees chosen in Stage 6 (`S6-*`) | Notebook 5, Parts 1 and 5 |
| `experiment_notes.md` | Dated log of what was done, what was seen, what went wrong and what was decided. Every row in `results.csv` can be traced to an entry here. | Written by hand after each session |
| `feature_sets.json` | The four feature lists A (58), B (39), C (15), D (6) | Notebook 3, Step 6 |
| `S5_scores_without_heartbleed.csv` | Stage 5: macro F1 with and without Heartbleed, weighted F1, attack recall, and how many of the 2 Heartbleed test rows were caught | Notebook 5, Part 1 (same as notebook 4, Step 9a) |
| `S5_memory.csv` | Stage 5: memory for each tree (the tree itself, the extra memory to classify 1,000 flows, and the total) | Notebook 5, Part 1 (same as notebook 4, Step 9b) |
| `S5_per_class_recall.csv` | Stage 5: for each class, the share of its test rows the model got right, for every run. `test rows` shows how many rows each number is based on. | Notebook 5, Part 1 (same as notebook 4, Step 7) |
| `S6_majority_baseline.csv` | A "detector" that calls every flow BENIGN, on each of the 5 splits. The floor every real model must beat. | Notebook 5, Part 2 |
| `S6_depth_sweep.csv` | **The main experiment.** One row per split (5) x feature list (8) x depth limit (12) = 480 trees, with every measure listed below | Notebook 5, Part 3 |
| `S6_ccp_sweep.csv` | Same measures for cost-complexity pruning (`ccp_alpha`), split 42 only: 8 lists x 13 pruning strengths | Notebook 5, Part 4 |
| `S6_validation_sweep.csv` | The depth sweep repeated on a **validation** set (20% of the training set), used only to choose the smallest good depth | Notebook 5, Part 5 |
| `S6_validation_choice.csv` | The depth chosen for each list, under the main rule (1 point) and a stricter rule (0.1 points) | Notebook 5, Part 5 |
| `S6_summary_by_depth.csv` | `S6_depth_sweep.csv` averaged over the 5 splits (mean, min, max), plus split-42 costs and how much of the unlimited tree's score is kept | Notebook 5, Part 6 |
| `S6_summary_chosen_depth.csv` | Test results of the chosen depth next to the unlimited tree, for each list and rule | Notebook 5, Part 6 |
| `S7_friday_test.csv` | Stage 7: every tree from the split-42 depth sweep (8 lists x 12 depths), trained on the Wednesday training set and tested on the Wednesday test set and the Friday afternoon DDoS file | Notebook 7 |
| `S7_friday_summary.csv` | Stage 7: the same, for the unlimited trees and the depths chosen in Stage 6 only | Notebook 7 |
| `figures/fig1_*.png`, `figures/fig2_*.png` | Quick-look figures: recall of each class vs depth (A, A-NS), and macro F1 vs compact size for all 8 lists | Notebook 5, Part 6 |
| `figures/paper_fig*.png` | The two figures used in the paper: recall of each class vs depth, and depth limits vs pruning | Notebook 6 (from the CSVs above, no training) |

## Words used in the Stage 6 files

| Word | Meaning |
|---|---|
| **Split** (`seed`) | Which random 80/20 train/test split was used. 42 is the notebook 2 split; 43-46 were made the same way with different random numbers. The tree's own `random_state` is the same number. |
| **Feature list** (`feature_set`) | A, B, C, D from notebook 3. `-NS` ("no shortcuts") = the same list without `Destination Port`, `Init_Win_bytes_forward` and `Init_Win_bytes_backward`, giving A-NS 55, B-NS 36, C-NS 13, D-NS 4 features. |
| **`max_depth`** | The depth limit set for the tree. `none` = no limit (the untuned tree). `depth_reached` is how deep it actually grew. |
| **Attack recall** | Share of real attack flows the tree flagged as any attack. |
| **False alarm rate** | Share of benign flows the tree flagged as an attack. |
| **`macro_f1_no_hb`** | Macro F1 over the 5 classes other than Heartbleed (Heartbleed has only 2 test rows per split). |
| **`recall_<class>`, `caught_<class>`, `rows_<class>`** | Recall for one class, how many of its test rows were labelled correctly, and how many test rows it has. |
| **`avg_comparisons`** | Average number of yes/no questions the tree asks per test flow before reaching an answer: the tree's real amount of work, independent of the computer. |
| **`compact_bytes`** | Bytes needed to store the tree as plain arrays (per node: 1-byte feature number, 4-byte threshold, two 2-byte child numbers = 9 bytes; 13 bytes if the tree had 65,536 nodes or more). `compact_matches_sklearn = True` means a classifier using only those arrays gave exactly the same answer as scikit-learn on every test flow. |
| **`joblib_kb`, `ram_mb`, `training_time_s`, `inference_ms_per_1000`** | Same as in `results.csv`. In the summaries these come from split 42 only; times are only comparable within this one run. |
| **`root_feature`, `top3_features`** | The feature asked first, and the three features the tree relies on most (by scikit-learn's importance score). |
| **Retained / reduction (%)** | A smaller tree's score as a percentage of the unlimited tree's on the same split and list; and how much smaller (size) or less work (comparisons) it is. |

## Words used in the Stage 7 files

| Word | Meaning |
|---|---|
| **`test_file`** | Where the tree was tested: the Wednesday test set (same day as training) or Friday afternoon (DDoS, a new day). |
| **`accuracy_exact_label`** | Share of flows given exactly the right label. On Friday every DDoS flow counts as wrong, because the trees never saw the label "DDoS". |
| **`accuracy_attack_vs_normal`** | Share of flows put on the right side: normal called normal, attack called any attack. |
| **`false_alarm_rate`** | Share of normal flows called an attack. `false_alarms_called` says which attack name they were given. |
| **`attack_detection_rate`**, **`flagged_<attack>`** | Share (and count) of attack flows called any attack. |

## Column guide for `results.csv`

| Column | Meaning |
|---|---|
| `experiment_id` | Name of the run. `S5` = Stage 5 (untuned baseline). `S6-<list>-depth<d>` = Stage 6, the smallest depth chosen on the validation set. `S7-<list>-friday` = Stage 7, the unlimited tree trained on Wednesday and tested on the Friday afternoon DDoS file (its `accuracy` is exact-label accuracy; the other Friday numbers are in `notes`). |
| `date` | Day the run was done |
| `stage` | `5-baseline` = untuned decision tree; `6-shrink` = depth-limited tree chosen in Stage 6 |
| `dataset_file` | Which CICIDS2017 file was used |
| `num_samples` | Training rows + test rows (488,393 + 122,099 = 610,492) |
| `num_features` | How many features the tree was allowed to use |
| `features_used` | Which feature list (A, B, C, D, a list with the shortcut features removed, or an `-NS` list) |
| `max_depth` | S5 rows: how deep the untuned tree grew. S6 rows: the depth limit that was set. |
| `num_nodes` | How many questions and answers the tree has (its size) |
| `accuracy` | Share of all test rows labelled correctly. Looks high because most rows are BENIGN, so don't rely on it alone. |
| `precision`, `recall`, `f1` | Macro averages: every class counts equally, including Heartbleed (only 2 test rows). S6 rows give only `f1`; their macro F1 without Heartbleed is in `notes`. |
| `model_size_kb` | Size of the saved tree file (`.joblib`) |
| `training_time_s` | Seconds to train the tree. Only comparable between runs from the same session. |
| `inference_ms` | Milliseconds to classify **1,000** test flows (median of 5 tries) |
| `ram_mb` | Memory in MB: the tree itself plus the peak extra memory to classify 1,000 flows. Does not include Python or scikit-learn. |
| `notes` | Settings used, plus attack recall, missed attacks and false alarms |

## Re-running

Put `Wednesday-workingHours.pcap_ISCX.csv` in `data/` (see `data/README.md`) and run
`notebooks/05_shrinking_the_tree.ipynb` top to bottom (about 1.5 hours on a 2-core CPU).
It rewrites every file in this folder except `experiment_notes.md` and `feature_sets.json`.
