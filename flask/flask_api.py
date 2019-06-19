from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json

api = Blueprint("api", __name__)

db = SQLAlchemy()
ma = Marshmallow()
"""


function addBook/getBook/getBookWithID/bookDelete delete by 
id ,update

"""
# Declaring the model.
class Books(db.Model):
    __tablename__ = "Books"
   # ISBN  = db.Column(db.Integer, primary_key = True, autoincrement = True)
    #AuthorName = db.Column(db.Text)
    #BookName = db.Column(db.Text)
    #number = db.Column(db.Text)
    BookID=db.Column(db.Integer, primary_key = True, autoincrement = True)
    Title = db.Column(db.Text)
    Author = db.Column(db.Text)
    PublishedDate = db.Column(db.Text)
    Status = db.Column(db.Text)
    ISBN = db.Column(db.Text)
    SequenceNo = db.Column(db.Text)
    # Username = db.Column(db.String(256), unique = True)

    def __init__(self, Title,Author,PublishedDate,Status,ISBN,SequenceNo,BookID  = None):
        self.BookID  = BookID 
        self.Title = Title
        self.Author = Author 
        self.PublishedDate = PublishedDate 
        self.Status = Status 
        self.ISBN = ISBN 
        self.SequenceNo = SequenceNo 

class BooksSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("BookID", "Title","Author","PublishedDate","Status","ISBN","SequenceNo")
        #fields = ("ISBN", "AuthorName","BookName","number")

BookSchema = BooksSchema()
booksSchema = BooksSchema(many = True)

# Endpoint to show all book
@api.route("/book", methods = ["GET"])
def getBook():
    books = Books.query.all()
    result = booksSchema.dump(books)

    return jsonify(result.data)

# Endpoint to get book by id.
@api.route("/book/<id>", methods = ["GET"])
def getBookWithID(id):
    book = Books.query.get(id)

    return BookSchema.jsonify(book)

# Endpoint to create new book
@api.route("/book", methods = ["POST"])
def addBook():
    Title = request.json["Title"]
    Author = request.json["Author"]
    PublishedDate = request.json["PublishedDate"]
    Status="available"
    ISBN = request.json["ISBN"]
    SequenceNo=request.json["SequenceNo"]


    newBook = Books(Title = Title,Author=Author,PublishedDate=PublishedDate,Status=Status,ISBN=ISBN,SequenceNo=SequenceNo)
  
    db.session.add(newBook)
    db.session.commit()

    return BookSchema.jsonify(newBook)

# Endpoint to update book.
@api.route("/book/<id>", methods = ["PUT"])
def bookUpdate(id):
    book = Books.query.get(id)
    Title = request.json["Title"]
    Author = request.json["Author"]
    PublishedDate = request.json["PublishedDate"]
    ISBN = request.json["ISBN"]
    SequenceNo = request.json["SequenceNo"]
    


    book.Title = Title
    book.Author = Author
    book.PublishedDate = PublishedDate
    book.ISBN=ISBN
    book.SequenceNo=SequenceNo

    db.session.commit()

    return BookSchema.jsonify(book)

# Endpoint to deletebook.
@api.route("/book/<id>", methods = ["DELETE"])
def bookDelete(id):
    book = Books.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return BookSchema.jsonify(book)


