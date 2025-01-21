from .data_manager_interface import DataManagerInterface
from models import db, User, Movie


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.db = db


    def get_all_users(self):
        return [{"id": user.id, "name": user.name} for user in User.query.all()]

    def get_user_movies(self, user_id):
        return [{"id": movie.id, "name": movie.name, "director": movie.director,
                 "year": movie.year, "rating": movie.rating}
                for movie in Movie.query.filter_by(user_id = user_id).all()]

    def add_user(self, user_name):
        new_user = User(name = user_name)
        self.db.session.add(new_user)
        self.db.session.commit()

    def add_movie(self, user_id, movie_details):
        new_movie = Movie(user_id = user_id, **movie_details)
        self.db.session.add(new_movie)
        self.db.session.commit()

    def update_movie(self, movie_id, updates):
        movie = Movie.query.get(movie_id)
        if not movie:
            return False
        for key, value in updates.items():
            setattr(movie, key, value)
        self.db.session.commit()
        return True

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()

