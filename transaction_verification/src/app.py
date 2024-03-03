import sys
import os

FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(
    os.path.join(FILE, "../../../utils/pb/transaction_verification")
)
sys.path.insert(0, utils_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc
from concurrent import futures


# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.TransactionVerificationServicer
class TransactionVerification(
    transaction_verification_grpc.TransactionVerificationServiceServicer
):
    # Create an RPC function to say hello
    def VerifyTransaction(self, request, context):
        response = transaction_verification.TransactionVerificationResponse()

        print("Handle transaction")
        print(request.user)
        # check if the list of items is not empty,
        # the required user data is all filled-in, and the credit card format is correct
        # add some validation error messages
        response.verification = True

        if request.items is None or len(request.items) == 0:
            response.verification = False

        if request.user is None or not request.user.name or not request.user.contact:
            response.verification = False

        if (
            request.creditCard is None
            or not request.creditCard.number
            or not request.creditCard.expirationDate
            or not request.creditCard.cvv
        ):
            response.verification = False

        return response


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add TransactionVerification
    transaction_verification_grpc.add_TransactionVerificationServiceServicer_to_server(
        TransactionVerification(), server
    )
    # Listen on port 50052
    port = "50052"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50052.")
    # Keep thread alive
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
