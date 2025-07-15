import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize SQLAlchemy for database interactions
db = SQLAlchemy()

# Initialize Flask-Migrate for handling database migrations
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'main.auth'
login_manager.login_message = 'Lütfen giriş yapın!'
login_manager.login_message_category = 'info'

def create_app():
    # Create a Flask app instance with specified template and static folder paths
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')

    # Configure the database URI with absolute path
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(basedir, 'instance', 'finance.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SECRET_KEY'] = 'a2m6mh51fk1152'
    
    # Ensure instance folder exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Initialize database and migration modules with the app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize login manager
    login_manager.init_app(app)
    
    # Import User model for login manager
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Import and register the main blueprint for routing
    from .routes import main
    app.register_blueprint(main)
    
    return app
