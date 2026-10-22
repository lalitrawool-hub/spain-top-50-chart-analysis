"""Reusable descriptive and comparison metrics."""
import pandas as pd


def overview_metrics(df):
    return {"chart_days": int(df["date"].nunique()), "unique_songs": int(df["song_key"].nunique()),
            "artists": int(df["artist"].nunique()), "avg_popularity": float(df["popularity"].mean()),
            "avg_position": float(df["position"].mean()), "mean_duration_min": float(df["duration_ms"].mean() / 60000)}


def compare_groups(df, group_column):
    """Compare actual observed group values; missing values stay unclassified."""
    working = df.dropna(subset=[group_column]).copy()
    if group_column == "is_explicit":
        working[group_column] = working[group_column].map({True: "Explicit", False: "Clean"})
    elif group_column == "album_type":
        working[group_column] = working[group_column].str.title()
    return working.groupby(group_column, dropna=True).agg(
        chart_rows=("song_key", "size"), unique_songs=("song_key", "nunique"),
        avg_popularity=("popularity", "mean"), avg_position=("position", "mean"),
        avg_duration_min=("duration_ms", lambda x: x.mean() / 60000),
        avg_tracks=("total_tracks", "mean")).reset_index()


def daily_chart_summary(df):
    return df.groupby("date").agg(avg_position=("position", "mean"), avg_popularity=("popularity", "mean"),
                                    unique_songs=("song_key", "nunique")).reset_index()
