import mysql.connector

connection = mysql.connector.connect(user="root", password="root", host="mysql", port="3306", database="db")
print("Succesfully connected to db")

cursor = connection.cursor()
cursor.execute("SELECT * FROM items")
items = cursor.fetchall()
connection.close()

print("results are: ", items)
