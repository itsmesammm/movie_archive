from .data_manager_interface import DataManagerInterface
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
                 "year": movie.year, "rating": movie.rating}
                for movie in Movie.query.filter_by(user_id = user_id).all()]

    def add_user(self, user_name):
        new_user = User(name = user_name)
        self.db.session.add(new_user)
        self.db.session.commit()

    def add_movie(self, user_id, movie_details):
        if "fetch_from_api" in movie_details and movie_details["fetch_from_api"]:
            try:
                api_data = self.fetch_movie_from_api(movie_details["name"])
                movie_details.update(api_data)
            except Exception as e:
                raise ValueError(f"Failed to add movie from API: {e}")

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

    def fetch_movie_from_api(self, title):
        """Fetch movie details from OMDb API by title"""
        api_key = os.getenv('OMDB_API_KEY')
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
        response = requests.get(url)

        if response.status_code = 200:
            data = response.json()
            if data.get("Response") == "True":
                #Extract required fields
                return {
                    "name": data["Title"],
                    "director": data["Director"],
                    "year": int(data["Year"]),
                    "poster": data["Poster"]
                }
            else:
                raise ValueError(f"Movie not found: {title}")
        else:
            raise ConnectionError("Failed to fetch data from OMDb API")
