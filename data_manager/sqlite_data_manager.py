from .data_manager_interface import DataManagerInterface
from api_utils import fetch_movie_details
from models import db, User, Movie
import requests
import os


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.db = db

    def get_all_users(self):
        return [{"id": user.id, "name": user.name} for user in User.query.all()]

    def get_user_movies(self, user_id):
        return [{"id": movie.id, "name": movie.name, "director": movie.director,
                 "year": movie.year, "rating": movie.rating, "poster": movie.poster}
                for movie in Movie.query.filter_by(user_id = user_id).all()]

    def add_user(self, user_name):
        new_user = User(name = user_name)
        self.db.session.add(new_user)
        self.db.session.commit()

    def get_user_by_id(self, user_id):
        user = User.query.get(user_id)  # Query the user directly using SQLAlchemy
        if user:
            return {"id": user.id, "name": user.name}  # Return as a dictionary
        return None

    def add_movie(self, user_id, movie_details):
        try:
            api_data = self.fetch_movie_from_api(movie_details["name"])
            movie_details.update(api_data)

        except Exception as e:
            raise # Re-raise the ValueError to be caught in app.py

        new_movie = Movie(user_id=user_id, **movie_details)
        self.db.session.add(new_movie)
        self.db.session.commit()

    def update_movie(self, movie_id, updates):
        movie = Movie.query.get_or_404(movie_id)
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

    def fetch_movie_from_api(self, title):
        """
        Fetch movie details from the OMDb API by title.
        Note: This method leverages the `fetch_movie_details` function
        from `api_utils.py` for modularity and reusability.
        """
        try:
            api_key = os.getenv('OMDB_API_KEY')
            if not api_key:
                raise ValueError("OMDB_API_KEY is not set in the environment variables.")

            return fetch_movie_details(api_key, title)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to fetch data from OMDb API: {e}")

