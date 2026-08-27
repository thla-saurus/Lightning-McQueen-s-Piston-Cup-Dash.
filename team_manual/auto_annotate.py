"""
auto_annotate.py — turns "draw a box by hand on every photo" into
"run this script, spot-check the results."

Uses MediaPipe's HandLandmarker (21 hand keypoints, runs on CPU, no GPU
needed, no internet after the first run) to do two things automatically,
per image:

  1. BOUNDING BOX: min/max of the 21 landmark (x,y) positions, padded a
     bit, becomes the YOLO box -- no manually dragging a rectangle.
  2. CLASS LABEL: counts which fingers are extended vs curled from the
     landmark geometry, and classifies open_balm (4-5 fingers extended)
     vs peace_sign (exactly index+middle extended) -- no manually
     clicking "this one's a palm" required either.

⚠️ CLASS ID NUMBERS ARE CONFIRMED (0=peace_sign, 1=open_balm, per Zeyad's
data.yaml) and already set correctly below. If Zeyad ever retrains with a
different order, these two constants are the only thing that needs updating.

Setup (one-time, downloads MediaPipe's ~8MB hand model on first run):
    pip install mediapipe opencv-python

Usage:
    python auto_annotate.py --images_dir raw_submissions --out_dir .

What you still have to do by hand: only whatever lands in the `review/`
folder this script produces -- photos where no hand was detected, or the
gesture was ambiguous. Usually well under 10% of your photos. Everything
else needs zero manual box-drawing.
"""
import argparse
import os
import shutil
from dataclasses import dataclass
from typing import List, Optional, Tuple

import cv2
import numpy as np

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
MODEL_PATH = os.path.join(os.path.dirname(__file__), "hand_landmarker.task")

# MediaPipe's 21-landmark indices we need
WRIST = 0
THUMB_TIP, THUMB_IP = 4, 3
FINGER_TIPS = {"index": 8, "middle": 12, "ring": 16, "pinky": 20}
FINGER_PIPS = {"index": 6, "middle": 10, "ring": 14, "pinky": 18}

# ✅ CONFIRMED by Zeyad directly (checked against his data.yaml):
#     0 = peace_sign
#     1 = open_balm
STEER_CLASS_ID = 1    # open_balm
BOOST_CLASS_ID = 0    # peace_sign
STEER_CLASS_NAME = "open_balm"
BOOST_CLASS_NAME = "peace_sign"


def _ensure_model():
    if os.path.exists(MODEL_PATH):
        return
    print("Downloading MediaPipe hand-landmark model (one-time, ~8MB)...")
    import urllib.request
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


def _make_landmarker():
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision
    _ensure_model()
    options = vision.HandLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=MODEL_PATH),
        num_hands=1,
        min_hand_detection_confidence=0.5,
    )
    return vision.HandLandmarker.create_from_options(options)


@dataclass
class GestureResult:
    class_id: Optional[int]     # None if ambiguous / low confidence -> needs manual review
    class_name: str
    bbox_norm: Optional[Tuple[float, float, float, float]]  # (x_center, y_center, w, h), all 0-1
    fingers_extended: int


def _finger_extended(landmarks, tip_idx: int, pip_idx: int) -> bool:
    """A finger is 'extended' if its tip is meaningfully further from the
    wrist than its PIP joint is -- orientation-independent (works whether
    the hand is upright, sideways, or rotated)."""
    wrist = landmarks[WRIST]
    tip, pip = landmarks[tip_idx], landmarks[pip_idx]
    dist_tip = ((tip[0] - wrist[0]) ** 2 + (tip[1] - wrist[1]) ** 2) ** 0.5
    dist_pip = ((pip[0] - wrist[0]) ** 2 + (pip[1] - wrist[1]) ** 2) ** 0.5
    return dist_tip > dist_pip * 1.15


def _thumb_extended(landmarks) -> bool:
    wrist = landmarks[WRIST]
    tip, ip = landmarks[THUMB_TIP], landmarks[THUMB_IP]
    dist_tip = ((tip[0] - wrist[0]) ** 2 + (tip[1] - wrist[1]) ** 2) ** 0.5
    dist_ip = ((ip[0] - wrist[0]) ** 2 + (ip[1] - wrist[1]) ** 2) ** 0.5
    return dist_tip > dist_ip * 1.1


