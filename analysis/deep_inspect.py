import sqlite3
import json

db_path = r'c:\Users\phu_v\Documents\WorkSpaceAntigraty\human-resource\ZKTimeNet08.db'

def deep_inspect_employees():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Names from new list - being more flexible with searching
    names = ["PHUTTIYAR", "KHUNTHAMOUN", "PHOUKHONG", "SAENGSOULICHAN", "LIN", "PHONEPASERD", "VOUTTHANAKONE", "SEEHALATH"]
    
    results = {}
    
    # 1. Broad search for these people
    cursor.execute("SELECT * FROM hr_employee")
    cols = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    
    matched_emps = []
    for row in rows:
        record = dict(zip(cols, row))
        full_text = " ".join(str(v) for v in record.values()).lower()
        for name in names:
            if name.lower() in full_text:
                matched_emps.append(record)
                break
    
    results['matched_employees'] = matched_emps

    # 2. Check CustomStateValue for "bank" or "account"
    try:
        cursor.execute("SELECT * FROM CustomStateValue WHERE CustomName LIKE '%bank%' OR CustomName LIKE '%account%' OR Value LIKE '%bank%' OR Value LIKE '%account%'")
        cols = [description[0] for description in cursor.description]
        results['custom_state_bank'] = [dict(zip(cols, row)) for row in cursor.fetchall()]
    except: pass

    # 3. Check for the account numbers themselves as substrings in ALL text columns of hr_employee
    accounts = ["05720040000011893", "05720040000017878", "05720040000017867"]
    matches_in_emp = []
    for row in rows:
        record = dict(zip(cols, row))
        for acc in accounts:
            if any(acc in str(v) for v in record.values()):
                matches_in_emp.append(record)
                break
    results['account_matches_in_hr_employee'] = matches_in_emp

    conn.close()
    return results

if __name__ == "__main__":
    try:
        data = deep_inspect_employees()
        print(json.dumps(data, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
