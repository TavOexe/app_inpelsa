import pypyodbc
import sys

DRIVER = 'SQL Server'
SERVER = 'DESKTOP-T3ER55E\SQLEXPRESS'
DATABASE = '007BDCOMUN'
#uid = <username>
#pwd = <password>
connection_string = f"""
    DRIVER={{{DRIVER}}};
    SERVER={SERVER};
    DATABASE={DATABASE};
    Trusted_Connection=yes;
"""
conn = pypyodbc.connect(connection_string)
print(conn)

cursor = conn.cursor()
cursor.execute("SELECT * FROM dbo.VENTASINVENTARIO")
row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()

cursor.close()
conn.close()

# Path: prueba-dbinpelsa.py