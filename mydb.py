import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '',
)

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create database
cursorObject.execute("CREATE DATABASE company")

print("All done!")