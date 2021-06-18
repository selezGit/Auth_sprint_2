from app.api.v1.exceptions import error_handler
from app.api.v1.proto.auth_pb2 import (LoginRequest, LogoutRequest,
                                       RefreshTokenRequest, TestTokenRequest, LoginViaGoogleRequest)
from app.api.v1.proto.connector import ConnectServerGRPC
from flask import jsonify
from google.protobuf.json_format import MessageToDict


client = ConnectServerGRPC().conn_auth()


@error_handler
def login_logic(login: str, password: str, user_agent: str):
    login_data = LoginRequest(
        login=login, password=password, user_agent=user_agent)
    request = MessageToDict(client.Login(login_data))
    return jsonify(request)


@error_handler
def logout_logic(access_token: str, user_agent: str):
    logout_data = LogoutRequest(
        access_token=access_token, user_agent=user_agent)
    client.Logout(logout_data)
    return jsonify(
        status='success',
        message='Log out succeeded, token is no longer valid'
    )


@error_handler
def refresh_logic(refresh_token: str, user_agent: str):
    refresh_data = RefreshTokenRequest(refresh_token=refresh_token,
                                       user_agent=user_agent)
    request = MessageToDict(client.RefreshToken(refresh_data))
    return jsonify(request)


@error_handler
def test_logic(access_token: str, user_agent: str):
    test_token_data = TestTokenRequest(access_token=access_token,
                                       user_agent=user_agent)
    client.TestToken(test_token_data)
    return jsonify(status='Token is valid')


@error_handler
def login_via_google_logic(social_id: str, social_name: str,
                           email: str, user_agent: str):
    login_via_google_data = LoginViaGoogleRequest(social_id=social_id,
                                                  social_name=social_name,
                                                  email=email,
                                                  user_agent=user_agent)
    request = MessageToDict(client.LoginViaGoogle(login_via_google_data))
    return jsonify(request)
