from http import HTTPStatus

from app.api.v1.exceptions import error_handler
from app.api.v1.proto.auth_pb2 import (UserAddRole, UserAppendSNRequest,
                                       UserCreateRequest, UserDeleteMe,
                                       UserDeleteSN, UserGetRequest,
                                       UserHistoryRequest, UserRemoveRole,
                                       UserUpdateEmailRequest,
                                       UserUpdatePasswordRequest)
from app.api.v1.proto.connector import ConnectServerGRPC
from flask import jsonify
from google.protobuf.json_format import MessageToDict

client = ConnectServerGRPC().conn_user()


@error_handler
def create_user_logic(login: str, email: str, password: str):
    create_user_data = UserCreateRequest(
        login=login, email=email, password=password)
    request = MessageToDict(client.Create(create_user_data))
    response = jsonify(request)
    response.status_code = HTTPStatus.CREATED
    return response


@error_handler
def delete_user_logic(access_token: str, user_agent: str):
    delete_user_data = UserDeleteMe(access_token=access_token,
                                    user_agent=user_agent)
    client.DeleteMe(delete_user_data)
    return jsonify(message='user successfully deleted')


@error_handler
def delete_sn_logic(uuid: str, user_agent: str, access_token: str):
    delete_sn_data = UserDeleteSN(uuid=uuid,
                                  user_agent=user_agent,
                                  access_token=access_token)
    client.DeleteSN(delete_sn_data)
    return jsonify(message='social network successfully deleted')


@error_handler
def get_user_logic(access_token: str, user_agent: str):
    get_user_data = UserGetRequest(
        access_token=access_token, user_agent=user_agent)
    request = MessageToDict(client.Get(get_user_data))
    return jsonify(request)


@error_handler
def history_logic(skip: int, limit: int,
                  access_token: str, user_agent: str):
    history_data = UserHistoryRequest(skip=skip,
                                      limit=limit,
                                      access_token=access_token,
                                      user_agent=user_agent)
    request = MessageToDict(client.GetHistory(history_data))
    return jsonify(request)


@error_handler
def change_password_logic(old_password: str, new_password: str,
                          access_token: str, user_agent: str):
    change_password_data = UserUpdatePasswordRequest(old_password=old_password,
                                                     new_password=new_password,
                                                     access_token=access_token,
                                                     user_agent=user_agent)
    client.UpdatePassword(change_password_data)
    return jsonify(status='Success')


@error_handler
def change_email_logic(email: str,
                       access_token: str, user_agent: str):
    upate_email_data = UserUpdateEmailRequest(access_token=access_token,
                                              user_agent=user_agent,
                                              email=email)
    client.UpdateEmail(upate_email_data)
    return jsonify(status='Success')


@error_handler
def append_google_SN_logic(email: str, access_token: str, user_agent: str,
                           social_id: str, social_name: str):
    append_SN_data = UserAppendSNRequest(email=email,
                                         access_token=access_token,
                                         user_agent=user_agent,
                                         social_id=social_id,
                                         social_name=social_name)
    client.AppendSN(append_SN_data)

    return jsonify(status='Success')


@error_handler
def add_role_logic(access_token: str, user_agent: str,
                   user_id: str, role_id: int):
    add_role_data = UserAddRole(access_token=access_token,
                                user_agent=user_agent,
                                user_id=user_id,
                                role_id=role_id)
    request = MessageToDict(client.addRole(add_role_data))
    return jsonify(request)


@error_handler
def del_role_logic(access_token: str, user_agent: str,
                   user_id: str, role_id: int):
    del_role_data = UserRemoveRole(access_token=access_token,
                                   user_agent=user_agent,
                                   user_id=user_id,
                                   role_id=role_id)
    request = MessageToDict(client.removeRole(del_role_data))
    return jsonify(request)
