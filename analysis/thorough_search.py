import sqlite3
import json

db_path = r'c:\Users\phu_v\Documents\WorkSpaceAntigraty\human-resource\ZKTimeNet08.db'

def thorough_search():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # BCEL account numbers usually start with 0572, 0312, etc. (often BCEL is 057...)
    # I will search for the specific account of Phuttiyar
    acc_to_find = "05720040000011893"
    part_to_find = "11893"
    
    results = {}
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        try:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = [c[1] for c in cursor.fetchall()]
            
            for col in cols:
                query = f"SELECT * FROM {table} WHERE CAST(\"{col}\" AS TEXT) LIKE ?"
                cursor.execute(query, (f'%{part_to_find}%',))
                rows = cursor.fetchall()
                if rows:
                    if table not in results: results[table] = []
                    for row in rows:
                        results[table].append(dict(zip(cols, row)))
        except:
            continue

    conn.close()
    return results

if __name__ == "__main__":
    try:
        data = thorough_search()
        print(json.dumps(data, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
