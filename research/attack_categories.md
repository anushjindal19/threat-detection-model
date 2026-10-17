# Attack Categories in CICIDS2017

CICIDS2017 was built by the Canadian Institute for Cybersecurity by running real attack
tools against a small simulated network over 5 days, while also generating normal
("benign") background traffic. Each network flow in the dataset is labelled with what it
actually was.

This file explains what each category generally means, in plain language. **The exact
label spelling in your CSV file (e.g. `BENIGN`, `DDoS`, `PortScan`) can vary slightly
between file versions — always confirm the real label strings yourself with:**

```python
df["Label"].value_counts()
```

**Do not assume a label exists until you've seen it in your actual data.**

---

### BENIGN
Normal, everyday network activity — a user browsing, downloading a file, checking email,
etc. This is the "not an attack" class, and in most captured files it is the large
majority of the traffic.

### DoS (Denial of Service)
Traffic designed to overwhelm a service (e.g. a web server) with more requests than it
can handle, so real users can't get through. CICIDS2017 includes several DoS tool
variants (e.g. Hulk, GoldenEye, Slowloris, Slowhttptest) — you may see these as separate
sub-labels rather than one single "DoS" label.

### DDoS (Distributed Denial of Service)
The same idea as DoS, but the flood of traffic comes from many sources at once instead
of one, making it harder to block by simply blocking a single IP address.

### Port Scan
Traffic that systematically probes a range of ports on a target machine to discover
which services are running and might be exploitable. This is usually a *reconnaissance*
step an attacker takes before a real attack, not an attack in itself.

### Brute Force (FTP-Patator / SSH-Patator)
Repeated, automated login attempts (many different username/password combinations)
trying to guess valid credentials for a service like FTP or SSH.

### Web Attack
A group of attacks targeting web applications specifically, such as:
- **Brute Force** — guessing website login credentials.
- **XSS (Cross-Site Scripting)** — injecting malicious scripts into web pages viewed by
  other users.
- **SQL Injection** — inserting malicious SQL code through a web form to manipulate a
  database.

### Bot(net)
Traffic from a machine that has been infected with malware and is now controlled
remotely as part of a "botnet," often used to launch further attacks or send spam.

### Infiltration
Traffic representing an attacker who has already gained a foothold inside the network
(e.g. via a malicious file/exploit) and is now operating from within, rather than
attacking from outside.

### Heartbleed
Traffic exploiting the specific "Heartbleed" vulnerability (CVE-2014-0160) in older
versions of OpenSSL, which could leak memory contents (potentially including passwords
or private keys) from a vulnerable server.

---

## Why this matters for the project

1. **Don't merge classes blindly.** "DoS Hulk" and "DoS Slowloris" are both denial-of-service
   attacks, but they behave very differently at the network level. Whether to group them
   into one "DoS" class or keep them separate is a real modelling decision — document
   whichever choice you make and why.
2. **Class imbalance is expected.** BENIGN traffic will vastly outnumber most attack
   types, and some attack types (e.g. Heartbleed) may have only a handful of samples in
   a single day's file. This affects how you should read accuracy and F1 later.
3. **These descriptions are general background**, sourced from the public CICIDS2017
   documentation and the original paper (see `references.md`). Cite that paper properly
   in `literature_review.md` rather than just this file.
