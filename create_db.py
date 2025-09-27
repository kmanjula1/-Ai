import sqlite3

conn = sqlite3.connect("data.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    product TEXT,
    revenue REAL,
    date TEXT
)
""")

cur.executemany("""
INSERT INTO sales (product, revenue, date) VALUES (?, ?, ?)
""", [
    ("Product A", 1000, "2025-09-01"),
    ("Product B", 1500, "2025-09-02"),
    ("Product C", 1200, "2025-09-03"),
    ("Product D", 800, "2025-09-04"),
    ("Product E", 950, "2025-09-05")
])

conn.commit()
conn.close()
print("Sample database created!")