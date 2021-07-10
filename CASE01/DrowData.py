# -*- coding: UTF-8 -*-
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('iot.db')
df = pd.read_sql_query("SELECT id, cds, temp, humi, ts FROM Env "
                       "order by ts desc limit 15", con=conn)
df = df[::-1] # reverse
print(df)

# 繪圖
plt.plot(df['ts'], df['temp'], label="temp")  # 繪製折線圖
plt.plot(df['ts'], df['humi'], label="humi")  # 繪製折線圖
plt.grid(True)
# 圖例
plt.xlabel('time')
plt.ylabel('value')
plt.xticks(rotation=90)
plt.legend()
plt.show()

conn.close()