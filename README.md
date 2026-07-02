# PyNIDS
Network Intrusion Detection System that implements the Scapy Python
library for packet capture and analysis and machine learning
(Isolation Forest) for anomaly detection.

## 1. How it works

The model is first trained on a safe and normal connection
(a must!) to ensure proper training and accurate results. After this you will no longer
need to retrain the model. After the model is trained the detection system will start.
It captures packets and groups them by connection (both end ports and IPs are the same)
in a "flow". These flows have a maximum duration of 30 seconds of traffic, at the end of
which they are sent to the model for analysis. The model generates a score based on its
training to judge whether the connection is normal or not. If the score is too low, it will
display a simplified alert in the console and save the full alert with as much
detail as possible in a JSON file. Whether someone is watching the program or not, any
anomaly is saved in the JSON file and can only be removed by the user.

## 2. Architecture

| File            | Responsibility                                   |
|-----------------|--------------------------------------------------|
| `main.py`       | Orchestrates all modules and manages threading   |
| `capture.py`    | Captures raw packets using Scapy                 |
| `flow.py`       | Groups packets into flows by connection          |
| `features.py`   | Extracts numerical features from each flow       |
| `detector.py`   | Isolation Forest model — training and detection  |
| `dashboard.py`  | Live terminal dashboard using rich               |
| `alert.py`      | Formats, displays, and logs alerts to JSON       |

## 3. Installation and Requirements

Install all .py files and be sure the following libraries are installed: time, scapy, collections, numpy, pickle, os, sklearn, json, datetime, rich, threading

## 4. How to run it

i. Find your network interface name :
- Linux : `ip a`
- Windows : `ipconfig`
- macOS : `ifconfig`

ii. Set the `INTERFACE` variable in `main.py` to your interface (e.g. `eth0`)

iii. Start the program with root privileges

iv. Enter the training phase — ensure normal data traffic to have the model
as accurate as possible. This phase is a one time thing and you
will never need to do it again unless you want to retrain.

v. When the model is trained the detection system will start automatically.

vi. All alerts will be displayed briefly in the console
and permanently in the JSON file with as much detail as needed.

vii. To stop the program press `Ctrl+C` in the terminal.

## 5. Limitations

This project presents a number of limitations including :

i. The model is not very intelligent and can easily give wrong predictions
if not trained properly — it is heavily dependent on the training phase, which is long
yet may not always produce accurate results.

ii. It is easy to have false positives, as normal traffic can sometimes be flagged as
anomalies.

iii. This code is not up to date and will fail when faced with modern intrusion techniques.
It is a proof of concept.
