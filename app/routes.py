from flask import Blueprint, jsonify

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description
        
books = [
    Book(1, "The Giving Tree", "One of Shel Silverstein's many books"),
    Book(2, "The Very Hungry Caterpillar", "Popular children's book"),
    Book(3, "The Snowy Day", "Caldecott Medal winner for beautiful illustrations")
] 

hello_world_bp = Blueprint("hello_world", __name__)

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("/<book_id>", methods=["GET"])
def handle_book(book_id):
    book_id = int(book_id)
    for book in books:
        if book.id == book_id:
            return {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
            
    return {"message": f"book {book_id} not found"}, 404

@books_bp.route("", methods=["GET"])
def handle_books():
    books_response = [] 
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })   
    return jsonify(books_response), 200

@hello_world_bp.route("/hello-world", methods=["GET"]    
)
def say_hello_world():
    my_beautiful_world = "Hello, World!"
    return my_beautiful_world, 200

@hello_world_bp.route("/hello/JSON", methods=["GET"])
def say_hello_json():
    return {
        "name": "Chemille",
        "message": "Need more coffee!", 
        "hobbies": ["Snacks", "Coding", "Cooking"]
    }, 200
    
@hello_world_bp.route("/broken-endpoint-with-broken-server-code", methods=["GET"])
def broken_endpoint():
    response_body = {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }
    
    new_hobby = "Surfing"
    response_body["hobbies"].append(new_hobby)
    return response_body