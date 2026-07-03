#BackendCine\cineviews\blueprints.py
from .apis.movie import api as api_movies
from .apis.review import api as api_reviews
from .apis.user import api as api_users
from .apis.watched import api as api_watched
#from .apis.actor import api as api_actors

blueprints = [
  api_movies,
  api_reviews,
  api_users,
  api_watched,
  #api_actors,
]