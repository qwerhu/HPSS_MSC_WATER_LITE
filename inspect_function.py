import cx_Oracle
import sys

db = cx_Oracle.connect('zlsdb','hbjt_zlsdb','10.10.1.127/server1')
print(db)

cursor = db.cursor()

sql = 'select * from A_FM'

cursor.execute(sql)

rs1 = cursor.fetchone()
print(rs1)

rs = cursor.fetchall()
print(rs)
print(sys.platform)



