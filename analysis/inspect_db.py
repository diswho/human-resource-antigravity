import sqlite3
import json

db_path = r'c:\Users\phu_v\Documents\WorkSpaceAntigraty\human-resource\ZKTimeNet08.db'

def get_schema():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    schema = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        schema[table] = [
            {"cid": c[0], "name": c[1], "type": c[2], "notnull": c[3], "pk": c[5]}
            for c in columns
        ]
    
    conn.close()
    return schema

if __name__ == "__main__":
    try:
        schema = get_schema()
        print(json.dumps(schema, indent=2))
    except Exception as e:
        print(f"Error: {e}")
