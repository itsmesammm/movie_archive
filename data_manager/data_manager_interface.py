from abc import ABC, abstractmethod
import sqlalchemy

class DataManagerInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        """Retrieve all users."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Retrieve all movies for specific user"""
        pass

    @abstractmethod
    def add_user(self, user_name):
        """Add a user with the given name."""
        pass

    @abstractmethod
    def add_movie(self, user_id, movie_details):
        """Add movie for a user"""
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, updated_details):
        """Update movie details for a user"""
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """Delete movie for a user"""
        pass







