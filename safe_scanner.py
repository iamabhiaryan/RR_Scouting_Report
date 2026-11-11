import csv

def scan_headers(filename):
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader) # Grab only the first row (the column names)
            print(f"\n✅ SUCCESS: {filename}")
            print(f"Columns: {headers}")
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find '{filename}' in this folder.")

# Scan the three core database tables
scan_headers('playing_eleven.csv')
scan_headers('ball_by_ball.csv')
scan_headers('matches.csv')
