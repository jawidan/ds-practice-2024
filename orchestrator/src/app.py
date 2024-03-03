import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb/fraud_detection"))
transaction_verification_utils_path = os.path.abspath(
    os.path.join(FILE, "../../../utils/pb/transaction_verification")
)

sys.path.insert(0, utils_path)
sys.path.insert(1, transaction_verification_utils_path)


import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc
from flask import jsonify

import grpc


def greet(name="you"):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel("fraud_detection:50051") as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.HelloServiceStub(channel)
        # Call the service through the stub object.
        response = stub.SayHello(fraud_detection.HelloRequest(name=name))
    return response.greeting


def detect_fraud(name="you"):
    with grpc.insecure_channel("fraud_detection:50051") as channel:
        stub = fraud_detection_grpc.HelloServiceStub(channel)
        response = stub.SayHello(fraud_detection.HelloRequest(name=name))
    return response.greeting


def verify_transaction(order):
    with grpc.insecure_channel("transaction_verification:50052") as channel:
        stub = transaction_verification_grpc.TransactionVerificationServiceStub(channel)
        response = stub.VerifyTransaction(
            transaction_verification.TransactionVerificationRequest(
                user=order.get("user"),
                creditCard=order.get("creditCard"),
                items=order.get("items"),
                billingAddress=order.get("billingAddress"),
                termsAndConditionsAccepted=order.get("termsAndConditionsAccepted"),
            )
        )
    
    # Check if the response has an 'errors' attribute and collect errors, if any.
    # This assumes 'errors' could be a list or repeated field in your response.
    # Adjust the handling if 'errors' is structured differently.
    errors = getattr(response, "errors", None)
    if errors is None:  # If there's no errors attribute or it's empty
        errors_list = []
    elif isinstance(errors, str):  # If errors is just a single string
        errors_list = [errors]
    else:  # Assuming errors is a list or repeated field
        errors_list = list(errors)
    
    return {
        "verification": str(response.verification),
        "errors": errors_list,  # Include the errors in the response
    }



# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request
from flask_cors import CORS

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app)


# Define a GET endpoint.
@app.route("/", methods=["GET"])
def index():
    """
    Responds with 'Hello, [name]' when a GET request is made to '/' endpoint.
    """
    # Test the fraud-detection gRPC service.
    response = greet(name="orchestrator")
    # Return the response.
    return response


@app.route("/checkout", methods=["POST"])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Print request object data
    order = request.json

    transaction_verification_response = verify_transaction(order)
    print("transaction reqeust: " , order)
    print("Transaction Verification 45$ ",transaction_verification_response)


    return transaction_verification_response
    # return transaction_verification_response.jsonify()


if __name__ == "__main__":
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host="0.0.0.0")






    # Dummy
    # order_status_response = {
    #     "orderId": "12345",
    #     "status": "Order Approved",
    #     "verification": "True",
    #     "suggestedBooks": [
    #         {"bookId": "123", "title": "Dummy Book 1", "author": "Author 1"},
    #         {"bookId": "456", "title": "Dummy Book 2", "author": "Author 2"},
    #     ],
    # }