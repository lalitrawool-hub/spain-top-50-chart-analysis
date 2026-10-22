# Content Maturity, Release Lifecycle & Playlist Rotation Analysis of Spain Top 50 Songs

A Streamlit dashboard for exploring chart history, observed song lifecycles, playlist turnover, cohort retention, and descriptive differences by explicit status and release type. Every displayed measure is calculated from the CSV; no values are hard-coded as findings.

## Dataset

Place the Spain Top 50 CSV in the project root. The included `Atlantic_Spain .csv` file is detected automatically. Required fields are `date`, `position`, `song`, `artist`, `popularity`, `duration_ms`, `album_type`, `total_tracks`, and `is_explicit`. The loader parses day-first dates, validates essential fields, normalizes common boolean values, and drops rows that cannot identify a dated song and artist. The cover URL is optional.

Lifecycle is measured from the first to the last observed chart date, inclusive; gaps do not imply continuous chart presence. Observed days count distinct chart dates. Churn compares distinct song/artist pairs between consecutive available chart dates. Retention is the weighted share of each debut-date cohort observed in the chart at each age in days; it describes chart presence in snapshots, not streaming audience retention.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run basic unit tests with `python -m unittest discover -s tests`.

## Project layout

- `app.py` — dashboard, filters, and visualizations
- `src/data_cleaning.py` — CSV discovery, validation, and normalization
- `src/lifecycle.py` — lifecycle, turnover, and retention calculations
- `src/metrics.py` — summaries and comparison tables
- `tests/` — deterministic tests using a tiny synthetic fixture
