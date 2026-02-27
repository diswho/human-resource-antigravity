import sqlite3
import json

db_path = r'c:\Users\phu_v\Documents\WorkSpaceAntigraty\human-resource\ZKTimeNet08.db'

def audit_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    table_stats = []
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            if count > 0:
                table_stats.append({"table": table, "rows": count})
        except:
            continue
            
    # Sort by row count descending
    table_stats.sort(key=lambda x: x['rows'], reverse=True)
    
    conn.close()
    return table_stats

if __name__ == "__main__":
    try:
        stats = audit_db()
        print(json.dumps(stats, indent=2))
    except Exception as e:
        print(f"Error: {e}")
