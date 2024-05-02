import json
import sys
import os
import queue

FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb/order_executor"))
sys.path.insert(0, utils_path)

import grpc
from concurrent import futures


import order_executor_pb2 as oe_pb2
import order_executor_pb2_grpc as oe_pb2_grpc

class OrderExecutorService(oe_pb2_grpc.OrderExecutorServiceServicer):
    def DequeueOrder(self, request, context):
        print("Order is being executed…")
        return oe_pb2.DequeueResponse(message="Order is being executed...")
       
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    oe_pb2_grpc.add_OrderExecutorServiceServicer_to_server(OrderExecutorService(), server)

    port = "50055"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started. Listening on port {port}.")

    server.wait_for_termination()

if __name__ == "__main__":
    serve()
