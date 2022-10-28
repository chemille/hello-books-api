from app import db 
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["GET"])
def read_all_books():
    books = Book.query.all() 
    books_response = [] 
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
    
    return make_response(f"Book {new_book.title} successfully created", 201)

# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description
        
# books = [
#     Book(1, "The Giving Tree", "One of Shel Silverstein's many books"),
#     Book(2, "The Very Hungry Caterpillar", "Popular children's book"),
#     Book(3, "The Snowy Day", "Caldecott Medal winner for beautiful illustrations")
# ] 


# # # helper fx
# def validate_book(book_id):
#     # handle invalid book_id, return 400
#     try:
#         book_id = int(book_id) 
#     except:
#         abort(make_response({"message": f"book {book_id} invalid"}, 400))
#     # search for book_id in data, return book
#     for book in books:
#         if book.id == book_id:
#             return book    
#     # return a 404 for non-existing book
#     abort(make_response({"message": f"book {book_id} not found"}, 404))

# @books_bp.route("/<book_id>", methods=["GET"])
# def handle_book(book_id):
#     book = validate_book(book_id) # call helper fx
#     # now this fx only does one thing: print out json that we want
#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description
#     }

