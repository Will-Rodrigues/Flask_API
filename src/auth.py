from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from src.database import User, db
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from src.constants.http_status_code import *


auth = Blueprint("auth", __name__, url_prefix="/api")

@auth.post("/cadastrar")
def register():
    nome = request.json['nome']
    email = request.json['email']
    pais = request.json['pais']
    estado = request.json['estado']
    municipio = request.json['municipio']
    cep = request.json['cep']
    rua = request.json['rua']
    numero_endereco = request.json['numero_endereco']
    complemento_endereco = request.json['complemento_endereco']
    cpf = request.json['cpf']
    pis_nit = request.json['pis_nit']
    senha = request.json['senha']
    senha2 = request.json['senha2']

    if len(senha) < 6:
        return jsonify({'error': 'Senha muito curta.'}), HTTP_400_BAD_REQUEST

    if senha != senha2:
        return jsonify({'error': 'Senhas diferentes'}), HTTP_400_BAD_REQUEST
    
    if len(nome) < 3:
        return jsonify({'error': 'Nome muito curto.'}), HTTP_400_BAD_REQUEST
    
    if not nome.isalnum():
        return jsonify({'error': 'Nome precisa ser alfanumerico.'}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': 'E-mail inválido.'}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'E-mail já registrado'}), HTTP_409_CONFLICT

    if User.query.filter_by(cpf=cpf).first() is not None:
        return jsonify({'error': 'CPF já cadastrado.'}), HTTP_409_CONFLICT

    if User.query.filter_by(pis_nit=pis_nit).first() is not None:
        return jsonify({'error': 'PIS ou NIT já cadastrado.'}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(senha)

    user = User(nome=nome, senha=pwd_hash, email=email, pais=pais, estado=estado, municipio=municipio, cep=cep, rua=rua, numero_endereco=numero_endereco, complemento_endereco=complemento_endereco, cpf=cpf, pis_nit=pis_nit)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'Usuário criado com sucesso!',
        'user' : {
            'nome': nome,
            'email': email,
            'pais': pais,
            'estado': estado,
            'municipio': municipio,
            'cep': cep,
            'rua': rua,
            'numero_endereco': numero_endereco,
            'complemento_endereco': complemento_endereco,
            'cpf': cpf,
            'pis_nit': pis_nit
        }
    }), HTTP_201_CREATED

@auth.post("/entrar")
def login():
    email = request.json.get('email', '')
    senha = request.json.get('senha', '')

    user=User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.senha, senha)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user':{
                    'refresh': refresh,
                    'acess': access,
                    'nome': user.nome,
                    'email': user.email
                }
            }), HTTP_200_OK

    return jsonify({'error': 'E-mail ou senha incorretos'}), HTTP_401_UNAUTHORIZED


@auth.get("/cadastro")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    return jsonify ({
        'nome': user.nome,
        'email': user.email,
        'pais': user.pais,
        'estado': user.estado,
        'municipio': user.municipio,
        'cep': user.cep,
        'rua': user.rua,
        'numero_endereco': user.numero_endereco,
        'complemento_endereco': user.complemento_endereco,
        'cpf': user.cpf,
        'pis_nit': user.pis_nit
    }), HTTP_200_OK

@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify ({
        'access': access
    }), HTTP_200_OK

@auth.delete("/deletar/<int:id>")
@jwt_required()
def delete_bookmark(id):
    user_id = get_jwt_identity()
    user = User.query.get(id=user_id).first()

    if not user:
        return jsonify({
            'message': 'item not found'
        }), HTTP_404_NOT_FOUND

    db.session.delete(user)
    db.session.commit()
    
    return jsonify ({}), HTTP_204_NO_CONTENT

