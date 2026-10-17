# Feature Documentation

One row per column of the Wednesday CICIDS2017 file (`Wednesday-workingHours.pcap_ISCX.csv`).
Column names are shown exactly as they appear in the raw CSV, including leading spaces.

## Summary of the decisions

- The file has **78 input features** plus the `Label` column.
- **20 are removed** and **58 are kept**. The 58 kept features are feature set **A**.
  Sets B (39), C (15) and D (6) are smaller selections from A (see notebook 3).
- Why the 20 were removed:
  - **10 are always 0 in this file**, so they carry no information: Bwd PSH Flags,
    Fwd URG Flags, Bwd URG Flags, CWE Flag Count, and the 6 Bulk columns.
  - **6 are exact copies** of a column that is kept: Avg Fwd Segment Size, Avg Bwd
    Segment Size, Fwd Header Length.1, Subflow Fwd Packets, Subflow Fwd Bytes,
    Subflow Bwd Packets.
  - **1 ranks flows in exactly the same order** as a kept column: Packet Length Variance.
  - **3 are nearly (not exactly) identical** to a kept column: Subflow Bwd Bytes,
    ECE Flag Count, Average Packet Size.
- **Every one of these reasons was tested on the real data** in notebook 4, Step 3, not
  just taken from what other papers say. Four claims did not fully hold. Three were close
  enough that the column stays removed (the reason now says "nearly identical"). One,
  **Fwd PSH Flags**, was wrong: it is not always zero, so it was **put back**.
- The Data Type column below was corrected on 23-10-2026 to match what `df.info()`
  printed in notebook 1. Several count columns were written as `float64` but are
  actually `int64`.

## Table

