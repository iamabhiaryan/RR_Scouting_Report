import csv
from collections import defaultdict

def process_rr_hackathon_data(ball_by_ball_file):
    batsmen_stats = defaultdict(lambda: {"runs": 0, "balls": 0, "boundaries": 0})
    bowlers_stats = defaultdict(lambda: {"runs": 0, "balls": 0, "wickets": 0})

    print("⏳ Parsing ball-by-ball database files natively...")
    
    with open(ball_by_ball_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Parse numeric values cleanly
                over_id = int(float(row['overid']))
                runs = int(float(row['runs']))
                
                # Handle 'true'/'false' string text booleans safely
                is_wicket = 1 if row['is_wicket'].strip().lower() == 'true' else 0
                is_four = 1 if row['is_four'].strip().lower() == 'true' else 0
                is_six = 1 if row['is_six'].strip().lower() == 'true' else 0
                
                striker = row['striker_name'].strip()
                bowler = row['bowler_name'].strip()
                
                # Filter strictly for Death Overs (Overs 16 to 20)
                if over_id >= 16 and striker and bowler:
                    # 1. Aggregate Batting Statistics
                    batsmen_stats[striker]["runs"] += runs
                    batsmen_stats[striker]["balls"] += 1
                    if is_four or is_six:
                        batsmen_stats[striker]["boundaries"] += 1
                        
                    # 2. Aggregate Bowling Statistics
                    bowlers_stats[bowler]["runs"] += runs
                    bowlers_stats[bowler]["balls"] += 1
                    if is_wicket:
                        bowlers_stats[bowler]["wickets"] += is_wicket
                        
            except (ValueError, KeyError, TypeError):
                continue

    # 3. Compile Batting Shortlist Leaderboard
    batting_leaderboard = []
    for player, stats in batsmen_stats.items():
        if stats["balls"] >= 5: # Qualification threshold
            sr = (stats["runs"] / stats["balls"]) * 100
            boundary_pct = (stats["boundaries"] / stats["balls"]) * 100
            clutch_index = (sr * 0.7) + (boundary_pct * 0.3)
            
            batting_leaderboard.append({
                "Player Name": player,
                "Pressure Runs": stats["runs"],
                "Balls Faced": stats["balls"],
                "Strike Rate": round(sr, 1),
                "Clutch Index": round(clutch_index, 1)
            })
            
    # 4. Compile Bowling Shortlist Leaderboard
    bowling_leaderboard = []
    for player, stats in bowlers_stats.items():
        if stats["balls"] >= 6: # Qualification threshold (minimum 1 over bowled)
            economy = (stats["runs"] / stats["balls"]) * 6
            clutch_score = (100 - (economy * 7)) + (stats["wickets"] * 8)
            
            bowling_leaderboard.append({
                "Player Name": player,
                "Runs Conceded": stats["runs"],
                "Balls Bowled": stats["balls"],
                "Economy Rate": round(economy, 2),
                "Wickets Taken": stats["wickets"],
                "Clutch Score": round(max(0, min(100, clutch_score)), 1)
            })

    # Sort entries by their pressure rating descending
    batting_leaderboard.sort(key=lambda x: x["Clutch Index"], reverse=True)
    bowling_leaderboard.sort(key=lambda x: x["Clutch Score"], reverse=True)
    
    return batting_leaderboard[:15], bowling_leaderboard[:15]

if __name__ == "__main__":
    top_batsmen, top_bowlers = process_rr_hackathon_data('ball_by_ball.csv')
    print("\n🔥 TOP 5 RELIABLE BATSMEN UNDER PRESSURE 🔥")
    for idx, b in enumerate(top_batsmen[:5], 1):
        print(f"{idx}. {b['Player Name']} | Clutch Index: {b['Clutch Index']} | SR: {b['Strike Rate']} ({b['Pressure Runs']} runs off {b['Balls Faced']} balls)")
    print("\n🎯 TOP 5 RELIABLE BOWLERS UNDER PRESSURE 🎯")
    for idx, b in enumerate(top_bowlers[:5], 1):
        print(f"{idx}. {b['Player Name']} | Clutch Score: {b['Clutch Score']} | Econ: {b['Economy Rate']} ({b['Wickets Taken']} wickets taken)")
