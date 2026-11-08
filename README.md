# Distributed Systems Simulation (Byzantine Generals Lite)

A minimal, educational simulation of **a one-shot majority vote** built with Python's standard `socket` and `threading` libraries. Four processes (P, Q, R, S) communicate over local TCP sockets. **Process P is faulty** — it randomly chooses between `attack` and `retreat`. The honest processes try to reach a majority vote, but the presence of a single faulty node can disrupt the outcome.

## Requirements

- **Python 3.8+**
- No external dependencies

## Installation & Usage

```bash
# Clone the repo
git clone https://github.com/einye/byzantine-majority-vote-sim.git
cd byzantine-majority-vote-sim

# Run the simulation
python byzantine-majority-vote.py