from flask import request, jsonify, url_for
from app import app, db
from models import User, Book
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from sqlalchemy import or_
import re
from serializers import serialize_book
from utils import is_author


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"message": "Please enter a valid email"}), 400

    if User.query.filter(or_(User.username == username, User.email == email)).first():
        return jsonify({"message": "Username or email already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200


@app.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": new_access_token}), 200


@app.route("/api/books", methods=["POST"])
@jwt_required()
def add_book():
    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"message": "Please enter valid data"}), 400

    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    if not current_user:
        return jsonify({"message": "User not found"}), 404

    book = Book(title=title, author=current_user)
    db.session.add(book)
    db.session.commit()

    return (
        jsonify({"message": "Book added successfully", "book": serialize_book(book)}),
        201,
    )


@app.route("/api/books", methods=["GET"])
@jwt_required()
def get_books():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    books_query = Book.query.paginate(page=page, per_page=per_page, error_out=False)

    books = books_query.items

    serialized_books = [serialize_book(book) for book in books]

    pagination_info = {
        "count": books_query.total,
        "current_page": books_query.page,
        "per_page": books_query.per_page,
    }

    if books_query.has_next:
        pagination_info["next_page"] = url_for(
            "get_books", page=books_query.next_num, per_page=per_page, _external=True
        )
    if books_query.has_prev:
        pagination_info["prev_page"] = url_for(
            "get_books", page=books_query.prev_num, per_page=per_page, _external=True
        )

    return jsonify({"results": serialized_books, "pagination": pagination_info}), 200


@app.route("/api/books/<int:book_id>", methods=["GET"])
@jwt_required()
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(serialize_book(book)), 200


@app.route("/api/books/<int:book_id>", methods=["PATCH"])
@jwt_required()
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get_or_404(book_id)
    current_user = User.query.filter_by(email=get_jwt_identity()).first()

    if not is_author(book, current_user):
        return jsonify({"message": "Forbidden!"}), 403

    book.title = data.get("title")

    db.session.commit()

    return jsonify(serialize_book(book)), 200


@app.route("/api/books/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    current_user = User.query.filter_by(email=get_jwt_identity()).first()

    if not is_author(book, current_user):
        return jsonify({"message": "Forbidden!"}), 403

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200