| Feature | Meaning | Data Type | Keep/Remove | Reason |
|---|---|---|---|---|
| `' Destination Port'` | Port number on the receiving end of the flow (e.g. 80 = HTTP, 22 = SSH) | int64 (categorical identifier, not a quantity) | Keep | Attacks target specific services (SSH/FTP brute force, web attacks on 80/8080, port scans hitting many ports). Caveat: CICIDS2017 attacks were run against fixed ports, so the tree may lean on this too heavily. Train once with and once without it and compare. |
| `' Flow Duration'` | Total time the flow lasted (microseconds) | int64 | Keep | Behavioural: DoS and slow attacks have distinctly short or long durations. |
| `' Total Fwd Packets'` | Number of packets sent forward (client → server) | int64 | Keep | Core volume feature: floods and scans send unusually many or few packets. |
| `' Total Backward Packets'` | Number of packets sent backward (server → client) | int64 | Keep | Shows whether the server actually responded. Scans and floods often get little or no reply. |
| `'Total Length of Fwd Packets'` | Total bytes of payload sent forward | int64 | Keep | Separates tiny probes from large uploads or exfiltration. |
| `' Total Length of Bwd Packets'` | Total bytes of payload sent backward | int64 | Keep | Shows how much data the server returned. Useful for spotting data theft and Heartbleed-style leaks. |
| `' Fwd Packet Length Max'` | Size of the largest forward packet | int64 | Keep | Attack tools often send fixed or unusual packet sizes. |
| `' Fwd Packet Length Min'` | Size of the smallest forward packet | int64 | Keep | Probe and handshake-only flows have characteristic minimum sizes. |
| `' Fwd Packet Length Mean'` | Average forward packet size | float64 | Keep | Summarises payload habits of the client. Not a duplicate: Avg Fwd Segment Size is the one that duplicates it. |
| `' Fwd Packet Length Std'` | Standard deviation of forward packet sizes | float64 | Keep | Automated tools tend to send uniform packets (low std), humans do not. |
| `'Bwd Packet Length Max'` | Size of the largest backward packet | int64 | Keep | Reflects server response behaviour under attack. |
| `' Bwd Packet Length Min'` | Size of the smallest backward packet | int64 | Keep | Same family, but captures the smallest server replies (e.g. bare ACKs or resets). |
| `' Bwd Packet Length Mean'` | Average backward packet size | float64 | Keep | Summarises server response size. Avg Bwd Segment Size duplicates it, so keep this one. |
| `' Bwd Packet Length Std'` | Standard deviation of backward packet sizes | float64 | Keep | Uniform server replies can indicate scripted interactions. |
| `'Flow Bytes/s'` | Data transfer rate of the flow (bytes per second) | float64 (contains `inf`/`NaN` from zero-duration flows) | Keep | Throughput is one of the strongest DoS/DDoS signals. It is a ratio, which a tree cannot compute from the raw columns. |
| `' Flow Packets/s'` | Packet rate of the flow (packets per second) | float64 (contains `inf`/`NaN` from zero-duration flows) | Keep | Packet rate catches floods and scans, and is again a ratio the tree can't build itself. |
| `' Flow IAT Mean'` | Average time gap between consecutive packets in the flow (IAT = inter-arrival time, microseconds) | float64 | Keep | Automated attacks are far more regular and faster than human traffic. |
| `' Flow IAT Std'` | Standard deviation of those gaps (how irregular the timing is) | float64 | Keep | Very low std suggests machine-generated timing. |
| `' Flow IAT Max'` | Longest gap between two packets in the flow | int64 | Keep | Slow attacks (e.g. Slowloris) hold connections open with long pauses. |
| `' Flow IAT Min'` | Shortest gap between two packets in the flow | int64 | Keep | Captures burst behaviour. |
| `'Fwd IAT Total'` | Total of all time gaps between forward packets | int64 | Keep | Client-side activity span. Not identical to Flow Duration, since the server may keep the flow alive. |
| `' Fwd IAT Mean'` | Average gap between forward packets | float64 | Keep | Client send rhythm. |
| `' Fwd IAT Std'` | Standard deviation of forward gaps | float64 | Keep | Regularity of the client's timing. |
| `' Fwd IAT Max'` | Longest gap between forward packets | int64 | Keep | Detects long client-side pauses. |
| `' Fwd IAT Min'` | Shortest gap between forward packets | int64 | Keep | Detects rapid-fire client bursts. |
| `'Bwd IAT Total'` | Total of all time gaps between backward packets | int64 | Keep | Server-side activity span. |
| `' Bwd IAT Mean'` | Average gap between backward packets | float64 | Keep | Server response rhythm. |
| `' Bwd IAT Std'` | Standard deviation of backward gaps | float64 | Keep | Regularity of the server's timing. |
| `' Bwd IAT Max'` | Longest gap between backward packets | int64 | Keep | Shows stalled or slow server responses. |
| `' Bwd IAT Min'` | Shortest gap between backward packets | int64 | Keep | Shows burst responses. |
| `'Fwd PSH Flags'` | Number of times the TCP PSH ("push data now") flag was set in forward packets | int64 | **Keep** (added back 23-10-2026) | First removed as "almost always 0". The check showed it is non-zero in **4.32%** of training rows (2 distinct values), so it carries real information. Checked in notebook 4, Step 3. It is in list A (58 features) but not in B, because B already has PSH Flag Count, which counts PSH flags in both directions. |
| `' Bwd PSH Flags'` | Number of times the PSH flag was set in backward packets | int64 | Remove | Always 0 in this file (1 distinct value), so it has zero information. Checked in notebook 4, Step 3. |
| `' Fwd URG Flags'` | Number of times the TCP URG ("urgent data") flag was set in forward packets | int64 | Remove | Always 0 in this file (1 distinct value). Checked in notebook 4, Step 3. |
| `' Bwd URG Flags'` | Number of times the URG flag was set in backward packets | int64 | Remove | Always 0 in this file (1 distinct value). Checked in notebook 4, Step 3. |
| `' Fwd Header Length'` | Total bytes of protocol headers in forward packets | int64 | Keep | Reflects packet count and TCP options. Different tools set different header options. |
| `' Bwd Header Length'` | Total bytes of protocol headers in backward packets | int64 | Keep | Same idea for the server side. |
| `'Fwd Packets/s'` | Forward packets per second | float64 | Keep | Client send rate, which matters because attacker traffic is often asymmetric. |
| `' Bwd Packets/s'` | Backward packets per second | float64 | Keep | Server reply rate. A big gap between Fwd and Bwd rates suggests flooding or scanning. |
| `' Min Packet Length'` | Smallest packet in the flow, either direction | int64 | Keep | Flow-level size floor, useful for probe and handshake-only flows. |
| `' Max Packet Length'` | Largest packet in the flow, either direction | int64 | Keep | Flow-level size ceiling. |
| `' Packet Length Mean'` | Average packet size across the whole flow | float64 | Keep | Summarises overall payload habits. |
| `' Packet Length Std'` | Standard deviation of packet sizes across the flow | float64 | Keep | Uniform sizes indicate automation. |
| `' Packet Length Variance'` | Variance of packet sizes (the square of the std) | float64 | Remove | It is Packet Length Std squared, so it ranks flows in exactly the same order (Spearman = 1.000). A tree only uses the order of values, so it gives no new splits. Checked in notebook 4, Step 3. |
| `'FIN Flag Count'` | Number of packets with the TCP FIN (connection close) flag | int64 (count) | Keep | Shows how connections are closed. Abnormal teardown patterns appear in scans and DoS. |
| `' SYN Flag Count'` | Number of packets with the TCP SYN (connection open) flag | int64 (count) | Keep | Key for SYN floods and port scans. |
| `' RST Flag Count'` | Number of packets with the TCP RST (connection reset) flag | int64 (count) | Keep | Resets are common in scans and rejected connections. |
| `' PSH Flag Count'` | Number of packets with the PSH flag | int64 (count) | Keep | Indicates data being pushed, which helps separate application-level behaviour. |
| `' ACK Flag Count'` | Number of packets with the ACK (acknowledgement) flag | int64 (count) | Keep | Missing or excess ACKs signal half-open connections and floods. |
| `' URG Flag Count'` | Number of packets with the URG flag | int64 (count) | Keep | Rare but occasionally discriminative. A tree uses it only where it helps. |
| `' CWE Flag Count'` | Number of packets with the CWR (congestion window reduced) flag; the name is a known typo in the dataset | int64 (count) | Remove | Always 0 in this file (1 distinct value), so it has zero information. Checked in notebook 4, Step 3. |
| `' ECE Flag Count'` | Number of packets with the ECE (explicit congestion notification echo) flag | int64 (count) | Remove | Nearly identical to RST Flag Count: the two differ in **1** of 488,393 training rows. Keeping both would add almost nothing. Checked in notebook 4, Step 3 (first claimed exactly identical, which was not quite true; decided 23-10-2026 to keep it out). |
| `' Down/Up Ratio'` | Ratio of download (backward) to upload (forward) traffic | int64 | Keep | Asymmetry feature: scans and floods are upload-heavy, exfiltration is download-heavy. |
| `' Average Packet Size'` | Average size of a packet in the flow | float64 | Remove | Almost the same ordering as Packet Length Mean (Spearman = **0.9976**, where 1.0 would be identical). Checked in notebook 4, Step 3 (first claimed exactly the same ordering; decided 23-10-2026 to keep it out). |
| `' Avg Fwd Segment Size'` | Average size of forward segments | float64 | Remove | Identical to Fwd Packet Length Mean on every row. Checked in notebook 4, Step 3. |
| `' Avg Bwd Segment Size'` | Average size of backward segments | float64 | Remove | Identical to Bwd Packet Length Mean on every row (largest difference 0.000001, a rounding error). Checked in notebook 4, Step 3. |
| `' Fwd Header Length.1'` | Duplicate copy of `Fwd Header Length` (pandas added `.1` because the name appeared twice in the CSV) | int64 (duplicate column) | Remove | Identical to Fwd Header Length on every row. Checked in notebook 4, Step 3. |
| `'Fwd Avg Bytes/Bulk'` | Average bytes per "bulk" transfer in the forward direction | int64 | Remove | Always 0 in this file (1 distinct value), so there is nothing to split on. Checked in notebook 4, Step 3. |
| `' Fwd Avg Packets/Bulk'` | Average packets per bulk transfer, forward | int64 | Remove | Always 0 in this file (1 distinct value), so there is nothing to split on. Checked in notebook 4, Step 3. |
| `' Fwd Avg Bulk Rate'` | Average bulk transfer rate, forward | int64 | Remove | Always 0 in this file (1 distinct value), so there is nothing to split on. Checked in notebook 4, Step 3. |
| `' Bwd Avg Bytes/Bulk'` | Average bytes per bulk transfer, backward | int64 | Remove | Always 0 in this file (1 distinct value), so there is nothing to split on. Checked in notebook 4, Step 3. |
| `' Bwd Avg Packets/Bulk'` | Average packets per bulk transfer, backward | int64 | Remove | Always 0 in this file (1 distinct value), so there is nothing to split on. Checked in notebook 4, Step 3. |
| `'Bwd Avg Bulk Rate'` | Average bulk transfer rate, backward | int64 | Remove | Always 0 in this file (1 distinct value), so there is nothing to split on. Checked in notebook 4, Step 3. |
| `'Subflow Fwd Packets'` | Average number of forward packets per subflow | int64 (count) | Remove | Identical to Total Fwd Packets on every row. Checked in notebook 4, Step 3. |
| `' Subflow Fwd Bytes'` | Average forward bytes per subflow | int64 | Remove | Identical to Total Length of Fwd Packets on every row. Checked in notebook 4, Step 3. |
| `' Subflow Bwd Packets'` | Average number of backward packets per subflow | int64 (count) | Remove | Identical to Total Backward Packets on every row. Checked in notebook 4, Step 3. |
| `' Subflow Bwd Bytes'` | Average backward bytes per subflow | int64 | Remove | Nearly identical to Total Length of Bwd Packets: they differ in only **34** of 488,393 training rows (0.007%). In those few rows the difference can be large (up to 469,129 bytes), but 34 rows are too few to matter for the tree. Checked in notebook 4, Step 3 (first claimed exactly identical; decided 23-10-2026 to keep it out). |
| `'Init_Win_bytes_forward'` | TCP window size (receive buffer, bytes) advertised in the first forward packet; `-1` when there's no TCP handshake | int64 (`-1` is a placeholder, not a real size) | Keep | Often among the most important features in CICIDS2017 papers. It reflects the sender's OS and tool fingerprint. Caveat: it may partly encode the lab setup rather than attack behaviour. |
| `' Init_Win_bytes_backward'` | Same, for the first backward packet | int64 (`-1` is a placeholder, not a real size) | Keep | Reflects how the server responded to the handshake. Same caveat as above. |
| `' act_data_pkt_fwd'` | Number of forward packets that carry at least 1 byte of actual data | int64 (count) | Keep | Separates flows that carry real data from empty probes and handshakes. |
| `' min_seg_size_forward'` | Smallest TCP segment header size seen in the forward direction | int64 | Keep | Low variance, but it acts as a tool/OS fingerprint and sometimes isolates specific attacks. Cheap to keep. |
| `'Active Mean'` | Average time the flow was active before going idle | float64 | Keep | Burst behaviour. Slow attacks have short active bursts. |
| `' Active Std'` | Standard deviation of active periods | float64 | Keep | Regularity of the bursts. |
| `' Active Max'` | Longest active period | int64 | Keep | Sustained activity, relevant to floods. |
| `' Active Min'` | Shortest active period | int64 | Keep | Smallest burst length. |
| `'Idle Mean'` | Average time the flow was idle before becoming active again | float64 | Keep | Key for slow-rate DoS (Slowloris, Slowhttptest), which deliberately sit idle. |
| `' Idle Std'` | Standard deviation of idle periods | float64 | Keep | Regularity of the pauses. |
| `' Idle Max'` | Longest idle period | int64 | Keep | Long idle holds are a slow-DoS signature. |
| `' Idle Min'` | Shortest idle period | int64 | Keep | Shortest pause between bursts. |
| `' Label'` | The class of the flow: `BENIGN` or one of the 5 attack types in this file (DoS Hulk, DoS GoldenEye, DoS slowloris, DoS Slowhttptest, Heartbleed) | object (string; must be encoded to numbers before training) | Keep | This is the target (`y`), not an input feature. Keep it, but split it off with `y = df['Label']` and `X = df.drop(columns='Label')` so it never leaks into `X`. |

## A note on data leakage

Some columns look harmless but leak information a real detector wouldn't have, or let
the model "cheat" by memorizing identities instead of learning patterns:

- **Flow ID** — often just a concatenation of IP:port:IP:port:protocol. Keeping it risks
  the model learning specific flow identities instead of general behaviour.
- **Source IP / Destination IP** — same risk; also, a model trained to recognize "attacks
  come from IP X" will fail completely against an attacker using a different IP.
- **Timestamp** — if attacks in a captured file happen to cluster in a specific time
  window, the model could learn "traffic at 14:32 = attack" instead of learning real
  traffic *behaviour*. That would not generalize.
- **Source Port / Destination Port** — these are more nuanced. A destination port (e.g.
  22 for SSH, 80 for HTTP) can be genuinely informative (some attacks target specific
  services), so this is a "keep, but think about it" case rather than an automatic
  removal. In this project it is kept, and its effect is tested in notebook 4.

When in doubt, ask: *"Would this column still be available and meaningful for a brand
new, real-time network flow the model has never seen before?"* If not, it's a leakage
risk.
