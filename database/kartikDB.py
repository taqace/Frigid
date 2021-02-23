import sqlite3
import random
from sqlite3 import Error


boxes = 'ABCDEFGHIJKLMNOPQRSTUVWX'
positions = 25
contents = ['virus-1','virus-2','virus-3','virus-4']
contacts = ['Patrick','Megan','John','Bob','Jim']
noteOne = ['abra','kadabra']
noteTwo = ['alla','kazam']
key = 1


def sql_connection():
    try:
        con = sqlite3.connect('kartik.db')
        print("Connection is established")
        return con
    except Error:
        print(Error)
       

def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE employees(key text PRIMARY KEY, box text,\
                      position text,contents text,contact text,note1 text, note2 text)")
    con.commit()

con = sql_connection() 
sql_table(con)
try:
    for i in boxes:
        for j in range(1,25):
            con.execute("""INSERT INTO employees(key,box,position,contents,contact,note1,note2) VALUES (?,?,?,?,?,?,?)""",\
                        (str(key),i,j,random.choice(contents),random.choice(contacts),random.choice(noteOne),random.choice(noteTwo)))
            key+=1
except:
    print('error')
con.commit()