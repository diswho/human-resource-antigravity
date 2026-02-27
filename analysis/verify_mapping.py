import sqlite3
import json

db_path = r'c:\Users\phu_v\Documents\WorkSpaceAntigraty\human-resource\ZKTimeNet08.db'

def verify_mapping():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Target employees from user request
    # 1: 60004 (Poum Chanthavong)
    # 2: 200126 (Maneevone Inthavong)
    # 3: 200045 (Latsamee Inthilath)
    # 4: 200152 (Voutthanakone Seehalath)
    # 5: 200397 (Souksavanh Manolom)
    # ...
    pins = ["60004", "200126", "200045", "200152", "200397", "200021", "200109", "1200223"]
    
    mapping_results = []
    
    for pin in pins:
        # Get Employee basic info
        cursor.execute("""
            SELECT e.emp_pin, e.emp_firstname, e.emp_lastname, e.emp_gender, e.emp_hiredate, p.posi_name, d.dept_name
            FROM hr_employee e
            LEFT JOIN hr_position p ON e.position_id = p.id
            LEFT JOIN hr_department d ON e.department_id = d.id
            WHERE e.emp_pin = ?
        """, (pin,))
        emp = cursor.fetchone()
        
        if emp:
            res = {
                "ລະຫັດ (ID)": emp[0],
                "ຊື່ (FirstName)": emp[1],
                "ນາມສະກຸນ (LastName)": emp[2],
                "ເພດ (Gender)": "ຍິງ" if emp[3] == 1 or (emp[1] and "Miss" in emp[1] or "ನ" in emp[1]) else "ຊາຍ",
                "ວ/ດ/ປ ເຂົ້າວຽກ (HireDate)": emp[4],
                "ຕຳແໜ່ງ (Position)": emp[5],
                "ພະແນກ (Dept)": emp[6]
            }
            mapping_results.append(res)
        else:
            mapping_results.append({"ລະຫັດ (ID)": pin, "status": "Not Found"})

    # Check for attendance summary (if possible)
    # Looking for tables that might have sum data
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE '%att%' OR name LIKE '%pay%');")
    att_tables = [row[0] for row in cursor.fetchall()]

    conn.close()
    return {
        "employee_mappings": mapping_results,
        "available_att_tables": att_tables
    }

if __name__ == "__main__":
    try:
        results = verify_mapping()
        print(json.dumps(results, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
