import sqlite3
import os

def updateSqliteTable():
    Id = "1811060744"
    sqliteConnection = sqlite3.connect("D:\\DoAnOpenCV\Database\db_opencv.db")
    cursor = sqliteConnection.cursor()
    query = "SELECT hotenSV FROM SINHVIEN WHERE maSV='%s'" % Id
    cursor.execute(query)
    input="(',)"
    output="    "
    data = str(cursor.fetchone())
    trans = data.maketrans(input, output)
    print(data.translate(trans).strip(" "))


updateSqliteTable()
