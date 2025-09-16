from __future__ import annotations
import argparse
import socket
import time
from typing import Tuple, Union

import cv2
import numpy as np

from common import Header, FLAG_MARKER, MAX_PAYLOAD

def split_bytes(data: bytes, chunk_size: int):
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]

def main():
    parser = argparse.ArgumentParser(description="UDP Video Streaming Server")
    parser.add_argument("--video", required=True, help="Path to video file, RTSP URL, or webcam index (int). Example: 0")
    parser.add_argument("--host", default="127.0.0.1", help="Client IP address to send packets to")
    parser.add_argument("--port", type=int, default=5000, help="Client UDP port")
    parser.add_argument("--jpeg-quality", type=int, default=70, help="JPEG quality 1-100")
    parser.add_argument("--scale", type=float, default=1.0, help="Resize factor for frames (e.g., 0.5)")
    parser.add_argument("--fps", type=float, default=0.0, help="Override FPS pacing (0 = derive from video)")
    parser.add_argument("--max-payload", type=int, default=MAX_PAYLOAD, help="Max payload bytes per UDP packet")

    args = parser.parse_args()

    # Prepare socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target: Tuple[str, int] = (args.host, args.port)

    # Open video source
    src: Union[int, str]
    try:
        src = int(args.video)
    except ValueError:
        src = args.video

    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video source: {args.video}")

    if args.fps > 0:
        fps = args.fps
    else:
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        if fps <= 1e-3:
            fps = 25.0
    frame_interval = 1.0 / float(fps)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), int(args.jpeg-quality) if hasattr(args, 'jpeg-quality') else int(args.jpeg_quality)]
    # The above is a defensive workaround in case argparse normalizes `jpeg-quality` to `jpeg_quality`

    # Fix parameter handling properly
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), int(args.jpeg_quality)]

    frame_id = 0
    print(f"[SERVER] Streaming to {target} at ~{fps:.2f} FPS, payload {args.max_payload} bytes")

    try:
        while True:
            t0 = time.time()
            ok, frame = cap.read()
            if not ok:
                print("[SERVER] End of stream or read error. Stopping.")
                break

            if args.scale and args.scale != 1.0:
                frame = cv2.resize(frame, None, fx=args.scale, fy=args.scale, interpolation=cv2.INTER_AREA)

            # Encode to JPEG
            ok, buf = cv2.imencode(".jpg", frame, encode_param)
            if not ok:
                print("[SERVER] JPEG encode failed, skipping frame")
                continue

            data = buf.tobytes()
            chunks = list(split_bytes(data, args.max_payload))
            total = len(chunks)

            for idx, payload in enumerate(chunks):
                flags = FLAG_MARKER if (idx == total - 1) else 0
                header = Header(
                    flags=flags,
                    frame_id=frame_id,
                    packet_idx=idx,
                    total_packets=total,
                    payload_size=len(payload),
                ).pack()
                sock.sendto(header + payload, target)

            frame_id += 1

            # Pace to FPS
            elapsed = time.time() - t0
            to_sleep = frame_interval - elapsed
            if to_sleep > 0:
                time.sleep(to_sleep)

    except KeyboardInterrupt:
        print("\n[SERVER] Interrupted by user. Exiting.")
    finally:
        cap.release()
        sock.close()

if __name__ == "__main__":
    main()
