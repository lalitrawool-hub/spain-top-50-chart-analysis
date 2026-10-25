"""Interactive Spain Top 50 analytics dashboard."""
from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.data_cleaning import load_data
from src.lifecycle import song_lifecycle, playlist_churn, retention_curve
from src.metrics import overview_metrics, compare_groups, daily_chart_summary

BG = "#080808"
SURFACE = "#111111"
SURFACE_HIGH = "#1A1A1A"
TEXT = "#F2F2F2"
MUTED = "#A1A1AA"
ROSE = "#A1A1AA"
AMBER = "#D4D4D4"
CYAN = "#FFFFFF"
MINT = "#BFBFBF"
SLATE = "#737373"

st.set_page_config(page_title="Spain Top 50 · Sonic Intelligence", page_icon="◈", layout="wide", initial_sidebar_state="expanded")
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
:root {{ color-scheme:dark; --bg:{BG}; --surface:{SURFACE}; --surface-high:{SURFACE_HIGH}; --text:{TEXT}; --muted:{MUTED}; --rose:{ROSE}; --amber:{AMBER}; --cyan:{CYAN}; }}
.stApp {{ background:var(--bg); color:var(--text); font-family:'Plus Jakarta Sans',sans-serif; }}
[data-testid="stAppViewContainer"], [data-testid="stHeader"] {{ background:var(--bg); }}
[data-testid="stSidebar"] {{ background:#050505; border-right:1px solid rgba(255,255,255,.12); }}
h1,h2,h3,h4 {{ font-family:'Plus Jakarta Sans',sans-serif!important; color:var(--text)!important; letter-spacing:-.025em; }}
h1 {{ font-weight:800!important; font-size:clamp(1.7rem,3vw,2.5rem)!important; line-height:1.12!important; }}
[data-testid="stMetric"] {{ background:linear-gradient(145deg,#1B1B1B,#101010); border:1px solid rgba(255,255,255,.12); border-radius:8px; padding:17px 18px; box-shadow:0 8px 22px rgba(0,0,0,.24); min-height:120px; }}
[data-testid="stMetricLabel"] {{ color:#A1A1AA!important; font-family:'JetBrains Mono',monospace; font-size:.69rem!important; letter-spacing:.08em; text-transform:uppercase; }}
[data-testid="stMetricValue"] {{ color:var(--text)!important; font-family:'JetBrains Mono',monospace; font-weight:700; }}
[data-testid="stPlotlyChart"], [data-testid="stDataFrame"] {{ background:#111111; border:1px solid rgba(255,255,255,.12); border-radius:8px; padding:5px; box-shadow:0 8px 22px rgba(0,0,0,.2); }}
.eyebrow {{ color:#D4D4D4; font-family:'JetBrains Mono',monospace; font-weight:600; letter-spacing:.15em; font-size:.68rem; text-transform:uppercase; }}
.subtitle {{ color:#A1A1AA; margin-top:-.55rem; font-size:.95rem; }}
.section-note {{ color:#A1A1AA; font-size:.82rem; margin-top:-.55rem; }}
.status-strip {{ background:linear-gradient(110deg,#111111,#1A1A1A); border:1px solid rgba(255,255,255,.13); border-radius:8px; padding:14px 18px; margin:14px 0 20px; }}
.tag {{ display:inline-block; font:500 .64rem 'JetBrains Mono',monospace; letter-spacing:.08em; text-transform:uppercase; color:#F2F2F2; background:rgba(255,255,255,.10); padding:4px 7px; border-radius:3px; }}
.sidebar-kicker {{ color:#A1A1AA; font:500 .62rem 'JetBrains Mono',monospace; letter-spacing:.15em; }}
div[data-testid="stRadio"] label p {{ font-size:.82rem; }}
div[data-testid="stTabs"] button {{ font-weight:600; }}
[data-baseweb="popover"] {{ background-color:#171717!important; border:1px solid #404040!important; }}
[data-baseweb="popover"] *, [data-baseweb="menu"] *, [role="listbox"] *, [role="option"] {{ color:#F2F2F2!important; }}
[role="listbox"], [data-baseweb="menu"] {{ background-color:#171717!important; }}
[role="option"] {{ background-color:#171717!important; }}
[role="option"]:hover, [role="option"][aria-selected="true"] {{ background-color:#333333!important; color:#FFFFFF!important; }}
</style>
""", unsafe_allow_html=True)


def polish(fig, height=350):
    fig.update_layout(height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=SURFACE, font=dict(family="Plus Jakarta Sans", color=TEXT, size=11),
                      margin=dict(l=18, r=18, t=34, b=18), hoverlabel=dict(bgcolor="#050505", font_color=TEXT),
                      legend=dict(orientation="h", y=1.12, x=0, title=None, font=dict(family="JetBrains Mono", size=9, color=MUTED)))
    fig.update_xaxes(showgrid=False, linecolor="rgba(255,255,255,.14)", zeroline=False, tickfont=dict(family="JetBrains Mono", size=9, color=MUTED))
    fig.update_yaxes(gridcolor="rgba(255,255,255,.10)", zeroline=False, tickfont=dict(family="JetBrains Mono", size=9, color=MUTED))
    return fig


@st.cache_data(show_spinner="Reading and validating chart history…")
def get_data():
    return load_data()


def metric_cards(items):
    for start in range(0, len(items), 3):
        row = items[start:start + 3]
        for column, (label, value, note, _accent) in zip(st.columns(3), row):
            with column:
                st.metric(label, value, help=note)


st.sidebar.markdown('<div class="sidebar-kicker">◉ SPAIN TOP 50 // INTELLIGENCE</div>', unsafe_allow_html=True)
st.sidebar.title("SONIC IBERIA")
st.sidebar.caption("Chart lifecycle & catalog analytics")
try:
    raw = get_data()
except Exception as exc:
    st.error(f"The dataset could not be loaded. {exc}")
    st.info("Place a valid CSV in the project root. Required columns are documented in README.md.")
    st.stop()

st.sidebar.divider()
st.sidebar.markdown('<div class="sidebar-kicker">INTELLIGENCE MODULES</div>', unsafe_allow_html=True)
page = st.sidebar.radio(
    "Navigate dashboard",
    ["Lifecycle Radar", "Song Trajectories", "Rotation Dynamics", "Explicit vs Formats", "Track Ledger"],
    label_visibility="collapsed",
)
st.sidebar.divider()
st.sidebar.markdown('<div class="sidebar-kicker">CHART FILTERS</div>', unsafe_allow_html=True)
min_date, max_date = raw["date"].min().date(), raw["date"].max().date()
date_range = st.sidebar.date_input("Chart date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = map(pd.Timestamp, date_range)
else:
    start_date = end_date = pd.Timestamp(date_range)
filtered = raw[raw["date"].between(start_date, end_date)].copy()
artist_options = sorted(filtered["artist"].dropna().unique().tolist())
selected_artists = st.sidebar.multiselect("Artists", artist_options, placeholder="All artists")
album_options = sorted(filtered["album_type"].dropna().unique().tolist())
selected_albums = st.sidebar.multiselect("Release type", album_options, default=album_options)
explicit_options = [x for x in [False, True] if filtered["is_explicit"].eq(x).any()]
explicit_labels = {False: "Clean", True: "Explicit"}
selected_explicit_labels = st.sidebar.multiselect("Content", [explicit_labels[x] for x in explicit_options], default=[explicit_labels[x] for x in explicit_options])
selected_explicit = [key for key, label in explicit_labels.items() if label in selected_explicit_labels]
if selected_artists:
    filtered = filtered[filtered["artist"].isin(selected_artists)]
filtered = filtered[filtered["album_type"].isin(selected_albums) & filtered["is_explicit"].isin(selected_explicit)]
st.sidebar.divider()
st.sidebar.markdown('<div class="sidebar-kicker">SOURCE DATA</div>', unsafe_allow_html=True)
st.sidebar.caption(f"{Path(raw.attrs.get('source_path', 'CSV')).name}")
st.sidebar.caption(f"{len(raw):,} valid rows · {raw['date'].nunique():,} chart dates")
st.markdown('<div class="eyebrow">SPAIN TOP 50 CHART INTELLIGENCE <span class="tag">DATASET VIEW</span></div>', unsafe_allow_html=True)
st.title(f"Spain Top 50 · {page}")
st.markdown(f'<div class="status-strip"><span class="tag">CHART HISTORY</span> &nbsp;{start_date:%d %b %Y} — {end_date:%d %b %Y} &nbsp;·&nbsp; {len(filtered):,} matching observations &nbsp;·&nbsp; Source: {Path(raw.attrs.get("source_path", "CSV")).name}</div>', unsafe_allow_html=True)
if filtered.empty:
    st.warning("No chart rows match these filters. Widen the date range or adjust selections.")
    st.stop()

metrics = overview_metrics(filtered)
life = song_lifecycle(filtered)
churn = playlist_churn(filtered)
latest_date = filtered["date"].max()
latest = filtered[filtered["date"].eq(latest_date)].copy()
current_life = life[life["last_seen"].eq(latest_date)].copy()
mean_turnover = churn.loc[churn["date"].ne(churn["date"].min()), "turnover"].mean()
metric_cards([
    ("Chart dates", f"{metrics['chart_days']:,}", "Observed snapshots", CYAN),
    ("Titles observed", f"{metrics['unique_songs']:,}", "Unique song / artist pairs", ROSE),
    ("Latest roster", f"{latest['song_key'].nunique():,}", f"As of {latest_date:%d %b %Y}", CYAN),
    ("Median chart span", f"{life['active_days'].median():.0f} d", "First to last observed date", AMBER),
    ("Mean popularity", f"{metrics['avg_popularity']:.1f}", "Source popularity field", ROSE),
    ("Mean entry turnover", f"{mean_turnover:.1%}" if pd.notna(mean_turnover) else "—", "New titles / chart size", AMBER),
])

if page == "Lifecycle Radar":
    st.markdown("### Lifecycle stages · latest observed roster")
    st.markdown('<p class="section-note">Bands use each title’s distinct chart appearances within the selected window: New 1–7, Developing 8–30, Established 31–90, Long-running 91+ chart dates.</p>', unsafe_allow_html=True)
    stage_order = ["New", "Developing", "Established", "Long-running"]
    current_life["stage"] = pd.cut(
        current_life["observed_days"], bins=[0, 7, 30, 90, float("inf")],
        labels=stage_order, include_lowest=True,
    )
    stages = current_life.groupby("stage", observed=False).size().reindex(stage_order, fill_value=0).rename("titles").reset_index()
    stages["share"] = stages["titles"] / max(stages["titles"].sum(), 1)
    stage_colors = {"New": "#737373", "Developing": "#A1A1AA", "Established": "#D4D4D4", "Long-running": "#FFFFFF"}
    c1, c2 = st.columns([1, 1.5])
    with c1:
        stage_fig = px.bar(stages, x="titles", y="stage", orientation="h", text="titles",
                           color="stage", color_discrete_map=stage_colors,
                           labels={"titles": "Titles in latest roster", "stage": "Observed lifecycle"})
        stage_fig.update_layout(showlegend=False, yaxis={"categoryorder": "array", "categoryarray": stage_order[::-1]})
        st.plotly_chart(polish(stage_fig, 285), width="stretch", config={"displayModeBar": False}, alt="Latest roster grouped into lifecycle stages by observed chart dates.")
    with c2:
        daily = daily_chart_summary(filtered)
        rank_fig = go.Figure(go.Scatter(x=daily["date"], y=daily["avg_position"], mode="lines",
                                        line=dict(color=CYAN, width=2.5), fill="tozeroy",
                                        fillcolor="rgba(255,255,255,.10)", name="Mean position"))
        rank_fig.update_yaxes(autorange="reversed", title="Mean chart position")
        rank_fig.update_xaxes(title=None)
        st.plotly_chart(polish(rank_fig, 285), width="stretch", config={"displayModeBar": False}, alt="Mean Spain Top 50 chart position over the selected date range.")

    st.markdown("### Rotation flow · recent chart snapshots")
    st.markdown('<p class="section-note">The initial selected date is a baseline and is excluded from entry turnover. Each following date compares distinct song / artist pairs with the previous available snapshot.</p>', unsafe_allow_html=True)
    recent_churn = churn.tail(90)
    churn_fig = go.Figure()
    churn_fig.add_bar(x=recent_churn["date"], y=recent_churn["entrants"], name="Entries", marker_color=CYAN)
    churn_fig.add_bar(x=recent_churn["date"], y=-recent_churn["exits"], name="Exits", marker_color=ROSE)
    churn_fig.update_layout(barmode="relative", yaxis_title="Titles entering / leaving", xaxis_title=None, hovermode="x unified")
    st.plotly_chart(polish(churn_fig, 310), width="stretch", config={"displayModeBar": False}, alt="Daily titles entering and leaving the chart in the most recent 90 snapshots.")

    a, b = st.columns(2)
    with a:
        st.markdown("### Longest observed spans")
        long_lived = life.sort_values(["active_days", "observed_days"], ascending=False).head(10)
        ledger = long_lived[["song", "artist", "active_days", "observed_days", "best_position", "mean_popularity"]].copy()
        ledger["mean_popularity"] = ledger["mean_popularity"].round(1)
        st.dataframe(ledger, width="stretch", hide_index=True, alt="Titles with the longest observed chart span.")
    with b:
        st.markdown("### Latest chart roster")
        roster = latest.sort_values("position").merge(
            life[["song_key", "active_days", "observed_days", "first_seen"]], on="song_key", how="left"
        )
        roster_view = roster[["position", "song", "artist", "popularity", "active_days", "observed_days"]].head(12)
        st.dataframe(roster_view, width="stretch", hide_index=True, alt="Top positions in the latest selected chart snapshot.")

elif page == "Song Trajectories":
    st.markdown("### Select a title · observed chart path")
    catalog = filtered[["song_key", "song", "artist"]].drop_duplicates().sort_values(["song", "artist"])
    labels = catalog.set_index("song_key").apply(lambda row: f"{row['song']} — {row['artist']}", axis=1).to_dict()
    selected_key = st.selectbox("Song and artist", catalog["song_key"].tolist(), format_func=lambda key: labels[key])
    track_rows = filtered[filtered["song_key"].eq(selected_key)].sort_values("date")
    track_info = life[life["song_key"].eq(selected_key)].iloc[0]
    metric_cards([
        ("First observed", f"{track_info['first_seen']:%d %b %Y}", "In selected date window", CYAN),
        ("Observed entries", f"{int(track_info['observed_days']):,}", "Distinct chart dates", ROSE),
        ("Observed span", f"{int(track_info['active_days']):,} d", "First to last appearance", AMBER),
        ("Best position", f"#{int(track_info['best_position'])}", "Source chart rank", CYAN),
        ("Mean popularity", f"{track_info['mean_popularity']:.1f}" if pd.notna(track_info["mean_popularity"]) else "—", "Source popularity field", ROSE),
        ("Last observed", f"{track_info['last_seen']:%d %b %Y}", "In selected date window", AMBER),
    ])
    c1, c2 = st.columns(2)
    with c1:
        rank_track = go.Figure(go.Scatter(x=track_rows["date"], y=track_rows["position"], mode="lines+markers",
                                          line=dict(color=CYAN, width=2), marker=dict(size=4, color=CYAN), name="Position"))
        rank_track.update_yaxes(autorange="reversed", title="Chart position")
        rank_track.update_xaxes(title=None)
        st.markdown("### Rank movement")
        st.plotly_chart(polish(rank_track, 330), width="stretch", config={"displayModeBar": False}, alt=f"Chart position history for {labels[selected_key]}.")
    with c2:
        popularity_track = go.Figure(go.Scatter(x=track_rows["date"], y=track_rows["popularity"], mode="lines+markers",
                                                line=dict(color=ROSE, width=2), marker=dict(size=4, color=ROSE), name="Popularity"))
        popularity_track.update_yaxes(title="Source popularity")
        popularity_track.update_xaxes(title=None)
        st.markdown("### Popularity history")
        st.plotly_chart(polish(popularity_track, 330), width="stretch", config={"displayModeBar": False}, alt=f"Recorded popularity history for {labels[selected_key]}.")
    st.markdown("### Observed entries")
    detail_columns = ["date", "position", "popularity", "duration_ms", "album_type", "total_tracks", "is_explicit"]
    st.dataframe(track_rows[detail_columns].rename(columns={"date": "Chart date", "position": "Position", "popularity": "Popularity", "duration_ms": "Duration (ms)", "album_type": "Release type", "total_tracks": "Tracks on release", "is_explicit": "Explicit"}), width="stretch", hide_index=True, alt=f"Daily chart observations for {labels[selected_key]}.")

elif page == "Rotation Dynamics":
    st.markdown("### Playlist turnover · entries and exits")
    st.markdown('<p class="section-note">Turnover is new titles divided by the chart size for that snapshot. “Returning” counts a new entry whose song / artist pair appeared earlier in the selected window.</p>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.6, 1])
    with c1:
        flow = go.Figure()
        flow.add_bar(x=churn["date"], y=churn["entrants"], name="New entries", marker_color=CYAN)
        flow.add_bar(x=churn["date"], y=-churn["exits"], name="Exits", marker_color=ROSE)
        flow.update_layout(barmode="relative", yaxis_title="Songs", xaxis_title=None, hovermode="x unified")
        st.plotly_chart(polish(flow, 360), width="stretch", config={"displayModeBar": False}, alt="Daily entries and exits for distinct song and artist pairs.")
    with c2:
        turnover_fig = go.Figure()
        turnover_fig.add_trace(go.Scatter(x=churn["date"], y=churn["turnover"], mode="lines",
                                          line=dict(color=AMBER, width=2), fill="tozeroy",
                                          fillcolor="rgba(255,255,255,.10)", name="Daily turnover"))
        turnover_fig.add_trace(go.Scatter(x=churn["date"], y=churn["returning"], mode="lines",
                                          line=dict(color=CYAN, width=1.5, dash="dot"), yaxis="y2", name="Returning titles"))
        turnover_fig.update_layout(yaxis={"title": "Entrants / chart size", "tickformat": ".0%"},
                                   yaxis2={"title": "Returning titles", "overlaying": "y", "side": "right", "showgrid": False}, xaxis_title=None)
        st.plotly_chart(polish(turnover_fig, 360), width="stretch", config={"displayModeBar": False}, alt="Daily entry turnover and returning titles over the selected window.")

    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday = churn.assign(weekday=churn["date"].dt.day_name()).groupby("weekday").agg(
        mean_entries=("entrants", "mean"), mean_exits=("exits", "mean"), mean_turnover=("turnover", "mean")
    ).reindex(day_order).dropna(how="all").reset_index()
    st.markdown("### Mean rotation by weekday")
    week_fig = go.Figure()
    week_fig.add_bar(x=weekday["weekday"], y=weekday["mean_entries"], name="Mean entries", marker_color=CYAN)
    week_fig.add_bar(x=weekday["weekday"], y=-weekday["mean_exits"], name="Mean exits", marker_color=ROSE)
    week_fig.update_layout(barmode="relative", yaxis_title="Mean titles per snapshot", xaxis_title=None)
    st.plotly_chart(polish(week_fig, 300), width="stretch", config={"displayModeBar": False}, alt="Mean chart entries and exits grouped by weekday.")
    st.markdown("### Recent snapshot transitions")
    st.dataframe(churn.tail(30).sort_values("date", ascending=False).rename(columns={"date": "Chart date", "chart_size": "Chart size", "entrants": "Entries", "exits": "Exits", "returning": "Returning", "turnover": "Turnover"}).assign(Turnover=lambda frame: frame["Turnover"].map(lambda value: f"{value:.1%}")), width="stretch", hide_index=True, alt="Daily chart transition counts for the latest 30 selected snapshots.")

elif page == "Explicit vs Formats":
    st.markdown("### Descriptive group comparisons")
    st.markdown('<p class="section-note">Averages use observed chart rows in the selected window. These are descriptive comparisons and do not imply that content or release format caused a chart outcome.</p>', unsafe_allow_html=True)
    explicit = compare_groups(filtered, "is_explicit")
    releases = compare_groups(filtered, "album_type")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Explicit vs clean")
        if explicit.empty:
            st.info("No explicit status values are available for this selection.")
        else:
            exp_fig = px.bar(explicit, x="is_explicit", y="avg_popularity", color="is_explicit",
                             color_discrete_map={"Clean": CYAN, "Explicit": ROSE}, text_auto=".1f",
                             labels={"is_explicit": "Content label", "avg_popularity": "Mean popularity"})
            exp_fig.update_layout(showlegend=False)
            st.plotly_chart(polish(exp_fig, 300), width="stretch", config={"displayModeBar": False}, alt="Mean popularity by explicit content status.")
            st.dataframe(explicit.round(2), width="stretch", hide_index=True, alt="Summary metrics for clean and explicit chart rows.")
    with c2:
        st.markdown("#### Singles vs albums")
        if releases.empty:
            st.info("No release type values are available for this selection.")
        else:
            rel_fig = px.bar(releases, x="album_type", y="avg_position", color="album_type",
                             color_discrete_sequence=[AMBER, CYAN, ROSE], text_auto=".1f",
                             labels={"album_type": "Release type", "avg_position": "Mean chart position"})
            rel_fig.update_yaxes(autorange="reversed")
            rel_fig.update_layout(showlegend=False)
            st.plotly_chart(polish(rel_fig, 300), width="stretch", config={"displayModeBar": False}, alt="Mean chart position by release type; lower positions rank higher.")
            st.dataframe(releases.round(2), width="stretch", hide_index=True, alt="Summary metrics by observed release type.")

    duration = filtered.groupby("song_key", as_index=False).agg(duration_ms=("duration_ms", "median"))
    scatter_data = life.merge(duration, on="song_key", how="left")
    scatter_data["duration_min"] = scatter_data["duration_ms"] / 60000
    st.markdown("### Track duration and observed chart span")
    scatter = px.scatter(scatter_data.dropna(subset=["duration_min", "active_days"]), x="duration_min", y="active_days",
                         color="album_type", color_discrete_sequence=[AMBER, CYAN, ROSE],
                         hover_data=["song", "artist", "observed_days", "best_position"],
                         labels={"duration_min": "Track duration (minutes)", "active_days": "Observed lifecycle span (days)", "album_type": "Release type"})
    st.plotly_chart(polish(scatter, 400), width="stretch", config={"displayModeBar": False}, alt="Track duration compared with observed lifecycle span for each title.")
    st.caption("Popularity, position, duration, and track-count comparisons use the recorded source values. Rows missing a compared value are omitted from that metric.")

else:
    st.markdown("### Latest chart snapshot · track ledger")
    st.markdown('<p class="section-note">Songs are ordered by their recorded chart position on the latest available date in the selected window. Lifecycle fields summarize appearances inside that same window.</p>', unsafe_allow_html=True)
    search = st.text_input("Find song or artist", placeholder="Type a title or artist name")
    roster = latest.sort_values("position").merge(
        life[["song_key", "first_seen", "last_seen", "active_days", "observed_days", "best_position", "mean_popularity"]],
        on="song_key", how="left",
    )
    if search.strip():
        query = search.strip()
        roster = roster[roster["song"].str.contains(query, case=False, regex=False) | roster["artist"].str.contains(query, case=False, regex=False)]
    columns = ["position", "song", "artist", "popularity", "album_type", "is_explicit", "duration_ms", "total_tracks", "first_seen", "active_days", "observed_days", "best_position"]
    names = {"position": "Rank", "song": "Song", "artist": "Artist", "popularity": "Popularity", "album_type": "Release type", "is_explicit": "Explicit", "duration_ms": "Duration (ms)", "total_tracks": "Release tracks", "first_seen": "First seen", "active_days": "Span (days)", "observed_days": "Chart dates", "best_position": "Best rank"}
    st.dataframe(roster[columns].rename(columns=names), width="stretch", hide_index=True, alt="Latest observed chart roster with positions and lifecycle measures.")

st.divider()
st.caption("Spain Top 50 · descriptive analytics from the selected source data · lifecycle stage bands are defined above")
