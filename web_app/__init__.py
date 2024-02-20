from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/elmahandzic/desktop/myflaskapp/web_app/analysis.db'
    
    db.init_app(app)

    with app.app_context():
        from .views import bp as views_bp
        app.register_blueprint(views_bp)
        
        # Import models here if you have them to ensure they're known to SQLAlchemy
        from . import models

    return app
