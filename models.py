from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from datetime import datetime


class User(db.Model):
    """
    User database Model

    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    books = db.relationship("Book", backref="author", lazy=True)

    def __repr__(self):
        """
        Representation method for user object

        """
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password):
        """
        Hashing Password method

        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Checking Password method

        """
        return check_password_hash(self.password, password)


class Book(db.Model):
    """
    Book database Model

    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    published_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        """
        Representation method for book object

        """
        return f"Book('{self.title}')"
