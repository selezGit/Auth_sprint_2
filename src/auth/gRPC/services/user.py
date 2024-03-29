from datetime import datetime, timezone

import auth_pb2_grpc
import crud
import grpc
from auth_pb2 import (UserAppendResponse, UserAppendSNRequest,UserDeleteSN, UserDeleteSNResponse, UserCreateRequest, UserDeleteMe, UserGetRequest,
                      UserHistory, UserHistoryRequest, UserHistoryResponse,
                      UserResponse, UserDeleteSNResponse,UserUpdateEmailRequest,
                      UserUpdatePasswordRequest, RoleResponse, UserAddRole, UserRemoveRole)
from db import no_sql_db as redis_method
from db.db import get_db
from jwt.exceptions import InvalidTokenError
from loguru import logger
from sqlalchemy.exc import IntegrityError
from utils.token import check_expire, decode_token


class UserService(auth_pb2_grpc.UserServicer):

    def Create(self, request: UserCreateRequest, context) -> UserResponse:
        db = next(get_db())
        if request.login is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('login field required!')
            return UserResponse()
        if request.password is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('password field required!')
            return UserResponse()
        if request.email is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('email field required!')
            return UserResponse()
        try:
            role = crud.role.get_by(db=db, name='confirm')

            user = crud.user.create(db=db, obj_in={
                'login': request.login,
                'email': request.email,
                'password': request.password
            }, role=role)
        except IntegrityError as e:
            logger.exception(e.orig.diag.message_detail)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(e.orig.diag.message_detail)
            return UserResponse()
        except Exception as e:
            logger.exception(e)
            context.set_code(grpc.StatusCode.WARNING)
            context.set_details()
            return UserResponse()
        user_response = UserResponse(
            id=str(user.id), login=user.login, email=user.email)
        return user_response

    def Get(self, request: UserGetRequest, context):
        db = next(get_db())
        if request.access_token is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('access_token field required!')
            return UserResponse()
        if request.user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return UserResponse()
        access_token = request.access_token
        user_agent = request.user_agent
        try:
            payload = decode_token(token=access_token)

        except InvalidTokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()
        if redis_method.check_blacklist(access_token):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()
        if not check_expire(payload['expire']):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()

        if user_agent != payload['agent']:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('user_agent not valid for this token!')
            return UserResponse()
        user = crud.user.get_by(db=db, id=payload['user_id'])
        roles = [RoleResponse(id=role.id, name=role.name) for role in user.roles]
        user_socials = [{'id': str(social.id), 'social_name': social.social_name, 'email': social.email} for social in user.social_account]

        return UserResponse(id=str(user.id), login=user.login, email=user.email, roles=roles, social_networks=user_socials)

    def GetHistory(self, request: UserHistoryRequest, context):
        db = next(get_db())
        if request.access_token is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('access_token field required!')
            return UserResponse()
        if request.user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return UserResponse()
        access_token = request.access_token
        user_agent = request.user_agent
        skip = request.skip or 0
        limit = request.limit or 50
        if access_token is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('access_token field required!')
            return UserHistoryResponse()
        if user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return UserHistoryResponse()
        try:
            payload = decode_token(token=access_token)

        except InvalidTokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()

        if not check_expire(payload['expire']):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserHistoryResponse()
        if redis_method.check_blacklist(access_token):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserHistoryResponse()
        if user_agent != payload['agent']:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('user_agent not valid for this token!')
            return UserHistoryResponse()

        history = crud.sign_in.get_history(
            db=db, user_id=payload['user_id'], skip=skip, limit=limit)

        row = [UserHistory(date=str(sign_in.logined_by), user_agent=sign_in.user_agent,
                           device_type=sign_in.user_device_type, active=sign_in.active) for sign_in in history]
        response = UserHistoryResponse(rows=row)
        return response

    def UpdateEmail(self, request: UserUpdateEmailRequest, context):
        db = next(get_db())

        if request.access_token is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('access_token field required!')
            return UserResponse()
        if request.user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return UserResponse()
        if request.email is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('email field required!')
            return UserResponse()
        access_token = request.access_token
        user_agent = request.user_agent
        email = request.email
        try:
            payload = decode_token(token=access_token)

        except InvalidTokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()

        if redis_method.check_blacklist(access_token):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()

        if not check_expire(payload['expire']):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()
        if user_agent != payload['agent']:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('user_agent not valid for this token!')
            return UserResponse()

        user = crud.user.get_by(db=db, id=payload['user_id'])

        try:
            user = crud.user.update(
                db=db, db_obj=user, obj_in={'email': email})
        except IntegrityError as e:
            logger.exception(e.orig.diag.message_detail)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(e.orig.diag.message_detail)
            return UserResponse()
        response = UserResponse(
            id=str(user.id), email=user.email, login=user.login)
        return response

    def UpdatePassword(self, request: UserUpdatePasswordRequest, context):
        db = next(get_db())
        access_token = request.access_token
        user_agent = request.user_agent
        new_password = request.new_password
        old_password = request.old_password
        if access_token is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('access_token field required!')
            return UserResponse()
        if user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return UserResponse()
        if new_password is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('new_password field required!')
            return UserResponse()
        if old_password is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('password field required!')
            return UserResponse()
        try:
            payload = decode_token(token=access_token)

        except InvalidTokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()

        if not check_expire(payload['expire']):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()
        if redis_method.check_blacklist(access_token):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()
        if user_agent != payload['agent']:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('user_agent not valid for this token!')
            return UserResponse()
        user = crud.user.get_by(db=db, id=payload['user_id'])

        if user.password_hash is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('method not allowed for this user type')
            return UserResponse()

        if not crud.user.check_password(user=user, password=old_password):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(f'password not valid!')
            return UserResponse()
        user = crud.user.update(db=db, db_obj=user, obj_in={
            'password': new_password})

        all_auth = redis_method.get_all_auth_user(payload['user_id'])

        for _, ref in all_auth.items():
            try:
                payload = decode_token(token=access_token)
            except InvalidTokenError as e:
                pass
            exp_for_black_list = datetime.fromtimestamp(
                payload['expire'], timezone.utc) - datetime.now(timezone.utc)
            redis_method.add_to_blacklist(
                access_token, exp=exp_for_black_list)

            redis_method.del_refresh_token(ref.decode())
        redis_method.del_all_auth_user(payload['user_id'])
        response = UserResponse(
            id=str(user.id), email=user.email, login=user.login)
        return response

    def DeleteMe(self, request: UserDeleteMe, context):
        db = next(get_db())
        access_token = request.access_token
        user_agent = request.user_agent
        if access_token is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('access_token field required!')
            return UserResponse()
        if user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return UserResponse()
        try:
            payload = decode_token(token=access_token)

        except InvalidTokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()
        if redis_method.check_blacklist(access_token):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()
        if not check_expire(payload['expire']):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserResponse()
        if user_agent != payload['agent']:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('user_agent not valid for this token!')
            return UserResponse()
        user = crud.user.get_by(db=db, id=payload['user_id'])
        all_auth = redis_method.get_all_auth_user(payload['user_id'])

        for _, ref in all_auth.items():
            try:
                payload = decode_token(token=access_token)
            except InvalidTokenError as e:
                pass
            exp_for_black_list = datetime.fromtimestamp(
                payload['expire'], timezone.utc) - datetime.now(timezone.utc)
            redis_method.add_to_blacklist(
                access_token, exp=exp_for_black_list)

            redis_method.del_refresh_token(ref.decode())
        redis_method.del_all_auth_user(payload['user_id'])
        crud.user.remove(db=db, db_obj=user)
        return UserResponse()

    def DeleteSN(self, request: UserDeleteSN, context):
        access_token = request.access_token
        user_agent = request.user_agent
        social_uuid = request.uuid
        if access_token is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('access_token field required!')
            return UserDeleteSNResponse()
        if user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return UserDeleteSNResponse()
        if social_uuid is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('uuid field required!')
            return UserDeleteSNResponse()

        try:
            payload = decode_token(token=access_token)

        except InvalidTokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserDeleteSNResponse()
        if redis_method.check_blacklist(access_token):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserDeleteSNResponse()
        if not check_expire(payload['expire']):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserDeleteSNResponse()
        if user_agent != payload['agent']:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('user_agent not valid for this token!')
            return UserDeleteSNResponse()
        db = next(get_db())

        social_accounts_count = crud.social_account.get_count_social_ids(
            db=db, user_id=payload['user_id'])
        user = crud.user.get_by(db=db, id=payload['user_id'])

        if social_accounts_count == 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('incorrect uuid, social network not found')
            return UserDeleteSNResponse()
        elif social_accounts_count == 1 and user.login is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(
                'to unlink social network, you need more than one SN')
            return UserDeleteSNResponse()

        crud.social_account.remove(
            db=db, db_obj=crud.social_account.get_by(db=db, id=social_uuid))
        return UserDeleteSNResponse()

    def AppendSN(self, request: UserAppendSNRequest, context):

        social_id = request.social_id
        social_name = request.social_name
        access_token = request.access_token
        user_agent = request.user_agent
        email = request.email

        if social_id is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('social_id field required!')
            return UserAppendResponse()
        if social_name is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('social_name field required!')
            return UserAppendResponse()
        if user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return UserAppendResponse()
        if access_token is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('access_token field required!')
            return UserAppendResponse()
        if email is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('email field required!')
            return UserAppendResponse()
        try:
            logger.info(access_token)
            payload = decode_token(token=access_token)

        except InvalidTokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserAppendResponse()
        if redis_method.check_blacklist(access_token):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserAppendResponse()
        if not check_expire(payload['expire']):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return UserAppendResponse()
        if user_agent != payload['agent']:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('user_agent not valid for this token!')
            return UserAppendResponse()
        db = next(get_db())

        if crud.social_account.get_by_social_id(db=db, social_id=social_id,
                                                social_name=social_name):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('this social network already binded')
            return UserAppendResponse()

        try:

            social = crud.social_account.create(db=db, obj_in={
                'user_id': payload['user_id'],
                'social_id': social_id,
                'social_name': social_name,
                'email': email
            })

        except IntegrityError as e:
            logger.exception(e.orig.diag.message_detail)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(e.orig.diag.message_detail)
            return UserAppendResponse()
        except Exception as e:
            logger.exception(e)
            context.set_code(grpc.StatusCode.WARNING)
            context.set_details()
            return UserAppendResponse()
        return UserDeleteSNResponse()

    def addRole(self, request: UserAddRole, context):
        access_token = request.access_token
        user_agent = request.user_agent
        role_id = request.role_id
        user_id = request.user_id

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

        user = crud.user.get(db=db, id=user_id)
        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('user with id %s not found' % (user_id,))
            return RoleResponse()
        role_obj = crud.role.get(db=db, id=role_id)
        if role_obj is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('role with id %s not found' % (role_id,))
            return RoleResponse()
        crud.user.append_role(db=db, user=user, role=role_obj)
        all_auth = redis_method.get_all_auth_user(user_id=user_id)

        for _, ref in all_auth.items():
            try:
                payload = decode_token(token=access_token)
            except InvalidTokenError as e:
                pass
            exp_for_black_list = datetime.fromtimestamp(
                payload['expire'], timezone.utc) - datetime.now(timezone.utc)
            redis_method.add_to_blacklist(
                access_token, exp=exp_for_black_list)

        roles = [RoleResponse(id=role.id, name=role.name) for role in user.roles]
        return UserResponse(id=str(user.id), login=user.login, email=user.email, roles=roles)

    def removeRole(self, request: UserRemoveRole, context):
        access_token = request.access_token
        user_agent = request.user_agent
        role_id = request.role_id
        user_id = request.user_id

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

        user = crud.user.get(db=db, id=user_id)
        role_obj = crud.role.get(db=db, id=role_id)
        if role_obj is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('role with id %s not found' % (role_id,))
            return RoleResponse()
        if role_obj.name == 'admin':
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details('role is admin not removed')
            return RoleResponse()

        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('user with id %s not found' % (user_id,))
            return RoleResponse()
        role = None
        for r in user.roles:
            if r.id == role_id:
                role = r
                break

        if role:
            crud.user.remove_role(db=db, user=user, role=role)
            all_auth = redis_method.get_all_auth_user(user_id=user_id)

            for _, ref in all_auth.items():
                try:
                    payload = decode_token(token=access_token)
                except InvalidTokenError as e:
                    pass
                exp_for_black_list = datetime.fromtimestamp(
                    payload['expire'], timezone.utc) - datetime.now(timezone.utc)
                redis_method.add_to_blacklist(
                    access_token, exp=exp_for_black_list)
        roles = [RoleResponse(id=role.id, name=role.name) for role in user.roles]
        return UserResponse(id=str(user.id), login=user.login, email=user.email, roles=roles)
