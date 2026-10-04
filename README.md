# Lightweight Cybersecurity Threat Detector

How small and cheap can a machine-learning model for detecting network attacks be made
before it starts missing attacks? This project trains decision trees on the public
**CICIDS2017** dataset and measures how detection changes as the model is made smaller.

**Research question:**
> How much detection performance can be retained while reducing the computational,
> memory, and model-size requirements of a machine-learning-based cybersecurity threat
> detector?

Author: Anush Jindal

## Repository layout

```
research/      research question and background notes
notebooks/     analysis notebooks, run in order
experiments/   results and a dated log of experiments
data/          how to download the CICIDS2017 files (the data itself is not committed)
models/        trained models are saved here (not committed)
```

## Setup

```
pip install -r requirements.txt
```

The notebooks run in Google Colab (the free CPU runtime is enough) or locally. See
`data/README.md` for the dataset files.

## Dataset

Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). Toward Generating a New
Intrusion Detection Dataset and Intrusion Traffic Characterization. *ICISSP 2018.*
Canadian Institute for Cybersecurity, University of New Brunswick:
https://www.unb.ca/cic/datasets/ids-2017.html
