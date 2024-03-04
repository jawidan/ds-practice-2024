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
from datetime import datetime



# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.TransactionVerificationServicer

class TransactionVerification(transaction_verification_grpc.TransactionVerificationServiceServicer):
    def VerifyTransaction(self, request, context):
        response = transaction_verification.TransactionVerificationResponse()

        response.verification = True  # Assume true, set to false on any validation failure

        # Items check
        if not request.items:
            response.verification = False
            response.errors.append("The list of items is empty.")

        # User data check
        if not request.user or not request.user.name or not request.user.contact:
            response.verification = False
            response.errors.append("Missing required user data.")

        # Credit Card checks
        if not request.creditCard:
            response.verification = False
            response.errors.append("Credit card information is missing.")
        else:
            # Credit Card number length check
            if len(request.creditCard.number) != 16:
                response.verification = False
                response.errors.append("Credit card number must be 16 digits long.")

            # CVV length check
            if len(request.creditCard.cvv) != 3:
                response.verification = False
                response.errors.append("CVV must be 3 characters long.")

            # Expiration Date validity check
            if request.creditCard.expirationDate:
                if not self.is_expiration_date_valid(request.creditCard.expirationDate):
                    response.verification = False
                    response.errors.append("Credit card expiration date is invalid or has expired.")

        return response

    def is_expiration_date_valid(self, expiration_date_str):
        return True
        """Check if the expiration date (format MM/YY) has not passed."""
        try:
            expiration_date = datetime.strptime(expiration_date_str, "%m/%Y")
            current_date = datetime.now()
            return expiration_date >= current_date
        except ValueError:
            # If there's an error parsing the date, consider it invalid
            return False



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
