# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String)

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Author name is required.")

        existing = Author.query.filter_by(name=value).first()
        if existing:
            raise ValueError("Author name must be unique.")

        return value

    @validates('phone_number')
    def validate_phone(self, key, value):
        if not value or len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")
        return value


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)

    @validates('content')
    def validate_content(self, key, value):
        if len(value) < 250:
            raise ValueError("Post content must be at least 250 characters.")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError("Post summary must be less than or equal to 250 characters.")
        return value

    @validates('category')
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either Fiction or Non-Fiction.")
        return value

    @validates('title')
    def validate_title(self, key, value):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError("Title must be clickbait-y.")
        return value
