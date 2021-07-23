# -*- coding: UTF-8 -*-
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt



def ConnectSQL(DBName,UID,PWD):
    server = 'localhost'
    database = DBName
    username = UID
    password = PWD
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    return cursor

cursor = ConnectSQL("iot", "SAM", "lf2netae86")



cursor.execute("SELECT TOP(15) id, cds, temp, humi, ts FROM Env "
                       "order by ts desc;")


'''row = cursor.fetchone()
while row:
    print(row[4])
    row = cursor.fetchone()'''

rows = cursor.fetchall()
result = ""
rowt = []
rowh = []
rowts = []
#print(rows)
for row in rows:
    #print(row.cds, row.temp,row.humi,row.ts)
    print(row)
    result+="{0}\t{1}\t{2}\t{3}\r\n".format(row.cds, row.temp,row.humi,row.ts)
    rowt.append(row.temp)
    rowh.append(row.humi)
    rowts.append(row.ts)


# 繪圖
plt.plot(rowts, rowt, label="temp")  # 繪製折線圖
plt.plot(rowts, rowh, label="humi")  # 繪製折線圖
plt.grid(True)
# 圖例
plt.xlabel('time')
plt.ylabel('value')
plt.xticks(rotation=90)
plt.legend()
plt.show()

