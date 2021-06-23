from app.api.v1.exceptions import error_handler
from app.api.v1.proto.auth_pb2 import (RoleGetList, RoleCreate)
from app.api.v1.proto.connector import ConnectServerGRPC
from flask import jsonify
from google.protobuf.json_format import MessageToDict

client = ConnectServerGRPC().conn_role()


@error_handler
def get_roles_logic(access_token: str, user_agent: str,
                    skip: int, limit: int):
    get_roles_data = RoleGetList(access_token=access_token,
                                 user_agent=user_agent,
                                 skip=skip,
                                 limit=limit)
    request = MessageToDict(client.Get(get_roles_data))
    return jsonify(request)


@error_handler
def create_role_logic(access_token: str, user_agent: str,
                      name: str):
    create_role_data = RoleCreate(access_token=access_token,
                                  user_agent=user_agent,
                                  name=name)
    request = MessageToDict(client.Create(create_role_data))
    return jsonify(request)
