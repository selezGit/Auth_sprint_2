import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'hard to guess string')
    ### google application creds
    CLIENT_ID = os.getenv('CLIENT_ID', r'144683256197-dgp5t8nspp3e0im5l59tot9vqeeop4hm.apps.googleusercontent.com') 
    CLIENT_SECRET = os.getenv('CLIENT_SECRET', r'RrrpZkdlU4UnlJOzo6-pL785')
    GOOGLE = {
        'name': 'google',
        'consumer_key': CLIENT_ID,
        'consumer_secret': CLIENT_SECRET,
        'request_token_params': {
            'scope': ['https://www.googleapis.com/auth/userinfo.email',
                    'https://www.googleapis.com/auth/userinfo.profile']
        },
        'base_url': 'https://www.googleapis.com/oauth2/v1/',
        'request_token_url': None,
        'access_token_method': 'POST',
        'access_token_url': 'https://accounts.google.com/o/oauth2/token',
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
    }

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}