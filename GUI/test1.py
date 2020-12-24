import pymysql

db = pymysql.connect("localhost", "root", "1234", "db_opencv")
cursor = db.cursor()
sql = "SELECT * FROM sinhvien"
cursor.execute(sql)
data = cursor.fetchall()
print(data, "\n")