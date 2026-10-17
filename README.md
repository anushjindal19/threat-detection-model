# Lightweight Cybersecurity Threat Detector

A research project that trains a small, fast machine-learning model to classify network
activity as **Normal**, **Suspicious**, or **Malicious/Attack**, using the public
**CICIDS2017** dataset.

**Research question:**
> How much detection performance can be retained while reducing the computational,
> memory, and model-size requirements of a machine-learning-based cybersecurity threat
> detector?

Author: Anush Jindal

---

## New here? Start with WELCOME.md

If you have never used Git, GitHub, Python, or Google Colab before, do not start with this
README — start with **[WELCOME.md](WELCOME.md)**. It's a short, friendly orientation to
every tool involved (especially Google Colab, where you'll do almost all your work), with
every official link in one place.

Need more depth on any step — exact commands, troubleshooting? That's
**[SETUP_GUIDE.md](SETUP_GUIDE.md)**.

Not sure what you should be working on right now vs. later? That's
**[FOLLOW_OR_DEFER.md](FOLLOW_OR_DEFER.md)** — a one-page compass: exactly what to do
next, in order, and an explicit list of what to deliberately leave alone for now.

Once your environment is set up, come back here for the project map.

---

## Where this project is right now

This repo currently covers **Stage 1 → Stage 4** of the full project plan:

| Stage | Name | Status |
|---|---|---|
| 1 | Research | Templates ready in `research/` — fill in as you learn |
| 2 | Dataset | Guide + notebook ready — `notebooks/01_dataset_exploration.ipynb` |
| 3 | Preprocessing | Guide + notebook ready — `notebooks/02_preprocessing.ipynb` |
| 4 | Feature Engineering | **You write this one** — see `notebooks/03_FEATURE_ENGINEERING_GUIDE.md` |
| 5+ | Baseline model, optimization, benchmarking, app/game | **Not started on purpose** — see note below |

**We deliberately stop before training the first model.** The point of Stages 1-4 is to
fully understand and prepare the data. Only once that is solid (and reviewed) do we move
on to training a Decision Tree baseline. Jumping ahead defeats the point of the exercise —
you would be tuning a model on data you don't actually understand yet.

Use **[CHECKLIST.md](CHECKLIST.md)** to confirm each stage is genuinely done before moving
to the next one.

---

## Folder structure

```
anush/
├── README.md                          ← you are here
├── WELCOME.md                         ← friendly orientation to every tool, especially Colab
├── SETUP_GUIDE.md                     ← detailed step-by-step setup, exact commands + troubleshooting
├── FOLLOW_OR_DEFER.md                 ← what to do now vs. deliberately not yet
├── CHECKLIST.md                       ← verification checklist for Stages 1-4
├── setup.bat                          ← one-click local environment setup (Windows)
├── requirements.txt                   ← Python libraries this project needs
├── .gitignore                         ← tells Git which files NOT to track (e.g. raw data)
│
├── research/
│   ├── research_question.md           ← the research question, spelled out
│   ├── literature_review.md           ← template — fill in as you read about IDS/ML
│   ├── references.md                  ← every official link you need, in one place
│   ├── attack_categories.md           ← what each CICIDS2017 attack type actually means
│   └── feature_documentation_template.md  ← Feature | Meaning | Type | Keep/Remove | Reason
│
├── notebooks/
│   ├── 00_welcome_and_resources.ipynb ← open this first in Colab — links + environment check
│   ├── 01_dataset_exploration.ipynb   ← load the data, inspect it, understand it
│   ├── 02_preprocessing.ipynb         ← clean it, split it safely (no data leakage)
│   ├── 03_feature_engineering.ipynb   ← SKELETON — you fill this in
│   ├── 03_FEATURE_ENGINEERING_GUIDE.md ← step-by-step instructions + resources for the above
│   └── PIPELINE_CHEATSHEET.ipynb      ← quick-reference: what to call and why, no solved code
│
├── data/
│   └── README.md                      ← which CICIDS2017 file to use + where to get it
│                                         (the actual .csv file is NEVER committed to GitHub)
│
├── models/                            ← trained models get saved here (not committed yet)
│
└── experiments/
    ├── results.csv                    ← one row per experiment (empty template for now)
    └── experiment_notes.md            ← your running notes on what you tried and why
```

`src/`, `app/`, `game/` are intentionally **not created yet** — they belong to later stages
(model training, optimization, and the application/game) and we don't want empty,
meaningless folders cluttering the repo before there's real code to put in them.

---

## The full pipeline (for context)

```
Public Cybersecurity Dataset → Data Understanding → Preprocessing → Feature Engineering
   → Baseline ML Model → Lightweight Model Optimization → Resource Benchmarking
   → Application/Game → Research Analysis
```

We are working on the first four boxes. Everything after "Feature Engineering" is future
work — do not start it yet (see `CHECKLIST.md`).

## Hardware note

Stages 1-4 (everything in this repo right now — research, dataset exploration,
preprocessing, feature engineering) need no GPU at all; free CPU-only Google Colab is
plenty.

**Update:** for Stage 5+ (baseline model and beyond, not started yet), this project will
use GPU-capable models instead of a CPU-only Decision Tree baseline. When you get there,
enable a GPU in Colab: **Runtime → Change runtime type → Hardware accelerator → GPU (T4)**.
See the "Update" note in `research/research_question.md` for what this means for the
research framing.
