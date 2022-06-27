import mysql.connector

FNAME_INDEX = 1

mydb = mysql.connector.connect(
  host="localhost",
  user="djangouser",
  password="capstone2022",
  database="mmd"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM student")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
