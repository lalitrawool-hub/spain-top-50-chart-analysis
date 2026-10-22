import pandas as pd
import unittest
from src.lifecycle import song_lifecycle, playlist_churn, retention_curve
from src.metrics import compare_groups


def sample_data():
    return pd.DataFrame({
        "date": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02"]),
        "song": ["A", "B", "A", "C"], "artist": ["X", "Y", "X", "Z"],
        "song_key": ["a — x", "b — y", "a — x", "c — z"], "position": [1, 2, 2, 1],
        "popularity": [80, 70, 81, 75], "album_type": ["single", "album", "single", "single"],
        "is_explicit": [False, True, False, False], "duration_ms": [180000, 200000, 180000, 190000],
        "total_tracks": [1, 10, 1, 1]})


class AnalyticsTests(unittest.TestCase):
    def test_lifecycle_and_churn(self):
        df = sample_data()
        life = song_lifecycle(df).set_index("song")
        self.assertEqual(life.loc["A", "active_days"], 2)
        churn = playlist_churn(df)
        self.assertEqual(churn.iloc[1]["entrants"], 1)
        self.assertEqual(churn.iloc[1]["exits"], 1)

    def test_retention_and_group_comparison(self):
        df = sample_data()
        curve = retention_curve(df)
        self.assertEqual(curve.iloc[0]["retention_rate"], 1)
        explicit = compare_groups(df, "is_explicit")
        self.assertEqual(set(explicit["is_explicit"]), {"Clean", "Explicit"})

