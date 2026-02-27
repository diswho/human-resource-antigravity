import sqlite3
import json

db_path = r'c:\Users\phu_v\Documents\WorkSpaceAntigraty\human-resource\ZKTimeNet08.db'

def trace_new_list():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Names from user's new list
    names = ["PHUTTIYAR", "PHOUKHONG", "LIN"]
    
    results = {}
    
    # 1. Match names to emp_pin and id
    cursor.execute("SELECT id, emp_pin, emp_firstname, emp_lastname, department_id, position_id FROM hr_employee")
    employees = cursor.fetchall()
    
    matched_ids = []
    for emp in employees:
        for name in names:
            if name.lower() in str(emp[2]).lower() or name.lower() in str(emp[3]).lower():
                matched_ids.append(emp[0])
                results[f"emp_{emp[0]}"] = {
                    "id": emp[0],
                    "pin": emp[1],
                    "name": f"{emp[2]} {emp[3]}",
                    "dept_id": emp[4],
                    "pos_id": emp[5]
                }
                break

    # 2. Check formulas
    cursor.execute("SELECT * FROM pay_formula")
    cols = [description[0] for description in cursor.description]
    results['formulas'] = [dict(zip(cols, row)) for row in cursor.fetchall()]

    # 3. Check for matching salary records for these pins (if mapped)
    # Most salaryRecord tables use ePin as string
    pins = [results[k]['pin'] for k in results if k.startswith('emp_')]
    if pins:
        query = f"SELECT * FROM pay_salaryRecord WHERE ePin IN ({','.join(['?']*len(pins))})"
        cursor.execute(query, pins)
        cols = [description[0] for description in cursor.description]
        results['salary_records'] = [dict(zip(cols, row)) for row in cursor.fetchall()]

    conn.close()
    return results

if __name__ == "__main__":
    try:
        data = trace_new_list()
        print(json.dumps(data, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
