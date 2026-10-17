# Dataset

**This folder does NOT contain the actual dataset file.** The CSV files are never
committed to GitHub (see the root `.gitignore` — it specifically excludes
`data/*.csv`). This README explains exactly what to download and where to put it.

## Why we don't commit the dataset

- CICIDS2017 files are large (each day's CSV can be several hundred MB to a few GB).
  GitHub is not built for hosting large data files, and free repos have size limits.
- Anyone who clones this repo can re-download the exact same file using the
  instructions below — there's no need to duplicate it in Git history.

## Which dataset

**CICIDS2017**, from the Canadian Institute for Cybersecurity (CIC), University of New
Brunswick (UNB).

- Official page: https://www.unb.ca/cic/datasets/ids-2017.html
- Kaggle mirror (easier — lets you download one day's CSV individually instead of a big
  combined archive): https://www.kaggle.com/datasets/cicdataset/cicids2017

## Which file to start with

**Do not download the whole dataset.** The full CICIDS2017 capture spans 5 days and is
several GB in total. For Stage 1-4 of this project, download **one single day's CSV
file** — this is enough to build and prove out the entire pipeline (load → understand →
clean → preprocess → engineer features).

A good first choice is one of the smaller, well-known files, for example:
- `Wednesday-workingHours.pcap_ISCX.csv` — contains BENIGN traffic plus several DoS
  attack variants, a good mix for a first pass.

(If that exact filename isn't available in whichever mirror you use, pick any single
day's file — Monday through Friday are all valid. Note in `experiment_notes.md` exactly
which file and filename you used, since results should always be traceable back to a
specific file.)

## Where to put it

1. Download the CSV file.
2. Place it directly inside this `data/` folder, e.g.:
   ```
   data/Wednesday-workingHours.pcap_ISCX.csv
   ```
3. It will **not** show up in `git status` as something to commit — `.gitignore`
   already excludes it. That's expected and correct.

## Using it in Google Colab

You don't have to download it to your PC at all if you're working in Colab — you can
upload it directly to your Colab session instead:

1. Open your notebook in Colab.
2. Click the folder icon on the left sidebar.
3. Click the upload icon and select the CSV file from your computer, **or** mount your
   Google Drive and reference a copy stored there (better if you'll reuse the file
   across multiple sessions, since uploaded files disappear when the Colab runtime
   resets).
4. Load it with:
   ```python
   df = pd.read_csv("Wednesday-workingHours.pcap_ISCX.csv")
   ```
   (adjust the filename to match exactly what you downloaded).

## Expanding later

Once the pipeline works end-to-end on one file, later stages (model optimization,
benchmarking) may use additional days' files. Document any new file added here, the same
way.
