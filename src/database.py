from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    pais = db.Column(db.String(30), nullable=False)
    estado = db.Column(db.String(30), nullable=False)
    municipio = db.Column(db.String(30), nullable=False)
    cep = db.Column(db.Integer, nullable=False)
    rua = db.Column(db.String(50), nullable=False)
    numero_endereco = db.Column(db.Integer, nullable=False)
    complemento_endereco = db.Column(db.String(10), nullable=False)
    cpf = db.Column(db.Integer, unique=True)
    pis_nit = db.Column(db.Integer, unique=True)
    senha = db.Column(db.Text(), nullable=False)

    def __repr__(self) -> str:
        return 'User>>> {self.username}'
