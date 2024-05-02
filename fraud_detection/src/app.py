import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures


import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures

class FraudDetectionService(fraud_detection_grpc.FraudDetectionServiceServicer):
    def DetectFraud(self, request, context):
        # Initialize the response object
        response = fraud_detection.FraudDetectionResponse()

        # Fraud detection logic (unchanged)
        if request.billingAddress.street == request.billingAddress.city == request.billingAddress.state:
            response.isFraudulent = True
            response.reason = "Billing address's street, city, and state are identical, which is suspicious."
        else:
            response.isFraudulent = False
            response.reason = "No fraud detected"

        # Update and log the vector clock
        # This is a simplistic approach; you'll need to adapt it based on your actual logic for handling vector clocks.
        service_id = 'fraud_detection'  # Identifier for this service
        # to do ver
        timestamps = request.vector_clock.timestamps if request.vector_clock else {}
        timestamps[service_id] = timestamps.get(service_id, 0) + 1  # Increment the timestamp for this service
        print(f"Updated Vector Clock for service {service_id}: {timestamps}")  # Example logging

        # Attach the updated vector clock to the response
        for service, timestamp in timestamps.items():
            response.vector_clock.timestamps[service] = timestamp

        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fraud_detection_grpc.add_FraudDetectionServiceServicer_to_server(FraudDetectionService(), server)
    # Adjust the port number as needed
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Fraud Detection Service started. Listening on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
