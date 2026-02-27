import sqlite3
import json

db_path = r'c:\Users\phu_v\Documents\WorkSpaceAntigraty\human-resource\ZKTimeNet08.db'

def search_employees():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tables likely to contain employee info based on schema inspection
    # Common table names in ZKTime: hr_employee, Personnel_Employee, hr_personnel, etc.
    # Looking for tables with 'emp' or 'person' in them
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE '%emp%' OR name LIKE '%person%');")
    tables = [row[0] for row in cursor.fetchall()]
    
    results = {}
    
    search_names = ["POUM", "CHANTHAVONG", "MANIVONE", "INTHAVONG"]
    
    for table in tables:
        try:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = [c[1] for c in cursor.fetchall()]
            
            # Simple content search in text columns
            for col in cols:
                for name in search_names:
                    query = f"SELECT * FROM {table} WHERE \"{col}\" LIKE ?"
                    cursor.execute(query, (f'%{name}%',))
                    rows = cursor.fetchall()
                    if rows:
                        if table not in results:
                            results[table] = {"columns": cols, "matches": []}
                        for row in rows:
                            results[table]["matches"].append(dict(zip(cols, row)))
        except Exception as e:
            continue
            
    conn.close()
    return results

if __name__ == "__main__":
    try:
        data = search_employees()
        print(json.dumps(data, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
