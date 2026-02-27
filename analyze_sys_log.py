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
    
    print("Distinct TableNames in sys_log:")
    cursor.execute("SELECT DISTINCT TableName FROM sys_log")
    for row in cursor.fetchall():
        print(f" - {row[0]}")
        
    print("\nDistinct OperateTypes in sys_log:")
    cursor.execute("SELECT DISTINCT OperateType FROM sys_log")
    for row in cursor.fetchall():
        print(f" - {row[0]}")

    print("\nSample records where TableName is not empty:")
    cursor.execute("SELECT * FROM sys_log WHERE TableName != '' LIMIT 10")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()
else:
    print("Database not found")
