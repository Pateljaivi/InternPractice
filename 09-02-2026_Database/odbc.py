import pyodbc

conn = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=CricketDB;'
    'Trusted_Connection=yes;'
)


try:
    conn = pyodbc.connect(conn)
    print("Successfully connected to database....")
except Exception as e:
    print(f"Still not working?Here is why:{e}")
cursor = conn.cursor()#->cursor object act as a middleware between sql database connection and sql commands


cursor.execute("INSERT INTO Cricket1(name,age) VALUES  ('bumrah', 40),( 'hardik', 36),('Axar Patel', 24)")
# row = cursor.fetchall()
# print(row)
conn.commit()
cursor.close()
conn.close()
