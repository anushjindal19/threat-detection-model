# Feature Engineering Guide — Stage 4

**This stage is yours to code.** Notebooks 1 and 2 gave you fully worked code because
they're mostly mechanical (inspect this, drop that). Feature engineering is where real
modelling judgment starts, and that judgment is the actual skill this project is meant
to build. So instead of a solved notebook, this is a **guide**: what to do, in what
order, why, and where to look — you write the code in
`notebooks/03_feature_engineering.ipynb`, which has the section headers and a few
starter/loading cells already in place for you.

Don't rush this stage. Understanding *why* a feature might matter is more valuable here
than getting through it quickly.

---

## Before you start

Make sure you have, from Notebook 2:
- `X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv` saved somewhere you can load
  them from (in `data/`, or your Colab session/Drive).
- A completed (or mostly completed) `research/feature_documentation_template.md` listing
  every remaining column, its meaning, and your keep/remove reasoning.

If you don't have those yet, go finish `02_preprocessing.ipynb` first — this stage
builds directly on it.

---

## Step 1 — Load your cleaned, split data

In `03_feature_engineering.ipynb`, load the four CSVs from Notebook 2. This part is just
`pd.read_csv(...)` four times — same pattern you've already used twice. No new syntax
needed; look back at Notebook 2, Step 9 if you forget the filenames you saved.

**Checkpoint:** print `X_train.shape` and `X_test.shape` and confirm they match what you
recorded at the end of Notebook 2.

---

## Step 2 — Group your remaining features by what they describe

