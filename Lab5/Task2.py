import random
import time

TOTAL_FRAMES = 10
WINDOW_SIZE = 4
LOSS_PROBABILITY = 0.2
TIMEOUT = 2

base = 0
next_seq = 0
acked = -1

def send_frames(start, end):
    for i in range(start, end + 1):
        print(f"Sending Frame {i}")

def simulate_ack(frame_number):
    if random.random() < LOSS_PROBABILITY:
        print(f"Frame {frame_number} lost, retransmitting frames {frame_number} to {min(frame_number + WINDOW_SIZE - 1, TOTAL_FRAMES - 1)}")
        return False
    print(f"ACK {frame_number} received")
    return True

while base < TOTAL_FRAMES:
    end = min(base + WINDOW_SIZE - 1, TOTAL_FRAMES - 1)
    send_frames(base, end)
    time.sleep(1)

    for i in range(base, end + 1):
        if simulate_ack(i):
            acked = i
        else:
            time.sleep(TIMEOUT)
            break

    if acked >= base:
        base = acked + 1
        next_seq = base
