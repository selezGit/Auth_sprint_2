from datetime import datetime, timedelta, timezone

import auth_pb2_grpc
import crud
import grpc
from auth_pb2 import (LoginRequest, LoginResponse, LogoutResponse,
                      RefreshTokenRequest, RefreshTokenResponse,
                      TestTokenRequest, TestTokenResponse, LoginViaGoogleRequest, LoginViaGoogleResponse)
from db import no_sql_db as redis_method
from db.db import get_db
from jwt.exceptions import InvalidTokenError
from user_agents import parse
from utils.token import (check_expire, create_access_token,
                         create_refresh_token, decode_token)
from loguru import logger
from sqlalchemy.exc import IntegrityError


class AuthService(auth_pb2_grpc.AuthServicer):
    def TestToken(self, request: TestTokenRequest, context):
        access_token = request.access_token
        user_agent = request.user_agent
        if access_token is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('access_token field required!')
            return TestTokenResponse()
        if user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return TestTokenResponse()

        try:
            payload = decode_token(token=access_token)

        except InvalidTokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return LoginResponse()
        if not check_expire(payload['expire']):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return TestTokenResponse()
        if redis_method.check_blacklist(access_token):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return TestTokenResponse()
        if user_agent != payload['agent']:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('user_agent not valid for this token!')
            return TestTokenResponse()
        return TestTokenResponse()

    def Login(self, request: LoginRequest, context):
        login = request.login
        password = request.password
        user_agent = request.user_agent

        if login is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('login field required!')
            return LoginResponse()
        if password is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('password field required!')
            return LoginResponse()
        if user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return LoginResponse()
        db = next(get_db())

        user = crud.user.get_by(db=db, login=login)
        if user is None:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(f'user with login: {login} not found!')
            return LoginResponse()

        if not crud.user.check_password(user=user, password=request.password):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(f'password not valid!')
            return LoginResponse()
        role = [role.name for role in user.roles]
        payload = {
            'user_id': str(user.id),
            'agent': request.user_agent,
            'role': role
        }
        refresh_delta = timedelta(days=7)

        _, expire_access, access_token = create_access_token(payload=payload)
        _, _, refresh_token = create_refresh_token(
            payload=payload, time=refresh_delta)

        user_agent = parse(request.user_agent)

        if 'SMART' in request.user_agent:
            device_type = 'smart'
        elif user_agent.is_mobile:
            device_type = 'mobile'

        else:
            device_type = 'web'

        sign_in = {
            'user_id': user.id,
            'user_device_type': device_type,
            'user_agent': request.user_agent,
        }
        crud.sign_in.create(db=db, obj_in=sign_in)

        redis_method.add_refresh_token(
            refresh_token=refresh_token, exp=refresh_delta)
        redis_method.add_auth_user(user_id=str(user.id), user_agent=request.user_agent, refresh_token=refresh_token,
                                   exp=refresh_delta)

        response = LoginResponse(access_token=access_token, refresh_token=refresh_token,
                                 expires_in=str(expire_access),
                                 token_type='Bearer')

        return response

    def RefreshToken(self, request: RefreshTokenRequest, context):
        user_agent = request.user_agent
        refresh_token = request.refresh_token
        db = next(get_db())

        if refresh_token is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('refresh_token field required!')
            return LoginResponse()
        if user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return LoginResponse()

        try:
            payload = decode_token(token=refresh_token)

        except InvalidTokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('refresh_token not valid!')
            return LoginResponse()
        if not check_expire(payload['expire']):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('refresh_token not valid!')
            return RefreshTokenResponse()
        if user_agent != payload['agent']:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('user_agent not valid for this token!')
            return RefreshTokenResponse()
        if not redis_method.check_whitelist(refresh_token=refresh_token):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid refresh token!')
            return RefreshTokenResponse()
        user = crud.user.get(db=db, id=payload['user_id'])
        if user is None:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(f'user not found!')
            return LoginResponse()

        check_refresh = redis_method.get_auth_user(
            payload['user_id'], user_agent=request.user_agent).decode()
        if check_refresh != refresh_token:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid refresh token! -')
            return RefreshTokenResponse()
        redis_method.del_refresh_token(refresh_token=refresh_token)
        refresh_delta = timedelta(days=7)
        role = [role.name for role in user.roles]

        payload_new = {
            'user_id': payload['user_id'],
            'agent': request.user_agent,
            'role': role
        }
        _, expire_access, access_token = create_access_token(payload=payload_new)
        payload_new['access_token'] = access_token
        _, _, refresh_token = create_refresh_token(
            payload=payload_new, time=refresh_delta)

        redis_method.add_refresh_token(refresh_token, exp=refresh_delta)
        redis_method.add_auth_user(
            payload['user_id'], request.user_agent, refresh_token, exp=refresh_delta)

        response = RefreshTokenResponse(access_token=access_token, refresh_token=refresh_token,
                                        expires_in=str(expire_access),
                                        token_type='Bearer')
        return response

    def Logout(self, request: LoginRequest, context):
        db = next(get_db())
        access_token = request.access_token
        user_agent = request.user_agent

        if access_token is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('access_token field required!')
            return LogoutResponse()
        if user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return LogoutResponse()
        if redis_method.check_blacklist(access_token):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('access_token not valid!')
            return LogoutResponse()
        try:
            payload = decode_token(token=access_token)

        except InvalidTokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return LoginResponse()
        if not check_expire(payload['expire']):
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('access_token not valid!')
            return LogoutResponse()
        if user_agent != payload['agent']:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('user_agent not valid for this token!')
            return LogoutResponse()

        sign_in = crud.sign_in.get_by(
            db=db, user_id=payload['user_id'], user_agent=user_agent)
        crud.sign_in.update(db=db, db_obj=sign_in, obj_in={'active': False})
        refresh_token = redis_method.get_auth_user(
            payload['user_id'], request.user_agent)
        redis_method.del_refresh_token(refresh_token)
        redis_method.del_auth_user(payload['user_id'], request.user_agent)
        exp_for_black_list = datetime.fromtimestamp(
            payload['expire'], timezone.utc) - datetime.now(timezone.utc)
        redis_method.add_to_blacklist(access_token, exp=exp_for_black_list)
        response = LoginResponse()
        return response

    def LoginViaGoogle(self, request: LoginViaGoogleRequest, context):

        if request.social_id is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('social_id field required!')
            return LoginViaGoogleResponse()
        if request.social_name is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('social_name field required!')
            return LoginViaGoogleResponse()
        if request.email is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('email field required!')
            return LoginViaGoogleResponse()
        if request.user_agent is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('user_agent field required!')
            return LoginViaGoogleResponse()
        db = next(get_db())

        user_id = crud.social_account.get_by_social_id(db=db, social_id=request.social_id,
                                                        social_name=request.social_name)
        if user_id:
            user_id = user_id[0]

        if user_id is None:
            try:
                role = crud.role.get_by(db=db, name='confirm')

                user = crud.user.create_social_account(
                    db=db, email=request.email, role=role)
                
                social = crud.social_account.create(db=db, obj_in={
                    'user_id': user.id,
                    'social_id': request.social_id,
                    'social_name': request.social_name,
                    'email': request.email
                })
                user_id = user.id
            except IntegrityError as e:
                logger.exception(e.orig.diag.message_detail)
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details(e.orig.diag.message_detail)
                return LoginViaGoogleResponse()
            except Exception as e:
                logger.exception(e)
                context.set_code(grpc.StatusCode.WARNING)
                context.set_details()
                return LoginViaGoogleResponse()

        user = crud.user.get_by(db=db, id=user_id)
        payload = {
            'user_id': str(user.id),
            'agent': request.user_agent
        }
        refresh_delta = timedelta(days=7)

        _, expire_access, access_token = create_access_token(payload=payload)
        _, _, refresh_token = create_refresh_token(
            payload=payload, time=refresh_delta)

        user_agent = parse(request.user_agent)

        if 'SMART' in request.user_agent:
            device_type = 'smart'
        elif user_agent.is_mobile:
            device_type = 'mobile'

        else:
            device_type = 'web'

        sign_in = {
            'user_id': user.id,
            'user_device_type': device_type,
            'user_agent': request.user_agent,
        }
        crud.sign_in.create(db=db, obj_in=sign_in)

        redis_method.add_refresh_token(
            refresh_token=refresh_token, exp=refresh_delta)
        redis_method.add_auth_user(user_id=str(user.id), user_agent=request.user_agent, refresh_token=refresh_token,
                                   exp=refresh_delta)

        response = LoginViaGoogleResponse(access_token=access_token, refresh_token=refresh_token,
                                          expires_in=str(expire_access),
                                          token_type='Bearer')

        return response
