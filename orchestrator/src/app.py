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



class VectorClock:
    def __init__(self, clock=None):
        if clock is None:
            self.clock = {'transaction_verification': 0, 'fraud_detection': 0, 'suggestions': 0}
        else:
            self.clock = clock

    def increment(self, service):
        if service in self.clock:
            self.clock[service] += 1

    def get_clock(self):
        return self.clock

    @classmethod
    def from_dict(cls, clock_dict):
        # This now correctly passes the clock_dict to the __init__ method
        return cls(clock=clock_dict)


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


def suggestBooks(order, vc):
    # Simulate vector clock increment by suggestion service
    with grpc.insecure_channel("suggestions:50053") as channel:
        stub = suggestions_grpc.BookSuggestionServiceStub(channel)
        request = suggestions.BookRequest(name=order.get("items", {})[0].get("name", ""))
        response = stub.SuggestBooks(request)
    vc.increment('suggestions')
    return {"suggestedBooks":[{"title": response.name}], "vc": vc.get_clock()}

def detect_fraud(order, vc):
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
        
    
    vc.increment('fraud_detection')
    return {"isFraudulent": response.isFraudulent, "reason": response.reason, "vc": vc.get_clock()}

def verify_transaction(order, vc):
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
    
    vc.increment('transaction_verification')
    return {"verification": str(response.verification), "errors": errors_list, "vc": vc.get_clock()}
    

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
    order_id = generate_order_id()
    log_message(f"Order ID {order_id} generated for transaction request: {order}")

    # Initialize Vector Clock for the order
    vc = VectorClock()

    # Adjusted to reflect event ordering and vector clock updates
    # Assuming sequential processing for simplicity; in a real scenario, you may need async handling
    vc_data = vc.get_clock()
    verification_response = verify_transaction(order, vc)
    vc_data = verification_response["vc"]  # Update VC from transaction verification

    if not verification_response["verification"] == "True":
        log_message(f"Transaction not verified: {verification_response['errors']}")
        return jsonify({
            "verification": "False",
            "orderStatus": "Transaction not verified",
            "errors": verification_response["errors"],
            "isFraudulent": False,
            "orderID": order_id,
            "vectorClock": vc_data
        })

    fraud_response = detect_fraud(order, VectorClock.from_dict(vc_data))
    vc_data = fraud_response["vc"]  # Update VC from fraud detection

    if fraud_response["isFraudulent"]:
        log_message(f"Fraudulent transaction detected: {fraud_response['reason']}")
        return jsonify({
            "verification": "False",
            "orderStatus": "Fraudulent Transaction",
            "errors": [fraud_response["reason"]],
            "isFraudulent": True,
            "orderID": order_id,
            "vectorClock": vc_data
        })

    suggested_books_response = suggestBooks(order, VectorClock.from_dict(vc_data))
    vc_data = suggested_books_response["vc"]  # Final VC update from suggestions

    log_message(f"Suggested Books: {suggested_books_response['suggestedBooks']}")
    return jsonify({
        "verification": "True",
        "orderID": order_id,
        "orderStatus": "Approved",
        "suggestedBooks": suggested_books_response["suggestedBooks"],
        "isFraudulent": False,
        "fraudReason": "",
        "vectorClock": vc_data
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