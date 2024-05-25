from flask import Flask
from databaseManager import DatabaseManager
from app import PageManager
import os

def create_app():
    app = Flask(__name__)

    
    secret_key = os.urandom(24).hex()

    
    app.config['SECRET_KEY'] = secret_key


    db_manager = DatabaseManager(app)

    
    page_manager = PageManager(app, db_manager)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)