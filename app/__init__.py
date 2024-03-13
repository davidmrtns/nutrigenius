from flask import Flask


app = Flask(__name__, template_folder="views", static_folder="../public")

def create_app():
    from app import routes
    routes.init_app(app)
    return app
