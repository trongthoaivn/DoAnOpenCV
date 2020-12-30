import sqlite3
import os


def updateSqliteTable():
    sqliteConnection = sqlite3.connect("D:\\DoAnOpenCV\Database\db_opencv.db")
    cursor = sqliteConnection.cursor()
    query = "SELECT * FROM SINHVIEN"
    cursor.execute(query)
    data = cursor.fetchall()
    while True:
        a = input("maSV:")
        for row in data:
            if row[0] == a:
                print(row[0] + " " + row[1])
                data.remove(row)
        if a == "e":
            break


updateSqliteTable()
