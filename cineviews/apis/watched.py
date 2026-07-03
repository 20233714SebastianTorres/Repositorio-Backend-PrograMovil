import traceback
from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload

from main.database import Session

from cineviews.models import WatchedMovie, Movie

api = Blueprint("cineviews_apis_watched", __name__)


# =====================================================
# REGISTRAR PELÍCULA VISTA
# =====================================================

@api.route("/apis/v1/watched", methods=["POST"])
def create_watched():

    response = None
    status = 201

    session = Session()

    try:

        data = request.get_json()

        existing = (
            session.query(WatchedMovie)
            .filter(
                WatchedMovie.user_id == data["user_id"],
                WatchedMovie.movie_id == data["movie_id"]
            )
            .first()
        )

        if existing:

            return jsonify({
                "message": "La película ya fue registrada como vista",
                "data": existing.to_dict(),
                "success": False,
                "error": None
            }), 409

        watched = WatchedMovie(
            user_id=data["user_id"],
            movie_id=data["movie_id"],
            watched_date=datetime.strptime(
                data["watched_date"],
                "%Y-%m-%d"
            ).date()
        )

        session.add(watched)
        session.commit()

        response = jsonify({
            "message": "Película registrada como vista",
            "data": watched.to_dict(),
            "success": True,
            "error": None
        })

    except Exception as e:

        session.rollback()

        traceback.print_exc()

        response = jsonify({
            "message": "Ocurrió un error al registrar la película",
            "data": None,
            "success": False,
            "error": str(e)
        })

        status = 500

    finally:
        session.close()

    return response, status


# =====================================================
# HISTORIAL DE PELÍCULAS VISTAS DE UN USUARIO
# =====================================================

@api.route("/apis/v1/users/<int:user_id>/watched", methods=["GET"])
def fetch_user_watched(user_id):

    response = None
    status = 200

    session = Session()

    try:

        watched = (
            session.query(WatchedMovie)
            .options(
                joinedload(WatchedMovie.movie)
            )
            .filter(
                WatchedMovie.user_id == user_id
            )
            .all()
        )

        data = []

        for item in watched:

            data.append({
                "id": item.id,
                "watched_date": item.watched_date.isoformat(),
                "movie": item.movie.to_dict()
            })

        response = jsonify({
            "message": "Historial obtenido correctamente",
            "data": data,
            "success": True,
            "error": None
        })

    except Exception as e:

        traceback.print_exc()

        response = jsonify({
            "message": "Ocurrió un error al obtener el historial",
            "data": None,
            "success": False,
            "error": str(e)
        })

        status = 500

    finally:
        session.close()

    return response, status


# =====================================================
# ELIMINAR REGISTRO DE PELÍCULA VISTA
# =====================================================

@api.route("/apis/v1/watched/<int:watched_id>", methods=["DELETE"])
def delete_watched(watched_id):

    response = None
    status = 200

    session = Session()

    try:

        watched = (
            session.query(WatchedMovie)
            .filter(
                WatchedMovie.id == watched_id
            )
            .first()
        )

        if watched is None:

            return jsonify({
                "message": "Registro no encontrado",
                "data": None,
                "success": False,
                "error": None
            }), 404

        session.delete(watched)
        session.commit()

        response = jsonify({
            "message": "Registro eliminado correctamente",
            "data": None,
            "success": True,
            "error": None
        })

    except Exception as e:

        session.rollback()

        traceback.print_exc()

        response = jsonify({
            "message": "Ocurrió un error al eliminar el registro",
            "data": None,
            "success": False,
            "error": str(e)
        })

        status = 500

    finally:
        session.close()

    return response, status