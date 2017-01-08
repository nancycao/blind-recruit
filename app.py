import os
from flask import Flask, request, redirect, url_for, render_template
import database
import parser

app = Flask(__name__)

@app.route("/", methods = ['POST','GET']) #Makes index show up when the root folder ("/") of the server is accessed by a user
def index():
    return render_template("main.html")

@app.route("/results/", methods = ['POST','GET'])
def results():
    link = request.form['link']
    json = parser.ocr_space_url(link)
    parsedText = json['ParsedResults'][0]['ParsedText']
    newText=""
    initials = "initials"
    name = ""
    phone = ""
    email = ""
    ID = database.genID()
    #database.insertEntry(initials, name, ID, phone, email)
    return render_template("results.html", initials=initials, id=ID, newText=parsedText)

@app.route("/search/", methods = ['POST','GET'])
def search():
    initials = request.form['initials']
    ID = request.form['id']
    entry = database.getEntry(initials, ID)
    return render_template("search.html", entry=entry)

if __name__ == "__main__": #Ensures that the app will only start if this file is not being imported from somewhere else but rather being accessed directly
    app.run()
