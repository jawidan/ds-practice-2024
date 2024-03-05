import sys
import os
from threading import Thread
from queue import Queue


# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb/fraud_detection"))
transaction_verification_utils_path = os.path.abspath(
    os.path.join(FILE, "../../../utils/pb/transaction_verification")
)
suggestions_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb/suggestions"))


sys.path.insert(0, utils_path)
sys.path.insert(1, transaction_verification_utils_path)
sys.path.insert(2, suggestions_path)


import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

from flask import jsonify

import grpc


def greet(name="you"):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel("fraud_detection:50051") as channel:
        stub = fraud_detection_grpc.HelloServiceStub(channel)
        response = stub.SayHello(fraud_detection.HelloRequest(name=name))
    return response.greeting


def suggestBooks(order):
    with grpc.insecure_channel("suggestions:50053") as channel:
        stub = suggestions_grpc.BookSuggestionServiceStub(channel) 
        request = suggestions.BookRequest(name = order.get("items", {})[0].get("name", ""))
        response = stub.SuggestBooks(request)
        
    return {
        "suggestedBooks":[
            {
            "title": response.name, 
            }
        ]
    }


def detect_fraud(order):

    with grpc.insecure_channel("fraud_detection:50051") as channel:
        stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        request = fraud_detection.FraudDetectionRequest(
            user=fraud_detection.User(
                name=order.get("user", {}).get("name", ""),
                contact=order.get("user", {}).get("contact", "")
            ),
            creditCard=fraud_detection.CreditCard(
                number=order.get("creditCard", {}).get("number", ""),
                expirationDate=order.get("creditCard", {}).get("expirationDate", ""),
                cvv=order.get("creditCard", {}).get("cvv", "")
            ),
            billingAddress=fraud_detection.Address(
                street=order.get("billingAddress", {}).get("street", ""),
                city=order.get("billingAddress", {}).get("city", ""),
                state=order.get("billingAddress", {}).get("state", ""),
                zip=order.get("billingAddress", {}).get("zip", ""),
                country=order.get("billingAddress", {}).get("country", "")
            )            
        )                
        response = stub.DetectFraud(request)
        
    return {
        "isFraudulent": response.isFraudulent,
        "reason": response.reason
    }



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
    order = request.json
    print("Transaction request:", order)

    # Initialize queues for communication between threads
    fraud_queue = Queue()
    verification_queue = Queue()

    # Define functions to be executed in separate threads
    def detect_fraud_thread():
        fraud_response = detect_fraud(order)
        fraud_queue.put(fraud_response)

    def verify_transaction_thread():
        verification_response = verify_transaction(order)
        verification_queue.put(verification_response)

    # Start threads for fraud detection and transaction verification
    fraud_thread = Thread(target=detect_fraud_thread)
    verification_thread = Thread(target=verify_transaction_thread)

    fraud_thread.start()
    verification_thread.start()

    # Wait for both threads to finish
    fraud_thread.join()
    verification_thread.join()

    # Retrieve results from the queues
    fraud_detection_response = fraud_queue.get()
    transaction_verification_response = verification_queue.get()

    print("Fraud Detection:", fraud_detection_response)
    print("Transaction Verification:", transaction_verification_response)

    # Check if fraud detected or transaction not verified
    if fraud_detection_response["isFraudulent"]:
        # Handling fraudulent transactions
        return jsonify({
            "verification": "False",
            "orderStatus": "Fraudulent Transaction",
            "errors": [fraud_detection_response["reason"]],
            "isFraudulent": True
        })

    if transaction_verification_response["verification"] != "True":
        # Handling failed transaction verification
        return jsonify({
            "verification": "False",
            "orderStatus": "Transaction not verified",
            "errors": transaction_verification_response["errors"],
            "isFraudulent": False
        })

    # Both fraud detection and transaction verification passed
    # Run suggested books service
    suggested_books_response = suggestBooks(order)
    print("Suggested Books:", suggested_books_response)

    # Return order verified with orderID and suggested books
    return jsonify({
        "verification": "True",
        "orderID": "2345",  # Placeholder for order ID
        "orderStatus": "Approved",
        "suggestedBooks": suggested_books_response["suggestedBooks"],
        "isFraudulent": False,
        "fraudReason": ""
    }), 200


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