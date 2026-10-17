# Research Question

## Update — GPU-capable models (decision made after the initial roadmap)

The original plan below was CPU-only, built entirely around a lightweight Decision Tree
baseline. That decision has since changed: **Stage 5+ (baseline model and beyond, not
started in this repo yet) will use GPU-capable models** in Colab instead of a CPU-only
Decision Tree.

**What this does and doesn't affect:**
- Stages 1-4 (research, dataset exploration, preprocessing, feature engineering — what's
  actually built in this repo right now) are **unaffected**. Understanding the data,
  cleaning it, and engineering features doesn't depend on which model trains on it later.
- The "resource-constrained hardware" framing below is the *original* research angle. It
  is being revisited as part of Stage 5 planning — worth deciding explicitly (and writing
  down here) whether the project keeps a resource-vs-accuracy comparison (e.g. a GPU
  model as the "large/high-accuracy" end of a trade-off curve, benchmarked against a
  small CPU model — see `README.md`'s pipeline diagram) or moves fully away from the
  lightweight-detector framing toward "best achievable detection accuracy."
- Until that's decided, the original question below stands as the historical starting
  point — don't delete it, update it in place once Stage 5 is actually being planned.

---

## Project

Lightweight Machine-Learning-Based Cybersecurity Threat Detection for
Resource-Constrained Hardware *(original framing — see Update note above)*.

## The question

> How much detection performance can be retained while reducing the computational,
> memory, and model-size requirements of a machine-learning-based cybersecurity threat
> detector?

In plain language:

> How small and fast can we make the cybersecurity AI before its detection performance
> becomes significantly worse?

## Why this question matters

Most published intrusion-detection research chases the highest possible accuracy using
large, complex models (deep neural networks, huge ensembles). That's useful, but it
usually assumes you have a powerful server to run the model on.

Real devices that could benefit from on-device threat detection — a home router, a
Raspberry Pi, an old laptop, an IoT gateway — do **not** have that kind of hardware. If a
detector needs a GPU and gigabytes of RAM just to classify one network flow, it is
useless in exactly the places lightweight security matters most.

This project asks the opposite question: instead of "how accurate can we get," it asks
"how cheap can we get while staying accurate enough to be useful."

## Sub-questions

1. Which features of a network flow are actually most important for telling attacks
   apart from normal traffic?
2. How much can the model (a Decision Tree, to start) be pruned/shrunk before its
   detection performance drops noticeably?
3. How does model size relate to inference latency and memory usage in practice?
4. Can the final, optimized detector run comfortably on an ordinary laptop CPU — no GPU,
   no server?

## Scope (what this project is NOT trying to do)

- It is **not** trying to detect every possible cyberattack that exists — only the
  attack types actually represented in the CICIDS2017 dataset.
- It is **not** trying to build a production-ready intrusion detection system — it is a
  research project comparing accuracy vs. resource cost.
- It is **not** starting with deep learning. The baseline is a Decision Tree
  specifically because it is small, fast, interpretable, and CPU-friendly — a sensible
  starting point for a *lightweight* detector.

## Status

This file is a starting point. As you read more about intrusion detection research (see
`literature_review.md`), refine this question if needed — but keep the core idea
(accuracy vs. resource cost trade-off) intact, since that's what the whole pipeline is
built around.
