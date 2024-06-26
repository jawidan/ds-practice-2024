# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import suggestions_pb2 as suggestions_dot_suggestions__pb2


class BookSuggestionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SuggestBooks = channel.unary_unary(
                '/suggestions.BookSuggestionService/SuggestBooks',
                request_serializer=suggestions_dot_suggestions__pb2.BookRequest.SerializeToString,
                response_deserializer=suggestions_dot_suggestions__pb2.BookResponse.FromString,
                )


class BookSuggestionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SuggestBooks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BookSuggestionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SuggestBooks': grpc.unary_unary_rpc_method_handler(
                    servicer.SuggestBooks,
                    request_deserializer=suggestions_dot_suggestions__pb2.BookRequest.FromString,
                    response_serializer=suggestions_dot_suggestions__pb2.BookResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'suggestions.BookSuggestionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BookSuggestionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SuggestBooks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/suggestions.BookSuggestionService/SuggestBooks',
            suggestions_dot_suggestions__pb2.BookRequest.SerializeToString,
            suggestions_dot_suggestions__pb2.BookResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
