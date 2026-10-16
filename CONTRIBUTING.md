# Contributing

Thanks for helping. Setup takes two minutes:

```bash
git clone <your fork>
cd VisageLab
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install opencv-contrib-python numpy pytest scikit-image ruff
pip install -e . --no-deps
python -m pytest -q
ruff check .
```

## Ground rules
- **Privacy first.** Never commit photos of real people, `data/`, models or CSV logs
  (all git-ignored). Test images must be synthetic or public domain.
- **Consent stays mandatory.** Do not add a way to enroll someone without the consent flag.
- **Every behaviour change needs a test.** Tests use synthetic faces (`tests/conftest.py`)
  wherever possible so they run fast and need no downloads.
- Keep runtime dependencies minimal (OpenCV + NumPy for the core library).
- Python 3.9 must keep working: add `from __future__ import annotations` to new modules
  and avoid `match` statements.

## Commit style
One focused change per commit, imperative subject line: `Add enrollment quality gate`.
