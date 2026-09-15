import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  database="ciel2027"
)

mycursor = mydb.cursor()

sql = "INSERT INTO etudiant (nom, prenom) VALUES (%s, %s)"
val = ("John", "Doe")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")