The roadmap for this project suggests these feature groups (from your CICIDS2017 file —
**confirm which of these actually exist as columns in your data; don't assume**):

- **Traffic volume** — total packets, total bytes, bytes/sec, packets/sec
- **Connection behavior** — flow duration, number/frequency of connections
- **Packet characteristics** — average packet size, packet length statistics (min/max/std)
- **Protocol** — TCP / UDP / ICMP / etc.
- **Port information** — source port, destination port

**Your task:** go through `df.columns` (or `X_train.columns`) and sort every remaining
column into one of these groups (or a group of your own, if a column doesn't fit). A
simple way to do this in code:

```python
# Example of the KIND of structure you're building — not a complete answer.
# You need to fill in the actual column names from YOUR dataset.
feature_groups = {
    "traffic_volume": [...],
    "connection_behavior": [...],
    "packet_characteristics": [...],
    "protocol": [...],
    "port_info": [...],
}
```

**Why this matters:** later, when you experiment with using fewer features (Step 4), it's
much easier to reason about "what happens if I drop the packet-characteristics group"
than to think about 70+ individual column names.

**Resource:** if a column name is unclear, search for it in the CICIDS2017 paper's
feature list (linked in `research/references.md`) or in CICFlowMeter's documentation
(the tool that generated these columns) — https://www.unb.ca/cic/research/applications.html
lists CICFlowMeter along with the dataset.

---

## Step 3 — Decide if any *new* features are worth engineering

"Feature engineering" doesn't only mean selecting existing columns — it can mean
*creating* new ones from existing ones, if that would capture something the raw columns
don't directly express. You don't have to do this, but it's worth genuinely considering
for at least one or two ideas, and writing down why you did or didn't pursue them.

Some questions to think about (not instructions to blindly implement):
- Is there a ratio between two existing columns that might be more informative than
  either column alone? (e.g. forward packets vs. backward packets — a very lopsided
  ratio might indicate a scan or flood rather than a real conversation)
- Could a port number be more useful as a *category* (well-known service vs. random
  ephemeral port) than as a raw number? A raw port number like `54231` vs `80` isn't
  meaningfully "bigger" in a way a Decision Tree needs — but Decision Trees can split on
  raw numeric thresholds fine, so think about whether this transformation actually adds
  information or is unnecessary for this specific model type.
- Are there near-duplicate columns (e.g. a "mean" and a "total" that are almost
  perfectly correlated) where keeping both adds size without adding information?

**If you create a new feature:** add it to both `X_train` and `X_test` using the exact
same formula (never compute it using statistics from the full combined dataset — same
leakage rule as before). Document it in `feature_documentation_template.md` just like any
other feature.

**It's completely fine to conclude "the existing columns are already good/behavioural
enough, no new features needed" — that's a valid, defensible outcome, not a cop-out, as
long as you explain your reasoning.**

---

## Step 4 — Set up the feature-selection experiment groups

This is the core of Stage 4's research value: instead of jumping straight to "use all
features" or "use 5 features" by gut feeling, define a few concrete feature sets to
compare later (comparison itself happens once you train models in the *next* stage,
which is out of scope for this repo — you're just *preparing* the sets now):

- **Experiment A** — a large feature set (most/all remaining columns)
- **Experiment B** — roughly 50% of the features
- **Experiment C** — only the features you judge most important
- **Experiment D** — a very small feature set (a handful of the most essential columns)

**How to decide what's "most important" for Experiments C and D**, a few valid
approaches (pick one, or combine, and document which you used):
1. **Domain reasoning** — based on your feature-group analysis in Step 2 and your
   understanding of the attack categories, which groups seem most likely to
   discriminate attacks from benign traffic?
2. **A quick statistical check** — scikit-learn has tools for this that you can run on
   `X_train`/`y_train` only (never on test data) to get a data-driven starting point.
   Look up: `sklearn.feature_selection` — https://scikit-learn.org/stable/modules/feature_selection.html
   (in particular, mutual information or a quick tree-based feature-importance
   estimate). You don't need to master this fully — reading that page and trying one
   function is enough for this stage.
3. **Correlation with the label** — for numeric features, you can look at how strongly
   each one separates BENIGN from attack rows using groupby/describe comparisons.

**What to save:** for each experiment (A-D), a simple Python list of column names,
something like:

```python
experiment_A_features = [...]  # large set
experiment_B_features = [...]  # ~50%
experiment_C_features = [...]  # most important, your judgment
experiment_D_features = [...]  # very small set
```

You are **not** training or scoring models against these yet — that's Stage 5 (baseline
model), which this repo intentionally stops before. You're just producing the *candidate*
feature sets so that stage can use them directly.

---

## Step 5 — Finish the feature documentation table

Go back to `research/feature_documentation_template.md` and make sure **every** column
that survived preprocessing has a row: its meaning, data type, which feature group it's
in, and (informed by Step 4) roughly how "essential" you consider it. This table is one
of the required deliverables for this stage — it should be complete and readable by
someone who has never seen this dataset.

---

## Step 6 — Save your engineered feature sets

Save whatever you produced so the next stage (baseline model — **not** part of this
repo yet) can pick up directly:

- The full engineered `X_train` / `X_test` (with any new features from Step 3 added).
- The four feature-set lists from Step 4 (Experiments A-D), e.g. as a small JSON or a
  Python dict saved with `pickle`/`joblib`, or even just documented as plain lists in a
  markdown file — whatever's easiest for you to reload correctly later. Consistency
  matters more than the format.

**Do not train a Decision Tree (or any model) in this notebook.** That's the very next
stage, and it's deliberately out of scope here — see `CHECKLIST.md` and the root
`README.md` for why.

---

## Resources for this stage

| Resource | Link |
|---|---|
| scikit-learn — Feature selection | https://scikit-learn.org/stable/modules/feature_selection.html |
| scikit-learn — Preprocessing data | https://scikit-learn.org/stable/modules/preprocessing.html |
| pandas — groupby (useful for comparing feature values across BENIGN vs attack rows) | https://pandas.pydata.org/docs/user_guide/groupby.html |
| CICIDS2017 official page (feature descriptions, via the linked paper) | https://www.unb.ca/cic/datasets/ids-2017.html |
| Original CICIDS2017 paper (see `research/literature_review.md` for the full citation) | linked from the page above |

---

## When you're done — checkpoint before you stop

Before you consider Stage 4 complete, you should be able to point to:

- [ ] `notebooks/03_feature_engineering.ipynb` loading the cleaned train/test data and
      running without errors.
- [ ] Every remaining column assigned to a feature group (Step 2).
- [ ] A documented decision (even if "none") on new engineered features (Step 3).
- [ ] Four defined feature-set lists for Experiments A-D (Step 4).
- [ ] `research/feature_documentation_template.md` fully filled in (Step 5).
- [ ] Engineered data + feature-set lists saved somewhere reloadable (Step 6).

Then check the rest off in `CHECKLIST.md`. **Stop there.** Training the baseline
Decision Tree is the next stage, on purpose not covered here — see the root
`README.md` for why.
