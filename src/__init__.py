from flask.json import jsonify
from src.constants.http_status_code import *
from flask import Flask
from os import path
from src.database import db
from flask_jwt_extended import JWTManager

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from src.auth import auth

    app.register_blueprint(auth)

    create_database(app)

    JWT_SECRET_KEY = 'JWT_SECRET_KEY'
    JWTManager(app)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Página não encontrar'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Alguma coisa deu errado, estamos trabalhando para solucionar'}), HTTP_500_INTERNAL_SERVER_ERROR

    return app


def create_database(app):
    if not path.exists('src/' + DB_NAME):
        db.create_all(app=app)
        print('Banco de dados criado com sucesso!')
