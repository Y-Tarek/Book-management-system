from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
app = Flask(__name__)
if os.getenv("FLASK_ENV") == "testing":
    app.config.from_object("config.TestConfig")
else:
    app.config.from_object("config.Config")


db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


from routes import *

if __name__ == "__main__":
    app.run(debug=True)
