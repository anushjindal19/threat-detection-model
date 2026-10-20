# References

## Python libraries

| Library | What it's for | Docs |
|---|---|---|
| pandas | Loading and manipulating tabular data | https://pandas.pydata.org/docs/ |
| NumPy | Numerical arrays and math | https://numpy.org/doc/ |
| scikit-learn | Decision trees, metrics and preprocessing | https://scikit-learn.org/stable/ |
| Matplotlib | Plotting | https://matplotlib.org/stable/ |
| Seaborn | Statistical plots, built on Matplotlib | https://seaborn.pydata.org/ |
| Joblib | Saving and loading trained models | https://joblib.readthedocs.io/ |
| Jupyter | The notebook format (.ipynb) | https://jupyter.org/documentation |

## Dataset

| Resource | Link |
|---|---|
| CICIDS2017 official dataset page (Canadian Institute for Cybersecurity, UNB) | https://www.unb.ca/cic/datasets/ids-2017.html |
| Original CICIDS2017 paper: Sharafaldin, Lashkari & Ghorbani, "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization," ICISSP 2018 | https://www.unb.ca/cic/datasets/ids-2017.html (paper linked from this page) |
| CICIDS2017 mirror on Kaggle (one CSV file per day) | https://www.kaggle.com/datasets/cicdataset/cicids2017 |

## Research papers (see `literature_review.md` for notes)

| Entry | Paper | Link |
|---|---|---|
| 2 | Engelen, Rimmer & Joosen (2021), *Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study*, IEEE SPW | https://lirias.kuleuven.be/retrieve/713070 |
| 3 | Arp et al. (2022), *Dos and Don'ts of Machine Learning in Computer Security*, USENIX Security | https://arxiv.org/abs/2010.09470 |
| 4 | Hooker et al. (2019), *What Do Compressed Deep Neural Networks Forget?*, arXiv | https://arxiv.org/abs/1911.05248 |
| 5 | Cantone, Marrocco & Bria (2024), *Machine Learning in Network Intrusion Detection: A Cross-Dataset Generalization Study*, IEEE Access 12 (preprint: arXiv 2402.10974) | https://doi.org/10.1109/ACCESS.2024.3472907 |
| 6 | Zheng et al. (2024), *Planter: Rapid Prototyping of In-Network ML Inference*, ACM SIGCOMM CCR | https://eng.ox.ac.uk/media/zetja3ek/zheng24planter.pdf |
| 7 | Mirsky et al. (2018), *Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection*, NDSS | https://arxiv.org/abs/1802.09089 |

## Other sources cited

| Source | Used for | Link |
|---|---|---|
| Breiman, Friedman, Olshen & Stone (1984), *Classification and Regression Trees*, Wadsworth | Cost-complexity pruning | (book) |
| Geirhos et al. (2020), *Shortcut Learning in Deep Neural Networks*, Nature Machine Intelligence 2(11) | Definition of a "shortcut" | https://doi.org/10.1038/s42256-020-00257-z |
| Lanvin et al. (2023), *Errors in the CICIDS2017 Dataset and the Significant Differences in Detection Performances It Makes*, CRiSIS 2022, LNCS 13857 | Dataset errors (limitations) | https://doi.org/10.1007/978-3-031-31108-6_2 |
| Nordby (2019), *emlearn*, Zenodo | Decision trees on microcontrollers | https://doi.org/10.5281/zenodo.2589394 |
| Pedregosa et al. (2011), *Scikit-learn: Machine Learning in Python*, JMLR 12 | The library used | https://jmlr.org/papers/v12/pedregosa11a.html |
| Microchip, *ATmega328P* product page | 32 KB flash / 2 KB SRAM budget | https://www.microchip.com/en-us/product/atmega328p |
| STMicroelectronics, *STM32F401xD STM32F401xE* datasheet (DS10086 rev. 5) | 512 KB flash / 96 KB RAM budget | https://www.st.com/resource/en/datasheet/stm32f401re.pdf |

## Background reading

| Topic | Resource |
|---|---|
| Intrusion detection systems (IDS) | https://en.wikipedia.org/wiki/Intrusion_detection_system |
| Train/test split and data leakage (scikit-learn) | https://scikit-learn.org/stable/common_pitfalls.html |
| Precision, recall and F1 | https://scikit-learn.org/stable/modules/model_evaluation.html |
| Decision trees | https://scikit-learn.org/stable/modules/tree.html |
