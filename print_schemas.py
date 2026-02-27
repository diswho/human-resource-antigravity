import sqlite3
import os

db_path = "ZKTimeNet08.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def print_schema(table_name):
    print(f"\n--- Schema for {table_name} ---")
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE name='{table_name}'")
    row = cursor.fetchone()
    if row:
        print(row[0])

print_schema("hr_employee")
print_schema("hr_department")
print_schema("hr_position")
print_schema("att_punches")

conn.close()
