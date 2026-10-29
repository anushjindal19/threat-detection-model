# Research Question

## Project

Lightweight machine-learning-based cybersecurity threat detection for resource-constrained
hardware.

## The question

> How much detection performance can be retained while reducing the computational,
> memory, and model-size requirements of a machine-learning-based cybersecurity threat
> detector?

Put simply: how small and fast can the detector be made before its detection becomes
noticeably worse?

## Why this question matters

Most published intrusion-detection research aims for the highest possible accuracy with
large, complex models (deep neural networks, large ensembles), which assumes a powerful
server to run them on.

The devices that would benefit most from on-device threat detection (a home router, a
Raspberry Pi, an IoT gateway, a microcontroller) do not have that hardware. A detector
that needs a GPU and gigabytes of RAM to classify one network flow is of no use there.

This project asks the opposite question: not "how accurate can the detector get", but
"how cheap can it get while staying accurate enough to be useful".

## Sub-questions

1. Which features of a network flow matter most for telling attacks apart from normal
   traffic?
2. How far can a decision tree be shrunk (by limiting its depth or pruning it) before its
   detection drops noticeably, and which attacks are lost first?
3. How does model size relate to inference cost (comparisons per flow, latency) and
   memory use?
4. Can the final detector fit the memory budget of a small CPU or microcontroller, with
   no GPU or server?

## Scope

- Only the attack types present in the CICIDS2017 files used (the Wednesday DoS attacks
  and Heartbleed, plus the Friday afternoon DDoS as an unseen test day) are covered.
- This is a research comparison of accuracy against resource cost, not a
  production-ready intrusion detection system.
- The model is a decision tree throughout: it is small, fast, interpretable and
  CPU-friendly, and its size can be controlled directly.

## How the project answers it

| Sub-question | Where |
|---|---|
| 1. Important features | Feature lists A-D (`notebooks/03_feature_engineering.ipynb`, `feature_documentation.md`) and the shortcut check (`notebooks/04_baseline_model.ipynb`) |
| 2. How far a tree can shrink | Depth and pruning sweeps with per-class recall, 5 splits, depth chosen on a validation set (`notebooks/05_shrinking_the_tree.ipynb`) |
| 3. Size vs cost | Nodes, compact size, comparisons per flow, prediction time and memory for every tree (notebooks 04 and 05) |
| 4. Small-device budget | Compact tree sizes compared with ATmega328P and STM32F401 memory budgets (notebook 05, `README.md`) |
| Generalisation | Wednesday-trained trees tested on the Friday afternoon file (`notebooks/07_friday_overfitting_check.ipynb`) |

Results are summarised in the root `README.md`.
