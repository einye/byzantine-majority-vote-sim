# Distributed Systems Simulation (Byzantine Generals Lite)

A minimal, educational simulation of **a one-shot majority vote** built with Python's standard `socket` and `threading` libraries. Four processes (P, Q, R, S) communicate over local TCP sockets. **Process P is faulty** - it randomly chooses between `attack` and `retreat`. The honest processes try to reach a majority vote, but the presence of a single faulty node can disrupt the outcome.

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
```
## Known Limitations (and why they make good discussion)
This is a teaching demo, not a production consensus protocol. It intentionally leaves out several essential pieces:

| **Missing piece** | **Consequence** |
|---|---|
| **Authentication** | Any process could impersonate another |
| **Message signing** | P can't be proven to have sent a specific command |
| **Ordered rounds / locking** | Threads can interleave unpredictably; some nodes may read `responses` mid-write |
| **Persistent state** | `responses` is reset only on script restart |
| **Retry / timeout handling** | If a node is offline, `send_message` crashes |
| **Dedup** | A process can be counted multiple times per round |
| **Leader election** | There's no tiebreaker; ties default to whichever is found first |

## Known Issues

- Shared responses dict is not thread-safe. Multiple server threads write to it concurrently. A Lock would fix this.
- send_message has no timeout. If a process isn't listening, the client hangs indefinitely.
- Threads are daemons, so when the main loop ends (Ctrl+C), in-flight messages may be lost. This is fine for a demo but not for correctness.
- The 3-second wait is arbitrary. On a slow machine, some messages may not arrive in time.