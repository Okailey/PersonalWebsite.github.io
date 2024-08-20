# from flask import Flask
# from views import views

# def create_app():
#     app = Flask(__name__)
#     app.register_blueprint(views)
#     return app

# if __name__ == "__main__":
#     create_app().run(debug=True, port=8000)

from flask import Flask
from views import views

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views)
    return app

# Create an instance of the app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8000)


   
