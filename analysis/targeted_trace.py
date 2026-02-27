import sqlite3
import json

db_path = r'c:\Users\phu_v\Documents\WorkSpaceAntigraty\human-resource\ZKTimeNet08.db'

def targeted_trace():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Target bank accounts
    accounts = [
        "03120040000007523", "05720040000005642", "04120030000012386",
        "05720040000003838", "05720040000015668", "05720040000002575",
        "00220030000034727", "02720010010026362", "05720040000011893",
        "05720040000017878", "05720040000017867"
    ]
    
    # Target net salary amounts
    salaries = [6900000, 5400000, 2995125, 3200000, 4800000, 4850000, 4200000, 3400000, 3500000, 4000000]

    results = {}

    # 1. Search in pay_empDetail (most likely for bank accounts)
    try:
        cursor.execute("SELECT * FROM pay_empDetail")
        cols = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        for row in rows:
            record = dict(zip(cols, row))
            for acc in accounts:
                if str(record.get('bank_account')) == acc or str(record.get('bank_accounts')) == acc or str(record.get('agent_account')) == acc:
                    if 'pay_empDetail' not in results: results['pay_empDetail'] = []
                    results['pay_empDetail'].append(record)
                    break
    except: pass

    # 2. Search in hr_employee (sometimes stored in custom fields)
    try:
        cursor.execute("SELECT * FROM hr_employee")
        cols = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        for row in rows:
            record = dict(zip(cols, row))
            for acc in accounts:
                # Check all text columns
                if any(str(val) == acc for val in record.values()):
                    if 'hr_employee' not in results: results['hr_employee'] = []
                    results['hr_employee'].append(record)
                    break
    except: pass

    # 3. Search in pay_salaryRecord (for NetPay)
    try:
        cursor.execute("SELECT * FROM pay_salaryRecord ORDER BY createTime DESC LIMIT 200")
        cols = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        for row in rows:
            record = dict(zip(cols, row))
            for s in salaries:
                if record.get('NetPay') and abs(record['NetPay'] - s) < 1:
                    if 'pay_salaryRecord' not in results: results['pay_salaryRecord'] = []
                    results['pay_salaryRecord'].append(record)
                    break
    except: pass

    conn.close()
    return results

if __name__ == "__main__":
    try:
        data = targeted_trace()
        print(json.dumps(data, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
