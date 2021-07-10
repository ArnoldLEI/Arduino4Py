import sqlite3


sql = '''
        SELECT NAME,MAX(SALARY) AS 最高薪資 FROM Employee
        UNION ALL
        SELECT NAME,MIN(SALARY) AS 最低薪資 FROM Employee
      '''

conn = sqlite3.connect('../CASE03/demo.db')
cursor = conn.cursor()
cursor.execute(sql)
rows = cursor.fetchall()
print(rows)

conn.commit()