def classify_gesture(landmarks: List[Tuple[float, float]]) -> GestureResult:
    """landmarks: 21 (x,y) points, normalized 0-1 (MediaPipe's native
    output format).

    STEER (open_balm) = 4-5 fingers extended. BOOST (peace_sign) = exactly
    index + middle extended, ring + pinky curled. Anything else (fist, 1
    finger, 3 fingers) is flagged for manual review rather than guessed
    at -- a wrong auto-label is worse than no label."""
    extended = {name: _finger_extended(landmarks, FINGER_TIPS[name], FINGER_PIPS[name])
                for name in FINGER_TIPS}
    thumb = _thumb_extended(landmarks)
    n_extended = sum(extended.values()) + (1 if thumb else 0)

    xs = [p[0] for p in landmarks]
    ys = [p[1] for p in landmarks]
    pad = 0.05
    x_min, x_max = max(0, min(xs) - pad), min(1, max(xs) + pad)
    y_min, y_max = max(0, min(ys) - pad), min(1, max(ys) + pad)
    bbox = ((x_min + x_max) / 2, (y_min + y_max) / 2, x_max - x_min, y_max - y_min)

    if n_extended >= 4:
        return GestureResult(STEER_CLASS_ID, STEER_CLASS_NAME, bbox, n_extended)
    if extended["index"] and extended["middle"] and not extended["ring"] and not extended["pinky"]:
        return GestureResult(BOOST_CLASS_ID, BOOST_CLASS_NAME, bbox, n_extended)
    return GestureResult(None, "AMBIGUOUS", bbox, n_extended)


def process_folder(images_dir: str, out_images_dir: str, out_labels_dir: str, review_dir: str):
    os.makedirs(out_images_dir, exist_ok=True)
    os.makedirs(out_labels_dir, exist_ok=True)
    os.makedirs(review_dir, exist_ok=True)

    landmarker = _make_landmarker()
    import mediapipe as mp

    stats = {"labeled": 0, "no_hand": 0, "ambiguous": 0}

    for root, _, files in os.walk(images_dir):
        for fname in files:
            if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            path = os.path.join(root, fname)
            img_bgr = cv2.imread(path)
            if img_bgr is None:
                continue
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
            result = landmarker.detect(mp_image)

            if not result.hand_landmarks:
                stats["no_hand"] += 1
                shutil.copy(path, os.path.join(review_dir, fname))
                continue

            landmarks = [(lm.x, lm.y) for lm in result.hand_landmarks[0]]
            gesture = classify_gesture(landmarks)

            if gesture.class_id is None:
                stats["ambiguous"] += 1
                shutil.copy(path, os.path.join(review_dir, fname))
                continue

            shutil.copy(path, os.path.join(out_images_dir, fname))
            label_path = os.path.join(out_labels_dir, os.path.splitext(fname)[0] + ".txt")
            xc, yc, w, h = gesture.bbox_norm
            with open(label_path, "w") as f:
                f.write(f"{gesture.class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")
            stats["labeled"] += 1

    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images_dir", default="raw_submissions")
    parser.add_argument("--out_dir", default=".")
    args = parser.parse_args()

    stats = process_folder(
        images_dir=args.images_dir,
        out_images_dir=os.path.join(args.out_dir, "images", "auto_labeled"),
        out_labels_dir=os.path.join(args.out_dir, "labels", "auto_labeled"),
        review_dir=os.path.join(args.out_dir, "review"),
    )
    total = sum(stats.values())
    print(f"\nAuto-labeled: {stats['labeled']}/{total}")
    print(f"No hand detected: {stats['no_hand']}/{total}  (blurry/out of frame -- probably just delete these)")
    print(f"Ambiguous gesture: {stats['ambiguous']}/{total}  -> copied to review/, label these by hand in Roboflow")
    print(f"\n~{100*stats['labeled']//max(total,1)}% of photos needed zero manual work.")


if __name__ == "__main__":
    main()
