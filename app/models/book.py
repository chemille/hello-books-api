from app import db


class Book(db.Model): # this tells SQLAlchemy this is a book class which is a model
    # and it has these 3 columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    
    def to_string(self):
        return f"{self.id}: {self.title} Description: {self.description}"