import sys
import os
from datetime import datetime

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb/transaction_verification"))
sys.path.insert(0, utils_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc
from concurrent import futures

class TransactionVerification(transaction_verification_grpc.TransactionVerificationServiceServicer):
    def VerifyTransaction(self, request, context):
        response = transaction_verification.TransactionVerificationResponse()
        response.verification = True

        if not request.items:
            response.verification = False
            response.errors.append("The list of items is empty.")

        if not request.user or not request.user.name or not request.user.contact:
            response.verification = False
            response.errors.append("Missing required user data.")

        if not request.creditCard:
            response.verification = False
            response.errors.append("Credit card information is missing.")
        else:
            if len(request.creditCard.number) != 16:
                response.verification = False
                response.errors.append("Credit card number must be 16 digits long.")

            if len(request.creditCard.cvv) != 3:
                response.verification = False
                response.errors.append("CVV must be 3 characters long.")

            if request.creditCard.expirationDate:
                if not self.is_expiration_date_valid(request.creditCard.expirationDate):
                    response.verification = False
                    response.errors.append("Credit card expiration date is invalid or has expired.")

        response.vector_clock.timestamps["transaction_verification"] = request.vector_clock.timestamps.get("transaction_verification", 0) + 1

        return response

    def is_expiration_date_valid(self, expiration_date_str):
        # Placeholder for actual implementation
        return True

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_verification_grpc.add_TransactionVerificationServiceServicer_to_server(TransactionVerification(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Transaction Verification Service started. Listening on port 50052.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
