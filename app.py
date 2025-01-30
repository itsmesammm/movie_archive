from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Movie
from data_manager.sqlite_data_manager import SQLiteDataManager
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Fallback to 'default_secret_key' if not set

# Ensure the 'data' directory exists
os.makedirs('data', exist_ok=True)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{base_dir}/data/movies.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# Initialize the data manager
data_manager = SQLiteDataManager(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def list_user_movies(user_id):
    user = data_manager.get_user_by_id(user_id)  # Fetch only one user
    if not user:
        flash("User not found")
        return redirect(url_for('list_users'))

    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user = user, movies = movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form.get('name')
        if user_name:
            data_manager.add_user(user_name)
            flash(f"User '{user_name}' added successfully!")
            return redirect(url_for('list_users'))
        else:
            flash("Name is required!")
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    movie_details = {}

    if request.method == 'POST':
        movie_details = {
            "name": request.form.get('name'),
            "director": request.form.get('director'),
            "year": request.form.get('year', type=int),
            "rating": request.form.get('rating', type=float),
            "poster": request.form.get('poster')
        }
        fetch_from_api = request.form.get('fetch_from_api') == 'on'
        if fetch_from_api:
            movie_details["fetch_from_api"] = True

        if movie_details["name"]:
            try:
                data_manager.add_movie(user_id, movie_details)
                flash(f"Movie '{movie_details['name']}' added successfully!")
                return redirect(url_for('list_user_movies', user_id=user_id))

            except ValueError as e:
                flash(str(e))
                return render_template('add_movie.html', user_id=user_id, movie_details=movie_details, form=request.form)

        else:
            flash("Movie title is required!")
            return render_template('add_movie.html', user_id=user_id, movie_details=movie_details, form=request.form)  # Return here!

    return render_template('add_movie.html', user_id=user_id, movie_details=movie_details)  # Return for GET requests

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        flash("Movie not found")
        return redirect(url_for('list_user_movies', user_id = user_id))

    if request.method == 'POST':
        updates = {
            "name": request.form.get('name'),
            "director": request.form.get('director'),
            "year": request.form.get('year', type=int),
            "rating": request.form.get('rating', type = float)
        }
        data_manager.update_movie(movie_id, updates)
        flash(f"Movie '{updates['name']}' updated successfully!")
        return redirect(url_for('list_user_movies', user_id = user_id))

    return render_template('update_movie.html', movie = movie)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST', 'DELETE'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    flash("Movie deleted successfully!")
    return redirect(url_for('list_user_movies', user_id=user_id))


if __name__ == "__main__":
    # comment the following block after create tables
    #with app.app_context():
    #    db.create_all()
    #   print("Database tables created successfully!")
    app.run(debug=True)
