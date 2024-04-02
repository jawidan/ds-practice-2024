import json
import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import grpc

# Setup for gRPC stubs
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

app = Flask(__name__)
CORS(app)

class VectorClock:
    def __init__(self, clock=None):
        self.clock = clock if clock else {'transaction_verification': 0, 'fraud_detection': 0, 'suggestions': 0}

    def increment(self, service):
        self.clock[service] = self.clock.get(service, 0) + 1

    def to_proto(self, service):
        if service == "fraud_detection":
            vc_proto = fraud_detection.VectorClock(timestamps=self.clock)
        elif service == "transaction_verification":
            vc_proto = transaction_verification.VectorClock(timestamps=self.clock)
        elif service == "suggestions":
            vc_proto = suggestions.VectorClock(timestamps=self.clock)
        else:
            raise ValueError(f"Unsupported service type: {service}")
        return vc_proto

    def update_from_proto(self, vc_proto):
        for service, timestamp in vc_proto.timestamps.items():
            self.clock[service] = max(self.clock.get(service, 0), timestamp)

    def get_clock(self):
        return self.clock


def log_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {message}\n"
    print(log_entry)
    os.makedirs(os.path.dirname('logs/'), exist_ok=True)
    with open('logs/logs.txt', 'a') as log_file:
        log_file.write(log_entry)

def generate_order_id():
    return int(datetime.now().timestamp() * 1000)

def detect_fraud(order, vc):
    vc.increment('fraud_detection')
    fraud_detection_vc_proto = vc.to_proto("fraud_detection")
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
        ),
        vector_clock=fraud_detection_vc_proto
    )
    with grpc.insecure_channel("fraud_detection:50051") as channel:
        stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        response = stub.DetectFraud(request)
    vc.update_from_proto(response.vector_clock)
    return {"isFraudulent": response.isFraudulent, "reason": response.reason, "vc": vc.get_clock()}

def verify_transaction(order, vc):
    vc.increment('transaction_verification')
    transaction_verification_vc_proto = vc.to_proto("transaction_verification")
    request = transaction_verification.TransactionVerificationRequest(
        user=transaction_verification.User(name=order.get("user", {}).get("name", ""), contact=order.get("user", {}).get("contact", "")),
        creditCard=transaction_verification.CreditCard(
            number=order.get("creditCard", {}).get("number", ""),
            expirationDate=order.get("creditCard", {}).get("expirationDate", ""),
            cvv=order.get("creditCard", {}).get("cvv", "")
        ),
        items=[transaction_verification.Item(name=item.get("name", ""), quantity=item.get("quantity", 0)) for item in order.get("items", [])],
        billingAddress=transaction_verification.BillingAddress(
            street=order.get("billingAddress", {}).get("street", ""),
            city=order.get("billingAddress", {}).get("city", ""),
            state=order.get("billingAddress", {}).get("state", ""),
            zip=order.get("billingAddress", {}).get("zip", ""),
            country=order.get("billingAddress", {}).get("country", "")
        ),
        termsAndConditionsAccepted=order.get("termsAndConditionsAccepted", False),
        vector_clock=transaction_verification_vc_proto
    )
    with grpc.insecure_channel("transaction_verification:50052") as channel:
        stub = transaction_verification_grpc.TransactionVerificationServiceStub(channel)
        response = stub.VerifyTransaction(request)
    vc.update_from_proto(response.vector_clock)
    return {"verification": str(response.verification), "errors": response.errors, "vc": vc.get_clock()}

def suggestBooks(order, vc):
    vc.increment('suggestions')
    suggestions_vc_proto = vc.to_proto("suggestions")
    request = suggestions.BookRequest(
        name=order.get("items", [{}])[0].get("name", ""),
        vector_clock=suggestions_vc_proto
    )
    with grpc.insecure_channel("suggestions:50053") as channel:
        stub = suggestions_grpc.BookSuggestionServiceStub(channel)
        response = stub.SuggestBooks(request)
    vc.update_from_proto(response.vector_clock)
    return {"suggestedBooks": [{"title": "Suggested Book"}], "vc": vc.get_clock()}

@app.route("/", methods=["GET"])
def index():
    return "Service is running."



def serialize_vector_clock(vc):
    """Serialize vector clock for JSON response."""
    return json.dumps(vc.get_clock())

@app.route("/checkout", methods=["POST"])
def checkout():
    order = request.json
    order_id = generate_order_id()
    vc = VectorClock()
    print("Checking ...")
    fraud_response = detect_fraud(order, vc)
    print(fraud_response["isFraudulent"], ". . .isFraudulent")
    if fraud_response["isFraudulent"]:
        log_message(f"Fraudulent transaction detected: {fraud_response['reason']}")
        return jsonify({
            "verification": "False",
            "orderStatus": "Fraudulent Transaction",
            "errors": [fraud_response["reason"]],
            "isFraudulent": True,
            "orderID": order_id  # Include numeric OrderID in the response
        })

    verification_response = verify_transaction(order, vc)
    if not verification_response["verification"] == "True":
        # Convert Protobuf RepeatedScalarContainer to a Python list for JSON serialization
        errors_list = list(verification_response["errors"]) if verification_response["errors"] else []
        return jsonify({
            "orderID": order_id,
            "orderStatus": "Transaction Verification Failed",
            "verification": "False",
            "errors": errors_list,  # Use the converted list here
            "vectorClock": verification_response["vc"]
        })

    suggested_books_response = suggestBooks(order, vc)
    return jsonify({
        "orderID": str(order_id),
        "orderStatus": "Transaction Successful",
        "verification": "True",  # Ensure consistency in response format
        "suggestedBooks": suggested_books_response["suggestedBooks"],
        "vectorClock": serialize_vector_clock(vc)
    }), 200


if __name__ == "__main__":
    log_message("Orchestrator service starting.")
    app.run(host="0.0.0.0", debug=True)
