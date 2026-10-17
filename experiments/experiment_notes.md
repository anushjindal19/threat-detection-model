# Experiment Notes

A running log of what you tried, on which data, and why. This is the messy, honest
notebook that backs up the tidy numbers in `results.csv` — every row in that CSV should
be traceable to an entry here.

**Nothing in `results.csv` should ever be invented.** If you haven't run an experiment
yet, leave the row out rather than filling in guessed numbers.

## Log format

Copy this block for each new entry:

```
### YYYY-MM-DD — short title

**Dataset file used:**
**What I did:**
**What I observed:**
**Any errors/problems:**
**Next step:**
```

---

## Entries

```
### 4-10-2026

Dataset file used: Wednesday-workingHours
18334 rows, 79 columns
Flow Bytes has 1008 missing values
Flow Packets has 1297, Flow Bytes has 289 infinite values
81909 duplicate rows (11.82% of all)
BENIGN and DoS Hulk are the most common (63.5% and 33.3%, respectively)
DoS GoldenEye, DoS slowloris and DoS Slowhttptest are rare (1.84%, 0.84% and 0.79%, respectively)
Heartbleed is the rarest at ~0.00 (only 11 counts)

```

```
### 6-10-2026

0.19% rows dropped for infinite values
11.7% rows dropped for duplicate values
No rows dropped for missing values
No identifier columns removed
X_train: (488393, 78)
X_test:  (122099, 78)
Stratified splitting worked cleanly, equal percentage split for train and test data

```
