from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(16), nullable=False, default="user")
