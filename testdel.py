import os


for x in range(2,11):
    if os.path.exists(r"D:\\DoAnOpenCV\test\User.1.%s.jpg" % x):
        os.remove(r"D:\\DoAnOpenCV\test\User.1.%s.jpg" % x)
    else:
        print("The file does not exist")
