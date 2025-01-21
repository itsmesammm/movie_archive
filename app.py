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

@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    # For now, we'll return the users as plain text
    return str(users)  # Eventually, replace this with a template



if __name__ == "__main__":
    # comment the following block after create tables
    #with app.app_context():
    #    db.create_all()
    #   print("Database tables created successfully!")
    app.run(debug=True)
