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

- The data is CICIDS2017: five days of lab traffic with 14 attack types. v1 used one day
  (Wednesday: four DoS attacks and Heartbleed); v2 uses all five days.
- This is a research comparison of accuracy against resource cost, not a
  production-ready intrusion detection system.
- The model is a decision tree throughout: it is small, fast, interpretable and
  CPU-friendly, and its size can be controlled directly.

## Two versions

The question has been answered twice. The second answer exists because the first one
scored about 99.9%, which was too good to be true.

| | v1 (`v1_random_split/`) | v2 (`v2_unseen_data/`) |
|---|---|---|
| Data | Wednesday only | All five days |
| What the tree learns | The name of each attack | Attack or normal |
| Features | Lists A-D, with and without three shortcut features | Lists A-D without the shortcut features |
| Test set | Random 20% of the same day | Later traffic, an attack type never seen, a day never seen |
| What its score means | How well the tree fills gaps in attack bursts it has already seen | How well the tree detects traffic it has not seen |

## How the project answers it

| Sub-question | v1 | v2 |
|---|---|---|
| 1. Important features | Feature lists A-D (`feature_documentation.md`, v1 notebook 03) and the shortcut check (v1 notebook 04) | Uses the shortcut-free lists only |
| 2. How far a tree can shrink | Depth and pruning sweeps with per-class recall, 5 random splits (v1 notebook 05) | The same sweeps scored on unseen traffic, with recall for every attack type (v2 notebooks 03 and 04) |
| 3. Size vs cost | Nodes, compact size, comparisons per flow, prediction time and memory (v1 notebooks 04 and 05) | Nodes, compact size and comparisons per flow (v2 notebook 03) |
| 4. Small-device budget | Compact tree sizes compared with ATmega328P and STM32F401 memory budgets (v1 notebook 05) | Same comparison for the v2 trees (v2 README) |
| Is the score real? | Friday check (v1 notebook 07) | Random split vs split by time (v2 notebook 01); the four tests (v2 notebook 03) |

Results are summarised in the root `README.md`, with details in each version's own README.
