import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF

# 1. Exact Synchronized Data (Minimum 5 High-Pressure Matches)
batters = [
    ("Angelo Mathews", "Sri Lanka", "Finisher / Lower (6+)", 7, 85.7, 181.8, 96.1, 55.2, 126.5),
    ("Fakhar Zaman", "Pakistan", "Top Order (1-3)", 9, 120.7, 188.9, 68.2, 54.9, 119.9),
    ("Babar Azam", "Pakistan", "Top Order (1-3)", 6, 124.7, 188.8, 64.0, 60.3, 119.4),
    ("Yashasvi Jaiswal", "India", "Top Order (1-3)", 5, 150.3, 203.2, 52.9, 39.6, 117.9),
    ("Naman Dhir", "Mumbai Indians", "Middle Order (4-5)", 21, 147.0, 200.0, 53.0, 44.0, 117.4),
    ("Jacob Bethell", "England", "Top Order (1-3)", 8, 135.9, 194.6, 58.7, 40.0, 116.1),
    ("George Linde", "South Africa", "Finisher / Lower (6+)", 10, 113.0, 178.5, 65.5, 58.1, 114.9),
    ("Ambati Rayudu", "Chennai Super Kings", "Middle Order (4-5)", 11, 108.7, 178.0, 69.3, 49.1, 114.2),
    ("Ruturaj Gaikwad", "India", "Top Order (1-3)", 10, 132.2, 188.9, 56.7, 44.8, 113.8),
    ("Dinesh Karthik", "India", "Wicketkeeper", 46, 112.9, 178.9, 66.0, 50.4, 113.7),
]

bowlers = [
    ("Vipraj Nigam", "Delhi Capitals", "IPL 2025, IPL 2026", 5, 9.77, 6.00, 3.77),
    ("Mohammad Nawaz", "Pakistan", "Pak vs Afg, Asia Cup 2025", 18, 7.26, 5.38, 1.88),
    ("Abrar Ahmed", "Pakistan", "Asia Cup 2025, Aus in Pak", 22, 7.05, 5.10, 1.95),
    ("Benjamin White", "Ireland", "Ire vs Afg, Eng in Ire", 5, 8.85, 5.79, 3.05),
    ("Matthew Humphreys", "Ireland", "Eng in Ire, Ind in Ire", 6, 6.99, 5.20, 1.79),
    ("Roston Chase", "West Indies", "Aus in WI, Ban in WI", 8, 7.49, 5.73, 1.76),
    ("Sufiyan Muqeemit", "Pakistan", "Asia Cup 2025, Rising Stars", 14, 6.14, 5.23, 0.90),
    ("Pramod Madushan", "Sri Lanka", "Rising Stars, Eng in SL", 6, 7.90, 6.45, 1.45),
    ("George Linde", "South Africa", "IPL 2026, Pak in SA", 5, 7.56, 6.44, 1.12),
    ("Hasan Mahmud", "Bangladesh", "Afg in Ban, Asia Cup 2025", 11, 7.75, 5.89, 1.86),
]

# 2. Generate High-Resolution Comparison Charts
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'

# Batter Chart
fig, ax = plt.subplots(figsize=(8.5, 3.1), dpi=220)
names_b = [b[0] for b in batters][::-1]
ord_sr = [b[4] for b in batters][::-1]
prs_sr = [b[5] for b in batters][::-1]
y = np.arange(len(names_b))
ax.barh(y - 0.18, ord_sr, height=0.35, label='Ordinary SR (MPI < 60)', color='#94A3B8')
ax.barh(y + 0.18, prs_sr, height=0.35, label='High-Pressure SR (MPI >= 60)', color='#E11D48')
ax.set_yticks(y)
ax.set_yticklabels(names_b, fontsize=8.5, fontweight='bold', color='#1E293B')
ax.set_xlabel('Strike Rate (%)', fontsize=8.5, fontweight='bold')
ax.set_title('Top 10 Batters: Ordinary vs. High-Pressure Strike Rate (Min 5 Matches)', fontsize=10, fontweight='bold', color='#1E1B4B')
ax.legend(loc='lower right', fontsize=8)
ax.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('bat_chart.png')
plt.close()

