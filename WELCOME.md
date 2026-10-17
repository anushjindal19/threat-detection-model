# Welcome, Anush 👋

This is your project repo: **Lightweight Cybersecurity Threat Detector**. This page is
your starting point — it explains every tool you'll touch, why you need it (or don't),
and exactly where to click. Read it once, top to bottom, before doing anything else.

You do **not** need to be an expert in any of this beforehand. Every tool below is
explained assuming you're opening it for the very first time.

---

## The 4 tools, and what each one actually is

| Tool | What it is, in one line | Do you need to install it? |
|---|---|---|
| **Google Colab** | A free website that runs your Python code in the browser, on Google's computers | No install — just a browser and a Google login |
| **GitHub** | A website that stores and backs up your project's code | No install — just a browser and a free account |
| **Git** | The tool that saves versions of your code and talks to GitHub | Only if you edit files on your own PC (optional day-to-day, since Colab can save straight to GitHub for you) |
| **Python** | The programming language everything is written in | Only needed locally if you install Git above — Colab already has Python built in |
| **VS Code** *(optional)* | A code editor for your PC | Not required for this project — Colab is where you'll actually write and run the notebooks. Only grab this later if you ever want to edit the plain `.md` files locally. |

**The short version: for 95% of this project, all you need is a browser, a Google
account, and a GitHub account. That's it.**

---

## ⭐ Google Colab — the main place you'll work

This is where you'll spend almost all your time, so it gets its own section.

**What it is:** think of it as a Word document, except instead of paragraphs, it has
"cells" — some cells hold explanations (text), some hold actual Python code you can run
by clicking a play button. It runs on Google's servers for free, so your own laptop
never has to do the heavy lifting.

**Official link:** https://colab.research.google.com/

**How to open this project's notebooks in Colab:**

1. Go to https://colab.research.google.com/ and sign in with your Google account.
2. Click **File → Open notebook** (top-left).
3. Click the **GitHub** tab in the dialog.
4. Type or paste: `shikhadiwakar/lightweight-cyber-threat-detector`
5. Press Enter — it'll list the notebooks in the repo (inside the `notebooks/` folder).
6. Click **`01_dataset_exploration.ipynb`** to open it.
7. Click **"Copy to Drive"** near the top of the screen — this saves your own editable
   copy. If you skip this, your changes won't be saved anywhere.
8. Run cells top to bottom by clicking the ▶️ button on the left of each code cell, or
   pressing `Shift + Enter`. Read the text cells above each code cell — they explain
   what you're about to run and what output to expect.

**Saving your work back to the real project (not just your Drive copy):**
- **File → Save a copy in GitHub**
- Pick this repository, keep the same file path (e.g. `notebooks/01_dataset_exploration.ipynb`)
- Write a short message describing what you changed
- Click OK — done. No terminal, no Git commands needed for this.

That save-to-GitHub button is genuinely the only "Git" step you need for day-to-day work.

---

## GitHub — where your code lives online

**Official link:** https://github.com

**What you need to do here:**
1. If you don't already have a GitHub account, sign up (free) at the link above.
2. You'll get an email invite to collaborate on this repo:
   **https://github.com/shikhadiwakar/lightweight-cyber-threat-detector**
   Click **Accept invitation** in that email (or in your GitHub notifications).
3. Once accepted, you can open the repo, browse the files, and (via Colab, above) edit
   and save notebooks directly into it.

You can always view the repo itself here: https://github.com/shikhadiwakar/lightweight-cyber-threat-detector

---

## Git & Python — only if you want to work locally too

Skip this section entirely for now if you're only using Colab. Come back to it later if
you want to edit the Markdown guide files on your own PC, or run things outside a
browser.

- **Git official download:** https://git-scm.com/downloads
- **Python official download:** https://www.python.org/downloads/ (when installing,
  tick "Add python.exe to PATH")
- **VS Code (optional editor):** https://code.visualstudio.com/

The repo has a `setup.bat` file that automates installing/setting these up locally on
Windows, plus a full command-by-command guide in `SETUP_GUIDE.md` if you ever need it.

---

## Where to go after this page

1. **`README.md`** — the project map: what's in each folder and why.
2. **`SETUP_GUIDE.md`** — the detailed, step-by-step version of everything above, with
   exact commands and troubleshooting, for when you need more depth than this page.
3. **`notebooks/01_dataset_exploration.ipynb`** — your actual first task. Open it in
   Colab (steps above) and start reading/running.
4. **`CHECKLIST.md`** — tick items off here as you complete each stage, so you (and
   whoever reviews this with you) can see real progress.

## All the official links, in one place

| Resource | Link |
|---|---|
| Google Colab | https://colab.research.google.com/ |
| This project's GitHub repo | https://github.com/shikhadiwakar/lightweight-cyber-threat-detector |
| GitHub (create account / general) | https://github.com |
| GitHub Docs — Getting Started | https://docs.github.com/en/get-started |
| Git | https://git-scm.com/downloads |
| Python | https://www.python.org/downloads/ |
| VS Code (optional) | https://code.visualstudio.com/ |
| pandas docs | https://pandas.pydata.org/docs/ |
| NumPy docs | https://numpy.org/doc/ |
| scikit-learn docs | https://scikit-learn.org/stable/ |
| CICIDS2017 dataset (official) | https://www.unb.ca/cic/datasets/ids-2017.html |
| CICIDS2017 mirror on Kaggle | https://www.kaggle.com/datasets/cicdataset/cicids2017 |

(The full, categorized reference list — including later-stage tools you don't need yet —
is in `research/references.md`.)

---

Take it one step at a time. You don't need to understand everything on this page today —
just enough to open Colab and get `01_dataset_exploration.ipynb` running. Everything else
will make more sense once you're actually inside a notebook, reading real explanations
next to real code.
