# Setup Guide — Zero to Running, Step by Step

This guide assumes you have **never used Git, GitHub, Python, or Google Colab before.**
Every command is exact, every step says where to run it, and every step explains what
"success" looks like. Read it in order — don't skip ahead.

Total time to get everything running: roughly 30-45 minutes.

---

## 0. The big picture — what are all these tools for?

Before touching anything, it helps to know *why* each tool exists:

| Tool | What it actually is | Why we need it here |
|---|---|---|
| **Python** | A programming language | The language we write all the code in |
| **Git** | A tool that tracks changes to your files over time | So you have a history of your work and can undo mistakes |
| **GitHub** | A website that stores a copy of your Git project online | So your code is backed up, visible, and shareable |
| **Google Colab** | A free website that runs Python code (Jupyter notebooks) in your browser, using Google's computers | So you don't need a powerful PC or GPU — Colab does the heavy lifting for free |

The workflow, in one sentence: **you write and run code in Google Colab, and you save
your work by pushing it to GitHub, which lives inside this project folder on your PC.**

---

## 1. Install Git

1. Go to the official download page: **https://git-scm.com/downloads**
2. Download the Windows installer and run it.
3. Click "Next" through the installer — the default options are fine for a beginner.
4. When it's done, open a terminal (search "Git Bash" or "PowerShell" in the Windows
   Start menu) and check it worked:
   ```bash
   git --version
   ```
   **Expected output** (version number may differ):
   ```
   git version 2.47.0.windows.2
   ```

**Troubleshooting:**
- `'git' is not recognized as an internal or external command` → Close and reopen your
  terminal (PATH changes need a fresh terminal window). If it still fails, restart your
  PC.
- Already have Git? Great — this project's `setup.bat` script checks for it
  automatically and skips this step if it's already installed.

---

## 2. Install Python (optional right now, needed for the local setup script)

You technically don't need Python installed locally to use Google Colab — Colab has its
own Python already. But this project includes a `setup.bat` script that sets up a local
Python environment too (useful for later stages, like benchmarking on your own PC), so
it's worth doing now.

1. Go to **https://www.python.org/downloads/**
2. Download the latest Python 3 installer.
3. **Important:** on the very first install screen, tick the checkbox **"Add python.exe
   to PATH"** before clicking Install. This is the single most common mistake beginners
   make.
4. After installing, check it worked in a terminal:
   ```bash
   python --version
   ```
   **Expected output:**
   ```
   Python 3.11.9
   ```

**Troubleshooting:**
- `'python' is not recognized...` → You likely missed the "Add to PATH" checkbox.
  Re-run the installer, choose "Modify," and enable that option.
- Multiple Python versions installed and confused about which one runs? Any Python 3.9+
  is fine for this project.

---

## 3. Create a GitHub account and a new repository

1. Go to **https://github.com** and sign up for a free account if you don't have one.
2. Once logged in, go to **https://github.com/new** to create a new repository.
3. Fill in:
   - **Repository name:** `lightweight-cyber-threat-detector`
   - **Description (optional):** "Lightweight ML-based cybersecurity threat detector — research project"
   - **Visibility:** Public or Private, your choice.
   - **Do NOT check** "Add a README file" — this project folder already has one, and
     checking that box would create a conflict when you push.
4. Click **Create repository**.
5. GitHub will show you a page with a URL like:
   ```
   https://github.com/YOUR_USERNAME/lightweight-cyber-threat-detector.git
   ```
   Keep this tab open — you'll need that URL in the next step.

---

## 4. Run the local setup script

This project includes `setup.bat`, which automates the boring parts: checking Git/Python
are installed, creating a Python virtual environment, installing the required packages,
and initializing the local Git repository.

1. Open the project folder in File Explorer: `C:\Users\shkhd\anush`
2. Double-click **`setup.bat`**.
3. A black terminal window will open and print progress for each step. Wait for it to
   finish — it ends with a "Setup complete!" message.

**What "success" looks like:** the last lines printed are:
```
================================================
 Setup complete!
================================================
```

**Troubleshooting:**
- A pip install step fails partway through → note which package name it mentions, and
  try running `.venv\Scripts\python.exe -m pip install PACKAGE_NAME` manually to see the
  full error.
- Script closes instantly with no output → right-click `setup.bat` → "Run as
  administrator," or run it from an already-open terminal instead of double-clicking, so
  you can read any error message before the window closes:
  ```bash
  cd C:\Users\shkhd\anush
  setup.bat
  ```

