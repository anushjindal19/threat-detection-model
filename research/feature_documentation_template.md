# Feature Documentation Table

Fill this in **after** you've loaded your actual CICIDS2017 file and run
`df.columns`, `df.info()`, and `df.head()` on it in `01_dataset_exploration.ipynb`.

**Do not guess column names ahead of time — different CICIDS2017 file versions have
slightly different column names/spacing (e.g. a leading space before `Label` is common).
Copy the real column names from your actual `df.columns` output.**

## How to fill this in

For every column in your dataset, add one row:

- **Feature** — the exact column name from `df.columns`.
- **Meaning** — what it represents, in plain language (use `attack_categories.md` and
  `references.md` — the CICIDS2017 paper describes how CICFlowMeter computes each flow
  feature — to help explain the less obvious ones).
- **Data Type** — what `df.dtypes` / `df.info()` says (`int64`, `float64`, `object`,
  etc.), and whether that's actually correct (e.g. a column of numbers stored as text
  should be flagged).
- **Keep / Remove** — your decision for the feature-engineering stage.
- **Reason** — why. Common reasons to **remove**: it's a pure identifier (e.g. Flow ID,
  raw Source/Destination IP, raw timestamp) that could cause data leakage or overfitting
  rather than teach the model real behavioural patterns; it's constant/near-constant
  across all rows; it duplicates another feature. Common reasons to **keep**: it
  describes traffic volume, timing, packet, protocol, or port *behaviour* that could
  genuinely help distinguish attacks from normal traffic.

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
| `'Fwd PSH Flags'` | Number of times the TCP PSH ("push data now") flag was set in forward packets | int64 | Remove | Almost always 0 or 1 and largely overlaps with PSH Flag Count, which is kept. Verify with the check below. |
| `' Bwd PSH Flags'` | Number of times the PSH flag was set in backward packets | int64 | Remove | Constant 0 in CICIDS2017 (the extractor never populates it), so it has zero information. |
| `' Fwd URG Flags'` | Number of times the TCP URG ("urgent data") flag was set in forward packets | int64 | Remove | Near-constant (almost always 0) and overlaps with URG Flag Count, which is kept. |
| `' Bwd URG Flags'` | Number of times the URG flag was set in backward packets | int64 | Remove | Constant 0 in CICIDS2017, so it has zero information. |
| `' Fwd Header Length'` | Total bytes of protocol headers in forward packets | int64 | Keep | Reflects packet count and TCP options. Different tools set different header options. |
| `' Bwd Header Length'` | Total bytes of protocol headers in backward packets | int64 | Keep | Same idea for the server side. |
| `'Fwd Packets/s'` | Forward packets per second | float64 | Keep | Client send rate, which matters because attacker traffic is often asymmetric. |
| `' Bwd Packets/s'` | Backward packets per second | float64 | Keep | Server reply rate. A big gap between Fwd and Bwd rates suggests flooding or scanning. |
| `' Min Packet Length'` | Smallest packet in the flow, either direction | int64 | Keep | Flow-level size floor, useful for probe and handshake-only flows. |
| `' Max Packet Length'` | Largest packet in the flow, either direction | int64 | Keep | Flow-level size ceiling. |
| `' Packet Length Mean'` | Average packet size across the whole flow | float64 | Keep | Summarises overall payload habits. |
| `' Packet Length Std'` | Standard deviation of packet sizes across the flow | float64 | Keep | Uniform sizes indicate automation. |
| `' Packet Length Variance'` | Variance of packet sizes (the square of the std) | float64 | Remove | Monotonic transform of Packet Length Std. Trees only use ordering, so it gives no new splits. |
| `'FIN Flag Count'` | Number of packets with the TCP FIN (connection close) flag | float64 (integer-valued count) | Keep | Shows how connections are closed. Abnormal teardown patterns appear in scans and DoS. |
| `' SYN Flag Count'` | Number of packets with the TCP SYN (connection open) flag | float64 (integer-valued count) | Keep | Key for SYN floods and port scans. |
| `' RST Flag Count'` | Number of packets with the TCP RST (connection reset) flag | float64 (integer-valued count) | Keep | Resets are common in scans and rejected connections. |
| `' PSH Flag Count'` | Number of packets with the PSH flag | float64 (integer-valued count) | Keep | Indicates data being pushed, which helps separate application-level behaviour. |
| `' ACK Flag Count'` | Number of packets with the ACK (acknowledgement) flag | float64 (integer-valued count) | Keep | Missing or excess ACKs signal half-open connections and floods. |
| `' URG Flag Count'` | Number of packets with the URG flag | float64 (integer-valued count) | Keep | Rare but occasionally discriminative. A tree uses it only where it helps. |
| `' CWE Flag Count'` | Number of packets with the CWR (congestion window reduced) flag; the name is a known typo in the dataset | float64 (integer-valued count) | Remove | Near-constant and, in CICIDS2017, tends to mirror the URG columns because of extractor quirks. Not a real congestion signal. |
| `' ECE Flag Count'` | Number of packets with the ECE (explicit congestion notification echo) flag | float64 (integer-valued count) | Remove | In CICIDS2017 it is reported to be identical to RST Flag Count (an extractor bug), so it adds nothing. Verify with the check below. |
| `' Down/Up Ratio'` | Ratio of download (backward) to upload (forward) traffic | float64 | Keep | Asymmetry feature: scans and floods are upload-heavy, exfiltration is download-heavy. |
| `' Average Packet Size'` | Average size of a packet in the flow | float64 | Remove | Almost the same quantity as Packet Length Mean, so it is redundant. |
| `' Avg Fwd Segment Size'` | Average size of forward segments | float64 | Remove | Identical to Fwd Packet Length Mean in this dataset. |
| `' Avg Bwd Segment Size'` | Average size of backward segments | float64 | Remove | Identical to Bwd Packet Length Mean in this dataset. |
| `' Fwd Header Length.1'` | Duplicate copy of `Fwd Header Length` (pandas added `.1` because the name appeared twice in the CSV) | float64 (integer-valued; duplicate column) | Remove | Exact duplicate of Fwd Header Length. Remove it if it somehow survived your cleaning. |
| `'Fwd Avg Bytes/Bulk'` | Average bytes per "bulk" transfer in the forward direction | float64 (integer-valued) | Remove | Zero in the overwhelming majority of flows, so there is almost nothing to split on. |
| `' Fwd Avg Packets/Bulk'` | Average packets per bulk transfer, forward | float64 (integer-valued) | Remove | Same near-constant zero issue. |
| `' Fwd Avg Bulk Rate'` | Average bulk transfer rate, forward | float64 (integer-valued) | Remove | Same near-constant zero issue. |
| `' Bwd Avg Bytes/Bulk'` | Average bytes per bulk transfer, backward | float64 (integer-valued) | Remove | Same near-constant zero issue. |
| `' Bwd Avg Packets/Bulk'` | Average packets per bulk transfer, backward | float64 (integer-valued) | Remove | Same near-constant zero issue. |
| `'Bwd Avg Bulk Rate'` | Average bulk transfer rate, backward | float64 (integer-valued) | Remove | Same near-constant zero issue. |
| `'Subflow Fwd Packets'` | Average number of forward packets per subflow | float64 (integer-valued count) | Remove | Equal to Total Fwd Packets in this dataset, so it is redundant. |
| `' Subflow Fwd Bytes'` | Average forward bytes per subflow | float64 (integer-valued) | Remove | Equal to Total Length of Fwd Packets, so it is redundant. |
| `' Subflow Bwd Packets'` | Average number of backward packets per subflow | float64 (integer-valued count) | Remove | Equal to Total Backward Packets, so it is redundant. |
| `' Subflow Bwd Bytes'` | Average backward bytes per subflow | float64 (integer-valued) | Remove | Equal to Total Length of Bwd Packets, so it is redundant. |
| `'Init_Win_bytes_forward'` | TCP window size (receive buffer, bytes) advertised in the first forward packet; `-1` when there's no TCP handshake | float64 (integer-valued; `-1` is a placeholder, not a real size) | Keep | Often among the most important features in CICIDS2017 papers. It reflects the sender's OS and tool fingerprint. Caveat: it may partly encode the lab setup rather than attack behaviour. |
| `' Init_Win_bytes_backward'` | Same, for the first backward packet | float64 (integer-valued; `-1` is a placeholder, not a real size) | Keep | Reflects how the server responded to the handshake. Same caveat as above. |
| `' act_data_pkt_fwd'` | Number of forward packets that carry at least 1 byte of actual data | float64 (integer-valued count) | Keep | Separates flows that carry real data from empty probes and handshakes. |
| `' min_seg_size_forward'` | Smallest TCP segment header size seen in the forward direction | float64 (integer-valued) | Keep | Low variance, but it acts as a tool/OS fingerprint and sometimes isolates specific attacks. Cheap to keep. |
| `'Active Mean'` | Average time the flow was active before going idle | float64 | Keep | Burst behaviour. Slow attacks have short active bursts. |
| `' Active Std'` | Standard deviation of active periods | float64 | Keep | Regularity of the bursts. |
| `' Active Max'` | Longest active period | float64 (integer-valued) | Keep | Sustained activity, relevant to floods. |
| `' Active Min'` | Shortest active period | float64 (integer-valued) | Keep | Smallest burst length. |
| `'Idle Mean'` | Average time the flow was idle before becoming active again | float64 | Keep | Key for slow-rate DoS (Slowloris, Slowhttptest), which deliberately sit idle. |
| `' Idle Std'` | Standard deviation of idle periods | float64 | Keep | Regularity of the pauses. |
| `' Idle Max'` | Longest idle period | float64 (integer-valued) | Keep | Long idle holds are a slow-DoS signature. |
| `' Idle Min'` | Shortest idle period | float64 (integer-valued) | Keep | Shortest pause between bursts. |
| `' Label'` | The class of the flow: `BENIGN` or the attack type (e.g. DoS, PortScan) | object (string; must be encoded to numbers before training) | Keep | This is your target (`y`), not an input feature. Keep it, but split it off with `y = df['Label']` and `X = df.drop(columns='Label')` so it never leaks into `X`. |

Add as many rows as you have columns. This table becomes Stage 4's main deliverable
alongside the feature-engineering notebook — it's the evidence that every column was a
deliberate decision, not guesswork.

## A note on data leakage (read before filling in "Keep/Remove")

Some columns look harmless but leak information a real detector wouldn't have, or let
the model "cheat" by memorizing identities instead of learning patterns:

- **Flow ID** — often just a concatenation of IP:port:IP:port:protocol. Keeping it risks
  the model learning specific flow identities instead of general behaviour.
- **Source IP / Destination IP** — same risk; also, a model trained to recognize "attacks
  come from IP X" will fail completely against an attacker using a different IP.
- **Timestamp** — if attacks in your captured file happen to cluster in a specific time
  window, the model could learn "traffic at 14:32 = attack" instead of learning real
  traffic *behaviour*. That would not generalize.
- **Source Port / Destination Port** — these are more nuanced. A destination port (e.g.
  22 for SSH, 80 for HTTP) can be genuinely informative (some attacks target specific
  services), so this is a "keep, but think about it" case rather than an automatic
  removal — explain your reasoning either way.

When in doubt, ask: *"Would this column still be available and meaningful for a brand
new, real-time network flow the model has never seen before?"* If not, it's a leakage
risk.
