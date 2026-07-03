#BackendCine\main\blueprints.py
from main.views import view as main_views
from main.apis import api as main_apis
from cineviews.blueprints import blueprints as cineviews_blueprints

def register(app):
  # append sub blueprints
  modules_blueprints = [
    cineviews_blueprints,
  ]
  # load main blueprint to app
  app.register_blueprint(main_views)
  app.register_blueprint(main_apis)
  # load sub blueprints to app
  for blueprints in modules_blueprints:
    for blueprint in blueprints:
      app.register_blueprint(blueprint)

