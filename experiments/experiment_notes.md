# Experiment Notes

A dated log of each experiment: the data used, what was run, what was observed, any
problems, and the next step. Every row in `results.csv` can be traced to an entry here.

## 2026-10-04 — Dataset exploration (notebook 01)

Numbers re-checked by re-running notebook 1 on 23-10-2026.

```
Dataset file used: Wednesday-workingHours.pcap_ISCX.csv
692,703 rows, 79 columns (78 features + Label), confirmed with df.shape on 23-10-2026.
  This line first said 18334 rows, which was wrong.
Column names have leading spaces in the raw file; stripped with df.columns.str.strip()
Missing values: only Flow Bytes/s, 1,008 rows
Infinite values: Flow Packets/s in 1,297 rows, Flow Bytes/s in 289 rows
  1,008 + 289 = 1,297. This fits the missing Flow Bytes/s rows being the same rows
  as the infinite Flow Packets/s ones (probably zero-duration flows), which would
  explain why notebook 2 dropped no extra rows for missing values. Not checked directly.
81,909 duplicate rows (11.82% of all)
Class counts:
  BENIGN            440,031 (63.52%)
  DoS Hulk          231,073 (33.36%)
  DoS GoldenEye      10,293 (1.49%)
  DoS slowloris       5,796 (0.84%)
  DoS Slowhttptest    5,499 (0.79%)
  Heartbleed             11 (0.0016%)
BENIGN and DoS Hulk make up ~97% of rows; the other DoS types are rare, and
Heartbleed is far too rare to score reliably (all 11 rows survived cleaning:
9 ended up in train, 2 in test).

```