# Bowler Chart
fig, ax = plt.subplots(figsize=(8.5, 3.1), dpi=220)
names_w = [w[0] for w in bowlers][::-1]
ord_ec = [w[4] for w in bowlers][::-1]
prs_ec = [w[5] for w in bowlers][::-1]
y2 = np.arange(len(names_w))
ax.barh(y2 - 0.18, ord_ec, height=0.35, label='Ordinary Economy (MPI < 60)', color='#94A3B8')
ax.barh(y2 + 0.18, prs_ec, height=0.35, label='High-Pressure Economy (MPI >= 60)', color='#2563EB')
ax.set_yticks(y2)
ax.set_yticklabels(names_w, fontsize=8.5, fontweight='bold', color='#1E293B')
ax.set_xlabel('Economy Rate (Runs Per Over - Lower is Better)', fontsize=8.5, fontweight='bold')
ax.set_title('Top 10 Bowlers: Ordinary vs. High-Pressure Economy Rate (Min 5 Matches)', fontsize=10, fontweight='bold', color='#1E1B4B')
ax.legend(loc='lower right', fontsize=8)
ax.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('bowl_chart.png')
plt.close()

# 3. Assemble Multi-Page Submission PDF
class ReportPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            self.set_fill_color(30, 27, 75)
            self.rect(0, 0, 210, 32, 'F')
            self.set_text_color(255, 255, 255)
            self.set_font('Helvetica', 'B', 15)
            self.set_xy(10, 7)
            self.cell(0, 7, 'RAJASTHAN ROYALS: SupeRR Selector Season 2 (Round 1)', ln=True)
            self.set_font('Helvetica', '', 9.5)
            self.set_text_color(244, 114, 182)
            self.set_x(10)
            self.cell(0, 6, 'Context-Aware Match Pressure Index (MPI) & Multi-Table Relational Scouting System', ln=True)
            self.ln(10)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 8, f'SupeRR Selector Hackathon Submission | Minimum 5 High-Pressure Matches Filter | Page {self.page_no()}', align='C')

pdf = ReportPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# --- PAGE 1: METHODOLOGY & BATTERS ---
pdf.add_page()
pdf.set_y(36)

# KPI Cards
kpis = [
    ("#1 CLUTCH BATTER", "Angelo Mathews", "+96.1 SR Lift | 126.5 Rating"),
    ("UNCAPPED FINISHER GEM", "Naman Dhir", "200.0 Pressure SR (21 Matches)"),
    ("#1 ECONOMY TIGHTENER", "Vipraj Nigam", "6.00 Pressure Econ (-3.77 RPO)")
]
for i, (label, val, sub) in enumerate(kpis):
    x = 10 + i * 64.5
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(225, 29, 72)
    pdf.rect(x, 36, 61, 20, 'FD')
    pdf.set_xy(x + 2, 38)
    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_text_color(225, 29, 72)
    pdf.cell(57, 4, label, ln=True)
    pdf.set_x(x + 2)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(57, 6, val, ln=True)
    pdf.set_x(x + 2)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(57, 4, sub)

pdf.set_y(61)
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(30, 27, 75)
pdf.cell(0, 7, '1. Match Pressure Index (MPI) & 6-Table Relational Architecture', ln=True)
pdf.set_font('Helvetica', '', 8.5)
pdf.set_text_color(51, 65, 85)
pdf.multi_cell(0, 4.5,
    "Our Python/Pandas pipeline merges six relational datasets (ball_by_ball, matches, competitions, playing_eleven, teams, and competition_team_player_mapping) to score every delivery from 0 to 100 across three pillars: (1) Urgency & Stage (0-40 pts via Required Run Rate and death overs), (2) Wicket Vulnerability (0-35 pts via wickets fallen), and (3) Contest Closeness (0-25 pts), plus a +10 Knockout Bonus from matches.csv. Deliveries with MPI >= 60 are isolated as High Pressure and compared directly against each player's Ordinary baseline (MPI < 60) with a >= 5 pressure matches filter."
)
pdf.ln(2)

# Batter Table
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(30, 27, 75)
pdf.cell(0, 7, '2. Top 10 High-Pressure Batters Leaderboard (Min 5 Matches)', ln=True)

