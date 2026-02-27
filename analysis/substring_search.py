import sqlite3
import json

db_path = r'c:\Users\phu_v\Documents\WorkSpaceAntigraty\human-resource\ZKTimeNet08.db'

def substring_search():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Common prefixes in the account list
    prefixes = ["0312", "0572", "0412", "0022", "0272"]
    
    results = {}
    
    # Tables to check with substrings
    tables_to_check = ["pay_empDetail", "hr_employee", "CustomStateValue", "pay_salaryRecord"]
    
    for table in tables_to_check:
        try:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = [c[1] for c in cursor.fetchall()]
            
            for col in cols:
                for pre in prefixes:
                    query = f"SELECT * FROM {table} WHERE \"{col}\" LIKE ?"
                    cursor.execute(query, (f'%{pre}%',))
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
        data = substring_search()
        print(json.dumps(data, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
