import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from analytics import build_relational_pressure_system

st.set_page_config(page_title="RR Multi-Table Pressure System", page_icon="🏏", layout="wide")

st.title("🏏 Rajasthan Royals: Multi-Table High-Pressure Scouting System")
st.markdown("Integrating **Ball-by-Ball, Matches, Competitions, Playing XIs, Teams & Player Mappings** to identify clutch performers.")
st.markdown("---")

# Sidebar Controls
st.sidebar.header("🎛️ Relational Model Controls")
mpi_threshold = st.sidebar.slider("High-Pressure Threshold (MPI)", 45, 80, 60)
knockout_only = st.sidebar.checkbox("🏆 Knockout / Elimination Matches Only", value=False)
min_matches = st.sidebar.slider("Minimum High-Pressure Matches", 1, 15, 3)
top_n = st.sidebar.slider("Leaderboard Size", 5, 25, 10)

@st.cache_data
def load_relational_data(cutoff, ko_flag):
    return build_relational_pressure_system(pressure_cutoff=cutoff, knockout_only=ko_flag)

raw_df, regime_df, bat_df, bowl_df = load_relational_data(mpi_threshold, knockout_only)

# Dynamic Competition Filter
all_comps = ["All Competitions"] + sorted(raw_df['comp_name'].dropna().unique().tolist())
selected_comp = st.sidebar.selectbox("Filter by Competition", all_comps)

if selected_comp != "All Competitions":
    bat_df = bat_df[bat_df['Competitions'].str.contains(selected_comp, na=False, regex=False)]
    bowl_df = bowl_df[bowl_df['Competitions'].str.contains(selected_comp, na=False, regex=False)]

tab1, tab2, tab3 = st.tabs([
    "📐 1. Relational Schema & MPI Proof",
    "🏏 2. Batter Pressure Rankings",
    "🎯 3. Bowler Pressure Rankings"
])

with tab1:
    st.subheader("Multi-Table Architecture & Empirical Pressure Proof")
    st.success("✅ Merged 6 Relational Tables: `ball_by_ball` + `matches` + `competitions` + `playing_eleven` + `teams` + `competition_team_player_mapping`")
    st.dataframe(
        regime_df[['Situation', 'Deliveries', 'Share (%)', 'Avg_MPI', 'Run Rate', 'Wicket_Rate_Pct']],
        use_container_width=True,
        hide_index=True
    )

    sample_df = raw_df.sample(min(25000, len(raw_df)), random_state=42)
    fig_dist = px.histogram(
        sample_df,
        x="MPI",
        color="Situation",
        nbins=40,
        title=f"Match Pressure Index Distribution (Knockout Bonus Active | Cutoff = {mpi_threshold})",
        color_discrete_map={"Ordinary": "#94a3b8", "High Pressure": "#e11d48"}
    )
    fig_dist.add_vline(x=mpi_threshold, line_dash="dash", line_color="black")
    st.plotly_chart(fig_dist, use_container_width=True)

with tab2:
    role_options = ["All Positions"] + sorted(bat_df['Role Profile'].dropna().unique().tolist())
    selected_role = st.selectbox("Filter Batters by Playing XI Role / Batting Order", role_options)
    
    f_bat = bat_df[bat_df['Matches'] >= min_matches]
    if selected_role != "All Positions":
        f_bat = f_bat[f_bat['Role Profile'] == selected_role]
    f_bat = f_bat.head(top_n)

    if not f_bat.empty:
        m1, m2, m3 = st.columns(3)
        m1.metric("#1 Clutch Batter", str(f_bat['Player Name'].iloc[0]), f"{f_bat['Team'].iloc[0]} | Rating: {f_bat['Clutch Rating'].iloc[0]}")
        m2.metric("Highest SR Lift vs. Ordinary", f"+{f_bat['SR Lift'].max()} SR")
        m3.metric("Avg Consistency Score", f"{f_bat['Consistency'].mean():.1f} / 100")

        fig_bat = go.Figure(data=[
            go.Bar(name='Ordinary Strike Rate', x=f_bat['Player Name'], y=f_bat['Ordinary SR'], marker_color='#94a3b8'),
            go.Bar(name='High-Pressure Strike Rate', x=f_bat['Player Name'], y=f_bat['Pressure SR'], marker_color='#e11d48')
        ])
        fig_bat.update_layout(barmode='group', title="Ordinary vs. High-Pressure Strike Rate", yaxis_title="Strike Rate (%)", height=400)
        st.plotly_chart(fig_bat, use_container_width=True)

        st.dataframe(f_bat, use_container_width=True, hide_index=True)
    else:
        st.warning("No batters match the selected filters. Try lowering Minimum Matches or switching Competition.")

with tab3:
    f_bowl = bowl_df[bowl_df['Matches'] >= min_matches].head(top_n)

    if not f_bowl.empty:
        m1, m2, m3 = st.columns(3)
        m1.metric("#1 Clutch Bowler", str(f_bowl['Player Name'].iloc[0]), f"{f_bowl['Team'].iloc[0]} | Rating: {f_bowl['Clutch Rating'].iloc[0]}")
        m2.metric("Best Economy Tightening", f"{f_bowl['Econ Saved'].max():+.2f} RPO")
        m3.metric("Avg Consistency Score", f"{f_bowl['Consistency'].mean():.1f} / 100")

        fig_bowl = go.Figure(data=[
            go.Bar(name='Ordinary Economy', x=f_bowl['Player Name'], y=f_bowl['Ordinary Econ'], marker_color='#94a3b8'),
            go.Bar(name='High-Pressure Economy', x=f_bowl['Player Name'], y=f_bowl['Pressure Econ'], marker_color='#2563eb')
        ])
        fig_bowl.update_layout(barmode='group', title="Ordinary vs. High-Pressure Economy (Lower = Better)", yaxis_title="Runs Per Over", height=400)
        st.plotly_chart(fig_bowl, use_container_width=True)

        st.dataframe(f_bowl, use_container_width=True, hide_index=True)
    else:
        st.warning("No bowlers match the selected filters. Try lowering Minimum Matches or switching Competition.")
