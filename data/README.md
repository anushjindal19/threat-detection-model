# Data

The dataset is not committed to this repository (the CSV files are git-ignored). This
folder only holds this README.

## Source

**CICIDS2017**, Canadian Institute for Cybersecurity, University of New Brunswick. Five days
of lab traffic (Monday 3 July to Friday 7 July 2017), as eight CSV files in the
`MachineLearningCVE` folder.

- Official page: https://www.unb.ca/cic/datasets/ids-2017.html
- Kaggle mirror (per-day CSV files): https://www.kaggle.com/datasets/cicdataset/cicids2017

## Files

| File | Day | Attacks in it | Used by |
|---|---|---|---|
| `Monday-WorkingHours.pcap_ISCX.csv` | Monday | none (normal traffic only) | v2 |
| `Tuesday-WorkingHours.pcap_ISCX.csv` | Tuesday | FTP-Patator, SSH-Patator | v2 |
| `Wednesday-workingHours.pcap_ISCX.csv` | Wednesday | DoS slowloris, DoS Slowhttptest, DoS Hulk, DoS GoldenEye, Heartbleed | v1 and v2 |
| `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv` | Thursday | Web Attack - Brute Force, XSS, Sql Injection | v2 |
| `Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv` | Thursday | Infiltration | v2 |
| `Friday-WorkingHours-Morning.pcap_ISCX.csv` | Friday | Bot | v2 |
| `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv` | Friday | PortScan | v2 |
| `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` | Friday | DDoS | v1 (notebook 07) and v2 |

Row counts before and after cleaning are in
`v2_unseen_data/results/02_data_summary.csv`.

## Where to put them

| Version | Folder |
|---|---|
| **v2** | this folder: `data/` |
| **v1** | `v1_random_split/data/` (v1 only needs the Wednesday file and the Friday DDoS file) |

v2's notebook 02 writes one cleaned table, `data/all_days_clean.pkl` (about 850 MB), which
the other v2 notebooks read. It is git-ignored as well.
