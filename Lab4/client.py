from __future__ import annotations
import argparse
import socket
import time
from collections import defaultdict, deque
from typing import Dict, Tuple

import cv2
import numpy as np

from common import Header, HEADER_SIZE, FLAG_MARKER

def main():
    parser = argparse.ArgumentParser(description="UDP Video Streaming Client")
    parser.add_argument("--bind", default="0.0.0.0", help="IP address to bind")
    parser.add_argument("--port", type=int, default=5000, help="UDP port to bind")
    parser.add_argument("--timeout", type=float, default=2.0, help="Seconds to wait before dropping incomplete frames")
    parser.add_argument("--window", type=int, default=50, help="Max frames to keep in reassembly window")
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.bind, args.port))
    sock.settimeout(0.1)

    print(f"[CLIENT] Listening on {args.bind}:{args.port}")

    # Reassembly buffers
    # frame_id -> (start_time, total_packets, received_count, dict(packet_idx->bytes))
    buffers: Dict[int, Tuple[float, int, int, Dict[int, bytes]]] = {}

    last_display = time.time()

    try:
        while True:
            # Receive packets
            try:
                packet, addr = sock.recvfrom(65535)
            except socket.timeout:
                packet = None

            if packet:
                if len(packet) < HEADER_SIZE:
                    # Malformed; ignore
                    continue
                hdr = Header.unpack(packet[:HEADER_SIZE])
                if hdr.magic != b"VS" or hdr.version != 1:
                    # Unknown protocol
                    continue

                payload = packet[HEADER_SIZE:HEADER_SIZE + hdr.payload_size]

                entry = buffers.get(hdr.frame_id)
                if entry is None:
                    buffers[hdr.frame_id] = (time.time(), hdr.total_packets, 0, {hdr.packet_idx: payload})
                else:
                    start_time, total_packets, received_count, parts = entry
                    total_packets = max(total_packets, hdr.total_packets)  # be tolerant
                    if hdr.packet_idx not in parts:
                        parts[hdr.packet_idx] = payload
                        received_count += 1
                    buffers[hdr.frame_id] = (start_time, total_packets, received_count, parts)

                # If we already have all packets, assemble immediately
                start_time, total_packets, received_count, parts = buffers[hdr.frame_id]
                if len(parts) == total_packets and (total_packets > 0):
                    ordered = b"".join(parts[i] for i in range(total_packets) if i in parts)
                    show_frame(ordered)
                    # Cleanup old frames
                    for fid in list(buffers.keys()):
                        if fid <= hdr.frame_id:
                            buffers.pop(fid, None)
                    continue

            # Drop stale/incomplete frames
            now = time.time()
            to_delete = []
            for fid, (start_time, total_packets, received_count, parts) in buffers.items():
                if now - start_time > args.timeout:
                    to_delete.append(fid)
            for fid in to_delete:
                buffers.pop(fid, None)

            # Keep window size bounded
            if len(buffers) > args.window:
                # drop the oldest
                oldest = min(buffers.keys())
                buffers.pop(oldest, None)

            # UI key handling
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\n[CLIENT] Interrupted by user. Exiting.")
    finally:
        cv2.destroyAllWindows()
        sock.close()

def show_frame(jpeg_bytes: bytes):
    arr = np.frombuffer(jpeg_bytes, dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if frame is None:
        return
    cv2.imshow("UDP Video Client", frame)

if __name__ == "__main__":
    main()
