# biblio\apis\user.py
import traceback
from datetime import date

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from main.database import Session
from cineviews.models import User

api = Blueprint('cineviews_apis_users', __name__)


@api.route('/apis/v1/users/register', methods=['POST'])
@api.route('/apis/v1/users/signup', methods=['POST'])
def register():
    response = None
    status = 200

    data = request.get_json(silent=True) or {}

    required_fields = ['username', 'password', 'first_name', 'last_name', 'email']
    missing_fields = [field for field in required_fields if not str(data.get(field, '')).strip()]

    if missing_fields:
        return jsonify({
            'message': 'Faltan campos obligatorios',
            'data': None,
            'success': False,
            'error': f'Campos requeridos: {", ".join(missing_fields)}'
        }), 400

    session = Session()

    try:
        existing_user = (
            session.query(User)
            .filter(
                (User.username == data['username'].strip()) |
                (User.email == data['email'].strip())
            )
            .first()
        )

        if existing_user:
            return jsonify({
                'message': 'Ya existe un usuario con ese username o email',
                'data': None,
                'success': False,
                'error': 'Conflict'
            }), 409

        birth_date = None
        if data.get('birth_date'):
            try:
                birth_date = date.fromisoformat(str(data['birth_date']))
            except ValueError:
                return jsonify({
                    'message': 'La fecha de nacimiento debe tener formato YYYY-MM-DD',
                    'data': None,
                    'success': False,
                    'error': 'Bad Request'
                }), 400

        user = User(
            username=data['username'].strip(),
            password=data['password'],
            first_name=data['first_name'].strip(),
            last_name=data['last_name'].strip(),
            email=data['email'].strip(),
            birth_date=birth_date,
            profile_picture=data.get('profile_picture'),
            bio=data.get('bio'),
            sex_id=data.get('sex_id'),
            nationality_id=data.get('nationality_id'),
            status=True
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        jwt = create_access_token(
            identity=user.username,
            additional_claims={'user_id': user.id}
        )

        response = jsonify({
            'message': 'Usuario creado correctamente',
            'data': {
                'user': user.to_dict(),
                'jwt': jwt
            },
            'success': True,
            'error': None
        })

    except Exception as e:
        session.rollback()
        traceback.print_exc()

        response = jsonify({
            'message': 'Ocurrió un error al crear el usuario',
            'data': None,
            'success': False,
            'error': str(e)
        })
        status = 500

    finally:
        session.close()

    return response, status


@api.route('/apis/v1/users/login', methods=['POST'])
def login():
    response = None
    status = 200

    data = request.get_json(silent=True) or {}

    identifier = data.get('username') or data.get('email') or data.get('user')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({
            'message': 'username/email y password son obligatorios',
            'data': None,
            'success': False,
            'error': 'Missing required fields'
        }), 400

    session = Session()

    try:
        user = (
            session.query(User)
            .filter(
                ((User.username == identifier) | (User.email == identifier)) &
                (User.password == password) &
                (User.status.is_(True))
            )
            .first()
        )

        if not user:
            return jsonify({
                'message': 'Usuario o contraseña incorrectos',
                'data': None,
                'success': False,
                'error': 'Unauthorized'
            }), 401

        jwt = create_access_token(
            identity=user.username,
            additional_claims={'user_id': user.id}
        )

        return jsonify({
            'message': 'Login exitoso',
            'data': {
                'user': user.to_dict(),
                'jwt': jwt
            },
            'success': True,
            'error': None
        }), 200

    except Exception as e:
        traceback.print_exc()

        return jsonify({
            'message': 'Ocurrió un error durante el login',
            'data': None,
            'success': False,
            'error': str(e)
        }), 500

    finally:
        session.close()