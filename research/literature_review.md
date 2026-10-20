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

> **Entries 2–7 were added on 20 Oct 2026.** They are first-pass summaries drafted with
> Claude from each paper and its abstract. Read at least the abstract, method and results
> of each paper yourself before you cite it, and rewrite these notes in your own words as
> you go.

## Entry 2 — The CICIDS2017 dataset has serious construction and labelling errors

**Citation:** Engelen, G., Rimmer, V., & Joosen, W. (2021). *Troubleshooting an Intrusion
Detection Dataset: the CICIDS2017 Case Study.* 2021 IEEE Security and Privacy Workshops
(SPW / WTMC).

**Link:** https://lirias.kuleuven.be/retrieve/713070

**What it says:**
- CICFlowMeter, the tool that turned the raw traffic into the CSV rows we use, ends a TCP
  flow at the first FIN packet. The leftover packets then become separate "appendix"
  flows that carry the same label. These appendix flows are **25.9%** of the dataset.
- Labels were assigned by IP address and time window only, and nobody checked whether a
  flow actually carried an attack. Many "attack" flows are failed or empty connections.
- The authors fixed the tool, regenerated the dataset from the original PCAPs, and added an
  **"Attempted"** label for attack flows with no meaningful payload. That relabelled
  447,362 flows. Some classes nearly vanish: Web XSS goes from 679 to 27 flows, and Web
  Brute Force from 1,365 to 151.

**How they did it:**
- They audited the pipeline stage by stage: attack simulation, then flow construction,
  then labelling, then feature extraction.
- They trained a Random Forest on the original, partly fixed and fully fixed versions,
  and compared **per-class F1 and feature importances**, not just overall accuracy.
- Key finding: overall accuracy stayed at **0.99** on every version, while per-class
  scores swung wildly. For example, XSS F1 went from 0.18 to 0.79. On the original data,
  the model was partly using flow-construction artifacts (header length, `Init_Win_bytes`,
  RST flags) as shortcuts.

**Relevance to this project:**
- Our data is CICIDS2017 Wednesday (DoS), so these errors affect our data directly.
  Report per-class recall/F1, not just accuracy.
- Their shortcut finding supports the "shortcut or behaviour?" check in notebook 4, Step
  6. `Init_Win_bytes` appears in both.
- Their corrected dataset could serve as a second test set.

---

## Entry 3 — Ten common mistakes in machine learning for security

**Citation:** Arp, D., Quiring, E., Pendlebury, F., Warnecke, A., Pierazzi, F., Wressnegger,
C., Cavallaro, L., & Rieck, K. (2022). *Dos and Don'ts of Machine Learning in Computer
Security.* USENIX Security Symposium 2022.

**Link:** https://arxiv.org/abs/2010.09470

**What it says:**
- Names 10 pitfalls across the ML workflow: sampling bias, label inaccuracy, data
  snooping, spurious correlations, biased parameter selection, inappropriate baseline,
  inappropriate performance measures, base-rate fallacy, lab-only evaluation, and
  inappropriate threat model.
- Every one of the 30 papers reviewed had at least 3 of these pitfalls. Sampling bias
  appeared in 90% of them and data snooping in 73%.

**How they did it:**
- **Prevalence study:** 30 papers from the four top security venues (CCS, S&P, USENIX
  Security, NDSS) over 10 years. Each paper was rated by two independent reviewers, with a
  third reviewer to settle disagreements.
- **Four case studies** reproduce published systems and show each pitfall changing the
  results. The intrusion-detection case study is the important one for us: on the Mirai
  data, a simple **boxplot rule on packet frequency** (AUC 0.998) **beat Kitsune** (AUC
  0.968, see Entry 7). The lesson is that a simple baseline can beat a complex model,
  because the lab attack was too easy to spot.

**Relevance to this project:**
- Use it as a checklist for our methodology section. We need a simple baseline (for
  example, a depth-1 tree or a single-feature rule), and we must not tune
  hyperparameters on the test set.
- The "spurious correlations" pitfall is the same as the shortcut issue in Entry 2.

---

## Entry 4 — Compression hurts rare and unusual examples first

**Citation:** Hooker, S., Courville, A., Clark, G., Dauphin, Y., & Frome, A. (2019). *What Do
Compressed Deep Neural Networks Forget?* arXiv:1911.05248.

**Link:** https://arxiv.org/abs/1911.05248

**What it says:**
- Overall accuracy barely changes when a model is compressed, but the losses are **not
  spread evenly**. They concentrate on a small set of atypical, hard or rare examples.
- On ImageNet, 90% pruning cost only about 4 points of top-1 accuracy (76.7 → 72.6). The
  number of classes that were significantly affected, however, rose from 68 at 30%
  pruning to 637 at 90%.

**How they did it:**
- They trained **populations of 30 models** at each pruning level (30% to 90% sparsity)
  and also tested post-training quantization. Using many models separates real effects
  from random seed noise.
- They defined **Pruning Identified Exemplars (PIEs)**: test examples where the most
  common prediction of the pruned models differs from that of the unpruned models.
- The uncompressed model was already much worse on PIEs (about 40% accuracy against 81%
  on everything else). A human study found that PIEs are more often mislabelled,
  fine-grained or ambiguous.

**Relevance to this project:**
- This is the template for idea 1, "what do compressed intrusion detectors forget?". Swap
  ImageNet classes for attack classes and neural network pruning for tree depth or leaf
  limits.
- Copy the method: several seeds per size, per-class metrics, and a check of whether the
  lost examples are the rare classes (for example, Heartbleed or Slowloris on our day).
