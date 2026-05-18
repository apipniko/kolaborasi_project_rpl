import mysql.connector
koneksi = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='toy_recommendation_db'
)
cursor = koneksi.cursor(dictionary=True)