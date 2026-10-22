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

NAVY = "#14243A"
INK = "#203047"
MUTED = "#738092"
GOLD = "#D5A63B"
BEIGE = "#F3EFE7"
PAPER = "#FFFEFB"
BLUE = "#6483A3"

st.set_page_config(page_title="Spain Top 50 · Chart Intelligence", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root {{ --navy:{NAVY}; --gold:{GOLD}; --paper:{PAPER}; --beige:{BEIGE}; }}
.stApp {{ background:var(--paper); color:var(--navy); font-family:'DM Sans',sans-serif; }}
[data-testid="stSidebar"] {{ background:#F4F1EA; border-right:1px solid #E8E2D7; }}
[data-testid="stSidebar"] * {{ color:var(--navy); }}
h1,h2,h3 {{ font-family:'Manrope',sans-serif!important; color:var(--navy)!important; letter-spacing:-.035em; }}
h1 {{ font-weight:800!important; font-size:clamp(1.7rem,4vw,2.65rem)!important; line-height:1.15!important; overflow-wrap:anywhere; }}
[data-testid="stMetric"] {{ background:white; border:1px solid #EEE9E0; border-radius:15px; padding:19px 21px; box-shadow:0 5px 20px rgba(20,36,58,.045); }}
[data-testid="stMetricLabel"] {{ color:#738092!important; font-size:.78rem!important; letter-spacing:.055em; text-transform:uppercase; }}
[data-testid="stMetricValue"] {{ color:var(--navy)!important; font-family:'Manrope',sans-serif; font-weight:700; }}
[data-testid="stPlotlyChart"] {{ background:#fff; border:1px solid #EEE9E0; border-radius:15px; padding:8px; box-shadow:0 5px 20px rgba(20,36,58,.035); }}
.eyebrow {{ color:#9A7728; font-weight:700; letter-spacing:.16em; font-size:.71rem; text-transform:uppercase; }}
.subtitle {{ color:#738092; margin-top:-.55rem; font-size:1rem; }}
.section-note {{ color:#738092; font-size:.88rem; margin-top:-.55rem; }}
div[data-testid="stTabs"] button {{ font-weight:600; }}
</style>
""", unsafe_allow_html=True)


def polish(fig, height=350):
    fig.update_layout(height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="white", font=dict(family="DM Sans", color=INK, size=12),
                      margin=dict(l=18, r=18, t=38, b=18), hoverlabel=dict(bgcolor=NAVY, font_color="white"),
                      legend=dict(orientation="h", y=1.12, x=0, title=None))
    fig.update_xaxes(showgrid=False, linecolor="#E7E9ED", zeroline=False)
    fig.update_yaxes(gridcolor="#EEF0F3", zeroline=False)
    return fig


@st.cache_data(show_spinner="Reading and validating chart history…")
def get_data():
    return load_data()


st.sidebar.markdown('<div class="eyebrow">Chart intelligence</div>', unsafe_allow_html=True)
st.sidebar.title("Spain Top 50")
st.sidebar.caption("Explore catalog maturity, release lifecycle and playlist rotation.")
try:
    raw = get_data()
except Exception as exc:
    st.error(f"The dataset could not be loaded. {exc}")
    st.info("Place a valid CSV in the project root. Required columns are documented in README.md.")
    st.stop()

st.sidebar.divider()
st.sidebar.subheader("Filters")
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
st.sidebar.caption(f"Source: `{Path(raw.attrs.get('source_path', 'CSV')).name}`")
st.sidebar.caption(f"{len(raw):,} valid chart rows · {raw['date'].nunique():,} chart dates")

st.markdown('<div class="eyebrow">Content maturity · release lifecycle · playlist rotation</div>', unsafe_allow_html=True)
st.title("Spain Top 50 — Chart Intelligence")
st.markdown('<p class="subtitle">A measured view of what enters, stays, and returns to the chart.</p>', unsafe_allow_html=True)
if filtered.empty:
    st.warning("No chart rows match these filters. Widen the date range or adjust selections.")
    st.stop()

metrics = overview_metrics(filtered)
life = song_lifecycle(filtered)
churn = playlist_churn(filtered)
k1, k2, k3 = st.columns(3)
k1.metric("Chart dates", f"{metrics['chart_days']:,}")
k2.metric("Songs in period", f"{metrics['unique_songs']:,}")
k3.metric("Artists", f"{metrics['artists']:,}")
k4, k5 = st.columns(2)
k4.metric("Avg. popularity", f"{metrics['avg_popularity']:.1f}" if pd.notna(metrics["avg_popularity"]) else "—")
k5.metric("Median lifecycle", f"{life['active_days'].median():.0f} days" if not life.empty else "—")

tab_overview, tab_lifecycle, tab_content = st.tabs(["Overview", "Lifecycle & rotation", "Content & release mix"])
with tab_overview:
    st.subheader("Chart pulse")
    st.markdown('<p class="section-note">Rank and popularity averages across the selected chart dates. Lower rank values indicate a stronger position.</p>', unsafe_allow_html=True)
    daily = daily_chart_summary(filtered)
    left, right = st.columns([1.35, 1])
    with left:
        rank_fig = go.Figure()
        rank_fig.add_trace(go.Scatter(x=daily["date"], y=daily["avg_position"], mode="lines", name="Average rank", line=dict(color=BLUE, width=2.5), fill="tozeroy", fillcolor="rgba(100,131,163,.10)"))
        rank_fig.update_yaxes(autorange="reversed", title="Average position")
        rank_fig.update_xaxes(title=None)
        st.plotly_chart(polish(rank_fig), width="stretch", config={"displayModeBar": False})
    with right:
        pop_fig = px.line(daily, x="date", y="avg_popularity", color_discrete_sequence=[GOLD], labels={"date": "Date", "avg_popularity": "Avg. popularity"})
        pop_fig.update_traces(line_width=2.5, fill="tozeroy", fillcolor="rgba(213,166,59,.12)")
        st.plotly_chart(polish(pop_fig), width="stretch", config={"displayModeBar": False})
    st.subheader("Songs with the longest observed chart span")
    top_life = life.head(12).sort_values("active_days")
    fig = px.bar(top_life, x="active_days", y="song", orientation="h", color="mean_position", color_continuous_scale=["#D5A63B", "#6483A3", NAVY],
                 hover_data={"artist": True, "chart_entries": True, "best_position": True, "active_days": True}, labels={"active_days": "Days from first to last appearance", "song": "Song", "mean_position": "Mean rank"})
    fig.update_layout(coloraxis_colorbar=dict(title="Mean<br>rank", thickness=10))
    st.plotly_chart(polish(fig, max(330, len(top_life) * 31)), width="stretch", config={"displayModeBar": False})

with tab_lifecycle:
    st.subheader("Lifecycle and playlist rotation")
    st.markdown('<p class="section-note">Span includes the first and last observed dates; active chart entries count snapshots. A gap between appearances remains a gap.</p>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.1, 1])
    with c1:
        age = px.histogram(life, x="active_days", nbins=30, color_discrete_sequence=[BLUE], labels={"active_days": "Observed lifecycle span (days)"})
        age.update_traces(marker_line_color="white", marker_line_width=1)
        st.plotly_chart(polish(age), width="stretch", config={"displayModeBar": False})
    with c2:
        churn_fig = go.Figure()
        churn_fig.add_bar(x=churn["date"], y=churn["entrants"], name="Entrants", marker_color=GOLD)
        churn_fig.add_bar(x=churn["date"], y=-churn["exits"], name="Exits", marker_color=BLUE)
        churn_fig.update_layout(barmode="relative", yaxis_title="Songs entering / leaving", xaxis_title=None)
        st.plotly_chart(polish(churn_fig), width="stretch", config={"displayModeBar": False})
    turnover_fig = px.line(churn, x="date", y="turnover", color_discrete_sequence=[GOLD],
                           labels={"date": "Date", "turnover": "Entrants / chart size"})
    turnover_fig.update_traces(line_width=2.5)
    turnover_fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(polish(turnover_fig, 290), width="stretch", config={"displayModeBar": False})
    st.subheader("Debut cohort retention")
    st.markdown('<p class="section-note">Weighted share of songs first seen on a chart date that are still present at each elapsed age. Only observed chart snapshots contribute.</p>', unsafe_allow_html=True)
    retention = retention_curve(filtered)
    if retention.empty:
        st.info("Retention is not available for this selection.")
    else:
        ret_fig = px.line(retention, x="tenure_day", y="retention_rate", color_discrete_sequence=[GOLD], labels={"tenure_day": "Days since first chart appearance", "retention_rate": "Share still charting"})
        ret_fig.update_traces(line_width=3, fill="tozeroy", fillcolor="rgba(213,166,59,.13)")
        ret_fig.update_yaxes(tickformat=".0%", range=[0, 1.02])
        st.plotly_chart(polish(ret_fig), width="stretch", config={"displayModeBar": False})
    st.subheader("Song lifecycle detail")
    display_life = life[["song", "artist", "first_seen", "last_seen", "active_days", "observed_days", "best_position", "mean_popularity", "album_type", "is_explicit"]].copy()
    display_life["mean_popularity"] = display_life["mean_popularity"].round(1)
    st.dataframe(display_life, width="stretch", hide_index=True)

with tab_content:
    st.subheader("Explicit vs. clean")
    st.markdown('<p class="section-note">Comparisons are descriptive averages over chart rows in the selected period; they do not imply causation.</p>', unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        explicit = compare_groups(filtered, "is_explicit")
        if explicit.empty:
            st.info("No explicit status values are available after filtering.")
        else:
            fig = px.bar(explicit, x="is_explicit", y="avg_popularity", color="is_explicit", color_discrete_map={"Clean": BLUE, "Explicit": GOLD},
                         text_auto=".1f", labels={"is_explicit": "Content", "avg_popularity": "Average popularity"})
            fig.update_layout(showlegend=False)
            st.plotly_chart(polish(fig, 300), width="stretch", config={"displayModeBar": False})
            st.dataframe(explicit.round(2), width="stretch", hide_index=True)
    with right:
        st.markdown("#### Single vs. album")
        releases = compare_groups(filtered, "album_type")
        if releases.empty:
            st.info("No release type values are available after filtering.")
        else:
            fig = px.bar(releases, x="album_type", y="avg_position", color="album_type", color_discrete_sequence=[GOLD, BLUE, NAVY],
                         text_auto=".1f", labels={"album_type": "Release type", "avg_position": "Average chart position"})
            fig.update_yaxes(autorange="reversed")
            fig.update_layout(showlegend=False)
            st.plotly_chart(polish(fig, 300), width="stretch", config={"displayModeBar": False})
            st.dataframe(releases.round(2), width="stretch", hide_index=True)
    st.caption("Popularity, position, duration, and track-count comparisons use the source dataset's recorded values. Unknown values are excluded only from the relevant comparison.")

st.divider()
st.caption("Spain Top 50 · descriptive analysis from the selected source data · no inferred or fabricated findings")
