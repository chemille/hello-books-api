from app import db 
from app.models.book import Book
from flask import Blueprint, jsonify, abort, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")

### helper fxs
def validate_book(book_id):
    # handle invalid book_id, return 400
    try:
        book_id = int(book_id) 
    except:
        abort(make_response({"message": f"book {book_id} invalid"}, 400))
    
    book = Book.query.get(book_id) # SQLAlchemy syntax to query for one Book resource. Returns an instance of Book.
    # This get method returns None if book is not found, so we need to handle it below
    
    if not book:
        abort(make_response({"message": f"book {book_id} not found"}, 404))
        
    return book # If book is truthy and found, it will return it and be stored in validate_book

## route fxs
@books_bp.route("", methods=["GET"])
def read_all_books():        
    books_response = [] 
    
    title_query = request.args.get("title") # this gets key-value pair in url 
    
    if title_query is not None:
        books = Book.query.filter_by(title=title_query) #keyword arg
        # so it's going to look for a field in our table called title and 
        # it's going to get all the books that match this title
    else:
        books = Book.query.all() 
        
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })   
    return jsonify(books_response)
    
@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()    
    new_book = Book(
        title = request_body["title"],
        description = request_body["description"]
    )
    db.session.add(new_book)
    db.session.commit()
    
    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)

@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id): # this fx is called whenever the HTTP reqest matches the decorator
    book = validate_book(book_id) # call helper fx
#     # now this fx only does one thing: print out json that we want
    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id) # use helper fx
    request_body = request.get_json()    
    
    book.title = request_body["title"]
    book.description = request_body["description"]
    # we never want to update an id. It's covered by postgreSQL
    
    db.session.commit() # this commits the change that we made so that it persists in the db
    
    return make_response(jsonify(f"Book #{book_id} successfully updated"))

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id) # use helper fx   
    
    db.session.delete(book)
    db.session.commit()
    
    return make_response(jsonify(f"Book #{book_id} successfully deleted"))