import sqlite3
import json

db_path = r'c:\Users\phu_v\Documents\WorkSpaceAntigraty\human-resource\ZKTimeNet08.db'

def inspect_details():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    results = {}
    
    # Check pay_empDetail
    try:
        cursor.execute("SELECT * FROM pay_empDetail LIMIT 20")
        cols = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        results['pay_empDetail'] = [dict(zip(cols, row)) for row in rows]
    except: pass

    # Check pay_formulaResult
    try:
        cursor.execute("SELECT * FROM pay_formulaResult LIMIT 20")
        cols = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        results['pay_formulaResult'] = [dict(zip(cols, row)) for row in rows]
    except: pass

    # Check pay_salarystructure
    try:
        cursor.execute("SELECT * FROM pay_salarystructure LIMIT 20")
        cols = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        results['pay_salarystructure'] = [dict(zip(cols, row)) for row in rows]
    except: pass

    conn.close()
    return results

if __name__ == "__main__":
    try:
        data = inspect_details()
        print(json.dumps(data, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
