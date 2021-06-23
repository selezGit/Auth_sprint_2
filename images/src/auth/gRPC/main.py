import auth_pb2_grpc
from concurrent import futures
import grpc

from db.db import init_db
from db.pre_start_load import init_data

from services.user import UserService
from services.auth import AuthService
from services.role import RoleService

from loguru import logger


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=6))
    auth_pb2_grpc.add_AuthServicer_to_server(AuthService(), server)
    auth_pb2_grpc.add_UserServicer_to_server(UserService(), server)
    auth_pb2_grpc.add_RoleServicer_to_server(RoleService(), server)
    server.add_insecure_port('[::]:50051')

    server.start()
    logger.info('Server startup.')
    server.wait_for_termination()


if __name__ == '__main__':
    init_db()
    init_data()
    serve()
