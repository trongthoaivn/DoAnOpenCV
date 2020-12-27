import sqlite3


def updateSqliteTable():

    Id = input("Id: ")
    Name = input("Name :")
    Birth = input("Birth :")
    Sex = input("Sex :")
    Class = input("Class :")
    try:
        sqliteConnection = sqlite3.connect('D:\\DoAnOpenCV\db_opencv.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        query = query = "update  sinhvien set maSV='%s', hotenSV ='%s', ngaysinhSV ='%s', gioitinhSV ='%s', lopSV='%s' where maSV='%s'" % (Id, Name, Birth, Sex, Class, Id)
        cursor.execute(query)
        sqliteConnection.commit()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)


updateSqliteTable()