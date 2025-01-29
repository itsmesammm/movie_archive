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
    movies = data_manager.get_user_movies(user_id)
    user = next((u for u in data_manager.get_all_users() if u['id'] == user_id), None)
    if user:
        return render_template('user_movies.html', user=user, movies=movies)
    flash("User not found")
    return redirect(url_for('list_users'))

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
    if request.method == 'POST':
        movie_details = {
            "name": request.form.get('name'),
            "director": request.form.get('director'),
            "year": request.form.get('year', type=int),
            "rating": request.form.get('rating', type=float),
            "poster": request.form.get('poster')  # Optional
        }
        fetch_from_api = request.form.get('fetch_from_api') == 'on'
        if fetch_from_api:
            movie_details["fetch_from_api"] = True
        if movie_details["name"]:
            try:
                data_manager.add_movie(user_id, movie_details)
                flash(f"Movie '{movie_details['name']}' added successfully!")
            except ValueError as e:
                flash(str(e))
            return redirect(url_for('list_user_movies', user_id=user_id))
        else:
            flash("Movie name is required!")
    return render_template('add_movie.html', user_id=user_id)

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        updates = {
            "name": request.form.get('name'),
            "director": request.form.get('director'),
            "year": request.form.get('year', type=int)
        }



if __name__ == "__main__":
    # comment the following block after create tables
    #with app.app_context():
    #    db.create_all()
    #   print("Database tables created successfully!")
    app.run(debug=True)
