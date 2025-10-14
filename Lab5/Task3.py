#!/usr/bin/env python3
"""
TCP Congestion Control Simulation
Phases: Slow Start, Congestion Avoidance, Timeout (loss)
Plot: cwnd vs rounds
Usage:
    python congestion_control.py --rounds 80 --seed 123 --p-loss 0.08 --ssthresh 16
"""
import argparse, random
import matplotlib.pyplot as plt

def simulate(rounds=80, p_loss=0.08, init_cwnd=1.0, ssthresh=16.0, rng=None):
    if rng is None:
        rng = random.Random()
    cwnd = init_cwnd
    cwnd_hist = []
    phase_hist = []
    for r in range(rounds):
        # Record current cwnd
        cwnd_hist.append(cwnd)
        # Loss event?
        loss = rng.random() < p_loss
        if loss:
            # Timeout / loss -> multiplicative decrease
            ssthresh = max(2.0, cwnd / 2.0)
            cwnd = 1.0
            phase_hist.append("LOSS")
            continue
        # ACK success path
        if cwnd < ssthresh:
            # Slow start: exponential (add 1 per RTT)
            cwnd = cwnd + 1.0
            phase_hist.append("SS")
        else:
            # Congestion avoidance: additive increase (1/cwnd per ACK ~ 1 per RTT)
            cwnd = cwnd + 1.0 / cwnd
            phase_hist.append("CA")
    return cwnd_hist, phase_hist

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=80)
    ap.add_argument("--seed", type=int, default=123)
    ap.add_argument("--p-loss", type=float, default=0.08)
    ap.add_argument("--ssthresh", type=float, default=16.0)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    cwnd_hist, phase_hist = simulate(args.rounds, args.p_loss, 1.0, args.ssthresh, rng)

    # Plot
    plt.figure(figsize=(8,4.5))
    plt.plot(range(len(cwnd_hist)), cwnd_hist, marker='o', linewidth=1)
    plt.xlabel("Transmission Round (RTT)")
    plt.ylabel("cwnd (segments)")
    plt.title("TCP Congestion Control: cwnd vs Rounds")
    plt.tight_layout()
    plt.savefig("cwnd_plot.png", dpi=150)

    # Also print a compact table to stdout
    print("Round\tcwnd\tPhase")
    for i, (c, ph) in enumerate(zip(cwnd_hist, phase_hist)):
        print(f"{i}\t{c:.2f}\t{ph}")

if __name__ == "__main__":
    main()
