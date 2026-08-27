# Dataset Collection Manual — Task 9.2 Gesture Dataset

For everyone on the team. Read this fully before recording anything —
there's a specific reason behind almost every instruction below, not
arbitrary rules. This has already been tested end-to-end by one team
member (78/82 photos auto-labeled correctly, verified) — follow it exactly
and it'll work the same for you.

---

## 0. Why this matters, concretely

The first model (trained on one person's photos only) scored:
- Combined F1: **0.53** (weak)
- Confusion matrix: `peace_sign` predicted 69 times when the real answer
  was `open_balm` — the two gestures were constantly mixed up
- One test photo got **zero detections at all**

Not a code bug — a small/single-source dataset problem. The fix is
everyone contributing diverse photos, then retraining. That's what this
manual walks you through.

---

## 1. The exact class names — copy exactly, do not "fix" them

```
open_balm
peace_sign
```

**Yes, "balm" not "palm."** This typo is already baked into the trained
model, the confusion matrix, and every existing label. If you label new
photos as `open_palm`, you create a **third, unrecognized class** — your
photos won't merge with the existing dataset, they'll corrupt it. Match
the typo exactly. Fixing it requires a full team decision + relabeling
everything from scratch, not something to do on your own.

## 2. The confirmed class ID numbers

```
0 = peace_sign
1 = open_balm
```

Confirmed directly from the model's `data.yaml`. Both scripts in this
manual already have this baked in correctly — you don't need to edit
anything before running them.

---

## 3. Setup (one-time)

```bash
python -m venv .venv
```
Windows:
```powershell
.venv\Scripts\Activate.ps1
```
Mac/Linux:
```bash
source .venv/bin/activate
```
You'll know it worked when your terminal prompt shows `(.venv)` at the
start.

Then, with the venv active:
```bash
pip install opencv-python mediapipe
```

---

## 4. Recording your clips (video method — faster than individual photos)

```bash
python capture_clip.py --name yourname --gesture open_balm --seconds 15
python capture_clip.py --name yourname --gesture peace_sign --seconds 15
```

A countdown starts, then a live camera window opens with a red "REC"
counter. **Hold the gesture and slowly move your hand around** — closer,
farther, tilted, side to side — for the full 15 seconds. That natural
movement gives you angle/distance diversity for free, instead of posing
for dozens of individual photos. Each clip auto-extracts roughly 45 frames.

**Minimum diversity checklist per person** (this is the actual thing being
tested, not raw photo count):
- [ ] 2+ different lighting setups
- [ ] 3+ hand angles/distances from the camera
- [ ] 1+ different background
- [ ] Roughly equal photos of both gestures

Your photos land in `raw_submissions/yourname_open_balm/` and
`raw_submissions/yourname_peace_sign/`.

---

## 5. Auto-annotation — do this before touching any manual tool

**Don't hand-label your photos.** Run this instead:

```bash
python auto_annotate.py --images_dir raw_submissions --out_dir .
```

This uses MediaPipe's hand-tracking model to find your hand in every
photo, automatically:
1. Computes the bounding box directly from 21 hand-keypoint positions
   (no manual dragging a rectangle).
2. Counts extended vs. curled fingers to decide `open_balm` (4-5 fingers
   extended) vs. `peace_sign` (exactly index+middle extended) — no manual
   clicking either.
3. Writes a standard YOLO-format `.txt` label file per image, automatically.

First run downloads a small (~8MB) model file — needs internet once, then
works offline.

**You'll see a printout like this when it's done:**
```
Auto-labeled: 78/82
No hand detected: 3/82  (blurry/out of frame -- probably just delete these)
Ambiguous gesture: 1/82  -> copied to review/, label these by hand

~95% of photos needed zero manual work.
```

### What "no hand detected" and "ambiguous" actually mean — read this part

The script is deliberately cautious. It will **never guess** at a label it
isn't confident about — a wrong auto-label silently teaches the model the
wrong thing, which is worse than no label at all. Instead, anything it's
unsure about gets copied into a `review/` folder for a human to check:

- **"No hand detected"** — MediaPipe couldn't find a hand in the frame at
  all. Usually a blurry frame, motion blur, hand partially out of frame,
  or bad lighting. **Safe to just delete these** — there's nothing to
  recover, the information isn't there.
- **"Ambiguous gesture"** — a hand WAS found, but the finger pattern
  wasn't clearly `open_balm` (4-5 fingers) or clearly `peace_sign` (exactly
  index+middle). This happens on a fist, a hand mid-transition between
  poses, or an unusual angle where fingers overlap in the camera's view.
  **Look at these yourself** — if it's obviously one of the two real
  gestures, label it by hand (see Section 6). If it's genuinely neither
  (a fist, a wave, anything else), delete it.

