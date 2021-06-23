from http import HTTPStatus

from app.api.v1.models.request_model import create_role_parser
from app.api.v1.services.role import create_role_logic, get_roles_logic
from flask import request
from flask_restx import Namespace, Resource

role_ns = Namespace(name='role', validate=True)


@role_ns.route('/', endpoint='role')
class Role(Resource):
    @role_ns.doc(security='access_token', params={
        'skip': {'in': 'query', 'default': 0},
        'limit': {'in': 'query', 'default': 50}})
    @role_ns.response(int(HTTPStatus.OK), 'Success')
    @role_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @role_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @role_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @role_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def get(self):
        skip = int(request.args.get('skip'))
        limit = int(request.args.get('limit'))
        access_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        return get_roles_logic(access_token=access_token,
                               user_agent=user_agent,
                               skip=skip, limit=limit)

    @role_ns.doc(security='access_token')
    @role_ns.expect(create_role_parser)
    @role_ns.response(int(HTTPStatus.OK), 'Success')
    @role_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @role_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or expired.')
    @role_ns.response(int(HTTPStatus.FORBIDDEN), 'permission denied.')
    @role_ns.response(int(HTTPStatus.TOO_MANY_REQUESTS), 'Too many requests')
    @role_ns.response(int(HTTPStatus.SERVICE_UNAVAILABLE), 'Internal server error.')
    def post(self):
        request_data = create_role_parser.parse_args()
        name = request_data.get('name')
        access_token = request.headers.get('Authorization')
        user_agent = request.headers.get('User-Agent')
        return create_role_logic(name=name, access_token=access_token, user_agent=user_agent)
