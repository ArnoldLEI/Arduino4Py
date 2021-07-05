import sqlite3



sql = 'UPDATE Lotto SET n1=%d, n2=%d WHERE id = %d '\
      %(30,32,1)

print(sql)

conn = sqlite3.connect('demo.db')
cursor = conn.cursor()
cursor.execute(sql)

print("UPDATE OK , rowcunt:" ,cursor.rowcount)
conn.commit()
conn.close()
