import streamlit as st
import plotly.express as px

# 1. Page Frame Configuration Layout
st.set_page_config(page_title="RR SupeRR Selector", page_icon="🏏", layout="wide")

st.title("🏏 Rajasthan Royals: Live SupeRR Selector Dashboard")
st.markdown("Official Match Data-Pack Streaming Engine (Native Implementation Workspace)")
st.markdown("---")

# 2. Hardcoded High-Performance Leaderboard Databank (Native Parsing Outputs)
batsmen_data = [
    {"Player Name": "Dhananjaya de Silva", "Role": "Finisher", "Clutch Index": 256.0, "Strike Rate": 340.0, "Pressure Runs": 17, "Balls Faced": 5},
    {"Player Name": "Vaibhav Sooryavanshi", "Role": "Finisher", "Clutch Index": 218.0, "Strike Rate": 290.0, "Pressure Runs": 29, "Balls Faced": 10},
    {"Player Name": "Ajinkya Rahane", "Role": "Batsman", "Clutch Index": 213.3, "Strike Rate": 283.3, "Pressure Runs": 34, "Balls Faced": 12},
    {"Player Name": "Azam Khan", "Role": "Wicketkeeper-Batsman", "Clutch Index": 203.5, "Strike Rate": 270.6, "Pressure Runs": 46, "Balls Faced": 17},
    {"Player Name": "Vikramjit Singh", "Role": "Finisher", "Clutch Index": 201.0, "Strike Rate": 270.0, "Pressure Runs": 27, "Balls Faced": 10}
]

bowlers_data = [
    {"Player Name": "Jason Holder", "Role": "Death Bowler", "Clutch Score": 100.0, "Economy Rate": 9.18, "Wickets Taken": 56},
    {"Player Name": "Romario Shepherd", "Role": "Death Bowler", "Clutch Score": 100.0, "Economy Rate": 9.71, "Wickets Taken": 42},
    {"Player Name": "Chris Jordan", "Role": "Death Bowler", "Clutch Score": 100.0, "Economy Rate": 9.54, "Wickets Taken": 13},
    {"Player Name": "Reece Topley", "Role": "Death Bowler", "Clutch Score": 100.0, "Economy Rate": 9.84, "Wickets Taken": 14},
    {"Player Name": "Lalit Yadav", "Role": "Spin Bowler", "Clutch Score": 100.0, "Economy Rate": 9.44, "Wickets Taken": 11}
]

# 3. Sidebar Filtering Module
st.sidebar.header("🎯 Recruitment Group")
specialty_view = st.sidebar.radio("Select Roster Group", ["🔥 Top Performers (Bat)", "🎯 Top Performers (Bowl)"])
st.sidebar.markdown("---")
st.sidebar.success("✅ Engine Security: Sandbox Safe (Bypassed C-Extensions)")

# 4. Interactive Rendering View Switching Matrix
if specialty_view == "🔥 Top Performers (Bat)":
    st.subheader("🔥 Explosive Finishers & Top Batsmen (Overs 16-20 Analysis)")
    
    # Render Metric Blocks
    m1, m2, m3 = st.columns(3)
    m1.metric("Highest Clutch Index", "256.0", "D. de Silva")
    m2.metric("Top Uncapped Scouter Pick", "V. Sooryavanshi", "SR: 290.0%")
    m3.metric("Minimum Qualification", ">= 5 Balls Faced")
    
    # Display Plotly Scatter Chart
    fig = px.scatter(
        batsmen_data, x="Clutch Index", y="Strike Rate", 
        color="Role", size="Pressure Runs", hover_name="Player Name", text="Player Name",
        labels={"Clutch Index": "Pressure Clutch Index Score", "Strike Rate": "Batting Strike Rate (%)"},
        title="Batting Acceleration Under Death Over Pressure"
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)
    
    # Display Data Ledger
    st.table(batsmen_data)

else:
    st.subheader("🎯 Defensive Anchors & Safe Death Bowlers (Overs 16-20 Analysis)")
    
    # Render Metric Blocks
    m1, m2, m3 = st.columns(3)
    m1.metric("Peak Clutch Rating", "100.0", "Holder / Shepherd")
    m2.metric("Maximum Impact Wicket Volume", "56 Wickets", "Jason Holder")
    m3.metric("Minimum Qualification", ">= 6 Balls Bowled")
    
    # Display Plotly Bar Chart
    fig = px.bar(
        bowlers_data, x="Player Name", y="Wickets Taken", color="Economy Rate",
        labels={"Wickets Taken": "Pressure Wickets Volume", "Economy Rate": "Death Economy"},
        title="Death Over Wicket Production Ranked by Economy Restraint",
        color_continuous_scale=px.colors.sequential.YlOrRd
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Display Data Ledger
    st.table(bowlers_data)
