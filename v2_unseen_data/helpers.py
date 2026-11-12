"""Shared code for the v2 notebooks.

Every v2 notebook starts with `from helpers import *`-style imports from this file, so the
same cleaning, the same splits and the same scoring are used everywhere.

Sections:
  1. Paths and settings
  2. Loading and cleaning the eight CICIDS2017 files
  3. Splitting by time order instead of at random
  4. Growing one tree and reading it at every size
  5. Scoring
"""
import copy
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# --------------------------------------------------------------------------------------
# 1. Paths and settings
# --------------------------------------------------------------------------------------
V2_DIR = Path(__file__).resolve().parent                 # .../v2_unseen_data
REPO_DIR = V2_DIR.parent
DATA_DIR = Path(os.environ.get("DATA_DIR", REPO_DIR / "data"))   # the raw CSV files go here
RESULTS_DIR = V2_DIR / "results"
FIG_DIR = RESULTS_DIR / "figures"
CLEAN_FILE = DATA_DIR / "all_days_clean.pkl"             # written by notebook 02

# (day, file name) in the order the traffic was recorded, 3 to 7 July 2017
DAY_FILES = [
    ("Monday", "Monday-WorkingHours.pcap_ISCX.csv"),
    ("Tuesday", "Tuesday-WorkingHours.pcap_ISCX.csv"),
    ("Wednesday", "Wednesday-workingHours.pcap_ISCX.csv"),
    ("Thursday", "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv"),
    ("Thursday", "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv"),
    ("Friday", "Friday-WorkingHours-Morning.pcap_ISCX.csv"),
    ("Friday", "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"),
    ("Friday", "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"),
]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
BENIGN = "BENIGN"

# The three features v1 found to be shortcuts: they describe the lab, not the attack.
SHORTCUT_FEATURES = ["Destination Port", "Init_Win_bytes_forward", "Init_Win_bytes_backward"]

DEPTHS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, None]     # None = no limit
PRUNING_STRENGTHS = [1e-7, 3e-7, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2]
SEED = 42

# How each flow is assigned to train / validation / test when splitting by time order
TRAIN_SHARE, VALIDATION_SHARE = 0.60, 0.20               # the last 20% is the test part


def load_feature_lists():
    """The four v2 feature lists: v1's lists A-D without the three shortcut features."""
    with open(V2_DIR / "feature_lists.json") as f:
        return json.load(f)


# --------------------------------------------------------------------------------------
# 2. Loading and cleaning
# --------------------------------------------------------------------------------------
def load_clean(path, verbose=True):
    """Read one CICIDS2017 CSV and clean it exactly like v1 (notebook 02):
    strip column names, drop rows with infinite values, missing values, exact duplicates.
    The rows stay in file order, which is the order the flows were recorded in blocks."""
    df = pd.read_csv(path, encoding="latin1", low_memory=False)
    df.columns = df.columns.str.strip()
    n_raw = len(df)
    numeric = df.select_dtypes(include=np.number).columns
    df = df[~np.isinf(df[numeric]).any(axis=1)]
    n_inf = n_raw - len(df)
    n = len(df)
    df = df.dropna()
    n_missing = n - len(df)
    n = len(df)
    df = df.drop_duplicates()
    n_dup = n - len(df)
    # Tidy the labels: remove spaces, and the broken dash character in "Web Attack ..."
    df["Label"] = (df["Label"].str.strip()
                   .str.replace(r"Web Attack\s+\S+\s+", "Web Attack - ", regex=True))
    counts = {"rows_raw": n_raw, "infinite_removed": n_inf, "missing_removed": n_missing,
              "duplicates_removed": n_dup, "rows_clean": len(df)}
    if verbose:
        print(f"{Path(path).name}: {n_raw:,} -> {len(df):,} rows")
    return df.reset_index(drop=True), counts


def load_all_days():
    """The cleaned data of all eight files in one table (made by notebook 02)."""
    if not CLEAN_FILE.exists():
        raise FileNotFoundError(f"{CLEAN_FILE} not found: run notebook 02 first.")
    return pd.read_pickle(CLEAN_FILE)


# --------------------------------------------------------------------------------------
# 3. Splitting by time order
# --------------------------------------------------------------------------------------
def time_position(df, group_columns):
    """For every row: how far through its own group it sits, from 0 (first) to 1 (last).
    A group is, for example, all 'DoS Hulk' rows of the Wednesday file, in file order."""
    grouped = df.groupby(group_columns, sort=False)
    return (grouped.cumcount() / grouped[group_columns[0]].transform("size")).to_numpy()


def time_parts(df, group_columns=("file", "Label")):
    """Label every row 'train', 'validation' or 'test' by time order:
    the first 60% of each group is train, the next 20% validation, the last 20% test."""
    pos = time_position(df, list(group_columns))
    return np.where(pos < TRAIN_SHARE, "train",
                    np.where(pos < TRAIN_SHARE + VALIDATION_SHARE, "validation", "test"))