---

## 5. Connect this folder to your GitHub repository

`setup.bat` already ran `git init` and made a first commit locally. Now you need to
connect it to the GitHub repository you created in Step 3, and push your code up.

Open a terminal in the project folder and run these commands **one at a time**, reading
the output after each:

```bash
git remote add origin https://github.com/YOUR_USERNAME/lightweight-cyber-threat-detector.git
```
(Replace the URL with your actual repository URL from Step 3. No output means success.)

```bash
git branch -M main
```
(Renames your local branch to `main`, matching GitHub's default. No output means success.)

```bash
git push -u origin main
```
**Expected output** (roughly):
```
Enumerating objects: 20, done.
...
To https://github.com/YOUR_USERNAME/lightweight-cyber-threat-detector.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

The first time you push, GitHub may open a browser window asking you to log in and
authorize Git — follow the prompts.

**Troubleshooting:**
- `remote origin already exists` → you already ran the `remote add` command once. Skip
  it and just run `git push -u origin main`.
- `Support for password authentication was removed` → GitHub no longer accepts your
  account password for `git push`. Either let the browser login popup finish (recommended
  for beginners — this uses GitHub's official device-login flow), or read
  https://docs.github.com/en/authentication for setting up a Personal Access Token.
- Refresh the GitHub repository page in your browser — you should now see all your
  project files there.

---

## 6. Set up Google Colab

1. Go to **https://colab.research.google.com/**
2. Sign in with the same Google account you'll use throughout the project.
3. To open a notebook that's already in your GitHub repo:
   - Click **File → Open notebook**
   - Click the **GitHub** tab
   - Paste your repository URL (or search your username) and select it
   - Click on `notebooks/01_dataset_exploration.ipynb`
4. Colab opens the notebook. Click the "Copy to Drive" button that appears at the top if
   you want to save your own editable copy (recommended) — otherwise your edits won't
   persist between sessions.

**Saving your work back to GitHub from Colab:**
- **File → Save a copy in GitHub**
- Choose the repository and the same file path (`notebooks/01_dataset_exploration.ipynb`)
- Add a short commit message describing what changed (e.g. "Add shape/columns inspection")
- Click OK — this creates a commit directly on GitHub, no terminal needed.

This is the easiest day-to-day workflow: **edit in Colab → "Save a copy in GitHub" → repeat.**
You only need the terminal `git` commands from Step 5 when you're working with files
outside of Colab (like editing these Markdown guide files locally).

**Troubleshooting:**
- Don't see your repository under the GitHub tab in Colab? Click "Include private
  repos" and make sure you've authorized Colab's GitHub connection when prompted.
- "Copy to Drive" vs. "Save a copy in GitHub" — Drive saves a personal copy only you can
  see; GitHub saves it to the actual project repository. Use **GitHub** as your real save
  destination for this project.

---

## 7. Everyday Git workflow (once things are set up)

If you ever edit files locally instead of through Colab's "Save a copy in GitHub" button,
use this three-command pattern from a terminal in the project folder:

```bash
git add .
git commit -m "Describe what you changed, in a few words"
git push
```

- `git add .` — stages all your changes (tells Git "these are ready to be saved").
- `git commit -m "..."` — actually saves a snapshot, with a short message explaining why.
- `git push` — uploads that snapshot to GitHub.

Run `git status` any time to see what's changed and not yet committed — it's always safe
to run and never changes anything by itself.

**A rule for this project: never commit the raw dataset CSV file.** The `.gitignore` in
this repo already blocks `data/*.csv` from being tracked, so `git add .` will correctly
skip it — but never force-add it (`git add -f`) either.

---

## 8. What to do next

Once this guide is complete (Git installed, Python installed, GitHub repo created and
pushed, Colab connected), move on to:

1. **`notebooks/01_dataset_exploration.ipynb`** — open it in Colab and follow it,
   downloading the one CICIDS2017 file described in `data/README.md` first.
2. Then **`notebooks/02_preprocessing.ipynb`**.
3. Then **`notebooks/03_FEATURE_ENGINEERING_GUIDE.md`** — this one you write yourself,
   using the guide for direction.
4. Use **`CHECKLIST.md`** to confirm each stage is genuinely done.

Come back to this guide any time you forget a command — that's what it's for.
