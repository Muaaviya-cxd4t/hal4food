import csv
import sqlite3
import os
import sys
CSV_FILE = "teams.csv"
DB_FILE = "teams.db"
TABLE_NAME = "teams"
print(" Current working directory:")
print(os.getcwd())
print("-" * 40)
if not os.path.exists(CSV_FILE):
    print(f" ERROR: {CSV_FILE} not found in this directory")
    sys.exit(1)
print(f" Found {CSV_FILE}")
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
print(f"✅ Connected to {DB_FILE}")
# --- Create table ---
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    team_name TEXT PRIMARY KEY,
    creativity INTEGER DEFAULT 0,
    innovation INTEGER DEFAULT 0,
    code_quality INTEGER DEFAULT 0,
    problem_solving INTEGER DEFAULT 0
)
""")
print("Table ensured")
inserted = 0
with open(CSV_FILE, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    required_cols = [
        "team_name",
        "creativity",
        "innovation",
        "code_quality",
        "problem_solving"
    ]

    # Validate CSV headers
    for col in required_cols:
        if col not in reader.fieldnames:
            print(f" ERROR: Missing column '{col}' in CSV")
            sys.exit(1)

    for row in reader:
        team = row["team_name"].strip()
        if not team:
            continue

        cursor.execute(f"""
        INSERT OR IGNORE INTO {TABLE_NAME}
        (team_name, creativity, innovation, code_quality, problem_solving)
        VALUES (?, ?, ?, ?, ?)
        """, (
            team,
            int(row["creativity"]),
            int(row["innovation"]),
            int(row["code_quality"]),
            int(row["problem_solving"])
        ))

        inserted += 1
        print(f" Inserted: {team}")

# --- Finish ---
conn.commit()
conn.close()

print("-" * 40)
print(f" Done. {inserted} rows processed.")
print(f" Database created: {DB_FILE}")
