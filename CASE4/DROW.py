import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('../CASE03/demo.db')
df = pd.read_sql_query("SELECT NAME,SALARY FROM Employee", con=conn)
print(df)

ma = df['SALARY'].rolling(window = 2).mean()
print(ma)
plt.plot(df.NAME.values, df.SALARY.values, 'r.')
plt.plot(df['NAME'],df['SALARY'])
plt.plot(df['NAME'],ma)

plt.xlabel('NAME')
plt.ylabel('SALARY')

plt.show()

conn.close()