# --------------------------------------------------------------------------------------
# 4. Growing one tree and reading it at every size
# --------------------------------------------------------------------------------------
def grow_tree(X, y):
    """One full-size decision tree with scikit-learn's default settings (same as v1)."""
    return DecisionTreeClassifier(random_state=SEED).fit(X, y)


def node_depths(model):
    """Depth of every node in the tree (the top question is depth 0)."""
    t = model.tree_
    depth = np.zeros(t.node_count, dtype=np.int32)
    for node in range(t.node_count):          # parents always come before their children
        for child in (t.children_left[node], t.children_right[node]):
            if child != -1:
                depth[child] = depth[node] + 1
    return depth


def predict_at_depths(model, X, depths=DEPTHS):
    """Classify X with the tree cut off at each depth in `depths`.

    A tree is grown from the top down, so the top d levels of a full tree are a depth-d
    tree. It differs from re-training with max_depth=d only where two questions were
    equally good and the tie was broken differently (measured in notebook 03: the two
    agree on more than 99.5% of flows). One grown tree therefore gives every depth limit.

    Returns {depth: (predictions, average comparisons per flow)}.
    """
    t = model.tree_
    answer_at_node = t.value[:, 0, :].argmax(axis=1)
    node = np.zeros(len(X), dtype=np.int64)       # every flow starts at the top question
    rows = np.arange(len(X))
    comparisons = 0                                # total questions asked so far
    wanted = sorted(d for d in depths if d is not None)
    out = {}
    step = 0
    while True:
        if step in wanted:
            out[step] = (model.classes_[answer_at_node[node]], comparisons / len(X))
        active = t.children_left[node] != -1      # flows that have not reached an answer
        if not active.any():
            break
        r, nd = rows[active], node[active]
        go_left = X[r, t.feature[nd]] <= t.threshold[nd]
        node[r] = np.where(go_left, t.children_left[nd], t.children_right[nd])
        comparisons += int(active.sum())
        step += 1
    final = (model.classes_[answer_at_node[node]], comparisons / len(X))
    for d in depths:
        if d is None or d not in out:             # no limit, or a limit deeper than the tree
            out[d] = final
    return out


def nodes_at_depth(depth_of_node, d):
    """Number of nodes left when the tree is cut at depth d (None = whole tree)."""
    return int(len(depth_of_node) if d is None else (depth_of_node <= d).sum())


def prune(model, strength):
    """Cost-complexity pruning of an already grown tree. Gives the same tree as training
    with ccp_alpha=strength (checked in notebook 03) without growing it again."""
    pruned = copy.deepcopy(model)
    pruned.ccp_alpha = strength
    pruned._prune_tree()
    return pruned


def compact_kb(n_nodes):
    """Size of the tree stored as plain arrays, as on a small device (same rule as v1):
    per node a 1-byte feature number, a 4-byte threshold and two child numbers."""
    index_bytes = 2 if n_nodes <= 65535 else 4
    return n_nodes * (1 + 4 + 2 * index_bytes) / 1024


# --------------------------------------------------------------------------------------
# 5. Scoring
# --------------------------------------------------------------------------------------
def score(said_attack, labels, unseen_attacks=()):
    """Score attack-vs-normal predictions.

    said_attack    : True where the tree called the flow an attack
    labels         : the original label of every flow (BENIGN or the attack's name)
    unseen_attacks : attack names the tree never saw in training

    Returns (summary, per_attack):
      summary    one dict: false-alarm rate, and recall for seen and for unseen attacks,
                 both pooled (all flows together) and averaged per attack type
      per_attack one dict per attack type in `labels`
    """
    labels = np.asarray(labels)
    said_attack = np.asarray(said_attack, dtype=bool)
    benign = labels == BENIGN
    per_attack = []
    for name in sorted(set(labels[~benign])):
        mine = labels == name
        per_attack.append({"attack": name, "seen_in_training": name not in unseen_attacks,
                           "rows": int(mine.sum()), "caught": int(said_attack[mine].sum()),
                           "recall": float(said_attack[mine].mean())})
    summary = {"benign_rows": int(benign.sum()),
               "false_alarms": int(said_attack[benign].sum()),
               "false_alarm_rate": float(said_attack[benign].mean()) if benign.any() else np.nan}
    for kind, flag in (("seen", True), ("unseen", False)):
        group = [a for a in per_attack if a["seen_in_training"] == flag]
        rows = sum(a["rows"] for a in group)
        summary[f"{kind}_attack_rows"] = rows
        summary[f"{kind}_attack_recall"] = sum(a["caught"] for a in group) / rows if rows else np.nan
        summary[f"{kind}_recall_per_attack_mean"] = (
            float(np.mean([a["recall"] for a in group])) if group else np.nan)
    return summary, per_attack
