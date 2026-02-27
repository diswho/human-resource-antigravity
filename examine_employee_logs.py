import sqlite3
import os
import sys

# Set encoding for output to handle Lao characters
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

db_path = "ZKTimeNet08.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Employee logs sample:")
    cursor.execute("SELECT * FROM sys_log WHERE TableName = 'Employee' LIMIT 20")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()
else:
    print("Database not found")
