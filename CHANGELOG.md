# Changelog

All notable changes are listed here. The project follows [Semantic Versioning](https://semver.org/).

## [1.5.0] - Part 6: documentation and publishing
### Added
- README rewritten (command table, CI badge, development section); `docs/ARCHITECTURE.md` with a
  module diagram and design rules; `docs/SERIES.md` (parts, tags, roadmap, how to publish).
- `scripts/publish_series.sh`: sets your name as author on every commit, fills in `LICENSE`, points
  the badges at your repository, pushes `main` and all tags. Covered by 3 tests.
### Fixed
- README no longer claims that swapping two classes is enough for a DNN backend.
- 67 tests in total.

## [1.4.0] - Part 5: doctor and bench
### Added
- `visagelab doctor [--camera]`: checks Python, NumPy, OpenCV, `cv2.face`, Haar files, data folder,
  gallery, display support and duplicate OpenCV wheels, with a suggested fix for each problem.
  Exit code 1 only for critical failures.
- `visagelab bench IMAGE [--runs N]`: per-stage timings (mean / median / p95) and estimated FPS.
- 10 new tests (64 total).
### Known limits
- The webcam check could only be tested for the "no camera" path in the build environment.

## [1.3.0] - Part 4: better evaluation
### Added
- `visagelab selftest`: leave-one-photo-out (FRR) and leave-one-person-out (FAR) estimate from the gallery alone.
- `evaluate` and `selftest` now print a per-person table (recall, precision) and a confusion matrix.
- `--json` export with sweep, per-person stats, confusion matrix and every sample.
- `Matcher.fit()` trains in memory (used by the self-test); `train()` = `fit()` + save.
- 12 new tests (54 total).
### Fixed
- With no impostor photos every threshold scores 100%, and the old report "recommended" the strictest
  one (20). The tool now says it cannot recommend a threshold. Same fix in the Streamlit lab.

## [1.2.0] - Part 3: enrollment quality gate
### Added
- `visagelab/quality.py`: face size, blur, brightness and contrast checks, plus duplicate detection.
- `visagelab/enrollment.py`: one shared `prepare()` step used by the CLI and the web lab.
- `enroll --no-quality-check` flag; rejection reasons are printed per photo.
- Webcam enrollment refuses bad shots and shows why on screen.
- Streamlit lab: same checks, shows a warning per rejected photo.
- `Gallery.crops(name)`; new `Settings` fields (`min_sharpness`, `min_brightness`, ...).
- 10 new tests (42 total).
### Changed
- Enrolling the same photo twice no longer stores it twice.
- Exit code is 1 when no photo survives the checks (was 0 only if at least one crop existed).
### Known limits
- Thresholds were calibrated on a single photo with synthetic blur/darkness; the Streamlit and
  webcam paths could not be run in the build environment.

## [1.1.0] - Part 2: project hygiene
### Added
- GitHub Actions workflow: tests on Python 3.9-3.12, lint on every push and pull request.
- `ruff` configuration (syntax errors and unused names only, so it stays quiet).
- `CONTRIBUTING.md`, pull-request and bug-report templates.
- `requirements-dev.txt`; `dev` extra now includes `pytest` and `scikit-image`.
### Fixed
- Removed an unused import in `tracker.py` (caught by the new lint step).

## [1.0.0] - Part 1: baseline
- Haar detection + LBPH recognition, eye alignment, consent-based gallery.
- IoU tracker with majority voting for video.
- `enroll`, `identify`, `list`, `remove`, `train`, `evaluate` commands.
- Streamlit lab and single-file browser app.
- 32 tests.
