from flask import Flask
from flasgger import Swagger
from flask_caching import Cache
from models import db
from config import Config
from routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    cache = Cache(app)
    Swagger(app)
    
    # Register routes
    register_routes(app, cache)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)