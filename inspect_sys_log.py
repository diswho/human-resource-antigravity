import sqlite3
import os

db_path = "ZKTimeNet08.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='sys_log'")
    print(cursor.fetchone()[0])
    
    cursor.execute("SELECT * FROM sys_log LIMIT 5")
    print("\nSample records:")
    for row in cursor.fetchall():
        print(row)
    conn.close()
else:
    print("Database not found")
