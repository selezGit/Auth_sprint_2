from http import HTTPStatus

from app import google
from app.api.v1.models.request_model import (auth_register_parser,
                                             change_email_parser,
                                             change_password_parser,
                                             delete_sn_parser,
                                             role_parser)
from app.api.v1.models.response_model import (nested_history_model,
                                              user_create_model,
                                              user_history_model)
from app.api.v1.services.user import (append_google_SN_logic,
                                      change_email_logic,
                                      change_password_logic, create_user_logic,
                                      delete_sn_logic, delete_user_logic,
                                      get_user_logic, history_logic, add_role_logic, del_role_logic)
from flask import request, session, url_for
from flask_restx import Namespace, Resource

user_ns = Namespace(name='user', validate=True)
user_ns.models[user_create_model.name] = user_create_model
user_ns.models[nested_history_model.name] = nested_history_model
user_ns.models[user_history_model.name] = user_history_model


@user_ns.route('/', endpoint='user')
class User(Resource):
    @user_ns.expect(auth_register_parser)
    @user_ns.response(int(HTTPStatus.CREATED), 'Success', user_create_model)
    @user_ns.response(int(HTTPStatus.CONFLICT), 'Email or login address is already registered.')
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @user_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def post(self):
        request_data = auth_register_parser.parse_args()
        login = request_data.get('login')
        email = request_data.get('email')
        password = request_data.get('password')
        return create_user_logic(login=login, email=email, password=password)

    @user_ns.doc(security='access_token')
    @user_ns.response(int(HTTPStatus.OK), 'Success')
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @user_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def delete(self):
        access_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        return delete_user_logic(access_token=access_token, user_agent=user_agent)


@user_ns.route('/delete_SN', endpoint='user_delete_SN')
class DeleteSN(Resource):
    @user_ns.doc(security='access_token')
    @user_ns.expect(delete_sn_parser)
    @user_ns.response(int(HTTPStatus.OK), 'Success')
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @user_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def delete(self):
        request_data = delete_sn_parser.parse_args()
        uuid = request_data.get('uuid')
        access_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        return delete_sn_logic(uuid=uuid, user_agent=user_agent, access_token=access_token)

@user_ns.route('/role', endpoint='user_role')
class UserRole(Resource):
    @user_ns.doc(security='access_token')
    @user_ns.expect(role_parser)
    @user_ns.response(int(HTTPStatus.OK), 'Success')
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @user_ns.response(int(HTTPStatus.FORBIDDEN), 'permission denied.')
    @user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @user_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def post(self):
        request_data = role_parser.parse_args()
        access_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        user_id = request_data.get('user_id')
        role_id = request_data.get('role_id')
        return add_role_logic(access_token=access_token, user_agent=user_agent, user_id=user_id, role_id=role_id)

    @user_ns.doc(security='access_token')
    @user_ns.expect(role_parser)
    @user_ns.response(int(HTTPStatus.OK), 'Success')
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @user_ns.response(int(HTTPStatus.FORBIDDEN), 'permission denied.')
    @user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @user_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def delete(self):
        request_data = role_parser.parse_args()
        access_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        user_id = request_data.get('user_id')
        role_id = request_data.get('role_id')
        return del_role_logic(access_token=access_token, user_agent=user_agent, user_id=user_id, role_id=role_id)


@user_ns.route('/append_google_SN', endpoint='auth_append_google_SN')
class AppendSN(Resource):
    @user_ns.doc(security='access_token')
    @user_ns.response(int(HTTPStatus.OK), 'Success')
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), 'email or password does not match')
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @user_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def get(self):
        resp = google.authorized_response()
        if resp is None:
            session['access_token'] = request.headers.get('Authorization')
            return google.authorize(callback=url_for('api.auth_append_google_SN', _external=True))
        access_token = session.pop('access_token', None)
        session['google_token'] = (resp.get('access_token'), '')
        user_agent = request.headers.get('User-Agent')
        userinfo = google.get('userinfo')
        social_id = userinfo.data.get('id')
        email = userinfo.data.get('email')
        return append_google_SN_logic(access_token=access_token,
                                      social_id=str(social_id),
                                      social_name='google',
                                      user_agent=user_agent,
                                      email=email)

    @google.tokengetter
    def get_google_oauth_token():
        return session.get('google_token')


@user_ns.route('/me', endpoint='user_me')
class UserMe(Resource):
    @user_ns.doc(security='access_token')
    @user_ns.response(int(HTTPStatus.OK), 'Success', user_create_model)
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @user_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def get(self):
        access_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        return get_user_logic(access_token=access_token, user_agent=user_agent)


@user_ns.route('/change-password', endpoint='user_change_password')
class ChangePassword(Resource):
    @user_ns.doc(security='access_token')
    @user_ns.expect(change_password_parser)
    @user_ns.response(int(HTTPStatus.OK), 'password changed successfully')
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @user_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def patch(self):
        request_data = change_password_parser.parse_args()
        old_password = request_data.get('old_password')
        new_password = request_data.get('new_password')
        access_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        return change_password_logic(old_password=old_password,
                                     new_password=new_password,
                                     access_token=access_token,
                                     user_agent=user_agent)


@user_ns.route('/change-email', endpoint='user_change_email')
class ChangeEmail(Resource):
    @user_ns.doc(security='access_token')
    @user_ns.expect(change_email_parser)
    @user_ns.response(int(HTTPStatus.OK), 'email changed successfully')
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @user_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def patch(self):
        request_data = change_email_parser.parse_args()
        email = request_data.get('email')
        access_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        return change_email_logic(email=email,
                                  access_token=access_token,
                                  user_agent=user_agent)


@user_ns.route('/history', endpoint='user_history')
class History(Resource):
    @user_ns.doc(security='access_token', params={
        'skip': {'in': 'query', 'default': 0},
        'limit': {'in': 'query', 'default': 50}})
    @user_ns.response(int(HTTPStatus.OK), 'success', user_history_model)
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @user_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @user_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def get(self):
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 50))
        access_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        return history_logic(skip=skip, limit=limit, access_token=access_token, user_agent=user_agent)
