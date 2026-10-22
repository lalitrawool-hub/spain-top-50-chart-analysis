"""Song lifecycles, playlist churn, and chart retention calculations."""
import pandas as pd


def song_lifecycle(df):
    """Summarize observed chart tenure (first to last appearance, inclusive)."""
    grouped = df.groupby(["song_key", "song", "artist"], dropna=False)
    result = grouped.agg(first_seen=("date", "min"), last_seen=("date", "max"),
                         chart_entries=("date", "nunique"), mean_position=("position", "mean"),
                         best_position=("position", "min"), mean_popularity=("popularity", "mean"),
                         peak_popularity=("popularity", "max"), album_type=("album_type", "last"),
                         is_explicit=("is_explicit", "last")).reset_index()
    result["active_days"] = (result["last_seen"] - result["first_seen"]).dt.days + 1
    result["observed_days"] = result["chart_entries"]
    result["days_since_last_seen"] = (df["date"].max() - result["last_seen"]).dt.days
    return result.sort_values(["active_days", "chart_entries", "mean_position"], ascending=[False, False, True]).reset_index(drop=True)


def playlist_churn(df):
    """Daily entrants, exits, returning titles, and chart turnover from set changes."""
    days = sorted(df["date"].dropna().unique())
    sets = {day: set(df.loc[df["date"].eq(day), "song_key"]) for day in days}
    rows = []
    previous = set()
    seen = set()
    for day in days:
        current = sets[day]
        # The first snapshot is the observed starting inventory, not a measured transition.
        entrants = len(current - previous) if rows else 0
        exits = len(previous - current) if rows else 0
        rows.append({"date": pd.Timestamp(day), "chart_size": len(current),
                     "entrants": entrants, "exits": exits,
                     "returning": len((current - previous) & seen),
                     "turnover": entrants / max(len(current), 1)})
        seen.update(current)
        previous = current
    return pd.DataFrame(rows)


def retention_curve(df):
    """Share of a debut-date cohort still charting after N days (observed snapshots)."""
    first = df.groupby("song_key")["date"].min().rename("first_seen")
    data = df[["song_key", "date"]].drop_duplicates().join(first, on="song_key")
    data["tenure_day"] = (data["date"] - data["first_seen"]).dt.days
    cohorts = data.groupby("first_seen")["song_key"].nunique()
    rows = []
    for day, cohort_size in cohorts.items():
        ages = data.loc[data["first_seen"].eq(day)].groupby("tenure_day")["song_key"].nunique()
        for tenure, retained in ages.items():
            rows.append({"first_seen": day, "tenure_day": int(tenure), "cohort_size": int(cohort_size),
                         "retained": int(retained), "retention_rate": retained / cohort_size})
    detail = pd.DataFrame(rows)
    if detail.empty:
        return detail
    # Average cohort retention at each age, weighted by cohort size.
    summary = detail.groupby("tenure_day", as_index=False).agg(retained=("retained", "sum"), cohort_size=("cohort_size", "sum"))
    summary["retention_rate"] = summary["retained"] / summary["cohort_size"]
    return summary
