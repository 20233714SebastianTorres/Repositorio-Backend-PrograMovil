# cineviews/apis/movie.py

import traceback

from flask import Blueprint, jsonify, request
from sqlalchemy.orm import selectinload

from main.database import Session
from main.middlewares import jwt_required

from cineviews.models import Movie, Review

api = Blueprint('cineviews_apis_movies', __name__)


# =====================================================
# LISTAR TODAS LAS PELÍCULAS
# =====================================================

@api.route('/apis/v1/movies', methods=['GET'])
# @jwt_required
def fetch_all():

    response = None
    status = 200

    session = Session()

    try:

        movies = session.query(Movie).all()

        response = jsonify({
            'message': 'Lista de películas',
            'data': [movie.to_dict() for movie in movies],
            'success': True,
            'error': None
        })

    except Exception as e:

        traceback.print_exc()

        response = jsonify({
            'message': 'Ocurrió un error al listar películas',
            'data': None,
            'success': False,
            'error': str(e)
        })

        status = 500

    finally:
        session.close()

    return response, status


# =====================================================
# BUSCAR POR GÉNERO
# =====================================================

@api.route('/apis/v2/movies', methods=['GET'])
# @jwt_required
def search_by_genre():

    response = None
    status = 200

    session = Session()

    try:

        query = session.query(Movie)

        genre = request.args.get('genre')

        if genre:
            query = query.filter(
                Movie.genre.ilike(f'%{genre}%')
            )

        movies = query.all()

        response = jsonify({
            'message': 'Películas filtradas correctamente',
            'data': [movie.to_dict() for movie in movies],
            'success': True,
            'error': None
        })

    except Exception as e:

        traceback.print_exc()

        response = jsonify({
            'message': 'Ocurrió un error al filtrar películas',
            'data': None,
            'success': False,
            'error': str(e)
        })

        status = 500

    finally:
        session.close()

    return response, status


# =====================================================
# BUSCAR POR TÍTULO
# =====================================================

@api.route('/apis/v3/movies', methods=['GET'])
# @jwt_required
def search_by_title():

    response = None
    status = 200

    session = Session()

    try:

        query = session.query(Movie)

        title = request.args.get('title')

        if title:
            query = query.filter(
                Movie.title.ilike(f'%{title}%')
            )

        movies = query.all()

        response = jsonify({
            'message': 'Películas encontradas correctamente',
            'data': [movie.to_dict() for movie in movies],
            'success': True,
            'error': None
        })

    except Exception as e:

        traceback.print_exc()

        response = jsonify({
            'message': 'Ocurrió un error al buscar películas',
            'data': None,
            'success': False,
            'error': str(e)
        })

        status = 500

    finally:
        session.close()

    return response, status


# =====================================================
# LISTAR PELÍCULAS CON REVIEWS
# =====================================================

@api.route('/apis/v4/movies', methods=['GET'])
# @jwt_required
def fetch_all_join():

    response = None
    status = 200

    session = Session()

    try:

        movies = (
            session.query(Movie)
            .options(
                selectinload(Movie.reviews)
            )
            .all()
        )

        response = jsonify({
            'message': 'Lista de películas con reviews',
            'data': [movie.to_dict() for movie in movies],
            'success': True,
            'error': None
        })

    except Exception as e:

        traceback.print_exc()

        response = jsonify({
            'message': 'Ocurrió un error al listar películas',
            'data': None,
            'success': False,
            'error': str(e)
        })

        status = 500

    finally:
        session.close()

    return response, status


# =====================================================
# DETALLE DE UNA PELÍCULA
# =====================================================

@api.route('/apis/v1/movies/<int:movie_id>', methods=['GET'])
# @jwt_required
def fetch_by_id(movie_id):

    response = None
    status = 200

    session = Session()

    try:

        movie = (
            session.query(Movie)
            .options(
                selectinload(Movie.reviews)
            )
            .filter(
                Movie.id == movie_id
            )
            .first()
        )

        if movie is None:

            return jsonify({
                'message': 'Película no encontrada',
                'data': None,
                'success': False,
                'error': None
            }), 404

        response = jsonify({
            'message': 'Detalle de película',
            'data': movie.to_dict(),
            'success': True,
            'error': None
        })

    except Exception as e:

        traceback.print_exc()

        response = jsonify({
            'message': 'Ocurrió un error al obtener la película',
            'data': None,
            'success': False,
            'error': str(e)
        })

        status = 500

    finally:
        session.close()

    return response, status


# =====================================================
# CREAR REVIEW
# =====================================================

@api.route('/apis/v1/reviews', methods=['POST'])
# @jwt_required
def create_review():

    response = None
    status = 201

    session = Session()

    try:

        data = request.json

        review = Review(
            content=data['content'],
            rating=data['rating'],
            user_id=data['user_id'],
            movie_id=data['movie_id']
        )

        session.add(review)
        session.commit()

        response = jsonify({
            'message': 'Comentario creado correctamente',
            'data': review.to_dict(),
            'success': True,
            'error': None
        })

    except Exception as e:

        session.rollback()

        traceback.print_exc()

        response = jsonify({
            'message': 'Ocurrió un error al crear el comentario',
            'data': None,
            'success': False,
            'error': str(e)
        })

        status = 500

    finally:
        session.close()

    return response, status

