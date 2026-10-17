# Follow Now vs. Defer — Read This Before You Start Any Session

A one-page compass for the whole project. When in doubt about "should I be doing this
right now," check here first.

---

## ✅ FOLLOW NOW — in this exact order

1. **`WELCOME.md`** — tools + all links (do this once).
2. **`notebooks/00_welcome_and_resources.ipynb`** — open in Colab, run the environment
   check cell, confirm it prints "Environment ready."
3. **`data/README.md`** — download **one** CICIDS2017 day-file (not the whole dataset).
4. **`notebooks/01_dataset_exploration.ipynb`** — run it top to bottom. If a cell errors
   (e.g. `df.columns` looks wrong), stop and diagnose before moving on — don't skip past
   an error by guessing.
5. **`research/attack_categories.md`** — read + update with any label you saw that isn't
   already listed.
6. **`notebooks/02_preprocessing.ipynb`** — run it top to bottom.
7. **`research/feature_documentation_template.md`** — fill in every remaining column.
8. **`notebooks/03_FEATURE_ENGINEERING_GUIDE.md`** — read the whole guide first.
9. **`notebooks/03_feature_engineering.ipynb`** — write the code yourself, following the
   guide. This one is yours — no solved version exists on purpose.
10. **`CHECKLIST.md`** — go through every box honestly before telling anyone this stage
    is "done."

If you're ever unsure what to open next, this numbered list is the answer.

---

## 🛑 DEFER — do not start these yet

These are real parts of the eventual project. None of them are cancelled. They are just
**not next** — starting them now means building on data/features you haven't actually
finished understanding yet, which wastes the work.

- ❌ Training a Decision Tree or any other model (`04_baseline_model.ipynb` doesn't
  exist yet — on purpose).
- ❌ Model optimization / pruning experiments (`max_depth`, `ccp_alpha`, etc.) — that's
  after a baseline exists.
- ❌ Resource benchmarking (model size, latency, RAM) — nothing to benchmark yet.
- ❌ The Streamlit dashboard or the React/FastAPI game (`app/`, `game/` folders don't
  exist yet — on purpose).
- ❌ Deep learning / neural networks — even with the GPU-model decision noted in
  `research/research_question.md`, that's a Stage 5 planning conversation, not something
  to just start coding.
- ❌ Downloading the full CICIDS2017 dataset (all 5 days) — one file is enough for
  Stages 1-4.
- ❌ Writing the final research report / paper sections (Abstract, Results, Discussion,
  etc.) — there are no real results yet to report.
- ❌ Inventing or guessing numbers for `experiments/results.csv` — every row must come
  from something you actually ran.

**Why this matters:** the original project roadmap is explicit that skipping ahead
"defeats the point of the exercise." A model trained on data you don't understand, or
features you didn't reason through, produces numbers that look fine but that you can't
actually explain or defend — which is the opposite of what this project is for.

---

## If you think you're ready to defer-list something

That's a real conversation to have, not a unilateral call — flag it (to whoever is
reviewing this project with you) with what you've completed from the "Follow now" list
and why you think the next stage is ready to start. `CHECKLIST.md` fully checked is the
evidence for that conversation.
