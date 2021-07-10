import sqlite3
import requests
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt

symbol = "2330"
date = "20210624"
path = "https://www.twse.com.tw/exchangeReport/BWIBBU?response=csv&date=%s&stockNo=%s"%(date,symbol)

#"日期","殖利率(%)","股利年度","本益比","股價淨值比","財報年/季"

csv = requests.get(path).text

#print(csv)


data = csv.split('\r\n')
data = list(filter(lambda l: len(l.split(',')) == 7, data ))
data = "\n".join(data)
#print(data)
df = pd.read_csv(StringIO(data))
df = df[df.columns[df.isnull().all() == False]]
#print(df.dtypes)
df = df.rename(columns={'殖利率(%)':'殖利率'})
df = df.rename(columns={'財報年/季':'財報年季'})
print(df)

plt.plot(df['日期'], df['殖利率'])
plt.show()

plt.plot(df['日期'], df['本益比'])
plt.show()

plt.plot(df['日期'], df['股價淨值比'])
plt.show()








