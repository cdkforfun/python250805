# db1.py
import sqlite3

con = sqlite3.connect(r"c:\work\sample.db") 

cur = con.cursor()
cur.execute("create table PhoneBook (name text, phone text);")
cur.execute("insert into PhoneBook values ('홍길동', '010-1234-5678');")
name = "이순신"
phone = "010-9876-5432" 
cur.execute("insert into PhoneBook values (?, ?);", (name, phone))
datalist = [("강감찬", "010-1111-2222"), ("유관순", "010-3333-4444")]
cur.executemany("insert into PhoneBook values (?, ?);", datalist)
cur.execute("select * from PhoneBook;")
for row in cur:
    print(row)

con.commit()  # 변경사항 저장

