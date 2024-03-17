import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import grpc
from threading import Thread
from queue import Queue

# Function to append log messages to logs.txt
def log_message(message):
    """Append a log message to logs.txt file with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {message}\n"
    print("Log entry: ", log_entry)  # Simplified debug print
    # Ensure the logs directory exists
    os.makedirs(os.path.dirname('logs/'), exist_ok=True)
    with open('logs/logs.txt', 'a') as log_file:
        log_file.write(log_entry)

# gRPC stubs import setup
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb/fraud_detection"))
transaction_verification_utils_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb/transaction_verification"))
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

def generate_order_id():
    """Generate a numeric OrderID based on current timestamp."""
    return int(datetime.now().timestamp() * 1000)  # Milliseconds since epoch

def greet(name="you"):
    with grpc.insecure_channel("fraud_detection:50051") as channel:
        stub = fraud_detection_grpc.HelloServiceStub(channel)
        response = stub.SayHello(fraud_detection.HelloRequest(name=name))
    return response.greeting

def suggestBooks(order):
    with grpc.insecure_channel("suggestions:50053") as channel:
        stub = suggestions_grpc.BookSuggestionServiceStub(channel)
        request = suggestions.BookRequest(name=order.get("items", {})[0].get("name", ""))
        response = stub.SuggestBooks(request)
        
    return {"suggestedBooks": [{"title": response.name}]}

def detect_fraud(order):
    with grpc.insecure_channel("fraud_detection:50051") as channel:
        stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        request = fraud_detection.FraudDetectionRequest(
            user=fraud_detection.User(name=order.get("user", {}).get("name", ""), contact=order.get("user", {}).get("contact", "")),
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
        
    return {"isFraudulent": response.isFraudulent, "reason": response.reason}

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
    
    errors = getattr(response, "errors", None)
    errors_list = [errors] if isinstance(errors, str) else list(errors) if errors else []
    
    return {"verification": str(response.verification), "errors": errors_list}

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def index():
    log_message("Index page accessed")
    response = greet(name="orchestrator")
    return response

@app.route("/checkout", methods=["POST"])
def checkout():
    order = request.json
    # Generate a unique numeric OrderID for the current order
    order_id = generate_order_id()
    log_message(f"Order ID {order_id} generated for transaction request: {order}")
    
    fraud_queue = Queue()
    verification_queue = Queue()

    def detect_fraud_thread():
        fraud_response = detect_fraud(order)
        fraud_queue.put(fraud_response)

    def verify_transaction_thread():
        verification_response = verify_transaction(order)
        verification_queue.put(verification_response)

    fraud_thread = Thread(target=detect_fraud_thread)
    verification_thread = Thread(target=verify_transaction_thread)

    fraud_thread.start()
    verification_thread.start()

    fraud_thread.join()
    verification_thread.join()

    fraud_detection_response = fraud_queue.get()
    transaction_verification_response = verification_queue.get()

    if fraud_detection_response["isFraudulent"]:
        log_message(f"Fraudulent transaction detected: {fraud_detection_response['reason']}")
        return jsonify({
            "verification": "False",
            "orderStatus": "Fraudulent Transaction",
            "errors": [fraud_detection_response["reason"]],
            "isFraudulent": True,
            "orderID": order_id  # Include numeric OrderID in the response
        })

    if transaction_verification_response["verification"] != "True":
        log_message(f"Transaction not verified: {transaction_verification_response['errors']}")
        return jsonify({
            "verification": "False",
            "orderStatus": "Transaction not verified",
            "errors": transaction_verification_response["errors"],
            "isFraudulent": False,
            "orderID": order_id  # Include numeric OrderID in the response
        })

    suggested_books_response = suggestBooks(order)
    log_message(f"Suggested Books: {suggested_books_response['suggestedBooks']}")

    return jsonify({
        "verification": "True",
        "orderID": order_id,  # Include numeric OrderID in the successful response
        "orderStatus": "Approved",
        "suggestedBooks": suggested_books_response["suggestedBooks"],
        "isFraudulent": False,
        "fraudReason": ""
    }), 200

if __name__ == "__main__":
    log_message("Starting the Flask application")
    app.run(host="0.0.0.0", debug=True)



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