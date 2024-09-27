import sqlite3

def create():
   with sqlite3.connect('database.db') as conn:
      cur = conn.cursor()
      cur.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER, name TEXT)")
      cur.execute("INSERT INTO STUDENTS VALUES(1,'Claus')")
      cur.execute("INSERT INTO STUDENTS VALUES(2,'Andreas')")
      cur.execute("INSERT INTO STUDENTS VALUES(3,'Emil')")
      cur.execute("INSERT INTO STUDENTS VALUES(4,'Torben')")

   

def read():
   
   students =[]
   
   with sqlite3.connect('database.db') as conn:
      cur = conn.cursor()
      cur.execute('SELECT * from students')
      for i in cur.fetchall():
         students.append({'id':i[0],'name':i[1]})

   return students

read()