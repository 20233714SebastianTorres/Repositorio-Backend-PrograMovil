import traceback
from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload

from main.database import Session
from cineviews.models import Review, Movie, User

api = Blueprint('cineviews_apis_reviews', __name__)


# ==========================================
# V1 - LISTAR REVIEWS SIMPLE
# ==========================================
@api.route('/apis/v1/reviews', methods=['GET'])
def fetch_all():
    response = None
    status = 200

    session = Session()

    try:
        reviews = session.query(Review).all()

        response = jsonify({
            "message": "lista de reviews",
            "data": [r.to_dict() for r in reviews],
            "success": True,
            "error": None
        })

    except Exception as e:
        traceback.print_exc()
        response = jsonify({
            "message": "Error al listar reviews",
            "data": None,
            "success": False,
            "error": str(e)
        })
        status = 500

    finally:
        session.close()

    return response, status


# ==========================================
# V2 - REVIEWS CON USER + MOVIE (JOIN REAL)
# ==========================================
@api.route('/apis/v2/reviews', methods=['GET'])
def fetch_all_join():
    response = None
    status = 200

    session = Session()

    try:
        reviews = (
            session.query(Review)
            .options(
                joinedload(Review.user),
                joinedload(Review.movie)
            )
            .all()
        )

        response = jsonify({
            "message": "lista de reviews con relaciones",
            "data": [r.to_dict() for r in reviews],
            "success": True,
            "error": None
        })

    except Exception as e:
        traceback.print_exc()
        response = jsonify({
            "message": "Error al listar reviews",
            "data": None,
            "success": False,
            "error": str(e)
        })
        status = 500

    finally:
        session.close()

    return response, status


# ==========================================
# V3 - FILTRAR POR MOVIE
# ==========================================
@api.route('/apis/v3/reviews', methods=['GET'])
def fetch_by_movie():
    response = None
    status = 200

    session = Session()

    try:
        movie_id = request.args.get('movie_id')

        query = session.query(Review)

        if movie_id:
            query = query.filter(Review.movie_id == movie_id)

        reviews = query.all()

        response = jsonify({
            "message": "reviews filtradas",
            "data": [r.to_dict() for r in reviews],
            "success": True,
            "error": None
        })

    except Exception as e:
        traceback.print_exc()
        response = jsonify({
            "message": "Error al filtrar reviews",
            "data": None,
            "success": False,
            "error": str(e)
        })
        status = 500

    finally:
        session.close()

    return response, status


# ==========================================
# V4 - CREAR REVIEW
# ==========================================
@api.route('/apis/v1/reviews', methods=['POST'])
def create_review():
    response = None
    status = 201

    session = Session()

    try:
        data = request.get_json()

        review = Review(
            content=data["content"],
            rating=data["rating"],
            user_id=data["user_id"],
            movie_id=data["movie_id"]
        )

        session.add(review)
        session.commit()

        response = jsonify({
            "message": "review creada",
            "data": review.to_dict(),
            "success": True,
            "error": None
        })

    except Exception as e:
        session.rollback()
        traceback.print_exc()

        response = jsonify({
            "message": "Error al crear review",
            "data": None,
            "success": False,
            "error": str(e)
        })
        status = 500

    finally:
        session.close()

    return response, status