# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import proto.auth_pb2 as auth__pb2


class AuthStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Login = channel.unary_unary(
                '/Auth/Login',
                request_serializer=auth__pb2.LoginRequest.SerializeToString,
                response_deserializer=auth__pb2.LoginResponse.FromString,
                )
        self.RefreshToken = channel.unary_unary(
                '/Auth/RefreshToken',
                request_serializer=auth__pb2.RefreshTokenRequest.SerializeToString,
                response_deserializer=auth__pb2.RefreshTokenResponse.FromString,
                )
        self.Logout = channel.unary_unary(
                '/Auth/Logout',
                request_serializer=auth__pb2.LogoutRequest.SerializeToString,
                response_deserializer=auth__pb2.LogoutResponse.FromString,
                )
        self.TestToken = channel.unary_unary(
                '/Auth/TestToken',
                request_serializer=auth__pb2.TestTokenRequest.SerializeToString,
                response_deserializer=auth__pb2.TestTokenResponse.FromString,
                )
        self.LoginViaGoogle = channel.unary_unary(
                '/Auth/LoginViaGoogle',
                request_serializer=auth__pb2.LoginViaGoogleRequest.SerializeToString,
                response_deserializer=auth__pb2.LoginViaGoogleResponse.FromString,
                )


class AuthServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Login(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RefreshToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Logout(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TestToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LoginViaGoogle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Login': grpc.unary_unary_rpc_method_handler(
                    servicer.Login,
                    request_deserializer=auth__pb2.LoginRequest.FromString,
                    response_serializer=auth__pb2.LoginResponse.SerializeToString,
            ),
            'RefreshToken': grpc.unary_unary_rpc_method_handler(
                    servicer.RefreshToken,
                    request_deserializer=auth__pb2.RefreshTokenRequest.FromString,
                    response_serializer=auth__pb2.RefreshTokenResponse.SerializeToString,
            ),
            'Logout': grpc.unary_unary_rpc_method_handler(
                    servicer.Logout,
                    request_deserializer=auth__pb2.LogoutRequest.FromString,
                    response_serializer=auth__pb2.LogoutResponse.SerializeToString,
            ),
            'TestToken': grpc.unary_unary_rpc_method_handler(
                    servicer.TestToken,
                    request_deserializer=auth__pb2.TestTokenRequest.FromString,
                    response_serializer=auth__pb2.TestTokenResponse.SerializeToString,
            ),
            'LoginViaGoogle': grpc.unary_unary_rpc_method_handler(
                    servicer.LoginViaGoogle,
                    request_deserializer=auth__pb2.LoginViaGoogleRequest.FromString,
                    response_serializer=auth__pb2.LoginViaGoogleResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Auth', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Auth(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Login(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Auth/Login',
            auth__pb2.LoginRequest.SerializeToString,
            auth__pb2.LoginResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RefreshToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Auth/RefreshToken',
            auth__pb2.RefreshTokenRequest.SerializeToString,
            auth__pb2.RefreshTokenResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Logout(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Auth/Logout',
            auth__pb2.LogoutRequest.SerializeToString,
            auth__pb2.LogoutResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TestToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Auth/TestToken',
            auth__pb2.TestTokenRequest.SerializeToString,
            auth__pb2.TestTokenResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LoginViaGoogle(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Auth/LoginViaGoogle',
            auth__pb2.LoginViaGoogleRequest.SerializeToString,
            auth__pb2.LoginViaGoogleResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class UserStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/User/Get',
                request_serializer=auth__pb2.UserGetRequest.SerializeToString,
                response_deserializer=auth__pb2.UserResponse.FromString,
                )
        self.GetList = channel.unary_unary(
                '/User/GetList',
                request_serializer=auth__pb2.UserGetListRequest.SerializeToString,
                response_deserializer=auth__pb2.UserGetListResponse.FromString,
                )
        self.GetHistory = channel.unary_unary(
                '/User/GetHistory',
                request_serializer=auth__pb2.UserHistoryRequest.SerializeToString,
                response_deserializer=auth__pb2.UserHistoryResponse.FromString,
                )
        self.Create = channel.unary_unary(
                '/User/Create',
                request_serializer=auth__pb2.UserCreateRequest.SerializeToString,
                response_deserializer=auth__pb2.UserResponse.FromString,
                )
        self.UpdateEmail = channel.unary_unary(
                '/User/UpdateEmail',
                request_serializer=auth__pb2.UserUpdateEmailRequest.SerializeToString,
                response_deserializer=auth__pb2.UserResponse.FromString,
                )
        self.UpdatePassword = channel.unary_unary(
                '/User/UpdatePassword',
                request_serializer=auth__pb2.UserUpdatePasswordRequest.SerializeToString,
                response_deserializer=auth__pb2.UserResponse.FromString,
                )
        self.DeleteMe = channel.unary_unary(
                '/User/DeleteMe',
                request_serializer=auth__pb2.UserDeleteMe.SerializeToString,
                response_deserializer=auth__pb2.UserResponse.FromString,
                )
        self.DeleteSN = channel.unary_unary(
                '/User/DeleteSN',
                request_serializer=auth__pb2.UserDeleteSN.SerializeToString,
                response_deserializer=auth__pb2.UserDeleteSNResponse.FromString,
                )
        self.AppendSN = channel.unary_unary(
                '/User/AppendSN',
                request_serializer=auth__pb2.UserAppendSNRequest.SerializeToString,
                response_deserializer=auth__pb2.UserAppendResponse.FromString,
                )
        self.addRole = channel.unary_unary(
                '/User/addRole',
                request_serializer=auth__pb2.UserAddRole.SerializeToString,
                response_deserializer=auth__pb2.UserResponse.FromString,
                )
        self.removeRole = channel.unary_unary(
                '/User/removeRole',
                request_serializer=auth__pb2.UserRemoveRole.SerializeToString,
                response_deserializer=auth__pb2.UserResponse.FromString,
                )


class UserServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetHistory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateEmail(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdatePassword(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteMe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteSN(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AppendSN(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addRole(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def removeRole(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=auth__pb2.UserGetRequest.FromString,
                    response_serializer=auth__pb2.UserResponse.SerializeToString,
            ),
            'GetList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetList,
                    request_deserializer=auth__pb2.UserGetListRequest.FromString,
                    response_serializer=auth__pb2.UserGetListResponse.SerializeToString,
            ),
            'GetHistory': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHistory,
                    request_deserializer=auth__pb2.UserHistoryRequest.FromString,
                    response_serializer=auth__pb2.UserHistoryResponse.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=auth__pb2.UserCreateRequest.FromString,
                    response_serializer=auth__pb2.UserResponse.SerializeToString,
            ),
            'UpdateEmail': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateEmail,
                    request_deserializer=auth__pb2.UserUpdateEmailRequest.FromString,
                    response_serializer=auth__pb2.UserResponse.SerializeToString,
            ),
            'UpdatePassword': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdatePassword,
                    request_deserializer=auth__pb2.UserUpdatePasswordRequest.FromString,
                    response_serializer=auth__pb2.UserResponse.SerializeToString,
            ),
            'DeleteMe': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteMe,
                    request_deserializer=auth__pb2.UserDeleteMe.FromString,
                    response_serializer=auth__pb2.UserResponse.SerializeToString,
            ),
            'DeleteSN': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteSN,
                    request_deserializer=auth__pb2.UserDeleteSN.FromString,
                    response_serializer=auth__pb2.UserDeleteSNResponse.SerializeToString,
            ),
            'AppendSN': grpc.unary_unary_rpc_method_handler(
                    servicer.AppendSN,
                    request_deserializer=auth__pb2.UserAppendSNRequest.FromString,
                    response_serializer=auth__pb2.UserAppendResponse.SerializeToString,
            ),
            'addRole': grpc.unary_unary_rpc_method_handler(
                    servicer.addRole,
                    request_deserializer=auth__pb2.UserAddRole.FromString,
                    response_serializer=auth__pb2.UserResponse.SerializeToString,
            ),
            'removeRole': grpc.unary_unary_rpc_method_handler(
                    servicer.removeRole,
                    request_deserializer=auth__pb2.UserRemoveRole.FromString,
                    response_serializer=auth__pb2.UserResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'User', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class User(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/User/Get',
            auth__pb2.UserGetRequest.SerializeToString,
            auth__pb2.UserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/User/GetList',
            auth__pb2.UserGetListRequest.SerializeToString,
            auth__pb2.UserGetListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetHistory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/User/GetHistory',
            auth__pb2.UserHistoryRequest.SerializeToString,
            auth__pb2.UserHistoryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/User/Create',
            auth__pb2.UserCreateRequest.SerializeToString,
            auth__pb2.UserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateEmail(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/User/UpdateEmail',
            auth__pb2.UserUpdateEmailRequest.SerializeToString,
            auth__pb2.UserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdatePassword(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/User/UpdatePassword',
            auth__pb2.UserUpdatePasswordRequest.SerializeToString,
            auth__pb2.UserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteMe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/User/DeleteMe',
            auth__pb2.UserDeleteMe.SerializeToString,
            auth__pb2.UserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteSN(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/User/DeleteSN',
            auth__pb2.UserDeleteSN.SerializeToString,
            auth__pb2.UserDeleteSNResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AppendSN(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/User/AppendSN',
            auth__pb2.UserAppendSNRequest.SerializeToString,
            auth__pb2.UserAppendResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def addRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/User/addRole',
            auth__pb2.UserAddRole.SerializeToString,
            auth__pb2.UserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def removeRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/User/removeRole',
            auth__pb2.UserRemoveRole.SerializeToString,
            auth__pb2.UserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class RoleStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/Role/Get',
                request_serializer=auth__pb2.RoleGetList.SerializeToString,
                response_deserializer=auth__pb2.RoleResponseList.FromString,
                )
        self.Create = channel.unary_unary(
                '/Role/Create',
                request_serializer=auth__pb2.RoleCreate.SerializeToString,
                response_deserializer=auth__pb2.RoleResponse.FromString,
                )
        self.Delete = channel.unary_unary(
                '/Role/Delete',
                request_serializer=auth__pb2.RoleRemove.SerializeToString,
                response_deserializer=auth__pb2.RoleResponse.FromString,
                )
        self.Update = channel.unary_unary(
                '/Role/Update',
                request_serializer=auth__pb2.RoleUpdate.SerializeToString,
                response_deserializer=auth__pb2.RoleResponse.FromString,
                )


class RoleServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RoleServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=auth__pb2.RoleGetList.FromString,
                    response_serializer=auth__pb2.RoleResponseList.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=auth__pb2.RoleCreate.FromString,
                    response_serializer=auth__pb2.RoleResponse.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=auth__pb2.RoleRemove.FromString,
                    response_serializer=auth__pb2.RoleResponse.SerializeToString,
            ),
            'Update': grpc.unary_unary_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=auth__pb2.RoleUpdate.FromString,
                    response_serializer=auth__pb2.RoleResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Role', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Role(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Role/Get',
            auth__pb2.RoleGetList.SerializeToString,
            auth__pb2.RoleResponseList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Role/Create',
            auth__pb2.RoleCreate.SerializeToString,
            auth__pb2.RoleResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Role/Delete',
            auth__pb2.RoleRemove.SerializeToString,
            auth__pb2.RoleResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Role/Update',
            auth__pb2.RoleUpdate.SerializeToString,
            auth__pb2.RoleResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
