# VisageLab

[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/ci.yml)
![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green)

A small, **consent-based** face recognition toolkit built on OpenCV only
(Haar detection + LBPH recognition). No dlib, no cmake, no model downloads.

It is built as a **series**: every part is a git tag you can check out and run
([docs/SERIES.md](docs/SERIES.md)). The project started from studying an existing open-source
template and redesigning it ([docs/REVERSE_ENGINEERING.md](docs/REVERSE_ENGINEERING.md)).

## Install

```bash
pip install -r requirements.txt      # opencv-contrib-python, numpy, streamlit, pandas
# or, as a command:  pip install -e .   -> gives you the `visagelab` command
python -m visagelab doctor           # checks the install and tells you how to fix problems
```

`opencv-contrib-python` is required (the `cv2.face` module lives in contrib). If you see
`module 'cv2' has no attribute 'face'`, run `doctor`: it checks Python, OpenCV, `cv2.face`, the Haar
files, your data folder and (with `--camera`) the webcam, and prints the fix for anything wrong.
The usual cause is having `opencv-python` and `opencv-contrib-python` installed together: keep
only the contrib one.

## Quick start

```bash
# 1. Enroll (consent is mandatory and recorded)
python -m visagelab enroll Alice a1.jpg a2.jpg a3.jpg --consent --note "verbal, 15 Oct"
python -m visagelab enroll Bob --camera --shots 5 --consent       # webcam, SPACE = capture

# 2. Identify
python -m visagelab identify                                      # webcam, q to quit
python -m visagelab identify --source photo.jpg --output out.jpg
python -m visagelab identify --source clip.mp4 --output out.mp4 --log seen.csv

# 3. Manage
python -m visagelab list
python -m visagelab remove Bob --yes
```

| Command | What it does |
|---|---|
| `enroll NAME [photos] --consent` | register a person (photos and/or webcam), with quality checks |
| `identify` | recognise faces in a webcam, image or video |
| `list` / `remove NAME` | see or delete enrolled people |
| `train` | force a model rebuild (normally automatic) |
| `selftest` | estimate accuracy from your gallery alone (leave-one-out) |
| `evaluate FOLDER` | measure accuracy on labelled test photos |
| `bench IMAGE` | time each pipeline stage, estimate FPS |
| `doctor` | diagnose the installation |

## Two web front-ends

* **Streamlit lab** — `streamlit run app.py`. Tabs: Enroll (upload / webcam) · Identify ·
  Evaluate (accuracy + threshold chart) · Gallery.
* **Browser app, no install** — open `web/index.html`: live webcam recognition, enrollment and an
  accuracy tester entirely in the browser (nothing uploaded). It uses its own lighter
  detector/matcher: a demo companion, not a port of the Python tool ([web/README.md](web/README.md)).

## Enrollment quality gate

Bad enrollment photos hurt recognition for as long as they stay in the gallery, so photos are
checked first and rejected with a reason:

```
[reject] a2.jpg: blurry (sharpness 0.0030 < 0.008)
[reject] a3.jpg: too dark (31 < 45); low contrast (14 < 20)
[dup]    1 photo(s) skipped: identical to one already used
```

Checks: face size, blur (Laplacian variance divided by contrast squared, so dim photos are not
mistaken for blurry ones), brightness, contrast, and duplicates (also against photos already
enrolled). Override with `--no-quality-check`. The limits live in `Settings` and were calibrated
on one public-domain portrait with synthetic degradations, so tune them on your own camera.

## Measure it before you trust it

**No test photos yet?** `python -m visagelab selftest` hides one photo at a time (genuine trials)
and one whole person at a time (impostor trials), so a gallery of 2+ people gives accuracy, FRR
and FAR immediately. It is optimistic (enrolled photos come from one sitting). With a single person
there are no impostors, and the tool says it cannot recommend a threshold.

**Realistic numbers:** put labelled photos in folders (`unknown` holds people who are **not** enrolled):

```
testset/Alice/*.jpg    testset/Bob/*.jpg    testset/unknown/*.jpg
```
```bash
python -m visagelab evaluate testset --csv report.csv --json report.json
```
You get accuracy, FRR (genuine people rejected or mis-named) and FAR (strangers accepted) for each
threshold, a per-person table (recall / precision), a confusion matrix and a recommended threshold.
Defaults (`threshold 55`, `margin 6`) came from a tiny test; **re-tune on your own data.**

## How it works

```
frame -> Haar face detect (confidence-ranked) -> eye-based align + CLAHE + ellipse mask
      -> LBPH distance to every enrolled person
      -> accept only if  best < threshold  AND  best beats runner-up by `margin`
      -> (video) IoU tracker + majority vote over 7 frames -> overlay
```

* **threshold** — LBPH distance; lower = closer. Lower threshold = stricter.
* **margin** — guards against look-alikes; ignored when only one person is enrolled.
* The model rebuilds itself automatically whenever the gallery changes.

More detail and a module diagram: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Privacy and responsible use

* Enrolling needs `--consent`; the time and your note are saved in `data/people.json`.
* Everything stays on your machine in `data/` (it is git-ignored; never commit it).
* `identify --log` records who was seen and when. Tell people if you use it.
* Not suitable for security, access control, or any decision that affects people.

## Development

```bash
pip install -r requirements-dev.txt && pip install -e . --no-deps
python -m pytest -q        # 67 tests, mostly on synthetic faces; real-photo tests need scikit-image
ruff check .
```
See [CONTRIBUTING.md](CONTRIBUTING.md) and [CHANGELOG.md](CHANGELOG.md).

## Limits

Haar + LBPH is simple and fast but sensitive to pose and lighting; it is weaker than modern
embedding models. A DNN backend (YuNet detector + SFace embeddings, both shipped with OpenCV) is the
planned next step: it needs a backend interface in the pipeline and a model-download command, not
just a swap of two classes (see the roadmap in [docs/SERIES.md](docs/SERIES.md)).
Webcam paths and the Streamlit app could not be exercised in the automated build environment.
