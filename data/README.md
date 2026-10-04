# Data

The dataset is not committed to this repository (`data/*.csv` is git-ignored). This
folder only holds this README.

## Source

**CICIDS2017**, Canadian Institute for Cybersecurity, University of New Brunswick.

- Official page: https://www.unb.ca/cic/datasets/ids-2017.html
- Kaggle mirror (per-day CSV files): https://www.kaggle.com/datasets/cicdataset/cicids2017

## Files used

| File | Used by | Contents |
|---|---|---|
| `Wednesday-workingHours.pcap_ISCX.csv` | Notebooks 01-05 | 692,703 flows: BENIGN plus DoS Hulk, DoS GoldenEye, DoS slowloris, DoS Slowhttptest and Heartbleed |
| `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` | Notebook 07 | BENIGN plus DDoS (LOIT HTTP flood); used only as an unseen test day |

## Placement

- **Local:** put the CSV files directly in this folder, e.g.
  `data/Wednesday-workingHours.pcap_ISCX.csv`.
- **Google Colab:** the notebooks mount Google Drive and read from
  `/content/drive/MyDrive/Colab Notebooks/threat detector/data`. Put the files there, or
  change the path variable at the top of each notebook.

Notebook 02 writes the cleaned train/test split (`X_train.csv`, `X_test.csv`,
`y_train.csv`, `y_test.csv`) to the same folder; these are git-ignored as well.
