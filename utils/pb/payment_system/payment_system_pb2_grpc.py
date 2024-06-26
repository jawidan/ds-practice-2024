# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import payment_system_pb2 as payment__system_dot_payment__system__pb2


class PaymentServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CheckBalance = channel.unary_unary(
                '/payment_system.PaymentService/CheckBalance',
                request_serializer=payment__system_dot_payment__system__pb2.CheckBalanceRequest.SerializeToString,
                response_deserializer=payment__system_dot_payment__system__pb2.CheckBalanceResponse.FromString,
                )
        self.ConfirmPayment = channel.unary_unary(
                '/payment_system.PaymentService/ConfirmPayment',
                request_serializer=payment__system_dot_payment__system__pb2.ConfirmPaymentRequest.SerializeToString,
                response_deserializer=payment__system_dot_payment__system__pb2.ConfirmPaymentResponse.FromString,
                )


class PaymentServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CheckBalance(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConfirmPayment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PaymentServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CheckBalance': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckBalance,
                    request_deserializer=payment__system_dot_payment__system__pb2.CheckBalanceRequest.FromString,
                    response_serializer=payment__system_dot_payment__system__pb2.CheckBalanceResponse.SerializeToString,
            ),
            'ConfirmPayment': grpc.unary_unary_rpc_method_handler(
                    servicer.ConfirmPayment,
                    request_deserializer=payment__system_dot_payment__system__pb2.ConfirmPaymentRequest.FromString,
                    response_serializer=payment__system_dot_payment__system__pb2.ConfirmPaymentResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'payment_system.PaymentService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PaymentService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CheckBalance(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/payment_system.PaymentService/CheckBalance',
            payment__system_dot_payment__system__pb2.CheckBalanceRequest.SerializeToString,
            payment__system_dot_payment__system__pb2.CheckBalanceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConfirmPayment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/payment_system.PaymentService/ConfirmPayment',
            payment__system_dot_payment__system__pb2.ConfirmPaymentRequest.SerializeToString,
            payment__system_dot_payment__system__pb2.ConfirmPaymentResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
