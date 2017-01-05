import psycopg2
import csv

#connect to database and set up to execute commands

#connect to database (currently connecting to local db)
conn = psycopg2.connext("dbname=postgres user=Amos")

#cursor to perform database operations
cur = conn.cursor()

#perform commands enclosed in parenthesis (must follow by cur.fetch___() to get tuple back)
cur.execute("CREATE TABLE table (id serial PRIMARY KEY, num integer, data varchar")
cur.execute("SELECT * FROM table")
cur.fetchall()

#make changes to databse persistent
conn.commit()

#disconnect/close db
cur.close()
conn.close()