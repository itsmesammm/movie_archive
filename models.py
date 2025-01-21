from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(80), nullable = False)
    movies = db.relationship('Movie', backref = 'user', lazy = True)

    def __repr__(self):
        return f"<User {self.name}>"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    name = db.Column(db.String(120), nullable = False)
    director = db.Column(db.String(120))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)

    def __repr__(self):
        return f"<Movie {self.name}>"
