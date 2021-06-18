from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_oauthlib.client import OAuth

from app.config import config

cors = CORS()
oauth = OAuth()

config = config.get('development')
google = oauth.remote_app(**config.GOOGLE)


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config)
    from .api.v1 import api_bp

    app.register_blueprint(api_bp)
    cors.init_app(app)
    oauth.init_app(app)
    Limiter(app, key_func=get_remote_address, default_limits=["20/minute"])
    return app
