# References & Official Resources

Every official link you need for this project, in one place. Bookmark this page.

## Tools you need to set up

| Tool | What it's for | Official link |
|---|---|---|
| Git | Version control (tracks changes to your code) | https://git-scm.com/downloads |
| GitHub | Hosts your Git repository online | https://github.com |
| GitHub Docs — Getting Started | Learn Git/GitHub basics | https://docs.github.com/en/get-started |
| Python | The programming language everything is written in | https://www.python.org/downloads/ |
| Google Colab | Free, no-install notebook environment (what we use to actually run code) | https://colab.research.google.com/ |
| Kaggle Notebooks | Alternative to Colab, also free and CPU-based | https://www.kaggle.com/code |

## Python libraries (documentation)

| Library | What it's for | Docs |
|---|---|---|
| pandas | Loading and manipulating tabular data | https://pandas.pydata.org/docs/ |
| NumPy | Numerical arrays and math | https://numpy.org/doc/ |
| scikit-learn | Machine learning models (Decision Tree, etc.) and preprocessing | https://scikit-learn.org/stable/ |
| Matplotlib | Plotting/graphs | https://matplotlib.org/stable/ |
| Seaborn | Nicer statistical plots, built on Matplotlib | https://seaborn.pydata.org/ |
| Joblib | Saving/loading trained models | https://joblib.readthedocs.io/ |
| Jupyter | The notebook format itself (.ipynb) | https://jupyter.org/documentation |

## Dataset

| Resource | Link |
|---|---|
| CICIDS2017 official dataset page (Canadian Institute for Cybersecurity, UNB) | https://www.unb.ca/cic/datasets/ids-2017.html |
| Original CICIDS2017 paper — Sharafaldin, Lashkari & Ghorbani, "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization," ICISSP 2018 | https://www.unb.ca/cic/datasets/ids-2017.html (paper linked from this page) |
| CICIDS2017 mirror on Kaggle (individual day CSV files — easier for a first, small download) | https://www.kaggle.com/datasets/cicdataset/cicids2017 |

> The dataset is normally distributed as one CSV file per day of capture (Monday,
> Tuesday, Wednesday, Thursday, Friday), each with different attack types. Start with
> **one single day's file** — see `data/README.md` for exactly which one and why.

## Background reading (concepts, not tied to one library)

| Topic | Resource |
|---|---|
| What is an Intrusion Detection System (IDS)? | https://en.wikipedia.org/wiki/Intrusion_detection_system |
| Train/test split & data leakage (scikit-learn's own explanation) | https://scikit-learn.org/stable/common_pitfalls.html |
| Precision, Recall, F1 explained | https://scikit-learn.org/stable/modules/model_evaluation.html |
| Decision Trees explained | https://scikit-learn.org/stable/modules/tree.html |
| Markdown syntax (for writing these .md files) | https://www.markdownguide.org/basic-syntax/ |

## Later-stage tools (not needed yet — for reference only)

| Tool | Stage it's used in | Link |
|---|---|---|
| Streamlit | Stage 9 — research dashboard app | https://docs.streamlit.io/ |
| FastAPI | Stage 9 (game option) — backend API | https://fastapi.tiangolo.com/ |
| React + Vite | Stage 9 (game option) — frontend | https://react.dev/ , https://vitejs.dev/ |
| Tailwind CSS | Stage 9 (game option) — styling | https://tailwindcss.com/ |

Do not install or set these up yet — they belong to a much later stage of the project.

## How to add to this list

As you read papers or tutorials for `literature_review.md`, add the links here too, so
this file stays the single source of truth for "where did this come from."
