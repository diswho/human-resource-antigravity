import sqlite3
import json

db_path = r'c:\Users\phu_v\Documents\WorkSpaceAntigraty\human-resource\ZKTimeNet08.db'

def inspect_salary_att():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Target IDs from previous search (e.g., ID 136 for 200126, ID 2039/2016 for Poum)
    # Using internal IDs found in previous search
    target_emp_ids = [136, 2016, 18] 
    
    tables_to_check = [
        "att_day_summary",
        "att_day_details",
        "pay_salaryRecord",
        "pay_empDetail",
        "pay_salarysetting",
        "pay_salarystructure"
    ]
    
    results = {}
    
    for table in tables_to_check:
        try:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = [c[1] for c in cursor.fetchall()]
            
            # Check for records for our target IDs
            # Most tables use 'employee_id' or 'emp_id' or 'EmployeeId'
            id_col = None
            for col in cols:
                if col.lower() in ['employee_id', 'emp_id', 'employeeid', 'id']:
                    id_col = col
                    break
            
            if id_col:
                query = f"SELECT * FROM {table} WHERE {id_col} IN ({','.join(['?']*len(target_emp_ids))}) LIMIT 10"
                cursor.execute(query, target_emp_ids)
                rows = cursor.fetchall()
                if rows:
                    results[table] = {
                        "columns": cols,
                        "data": [dict(zip(cols, row)) for row in rows]
                    }
        except Exception as e:
            results[table] = {"error": str(e)}

    conn.close()
    return results

if __name__ == "__main__":
    try:
        data = inspect_salary_att()
        print(json.dumps(data, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
