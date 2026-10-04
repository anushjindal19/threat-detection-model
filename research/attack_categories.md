# Attack Categories in CICIDS2017

CICIDS2017 was built by the Canadian Institute for Cybersecurity by running real attack
tools against a small simulated network over 5 days, while also generating normal
("benign") background traffic. Each network flow in the dataset is labelled with what it
actually was.

## Labels in the files used

**Wednesday** (`Wednesday-workingHours.pcap_ISCX.csv`, notebooks 01-05), raw file:

| Label | Flows | Share |
|---|---:|---:|
| BENIGN | 440,031 | 63.52% |
| DoS Hulk | 231,073 | 33.36% |
| DoS GoldenEye | 10,293 | 1.49% |
| DoS slowloris | 5,796 | 0.84% |
| DoS Slowhttptest | 5,499 | 0.79% |
| Heartbleed | 11 | 0.0016% |

The four DoS attacks target the web server 192.168.10.50. Heartbleed targets a different
machine, 192.168.10.51, on port 444.

**Friday afternoon** (`Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`, notebook 07),
after the same cleaning as notebook 02: 95,068 BENIGN and 128,014 DDoS. The DDoS was
sent with the LOIT tool from three attacking machines against port 80 of the same web
server (192.168.10.50) as Wednesday's DoS attacks.

---

## Categories

### BENIGN
Normal, everyday network activity: a user browsing, downloading a file, checking email,
etc. This is the "not an attack" class, and in most captured files it is the large
majority of the traffic.

### DoS (Denial of Service)
Traffic designed to overwhelm a service (e.g. a web server) with more requests than it
can handle, so real users can't get through. CICIDS2017 includes several DoS tools,
which appear as separate labels: Hulk and GoldenEye flood the server with HTTP requests,
while slowloris and Slowhttptest hold many connections open by sending data very slowly.

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
- **Brute Force**: guessing website login credentials.
- **XSS (Cross-Site Scripting)**: injecting malicious scripts into web pages viewed by
  other users.
- **SQL Injection**: inserting malicious SQL code through a web form to manipulate a
  database.

### Bot(net)
Traffic from a machine that has been infected with malware and is now controlled
remotely as part of a "botnet," often used to launch further attacks or send spam.

### Infiltration
Traffic representing an attacker who has already gained a foothold inside the network
(e.g. via a malicious file/exploit) and is now operating from within, rather than
attacking from outside.

### Heartbleed
Traffic exploiting the "Heartbleed" vulnerability (CVE-2014-0160) in older versions of
OpenSSL, which could leak memory contents (potentially including passwords or private
keys) from a vulnerable server.

---

## How this shapes the project

1. **The DoS classes are kept separate.** "DoS Hulk" and "DoS slowloris" are both
   denial-of-service attacks, but they behave very differently at the network level
   (a fast flood versus slow, mostly idle connections). Keeping them as separate classes
   shows which attack a shrinking tree loses first.
2. **The classes are heavily imbalanced.** BENIGN and DoS Hulk make up about 97% of the
   Wednesday rows, so plain accuracy says little about the rare attacks. Results are
   reported as per-class recall and macro F1.
3. **Heartbleed is too rare to score reliably.** All 11 rows survive cleaning (9 in the
   training set, 2 in the test set), so scores are also reported without Heartbleed.

The category descriptions are general background taken from the public CICIDS2017
documentation and the original paper (see `references.md`).
