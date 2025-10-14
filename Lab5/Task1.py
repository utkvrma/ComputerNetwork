import random
import time

NUM_FRAMES = 5
LOSS_PROBABILITY = 0.3
TIMEOUT = 2

def send_frame(frame_number):
    print(f"Sending Frame {frame_number}")
    if random.random() < LOSS_PROBABILITY:
        print(f"Frame {frame_number} lost, retransmitting ...")
        return False
    return True

def receive_ack(frame_number):
    time.sleep(1)
    if random.random() < LOSS_PROBABILITY:
        print(f"ACK {frame_number} lost, retransmitting Frame {frame_number} ...")
        return False
    print(f"ACK {frame_number} received")
    return True

frame_number = 0
while frame_number < NUM_FRAMES:
    sent = send_frame(frame_number)
    if not sent:
        time.sleep(TIMEOUT)
        continue

    ack_received = receive_ack(frame_number)
    if not ack_received:
        time.sleep(TIMEOUT)
        continue

    frame_number += 1
