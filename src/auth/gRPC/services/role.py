from datetime import datetime, timedelta, timezone

import auth_pb2_grpc
import crud
import grpc
from auth_pb2 import (RoleCreate, RoleUpdate, RoleRemove, RoleResponse, RoleGetList, RoleResponseList)
from db import no_sql_db as redis_method
from db.db import get_db
from jwt.exceptions import InvalidTokenError
from user_agents import parse
from utils.token import (check_expire, create_access_token,
                         create_refresh_token, decode_token)
from loguru import logger
from sqlalchemy.exc import IntegrityError


class RoleService(auth_pb2_grpc.RoleServicer):
    def Get(self, request: RoleGetList, context):
        access_token = request.access_token
        user_agent = request.user_agent
        skip = request.skip or 0
        limit = request.limit or 25
        try:
            payload = decode_token(token=access_token)

        except InvalidTokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return RoleResponse()
        if redis_method.check_blacklist(access_token):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return RoleResponse()
        if user_agent != payload['agent']:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('user_agent not valid for this token!')
            return RoleResponse()
        if not 'admin' in payload['role']:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('user is not admin')
            return RoleResponse()
        db = next(get_db())
        roles_db = crud.role.get_all(db=db, skip=skip, limit=limit)
        rows = [RoleResponse(id=role.id, name=role.name) for role in roles_db]
        return RoleResponseList(rows=rows)

    def Create(self, request: RoleCreate, context):
        access_token = request.access_token
        user_agent = request.user_agent
        try:
            payload = decode_token(token=access_token)

        except InvalidTokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return RoleResponse()
        if redis_method.check_blacklist(access_token):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return RoleResponse()
        if user_agent != payload['agent']:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('user_agent not valid for this token!')
            return RoleResponse()
        db = next(get_db())
        if not 'admin' in payload['role']:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('user is not admin')
            return RoleResponse()
        try:
            role = crud.role.create(db=db, obj_in={
                'name': request.name
            })
        except IntegrityError as e:
            logger.exception(e.orig.diag.message_detail)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(e.orig.diag.message_detail)
            return RoleResponse()
        return RoleResponse(id=role.id, name=role.name)