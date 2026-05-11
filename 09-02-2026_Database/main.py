# import pyodbc
# import sys
#
#
#
# #connection establish
# connString = (
#     'DRIVER={ODBC Driver 17 for SQL Server};'
#     'SERVER=localhost;'
#     'DATABASE=StudentDB;'
#     'Trusted_Connection=yes;'
# )
#
# #connect to database
# try:
#     conn = pyodbc.connect(connString)
#     print("Connected to DB")
# except Exception as e:
#     print(str(e))
#     sys.exit(0)
#
# #prepare the query
# query = 'Insert into S_Table1(Student_ID,First_name,Last_name,DOB,Standard,Section) values (?,?,?,?,?,?);'
# to_filter = [
#     ('jv',"patel",8,4,"A")
# ]
#
#
# try:
#     cur = conn.cursor()
#     cur.executemany(query, to_filter)
#     conn.commit()
# except Exception as e:
#     print(str(e))
#     conn.close()
#     sys.exit(0)
#
#
# #close the connection
# conn.close()


import pyodbc
import sys



#connection establish
# connString = (
#     'DRIVER={ODBC Driver 17 for SQL Server};'
#     'SERVER=localhost;'
#     'DATABASE=StudentDB;'
#     'Trusted_Connection=yes;'
# )
#
# #connect to database
# try:
#     conn = pyodbc.connect(connString)
#     print("Connected to DB")
# except Exception as e:
#     print(str(e))
#     sys.exit(0)
#
# #prepare the query
# query = 'Insert into Table2(First_name,Last_name) values (?,?);'
# to_filter = [
#     ('jv',"patel"),
#     ('atri',"patel")
# ]
#
#
# try:
#     cur = conn.cursor()
#     cur.executemany(query, to_filter)
#     conn.commit()
# except Exception as e:
#     print(str(e))
#     conn.close()
#     sys.exit(0)
#
#
# #close the connection
# conn.close()