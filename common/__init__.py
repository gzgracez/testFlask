from flask import Flask, render_template, url_for, redirect, session
import sys, csv, sqlite3

from pprint import pprint

app = Flask('common')
app.secret_key = "keyboard cat"

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("""DROP TABLE pluto;""")

sql_command = """
CREATE TABLE pluto (
num INT PRIMARY KEY,
borough VARCHAR(3),
schoolDis INT,
address STRING,
floors FLOAT,
landmark CHAR(50),
zipCode INT);"""

cursor.execute(sql_command)

with open("common/mn.csv") as data:
    data_stuff = [a for a in csv.reader(data)]
    header = data_stuff[0]
    ndict_mapping = {}
    for i in xrange(0, len(header)):
        ndict_mapping[i] = header[i]
#data_stuff.pop()
del data_stuff[0]
for key in data_stuff:
    b = (key[0])
    if (key[6]!="  "): 
        print type(key[6])
        sd = int(key[6])
    else: sd = 0
    add = (key[12])
    if key[42]!="  ":
        floors = float(key[42])
    else: floors = 0
    lm = (key[63])
    if key[8]!="     ": zc = int(key[8])
    else: zc = 0
    #sql = "insert into pluto (borough, schoolDis, address, floors,landmark, zipCode) values (" + b + ", " + sd + ", " + add + ", " + floors + ", " + lm + ", " + zc + ");"
    sql = "insert into pluto (borough, schoolDis, address, floors,landmark, zipCode) values (\"%s\",%d,\"%s\",%d,\"%s\",%d);" % (b,sd,add,floors,lm,zc)
    print sql
    cursor.execute(sql)
connection.commit()
connection.close()

@app.route("/")
def index():
    return render_template("index.html", markers=data_stuff)

@app.route("/data")
def mstr():
    return render_template("data.html", data_stuff=data_stuff)