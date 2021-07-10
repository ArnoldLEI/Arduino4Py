import sqlite3
import random


conn = sqlite3.connect('demo.db')
cursor = conn.cursor()

lottos = []

for i in range(1000):
    nums =set()
    while len(nums) < 5:
        n = random.randint(1,39)
        nums.add(n)
    lottos.append(tuple(nums))

sql = 'INSERT INTO Lotto(n1,n2,n3,n4,n5) '\
      'VALUES (?,?,?,?,?)'

cursor.executemany(sql, lottos)


conn.commit()
conn.close()