- Note the difference: they studied deep networks on images. Nobody seems to have done
  this cleanly for small trees on IDS data, and that gap is our opening.

---

## Entry 5 — Near-perfect within a dataset, close to random across datasets

**Citation:** Cantone, M., Marrocco, C., & Bria, A. (2024). *On the Cross-Dataset
Generalization of Machine Learning for Network Intrusion Detection.* Journal of Information
Security and Applications.

**Link:** https://arxiv.org/abs/2402.10974

**What it says:**
- Models trained and tested on the same dataset averaged **94.6% MCC**. Trained on one
  dataset and tested on another, they averaged **29.4% MCC**.
- No classifier generalized any single attack across every train/test pair. DoS
  Slowhttptest and the web attacks never went above 50% MCC.

**How they did it:**
- They used four datasets: CIC-IDS2017, CSE-CIC-IDS2018, and corrected re-extractions of
  each (LycoS-IDS2017 and their own LycoS-Unicas-IDS2018).
- They harmonized features by dropping identifiers (IPs, ports, Flow ID, timestamp),
  scaled all features to [0, 1], and used mostly binary labels.
- Models were LDA, Decision Tree, Random Forest and XGBoost, scored with MCC, F1 and
  AUROC. They did not use accuracy because of class imbalance.
- To explain the failures, they plotted the distributions of the top features for each
  attack in each dataset. The same attack tool often produced completely different feature
  values (likely different tool settings), and many attacks had very few unique rows.
- In 11 of 16 cross-dataset settings, the best results came from only 3–5 features.

**Relevance to this project:**
- Our ~99% scores on one Wednesday file probably won't hold elsewhere. Say so in the
  paper's limitations section.
- Their finding that a few features generalize best fits our feature sets C and D (15
  and 6 features). This is the basis for idea 3, "does a smaller tree transfer better?".
- Their choice of metrics (MCC, F1, AUROC) is a good model to follow.

---

## Entry 6 — Fitting decision trees into network switches under hard limits

**Citation:** Zheng, C., Zang, M., Hong, X., Perreault, L., Bensoussane, R., Vargaftik, S.,
Ben-Itzhak, Y., & Zilberman, N. (2024). *Planter: Rapid Prototyping of In-Network Machine
Learning Inference.* ACM SIGCOMM Computer Communication Review (Jan 2024).

**Link:** https://eng.ox.ac.uk/media/zetja3ek/zheng24planter.pdf

**What it says:**
- Planter is an open-source framework. It takes a trained model (Decision Tree, Random
  Forest, XGBoost, SVM, k-means, Naive Bayes and others), converts it into the
  match-action tables that a programmable switch runs, and tests it on real hardware.
- Here "lightweight" is a hard limit, not a preference: a switch has a fixed number of
  pipeline stages and table entries, and a model that exceeds them cannot run at all.

**How they did it:**
- It offers three ways to map a model onto the switch. Direct mapping turns each tree
  level into a pipeline stage, so deeper trees need more stages. Encode-based mapping
  turns features into codes and then looks up the answer, so the stage count stays flat
  as the tree grows. Lookup-based mapping precomputes results in tables.
- They tested on real targets: Intel Tofino switches, an FPGA, a SmartNIC and a Raspberry
  Pi (P4Pi). Use cases included CICIDS2017 and UNSW-NB15.
- Results: models that fit run at full switch speed (6.4 Tbps on Tofino) and match the
  accuracy of the same model in scikit-learn. Resource use (stages and table entries)
  depends on tree depth, number of trees and number of features.

**Relevance to this project:**
- It answers the stalled "breaking point" idea's problem of having no real budget: switch
  stages and table entries are real budgets. Report results as "the best tree that fits
  in N stages / M entries" instead of an arbitrary cutoff.
- It uses our dataset (CICIDS2017), so cite it as prior work on small trees under
  hardware limits.

---

## Entry 7 — A lightweight online IDS that runs on a Raspberry Pi

**Citation:** Mirsky, Y., Doitshman, T., Elovici, Y., & Shabtai, A. (2018). *Kitsune: An
Ensemble of Autoencoders for Online Network Intrusion Detection.* NDSS 2018.

**Link:** https://arxiv.org/abs/1802.09089

**What it says:**
- An **unsupervised, online** intrusion detector built for cheap devices such as routers.
  It needs no labels: it learns what normal traffic looks like and flags anything that
  looks different.
- It ran in real time on a **Raspberry Pi 3B** (single core), at about 5,400 packets per
  second.

**How they did it:**
- **Streaming feature extractor:** it keeps damped running statistics (count, mean,
  variance) per host, per IP pair and per socket, over 5 time windows (about 100 ms to 1
  min). Each update costs O(1) time and memory, so no packets are stored. This produces
  about 115 features.
- **Feature mapper:** clusters correlated features into small groups.
- **KitNET:** one tiny autoencoder per feature group, plus an output autoencoder that
  combines their reconstruction errors into one anomaly score. Using many small
  autoencoders instead of one big one was about 5× faster on the Pi.
- It was evaluated on IP-camera and IoT networks with real attacks (Mirai, ARP
  man-in-the-middle, SYN flood, scans and others). It beat other online detectors and
  matched offline ones.

**Relevance to this project:**
- It is the classic "lightweight IDS on real hardware" paper and closest to our original
  framing. Its sliding-window streaming features are close to our planned streaming
  pipeline.
- Read it together with Entry 3, which showed that a simple boxplot rule beat Kitsune on
  its own Mirai data. That supports comparing against simple baselines.
- Differences from us: Kitsune is unsupervised, works per packet and uses neural nets. We
  use supervised trees on CICFlowMeter flows.

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
