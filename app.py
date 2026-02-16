from flask import Flask
from views import views
from api import api
import logging

def create_app():
    app = Flask(__name__)

    # Set up logging configuration 
    logging.basicConfig(level=logging.INFO)

    # Register blueprints
    app.register_blueprint(api)
    app.register_blueprint(views)
    return app

# Create an instance of the app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8000)


   
