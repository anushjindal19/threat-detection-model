# What is in `experiments/`

Every number in this folder came from actually running a notebook. Nothing is estimated
or typed in by hand. If a number is not measured yet, the cell is left empty.

| File | What it is | Made by |
|---|---|---|
| `results.csv` | One row per experiment, with all the main numbers (see the column guide below) | Notebook 4, Step 7 (Step 9b adds `ram_mb`) |
| `experiment_notes.md` | Dated log of what was done, what was seen, what went wrong and what was decided. Every row in `results.csv` can be traced to an entry here. | Written by hand after each session |
| `feature_sets.json` | The four feature lists A (58), B (39), C (15), D (6) | Notebook 3, Step 6 |
| `S5_scores_without_heartbleed.csv` | Macro F1 with and without Heartbleed, weighted F1, attack recall, and how many of the 2 Heartbleed test rows were caught | Notebook 4, Step 9a |
| `S5_memory.csv` | Memory for each tree: the tree itself, the extra memory to classify 1,000 flows, and the total | Notebook 4, Step 9b |
| `S5_per_class_recall.csv` | For each class (BENIGN and each attack), the share of its test rows the model got right, for every run. `test rows` shows how many rows each number is based on. | Notebook 4, Step 7 |

The three `S5_*.csv` files are from the 23-10-2026 run, which still used the **old
57-feature list A**. Their `A`, `A_no_port` and `A_no_port_no_window` values will change
after notebooks 3 and 4 are re-run with the new list A (58 features).

## Column guide for `results.csv`

| Column | Meaning |
|---|---|
| `experiment_id` | Name of the run. `S5` = Stage 5 (baseline). `-v1` = made with the old 57-feature list A. |
| `date` | Day the run was done |
| `stage` | Project stage (`5-baseline` = untuned decision tree) |
| `dataset_file` | Which CICIDS2017 file was used |
| `num_samples` | Training rows + test rows (488,393 + 122,099 = 610,492) |
| `num_features` | How many features the tree was allowed to use |
| `features_used` | Which feature list (A, B, C, D, or a list with the shortcut features removed) |
| `max_depth` | How deep the tree grew. It was **not** set by us: the tree was untuned. |
| `num_nodes` | How many questions and answers the tree has (its size) |
| `accuracy` | Share of all test rows labelled correctly. Looks high because most rows are BENIGN, so don't rely on it alone. |
| `precision`, `recall`, `f1` | Macro averages: every class counts equally, including Heartbleed (only 2 test rows). Use `S5_scores_without_heartbleed.csv` to compare runs. |
| `model_size_kb` | Size of the saved tree file |
| `training_time_s` | Seconds to train the tree. Only comparable between runs from the same session. |
| `inference_ms` | Milliseconds to classify **1,000** test flows (median of 5 tries) |
| `ram_mb` | Memory in MB: the tree itself plus the peak extra memory to classify 1,000 flows. Does not include Python or scikit-learn. |
| `notes` | Settings used, plus attack recall, missed attacks and false alarms |

## After re-running notebooks 3 and 4

Step 9b prints 8 rows. Replace **all** rows in `results.csv` with them, which also
removes the `-v1` rows. Then copy the new Step 9 CSVs over the ones here, and add an
entry to `experiment_notes.md` saying what changed for list A.
