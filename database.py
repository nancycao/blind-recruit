import sqlite3
import string
import random

def createDB():
    f="hires.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops
    q = "CREATE TABLE people (initials TEXT, name TEXT, id TEXT, phone TEXT, email TEXT)" # phone TEXT, email TEXT
    c.execute(q)
    db.commit()
    db.close()

def insertEntry(initials, name, ID, phone, email):
    f="hires.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops
    q = "INSERT INTO people VALUES ('%s', '%s', '%s', '%s', '%s');"%(initials, name, ID, phone, email)
    c.execute(q)
    db.commit()
    db.close()

def genID(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getEntry(initials, ID):
    f="hires.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops
    q = "SELECT * FROM people where initials='%s' and ID='%s'"%(initials, ID)
    c.execute(q)
    return(c.fetchall()[0]) # returns ('NC', 'nancy', '59WK3C', '9171231234', 'ncao@stuy.edu')

#createDB()
#insertEntry("NC", "nancy", "9171231234", "ncao@stuy.edu")
getEntry("NC", "59WK3C")
