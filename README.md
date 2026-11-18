# 🏏 SupeRR Selector – Context-Aware Cricket Scouting System

### Rajasthan Royals | SupeRR Selector Season 2 – Round 1

A data-driven cricket scouting and player evaluation system that identifies clutch performers by analysing their performance under high-pressure match situations.

The project introduces a **Match Pressure Index (MPI)** to evaluate every delivery based on match context, then compares player performance in ordinary and high-pressure situations to identify valuable batters and bowlers.

---

## 🎯 Project Overview

Traditional cricket statistics measure overall performance, but they do not always reveal how a player performs when the match is under pressure.

**SupeRR Selector** addresses this problem through a context-aware analytics engine that:

- Calculates a Match Pressure Index (MPI) for every delivery.
- Identifies high-pressure match situations.
- Compares player performance under ordinary and high-pressure conditions.
- Identifies clutch batters and economical bowlers.
- Evaluates player consistency across multiple matches.
- Supports scouting through an interactive Streamlit dashboard.

The system combines ball-by-ball cricket data with multiple relational datasets to generate meaningful player insights.

---

## ⚡ Key Features

### 1. Match Pressure Index (MPI)

MPI measures the pressure associated with an individual delivery on a scale of **0–100**.

It is calculated using three major components and an additional knockout bonus.

| Component | Maximum Points | Description |
|---|---:|---|
| Urgency & Stage | 40 | Evaluates required run rate and death-over situations. |
| Wicket Vulnerability | 35 | Considers wickets already lost. |
| Contest Closeness | 25 | Measures how competitive the match situation is. |
| Knockout Bonus | +10 | Additional bonus for knockout matches. |

**Classification:**

- MPI ≥ 60 → High Pressure
- MPI < 60 → Ordinary

The pressure threshold can be adjusted interactively in the dashboard.

### 2. Clutch Batter Evaluation

The system compares a batter's performance in ordinary and high-pressure situations.

Key metrics:

- Ordinary Strike Rate
- High-Pressure Strike Rate
- Strike Rate Lift
- Performance Consistency
- Number of High-Pressure Matches
- Overall Clutch Rating

The leaderboard uses a minimum requirement of **5 high-pressure matches** to reduce rankings based on limited match samples.

### 3. Clutch Bowler Evaluation

The system identifies bowlers who control scoring when the match becomes difficult.

Key metrics:

- Ordinary Economy Rate
- High-Pressure Economy Rate
- Economy Saved
- Number of High-Pressure Matches

A lower high-pressure economy indicates better run control under pressure.

### 4. Interactive War-Room Dashboard

Built using Streamlit and Plotly, the dashboard provides:

- Interactive MPI threshold control (45–80).
- Dynamic player filtering.
- Ordinary vs. high-pressure performance comparisons.
- Player performance rankings.
- Statistical distribution and performance-delta visualisations.

---

## 🏆 Sample Project Results

The submitted analysis identified the following performers:

### Top Clutch Batter

| Player | High-Pressure SR | SR Lift | Clutch Rating |
|---|---:|---:|---:|
| Angelo Mathews | 181.8 | +96.1 | 126.5 |
| Fakhar Zaman | 188.9 | +68.2 | 119.9 |
| Babar Azam | 188.8 | +64.0 | 119.4 |

### Top Economy Tightener

| Player | Ordinary Economy | Pressure Economy | Economy Saved |
|---|---:|---:|---:|
| Vipraj Nigam | 9.77 | 6.00 | 3.77 |
| Mohammad Nawaz | 7.26 | 5.38 | 1.88 |
| Abrar Ahmed | 7.05 | 5.10 | 1.95 |

*These are results from the submitted analysis, not live or continuously updated player statistics.*

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.14 | Core programming language |
| Pandas | Data processing and relational data analysis |
| NumPy | Numerical calculations |
| Streamlit | Interactive dashboard |
| Plotly | Interactive charts and visualisations |
| CSV | Dataset storage and input |

---

## 🏗️ Project Structure

```text
SupeRR-Selector/
│
├── analytics.py
├── app.py
├── debug_data.py
├── safe_scanner.py
│
├── ball_by_ball.csv
├── matches.csv
├── competitions.csv
├── teams.csv
├── playing_eleven.csv
├── competition_team_player_mapping.csv
├── rr_domestic_uncapped_data.csv
│
├── bat_chart.png
├── bowl_chart.png
│
├── RR_Report file.pdf
├── requirements.txt
├── README.md
│
└── venv/
```

### Important Files

| File | Purpose |
|---|---|
| `analytics.py` | Core analytics engine and MPI calculations. |
| `app.py` | Streamlit interactive dashboard. |
| `ball_by_ball.csv` | Ball-by-ball match information. |
| `matches.csv` | Match-level information. |
| `competitions.csv` | Competition information. |
| `teams.csv` | Team information. |
| `playing_eleven.csv` | Playing XI information. |
| `competition_team_player_mapping.csv` | Relational mapping between
