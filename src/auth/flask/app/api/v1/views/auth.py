from http import HTTPStatus

from app import oauth
from app.api.v1.models.request_model import auth_login_parser
from app.api.v1.models.response_model import auth_login_model
from app.api.v1.services.auth import (login_logic, logout_logic, refresh_logic,
                                      test_logic)
from flask import jsonify, request, session, url_for
from flask_restx import Namespace, Resource

client_id = r'144683256197-dgp5t8nspp3e0im5l59tot9vqeeop4hm.apps.googleusercontent.com'
client_secret = r'RrrpZkdlU4UnlJOzo6-pL785'

google = oauth.remote_app(
    'google',
    consumer_key=client_id,
    consumer_secret=client_secret,
    request_token_params={
        'scope': ['https://www.googleapis.com/auth/userinfo.email', 
        'https://www.googleapis.com/auth/userinfo.profile', 'Openid']
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


auth_ns = Namespace(name='auth', validate=True)
auth_ns.models[auth_login_model.name] = auth_login_model


@auth_ns.route('/login', endpoint='auth_login')
class Login(Resource):
    @auth_ns.expect(auth_login_parser)
    @auth_ns.response(int(HTTPStatus.OK), 'Success', auth_login_model)
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), 'email or password does not match')
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @auth_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @auth_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def post(self):
        request_data = auth_login_parser.parse_args()
        login = request_data.get('login')
        password = request_data.get('password')
        user_agent = request.headers.get('User-Agent')
        return login_logic(login=login,
                           password=password,
                           user_agent=user_agent)


@auth_ns.route('/login_via_google', endpoint='auth_login_via_google')
class LoginViaGoogle(Resource):
    @auth_ns.response(int(HTTPStatus.OK), 'Success')
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), 'email or password does not match')
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @auth_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @auth_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def get(self):
        return google.authorize(callback=url_for('api.auth_authorized', _external=True))


@auth_ns.route('/login_via_google/authorized')
class Authorized(Resource):
    def get(self):
        resp = google.authorized_response()
        print(resp)
        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
        session['google_token'] = (resp['access_token'], '')
        me = google.get('userinfo')
        # сюда прописать логику регистрации нового юзера
        return jsonify({"data": me.data})


@auth_ns.route('/refresh', endpoint='auth_refresh')
class Refresh(Resource):
    @auth_ns.doc(security='refresh_token')
    @auth_ns.response(int(HTTPStatus.OK), 'Success', auth_login_model)
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @auth_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @auth_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def post(self):
        refresh_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        return refresh_logic(refresh_token=refresh_token,
                             user_agent=user_agent)


@ auth_ns.route('/logout', endpoint='auth_logout')
class Logout(Resource):
    @auth_ns.doc(security='access_token')
    @auth_ns.response(int(HTTPStatus.OK), 'Log out succeeded, token is no longer valid.')
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @auth_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @auth_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def post(self):
        access_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        return logout_logic(access_token=access_token,
                            user_agent=user_agent)


@auth_ns.route('/test-token', endpoint='auth_test_token')
class TestToken(Resource):
    @auth_ns.doc(security='access_token')
    @auth_ns.response(int(HTTPStatus.OK), 'Token is valid')
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @auth_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @auth_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def get(self):
        access_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        return test_logic(access_token=access_token,
                          user_agent=user_agent)


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
