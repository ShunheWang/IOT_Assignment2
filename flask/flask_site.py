
from flask import Flask, Blueprint, request, jsonify, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from database_utils import DatabaseUtils

site = Blueprint("site", __name__)
"""
set rout and create button function 
get data from form 
use the function create in api
to make change by json

set session when login 
set login home report1 ,report 2 
set logic when delete/update/and create


#clear session function
"""
# home webpage.
@site.route("/")
def index():
    #check session
    if(session.get("login") is None):
        return redirect("/login")
    else:
 
        # Use REST API.
        response = requests.get("http://127.0.0.1:5000/book")
        data = json.loads(response.text)

        return render_template("home.html",  books = data)
# report page
@site.route("/report1")
def report1():
    if(session.get("login") is None):
        return redirect("/login")
    else:
        return render_template("report1.html")
@site.route("/report2")
def report2():
    if(session.get("login") is None):
        return redirect("/login")
    else:
        return render_template("report2.html")
# login page set session if login successful
@site.route("/login", methods = ["GET", "POST"])
def login():
    # Use REST API.
    if(request.method == "POST"):
        lemail = request.form["lemail"]
        lpassword = request.form["lpassword"]
        if lemail=="admin" and lpassword=="abc123":
            session["login"] =lemail
            return redirect("/")
    
    return render_template("login.html")

# admin webpage.
@site.route("/createbook", methods = ["POST"])
def createbook(): 
    title = request.form["Title"]
    author = request.form["Author"]
    publishedDate = request.form["PublishedDate"]
    status = "avaliable"
    isbn = request.form["ISBN"]
    sequenceNo = 1
    with DatabaseUtils() as db:
        for no in db.getTitle():
            if  no[0]==title:
               sequenceNo = sequenceNo + 1
    headers = {
        "Content-type": "application/json"
    }
    data = {
        "Title": title,
        "Author": author,
        "PublishedDate": publishedDate,
        "Status": status,
        "ISBN": isbn,
        "SequenceNo": sequenceNo
    }       
    response = requests.post("http://127.0.0.1:5000/book", data = json.dumps(data), headers = headers)   

    # redirect back to home
    return redirect("/")
#admin page
@site.route("/updatebook", methods = ["POST"])
def updatebook():
    bookid = request.form["BookID"]
    title = request.form["Title"]
    author = request.form["Author"]
    publishedDate = request.form["PublishedDate"]
    isbn = request.form["ISBN"]
    sequenceNo="1"


    headers = {
        "Content-type": "application/json"
    }

    data = {
        "BookID": bookid,
        "Title": title,
        "Author": author,
        "PublishedDate": publishedDate,
        "ISBN": isbn,
        "SequenceNo": sequenceNo
    
    }

    response = requests.put("http://127.0.0.1:5000/book/"+bookid, data = json.dumps(data), headers = headers)
    # read response if needed

    # redirect back to home
    return redirect("/")

    # response = requests.get("http://127.0.0.1:5000/book")
    # data = json.loads(response.text)

    # return render_template("home.html",  books = data)
@site.route("/deletebook", methods = ["POST"])
def deletebook():
    bookid = request.form["BookID"]
    with DatabaseUtils() as db:
          for no in db.getBookState(bookid):
            if  no[0]=="borrowed":
                 print("can not borrow")
            else:
                response=requests.delete("http://127.0.0.1:5000/book/"+bookid)
    return redirect("/")
             #   sequenceNo=1
       
#clear session function
    
@site.route("/logout", methods = ["POST"])
def logout():
    session.clear()
    return render_template("login.html")






            