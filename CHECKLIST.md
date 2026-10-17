# Verification Checklist — Stages 1 through 4

Use this to confirm each stage is genuinely done before moving on. Check items off
honestly — this checklist is for you, not for show.

**Hard stop:** once every box below is checked, **stop**. Do not start training a
Decision Tree, do not start `04_baseline_model.ipynb` (it doesn't exist yet, on
purpose), and do not start the app or game. Those are separate future stages.

---

## Stage 1 — Research

- [ ] `research/research_question.md` read and understood in your own words (could you
      explain the research question out loud, without reading it?).
- [ ] `research/references.md` reviewed — you know where to find docs for pandas,
      NumPy, and scikit-learn when you need them.
- [ ] `research/literature_review.md` has at least the CICIDS2017 paper entry filled in
      (not just the template placeholder).
- [ ] `research/attack_categories.md` reviewed, and updated with descriptions for any
      label you saw in your real data that isn't already covered there.

## Stage 2 — Dataset

- [ ] Git, Python, and GitHub are all set up (`SETUP_GUIDE.md` Steps 1-5 complete), and
      this repo is pushed to your own GitHub account.
- [ ] Google Colab connected to your GitHub repo (`SETUP_GUIDE.md` Step 6).
- [ ] Exactly **one** CICIDS2017 day-file downloaded (not the whole dataset) — see
      `data/README.md`.
- [ ] `notebooks/01_dataset_exploration.ipynb` run top to bottom without errors.
- [ ] You can state, from memory or your notes: how many rows, how many columns, how
      many columns had missing values, how many had infinite values, how many duplicate
      rows, and what the class distribution looks like.
- [ ] `experiments/experiment_notes.md` has an entry recording the above.

## Stage 3 — Preprocessing

- [ ] You can explain, in your own words, why train/test split must happen before
      fitting any preprocessing step (not just recite the rule — actually explain why).
- [ ] `notebooks/02_preprocessing.ipynb` run top to bottom without errors.
- [ ] Infinite values, missing values, and duplicate rows handled, with the row-drop
      counts recorded in `experiments/experiment_notes.md`.
- [ ] Identifier columns (Flow ID, Source/Destination IP, Timestamp, etc.) removed, with
      reasoning — and this matches what's written in
      `research/feature_documentation_template.md`.
- [ ] `X_train`, `X_test`, `y_train`, `y_test` saved and reloadable.
- [ ] Class balance in `y_train` vs `y_test` checked and roughly matches (stratified
      split worked).

## Stage 4 — Feature Engineering

- [ ] `notebooks/03_FEATURE_ENGINEERING_GUIDE.md` read fully before writing any code.
- [ ] `notebooks/03_feature_engineering.ipynb` run top to bottom without errors, with
      every `TODO` cell filled in (not left as a comment-only placeholder).
- [ ] Every remaining feature assigned to a feature group (traffic volume, connection
      behavior, packet characteristics, protocol, port info, or your own group).
- [ ] A deliberate, documented decision made about new engineered features — either
      created (with reasoning) or explicitly decided against (with reasoning).
- [ ] Four feature-selection experiment sets defined (large / ~50% / most-important /
      very small), with your reasoning for what went into "most important."
- [ ] `research/feature_documentation_template.md` fully filled in — **every** surviving
      column has a Feature / Meaning / Data Type / Keep-Remove / Reason row.
- [ ] Final engineered `X_train` / `X_test` and the four feature-set lists saved
      somewhere reloadable.

## Git / GitHub hygiene (check throughout, not just at the end)

- [ ] The raw dataset CSV (and any large derived CSVs) never appear in `git status` as
      untracked-but-should-be-committed — `.gitignore` should already be handling this;
      if you ever see a `.csv` file staged with `git add .`, stop and check.
- [ ] Meaningful commits made along the way (not one giant commit at the very end) —
      e.g. "Add dataset exploration notebook," "Clean missing/infinite values," "Add
      feature documentation table."
- [ ] Everything pushed to GitHub — refresh the repository page in your browser and
      confirm the latest files are there.

---

## Once everything above is checked

Send/share the following (this mirrors what the original project roadmap asks for
before moving to model training):

1. Your GitHub repository link.
2. Which notebook(s) you want reviewed.
3. Dataset name/file used.
4. Number of rows and features (final, after cleaning).
5. Class distribution.
6. Your four feature-selection experiment sets and reasoning.
7. Any errors or problems you ran into along the way.

That review is the gate before Stage 5 (baseline Decision Tree) begins.
