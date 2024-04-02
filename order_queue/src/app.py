import json
import sys
import os
import queue

FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb/order_queue"))
sys.path.insert(0, utils_path)
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

import grpc
from concurrent import futures

# Define a global order queue. In a production environment, consider using a more robust queue or storage.
orders_queue = queue.Queue()

class OrderQueueService(order_queue_grpc.OrderQueueServiceServicer):
    def EnqueueOrder(self, request, context):
        # Assuming 'request' contains order details, and we're serializing and enqueueing it.
        # You might choose to store the order in a different format or structure.
        try:
            order_details = {
                'user': {'name': request.user.name, 'contact': request.user.contact},
                'creditCard': {
                    'number': request.creditCard.number, 
                    'expirationDate': request.creditCard.expirationDate, 
                    'cvv': request.creditCard.cvv
                },
                'userComment': request.userComment,
                # Additional fields as required
            }
            # Convert order_details to string for queueing. Consider a more structured approach for production.
            order_string = json.dumps(order_details)
            orders_queue.put(order_string)  # Enqueue the serialized order
            return order_queue.EnqueueResponse(success=True, message="Order enqueued successfully.")
        except Exception as e:
            return order_queue.EnqueueResponse(success=False, message=str(e))
       
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_queue_grpc.add_OrderQueueServiceServicer_to_server(OrderQueueService(), server)

    port = "50054"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started. Listening on port {port}.")

    server.wait_for_termination()

if __name__ == "__main__":
    serve()
