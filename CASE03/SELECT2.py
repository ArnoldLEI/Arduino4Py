import sqlite3
conn = sqlite3.connect('demo.db')
cursor = conn.cursor()

map = {}
for i in range(1,40):
    map[i] = 0


cursor.execute('PRAGMA TABLE_INFO("Lotto")')
names = [t[1] for t in cursor.fetchall()]



for name in names:
    print(name, end = '\t')
print('\n----------------------------------------------')

sql = ' SELECT id,n1,n2,n3,n4,n5,ts'\
      ' FROM Lotto'
cursor.execute(sql)
rows = cursor.fetchall()

for r in rows:
    for i in range(1,6):
        map[r[i]] = map[r[i]] + 1

print(map)
maxVal = max(map.values())
minVal = min(map.values())
print("max: ",maxVal)

for k, v in map.items():
    if (v==maxVal):
        print("%d (%d)" % (k,maxVal))
    if (v == minVal):
        print("%d (%d)" % (k, minVal))

"""for r in rows:
    print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t'
          .format(r[0],r[1],r[2],r[3],r[4],r[5],r[6]))"""

cursor.close()