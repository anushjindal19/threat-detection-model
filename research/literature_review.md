# Literature Review

This is a working document — fill it in as you read. A few starter entries are given so
you can see the expected format; replace/expand them with your own notes.

## How to use this file

For every paper, article, or documentation page you read that shapes a decision in this
project, add an entry below with:
- What it says
- How it's relevant to this project
- The link (also add it to `references.md`)

---

## Entry 1 — The CICIDS2017 dataset paper

**Citation:** Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). *Toward
Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization.*
Proceedings of the 4th International Conference on Information Systems Security and
Privacy (ICISSP 2018).

**Link:** https://www.unb.ca/cic/datasets/ids-2017.html

**What it says (fill in after reading):**
- TODO: summarize why the authors built this dataset, and what problems they found in
  older IDS datasets (e.g. KDD99, NSL-KDD).
- TODO: summarize how the traffic was captured and labelled (tool used: CICFlowMeter).

**Relevance to this project:**
- This is the dataset we're using — cite it properly in the final report.
- Understanding *how* the flow-level features (duration, packet counts, byte counts,
  etc.) were computed helps explain what each column in the CSV actually means, for
  `feature_documentation_template.md`.

---

## Entry 2 — (your next paper/article goes here)

**Citation:**

**Link:**

**What it says:**

**Relevance to this project:**

---

## Suggested topics to look into

You don't have to read academic papers only — blog posts and official docs count too,
as long as you note where the idea came from.

- What makes a "lightweight" or "efficient" ML model, generally (model size, FLOPs,
  latency as metrics).
- Prior work specifically on lightweight/efficient intrusion detection (search terms:
  "lightweight intrusion detection", "efficient IDS machine learning", "IDS resource
  constrained").
- Why Decision Trees are considered interpretable and CPU-friendly compared to neural
  networks (see the scikit-learn Decision Trees docs in `references.md`).
- Data leakage in ML pipelines — why fitting preprocessing on the full dataset before
  splitting is a common but serious mistake (see scikit-learn's "Common pitfalls" page
  in `references.md`).

Keep entries short and honest — a two- or three-sentence summary in your own words is
more useful later than a long copy-pasted abstract.
