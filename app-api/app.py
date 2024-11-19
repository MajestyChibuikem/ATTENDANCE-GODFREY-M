from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialize the database and JWT Manager
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def home():
        return "wlcome to flask app"
    # Load config and initialize extensions
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app-api/instance/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'

    db.init_app(app)
    jwt.init_app(app)
    
    # Register Blueprints
    from routes.auth import auth_bp
    from routes.users import users_bp
    from routes.attendance import attendance_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    home()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

