"""
capture_clip.py — record one short video per gesture, auto-extract frames.

Faster than posing for individual photos: hold the gesture and move your
hand around naturally while it records (angle, distance, tilt) -- that
movement gives you real diversity for free, instead of deliberately
re-posing dozens of times.

    python capture_clip.py --name yourname --gesture open_balm --seconds 15
    python capture_clip.py --name yourname --gesture peace_sign --seconds 15

⚠️ USE THESE EXACT GESTURE NAMES -- "open_balm" and "peace_sign" -- not
"open_palm" or "steer"/"boost" or anything else. "balm" is a typo baked
into Zeyad's already-trained model; matching it exactly means your new
photos merge cleanly into the SAME two classes the model already knows,
instead of accidentally creating a third, unrecognized class.
"""
import argparse
import os
import time

import cv2

VALID_GESTURES = ("open_balm", "peace_sign")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True, help="your first name, lowercase, no spaces")
    parser.add_argument("--gesture", required=True, choices=VALID_GESTURES)
    parser.add_argument("--out", default="raw_submissions")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--seconds", type=float, default=15.0)
    parser.add_argument("--fps_extract", type=float, default=3.0,
                         help="frames extracted per second of footage")
    args = parser.parse_args()

    out_dir = os.path.join(args.out, f"{args.name}_{args.gesture}")
    os.makedirs(out_dir, exist_ok=True)
    existing = len([f for f in os.listdir(out_dir) if f.endswith(".jpg")])

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera {args.camera}")

    print(f"Get ready: {args.gesture} gesture, recording in 3 seconds...")
    print("Move your hand around slowly once recording starts -- angles, distance, tilt.")
    time.sleep(3)

    interval = 1.0 / args.fps_extract
    last_capture = 0.0
    start = time.time()
    count = existing

    while time.time() - start < args.seconds:
        ok, frame = cap.read()
        if not ok:
            break

        elapsed = time.time() - start
        remaining = args.seconds - elapsed
        preview = frame.copy()
        cv2.putText(preview, f"REC  {remaining:0.1f}s left  |  saved: {count - existing}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("capture_clip.py", preview)
        cv2.waitKey(1)

        if elapsed - last_capture >= interval:
            count += 1
            path = os.path.join(out_dir, f"{args.name}_{args.gesture}_{count:04d}.jpg")
            cv2.imwrite(path, frame)
            last_capture = elapsed

    cap.release()
    cv2.destroyAllWindows()
    print(f"Done. {count - existing} frames extracted to {out_dir}")


if __name__ == "__main__":
    main()
