import unittest
from app import app, db
from models import User, Book
from flask_jwt_extended import create_access_token
from test_data import register_user_data, book_data, updated_book_data
from datetime import datetime
import os


class Test(unittest.TestCase):

    def setUp(self):
        """Set up test environment"""
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL","sqlite:///:memory:")
        self.app = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

            # Add User
            self.user = User(username="testuser", email="test@example.com")
            self.user.set_password("testpassword")
            db.session.add(self.user)
            db.session.commit()

            # Add Book
            self.book = Book(
                title="Game Of Thrones",
                author_id=self.user.id,
                published_date=datetime.now(),
            )
            db.session.add(self.book)
            db.session.commit()

            # Add another user for unthorized tests
            unauthorized_user = User(
                username="unauthorized", email="unauthorized@example.com"
            )
            unauthorized_user.set_password("12345678")
            db.session.add(unauthorized_user)
            db.session.commit()

            # Add Tokens
            self.access_token = create_access_token(identity="test@example.com")
            self.unauthorized_access_token = create_access_token(
                identity="tunauthorized@example.com"
            )

    def tearDown(self):
        """Tear down test environment"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def get_headers(self):
        """Helper function to return headers with JWT token"""
        return {"Authorization": "Bearer {}".format(self.access_token)}

    def get_unathorized_headers(self):
        """Helper function to return unauthorized headers with JWT token"""
        return {"Authorization": "Bearer {}".format(self.unauthorized_access_token)}

    def test_register_user(self):
        """Test user registration endpoint"""
        data = register_user_data
        response = self.app.post("/api/register", json=data)
        self.assertEqual(response.status_code, 201)

        # Test duplicate registration
        response = self.app.post("/api/register", json=data)
        self.assertEqual(response.status_code, 400)

    def test_login_user(self):
        """Test user login endpoint"""
        data = {"email": "test@example.com", "password": "testpassword"}
        response = self.app.post("/api/login", json=data)
        self.assertEqual(response.status_code, 200)

        # Test invalid credentials
        data["password"] = "wrongpassword"
        response = self.app.post("/api/login", json=data)
        self.assertEqual(response.status_code, 401)

    def test_add_book(self):
        """Test adding a book endpoint"""
        data = book_data
        response = self.app.post("/api/books", json=data, headers=self.get_headers())
        self.assertEqual(response.status_code, 201)

        # Test unauthorized access
        response = self.app.post("/api/books", json=data)
        self.assertEqual(response.status_code, 401)

        # Test wrong input
        response = self.app.post("/api/books", json={}, headers=self.get_headers())
        self.assertEqual(response.status_code, 400)

    def test_get_books(self):
        """Test getting all books endpoint"""
        response = self.app.get("/api/books", headers=self.get_headers())
        res_data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res_data.get("pagination").get("count"), 1)

        # Test pagination
        response = self.app.get(
            "/api/books?page=1&per_page=10", headers=self.get_headers()
        )
        self.assertEqual(response.status_code, 200)

    def test_get_book(self):
        """Test getting a specific book endpoint"""
        with app.app_context():
            user = User.query.filter_by(username="testuser").first()
            new_book = Book(
                title="Test Book", author_id=user.id, published_date=datetime.now()
            )
            db.session.add(new_book)
            db.session.commit()

            response = self.app.get(
                f"/api/books/{new_book.id}", headers=self.get_headers()
            )
            self.assertEqual(response.status_code, 200)

            # Test non-existent book
            response = self.app.get("/api/books/999", headers=self.get_headers())
            self.assertEqual(response.status_code, 404)

    def test_update_book(self):
        """Test updating a book endpoint"""
        with app.app_context():
            user = User.query.filter_by(username="testuser").first()
            new_book = Book(
                title="Test Book", author_id=user.id, published_date=datetime.now()
            )
            db.session.add(new_book)
            db.session.commit()

            data = updated_book_data
            response = self.app.patch(
                f"/api/books/{new_book.id}", json=data, headers=self.get_headers()
            )
            self.assertEqual(response.status_code, 200)

            # Test unauthorized update

            response = self.app.patch(
                f"/api/books/{new_book.id}",
                json=data,
                headers=self.get_unathorized_headers(),
            )
            self.assertEqual(response.status_code, 403)

    def test_delete_book(self):
        """Test deleting a book endpoint"""
        with app.app_context():
            user = User.query.filter_by(username="testuser").first()
            new_book = Book(
                title="Test Book", author_id=user.id, published_date=datetime.now()
            )
            db.session.add(new_book)
            db.session.commit()

            # Test unauthorized deletion
            response = self.app.delete(
                f"/api/books/{new_book.id}", headers=self.get_unathorized_headers()
            )
            self.assertEqual(response.status_code, 403)

            # Test success Delete
            response = self.app.delete(
                f"/api/books/{new_book.id}", headers=self.get_headers()
            )
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
