import sqlite3

#"證券代號","證券名稱","殖利率(%)","股利年度","本益比","股價淨值比","財報年/季"

bs = int(input('買進(1)賣出(2)查詢(3):'))
if bs == 3:
    symbol = input("請輸入股票代號: ")
    sql = '''
            SELECT 證券代號, 證券名稱, 本益比, 殖利率, 股價淨值比, ts FROM Stock
            WHERE 證券代號 = '%s'
          '''% symbol
else:
    pe = float(input('請輸入本益比: '))
    r  = float(input('請輸入殖利率: '))

    sql = '''
            SELECT 證券代號, 證券名稱, 本益比, 殖利率, 股價淨值比, ts FROM Stock
            WHERE (本益比 <= %.1f AND 本益比 > 0) AND 
                  (殖利率 >= %.1f AND 殖利率 > 0)AND 
                  (股價淨值比 %s 1 AND 股價淨值比 > 0)
          '''% (pe,r,'<' if bs == 1 else '>=')

conn = sqlite3.connect('twii.db')
cursor = conn.cursor()
cursor.execute(sql)
results = cursor.fetchall()

print('證券代號, 證券名稱, 本益比, 殖利率, 股價淨值比, ts')
for result in results:
    print(result)


#conn.commit()
conn.close()
