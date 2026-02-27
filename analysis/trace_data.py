import sqlite3
import json

db_path = r'c:\Users\phu_v\Documents\WorkSpaceAntigraty\human-resource\ZKTimeNet08.db'

def trace_data():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Target bank accounts to trace
    accounts = [
        "03120040000007523", "05720040000005642", "04120030000012386",
        "05720040000003838", "05720040000015668", "05720040000002575",
        "00220030000034727", "02720010010026362", "05720040000011893",
        "05720040000017878", "05720040000017867"
    ]
    
    # Target net salary amounts to trace
    salaries = [6900000, 5400000, 2995125, 3200000, 4800000, 4850000, 4200000, 3400000, 3500000, 4000000]

    # Find where accounts are stored
    account_locations = {}
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        try:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = [c[1] for c in cursor.fetchall()]
            
            for col in cols:
                # Check for accounts in text columns
                for acc in accounts:
                    query = f"SELECT COUNT(*) FROM {table} WHERE \"{col}\" = ?"
                    cursor.execute(query, (acc,))
                    count = cursor.fetchone()[0]
                    if count > 0:
                        if table not in account_locations: account_locations[table] = []
                        if col not in account_locations[table]: account_locations[table].append(col)
        except:
            continue

    # Query pay_salaryRecord for the target salaries
    salary_record_samples = []
    try:
        cursor.execute("SELECT * FROM pay_salaryRecord ORDER BY createTime DESC LIMIT 50")
        cols = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        for row in rows:
            record = dict(zip(cols, row))
            # Check if NetPay or Total matches any in our list (rounding might be an issue)
            for s in salaries:
                if record.get('NetPay') and abs(record['NetPay'] - s) < 10:
                    salary_record_samples.append(record)
                    break
    except:
        pass

    conn.close()
    return {
        "account_locations": account_locations,
        "salary_record_samples": salary_record_samples
    }

if __name__ == "__main__":
    try:
        results = trace_data()
        print(json.dumps(results, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
