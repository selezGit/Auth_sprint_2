import grpc
from fastapi import Depends, Header
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from proto.auth_pb2 import UserGetRequest
from proto.connector import ConnectServerGRPC
from google.protobuf.json_format import MessageToDict

client = ConnectServerGRPC().conn_auth()
oauth2_scheme = HTTPBearer(scheme_name='access_token')


def check_token(
    access_token: HTTPBasicCredentials = Depends(oauth2_scheme),
    user_agent: str = Header(None)
):
    token_data = UserGetRequest(access_token=access_token.credentials,
                                       user_agent=user_agent)
    try:
        request = MessageToDict(client.Get(token_data))
        roles = [values.get('name') for values in request.get('roles')]
        is_premium = True if set(['admin', 'premium']) & set(roles) else False

        return {'access': True, 'is_premium': is_premium}
    except grpc.RpcError:
        return {'access': False, 'is_premium': False}

