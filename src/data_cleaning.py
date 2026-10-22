"""Loading and validation for the Spain Top 50 chart dataset."""
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"date", "position", "song", "artist", "popularity", "duration_ms", "album_type", "total_tracks", "is_explicit"}


def find_dataset(path=None):
    """Find a CSV in the project root, preferring the supplied path."""
    if path:
        candidate = Path(path)
        if candidate.is_file():
            return candidate
        raise FileNotFoundError(f"Dataset not found: {candidate}")
    root = Path(__file__).resolve().parents[1]
    candidates = sorted(root.glob("*.csv"))
    if not candidates:
        raise FileNotFoundError(f"No CSV dataset found in {root}")
    return candidates[0]


def load_data(path=None):
    """Load, normalize, and validate source data. Invalid essential rows are dropped."""
    source = find_dataset(path)
    try:
        df = pd.read_csv(source)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as exc:
        raise ValueError(f"Could not read dataset at {source}: {exc}") from exc
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    for column in ("position", "popularity", "duration_ms", "total_tracks"):
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df["song"] = df["song"].astype("string").str.strip()
    df["artist"] = df["artist"].astype("string").str.strip()
    df["album_type"] = df["album_type"].astype("string").str.strip().str.lower()
    explicit = df["is_explicit"].astype("string").str.strip().str.lower()
    df["is_explicit"] = explicit.map({"true": True, "false": False, "1": True, "0": False, "yes": True, "no": False})
    essential = ["date", "position", "song", "artist"]
    invalid_rows = int(df[essential].isna().any(axis=1).sum())
    df = df.dropna(subset=essential)
    df = df[(df["position"] > 0) & df["song"].ne("") & df["artist"].ne("")]
    df["position"] = df["position"].astype(int)
    df["chart_date"] = df["date"].dt.strftime("%Y-%m-%d")
    df["song_key"] = df["song"].str.casefold() + " — " + df["artist"].str.casefold()
    df.attrs["source_path"] = str(source)
    df.attrs["invalid_rows_dropped"] = invalid_rows
    if df.empty:
        raise ValueError("No valid chart rows remain after validation.")
    return df.sort_values(["date", "position"]).reset_index(drop=True)