headers_b = ["Rank", "Player Name", "Team", "Role Profile", "Matches", "Ord SR", "Press SR", "SR Lift", "Consist.", "Rating"]
widths_b = [10, 34, 34, 34, 13, 13, 14, 13, 13, 12]
pdf.set_fill_color(30, 27, 75)
pdf.set_text_color(255, 255, 255)
pdf.set_font('Helvetica', 'B', 7.5)
for h, w in zip(headers_b, widths_b):
    pdf.cell(w, 6, h, border=1, align='C', fill=True)
pdf.ln()

pdf.set_font('Helvetica', '', 7.5)
for idx, b in enumerate(batters, 1):
    fill = idx % 2 == 0
    pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(15, 23, 42)
    row_vals = [str(idx), b[0], b[1][:18], b[2][:18], str(b[3]), f"{b[4]:.1f}", f"{b[5]:.1f}", f"+{b[6]:.1f}", f"{b[7]:.1f}", f"{b[8]:.1f}"]
    aligns = ['C', 'L', 'L', 'L', 'C', 'R', 'R', 'R', 'R', 'R']
    for val, w, al in zip(row_vals, widths_b, aligns):
        pdf.cell(w, 5.5, val, border=1, align=al, fill=fill)
    pdf.ln()

pdf.ln(3)
pdf.image('bat_chart.png', x=10, w=190)

# --- PAGE 2: BOWLERS, CODE PROOF & AUCTION STRATEGY ---
pdf.add_page()
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(30, 27, 75)
pdf.cell(0, 7, '3. Top 10 High-Pressure Bowlers Leaderboard (Min 5 Matches)', ln=True)

headers_w = ["Rank", "Player Name", "Team", "Competitions", "Matches", "Ord Econ", "Press Econ", "Econ Saved"]
widths_w = [12, 38, 36, 52, 14, 16, 17, 15]
pdf.set_fill_color(30, 27, 75)
pdf.set_text_color(255, 255, 255)
pdf.set_font('Helvetica', 'B', 7.5)
for h, w in zip(headers_w, widths_w):
    pdf.cell(w, 6, h, border=1, align='C', fill=True)
pdf.ln()

pdf.set_font('Helvetica', '', 7.5)
for idx, w_row in enumerate(bowlers, 1):
    fill = idx % 2 == 0
    pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(15, 23, 42)
    row_vals = [str(idx), w_row[0], w_row[1], w_row[2], str(w_row[3]), f"{w_row[4]:.2f}", f"{w_row[5]:.2f}", f"+{w_row[6]:.2f}"]
    aligns = ['C', 'L', 'L', 'L', 'C', 'R', 'R', 'R']
    for val, w, al in zip(row_vals, widths_w, aligns):
        pdf.cell(w, 5.5, val, border=1, align=al, fill=fill)
    pdf.ln()

pdf.ln(3)
pdf.image('bowl_chart.png', x=10, w=190)
pdf.ln(3)

# Uncapped Scouting Callout
pdf.set_fill_color(253, 242, 248)
pdf.set_draw_color(225, 29, 72)
pdf.set_font('Helvetica', 'B', 9)
pdf.set_text_color(190, 18, 60)
pdf.cell(0, 6, '  4. Rajasthan Royals Auction Strategy & Uncapped Talent Recommendations', ln=True, fill=True)
pdf.set_font('Helvetica', '', 8.5)
pdf.set_text_color(30, 41, 59)
pdf.multi_cell(0, 4.5,
    "- Uncapped Middle-Order Finisher (Naman Dhir): Ranks #5 overall across 21 high-pressure matches, accelerating from 147.0 Ordinary SR to 200.0 Pressure SR (+53.0 SR Lift).\n"
    "- Uncapped Death/Middle-Over Spinner (Vipraj Nigam): Ranks #1 among qualified bowlers, slashing his economy from 9.77 RPO in ordinary overs down to 6.00 RPO under pressure (+3.77 RPO saved).\n"
    "- Proven Experienced Anchors: Angelo Mathews (+96.1 SR Lift) and Dinesh Karthik (46 pressure matches, 178.9 Pressure SR) validate that the MPI model accurately captures elite finishing temperament."
)
pdf.ln(2)

# Code Proof Block
pdf.set_font('Helvetica', 'B', 9.5)
pdf.set_text_color(30, 27, 75)
