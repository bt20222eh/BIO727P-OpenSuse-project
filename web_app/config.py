import os

class Config:
    # Set the secret key to protect your app from CSRF attacks
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'BMD727P'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/elmahandzic/desktop/myflaskapp/web_app/analysis.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Other configuration options
    # Add additional configuration options as needed

    # Example: Uncomment and set the value to True to enable debug mode
    DEBUG = True

