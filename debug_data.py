import csv

with open('ball_by_ball.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    first_row = next(reader)
    print("\n--- SAMPLE ROW DATA ---")
    for key, value in first_row.items():
        print(f"'{key}': '{value}'")