This is normal and expected — you should see roughly 90-95% auto-labeled
and a small handful in `review/`. If you're seeing way more than ~10% in
`review/`, something's likely off with your lighting/framing — re-record
rather than force-labeling bad photos.

---

## 6. Manually labeling the `review/` leftovers

Only for the small number of photos that landed in `review/`. Use
**[Roboflow](https://roboflow.com/)** (free, browser-based, nothing to
install):

1. Create a free account, create a new project, select "Object Detection."
2. Upload your `review/` folder.
3. For each image: draw a tight box around just the hand (not the whole
   arm, not extra background). Assign the class label — `open_balm` or
   `peace_sign`, exactly as in Section 1. Skip/delete any image that
   isn't a real gesture at all.
4. Optional: use Roboflow's **auto-augment** step (flip, rotate,
   brightness jitter) before exporting — multiplies your dataset size for
   free.
5. **Export in YOLO format.** One `.txt` label file per image, same
   naming convention as the auto-labeled set.

---

## 7. Verifying your labels before you submit them (don't skip this)

Cheap insurance against a silent bug wrecking the whole submission. Pick
one file from each gesture and check it:

```bash
cat labels/auto_labeled/<any_open_balm_file>.txt
cat labels/auto_labeled/<any_peace_sign_file>.txt
```
(Windows PowerShell: use `Get-Content` instead of `cat`.)

**What correct looks like:**
```
1 0.381185 0.597728 0.320101 0.463245     <- open_balm file: MUST start with 1
0 0.316093 0.631008 0.224292 0.503200     <- peace_sign file: MUST start with 0
```
All 4 decimal numbers should be between 0 and 1. If either file starts
with the wrong number, or you see numbers outside 0–1, **stop and ask
before submitting** — something is misconfigured.

Also confirm your image and label counts actually match:
```bash
ls images/auto_labeled | wc -l
ls labels/auto_labeled | wc -l
```
(Windows: `(Get-ChildItem images\auto_labeled).Count` and same for labels.)
Both numbers should be identical.

---

## 8. Handing off your submission

Once verified, you have three sets of output for your review to decide on:
- `images/auto_labeled/` + `labels/auto_labeled/` — ready to go as-is
- Whatever you kept + manually labeled from `review/` — add to the same
  merged set
- Whatever you deleted from `review/` — just don't submit those, no
  further action needed

Push or send your final `images/` + `labels/` folders to whoever's
merging submissions before the next training run. Flag clearly if
anything about your class IDs looked off during Section 7's check —
that's the one thing that can't be silently merged, it has to be caught
first.

---

## Quick troubleshooting

- **`pip install` says "already satisfied" but nothing works** — you
  probably installed to your system Python instead of the venv. Make sure
  `(.venv)` is showing in your prompt before installing anything.
- **`python capture_clip.py` says "can't open file"** — you're not in the
  right folder. Run `ls` (or `dir` on Windows) and confirm you see
  `capture_clip.py` listed before running it.
- **Auto-annotate crashes with a mediapipe import error** — note the exact
  error message and mediapipe version (`pip show mediapipe`), then ask
  before proceeding — don't guess-fix it yourself, the fix depends on
  exactly what changed.
