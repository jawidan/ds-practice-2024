import json
import sys
import os
import queue

FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb/order_queue"))
payment_system_path = os.path.abspath(
    os.path.join(FILE, "../../../utils/pb/payment_system")
)
books_database_1_path = os.path.abspath(
    os.path.join(FILE, "../../../utils/pb/books_database_1")
)
sys.path.insert(0, utils_path)
sys.path.insert(1, payment_system_path)
sys.path.insert(2, books_database_1_path)

import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

import payment_system_pb2 as payment_system
import payment_system_pb2_grpc as payment_system_grpc

import books_database_1_pb2 as books_database_1
import books_database_1_pb2_grpc as books_database_1_grpc

import grpc
from concurrent import futures

# Define a global order queue. In a production environment, consider using a more robust queue or storage.
orders_queue = queue.Queue()


def check_balance(amount, creditCard):
    with grpc.insecure_channel(
        "payment_system:50060"
    ) as channel:  # Adjust the address as needed
        stub = payment_system_grpc.PaymentServiceStub(channel)
        order_request = payment_system.CheckBalanceRequest(
            amount=amount,
            card=payment_system.CreditCard(
                number=creditCard["number"],
                expirationDate=creditCard["expirationDate"],
                cvv=creditCard["cvv"],
            ),
        )
        response = stub.CheckBalance(order_request)
        return response


def confirm_payment(amount, creditCard):
    with grpc.insecure_channel("payment_system:50060") as channel:
        stub = payment_system_grpc.PaymentServiceStub(channel)
        order_request = payment_system.ConfirmPaymentRequest(
            amount=amount,
            card=payment_system.CreditCard(
                number=creditCard["number"],
                expirationDate=creditCard["expirationDate"],
                cvv=creditCard["cvv"],
            ),
        )
        response = stub.ConfirmPayment(order_request)
        return response


def prepare_order(order):
    with grpc.insecure_channel(
        "books_database_1:50057"
    ) as channel:  # Adjust the address as needed
        stub = books_database_1_grpc.OrderServiceStub(channel)
        order_request = books_database_1.PrepareOrderRequest(
            user=order["user"],
            items=[
                books_database_1.Item(name=item["name"], quantity=item["quantity"])
                for item in order["items"]
            ],
            billingAddress=order["billingAddress"],
        )
        response = stub.PrepareOrder(order_request)
        return response


def create_order(order):
    with grpc.insecure_channel("books_database_1:50057") as channel:
        stub = books_database_1_grpc.OrderServiceStub(channel)
        order_request = books_database_1.CreateOrderRequest(
            user=order["user"],
            items=[
                books_database_1.Item(name=item["name"], quantity=item["quantity"])
                for item in order["items"]
            ],
            billingAddress=order["billingAddress"],
        )
        response = stub.CreateOrder(order_request)
        return response


class OrderQueueService(order_queue_grpc.OrderQueueServiceServicer):
    def EnqueueOrder(self, request, context):
        # Assuming 'request' contains order details, and we're serializing and enqueueing it.
        # You might choose to store the order in a different format or structure.
        try:
            order_details = {
                "user": {"name": request.user.name, "contact": request.user.contact},
                "creditCard": {
                    "number": request.creditCard.number,
                    "expirationDate": request.creditCard.expirationDate,
                    "cvv": request.creditCard.cvv,
                },
                "userComment": request.userComment,
                "billingAddress": {
                    "city": request.billingAddress.city,
                    "country": request.billingAddress.country,
                    "state": request.billingAddress.state,
                    "street": request.billingAddress.street,
                    "zip": request.billingAddress.zip,
                },
                "items": [
                    {"quantity": item.quantity, "name": item.name}
                    for item in request.items
                ],
                # Additional fields as required
            }
            # Convert order_details to string for queueing. Consider a more structured approach for production.

            prepare_order_result = prepare_order(order_details)

            if not prepare_order_result.success:
                raise Exception("Order cannot be prepared")

            check_balance_result = check_balance(25, order_details["creditCard"])

            if not check_balance_result.success:
                raise Exception("Balance is not enough")

            create_order_result = create_order(order_details)

            if not create_order_result.success:
                raise Exception("Order cannot be created")

            confirm_payment_result = confirm_payment(25, order_details["creditCard"])

            if not confirm_payment_result.success:
                raise Exception("Payment not successful")

            order_string = json.dumps(order_details)
            orders_queue.put(order_string)  # Enqueue the serialized order
            return order_queue.EnqueueResponse(
                success=True, message="Order enqueued successfully."
            )
        except Exception as e:
            return order_queue.EnqueueResponse(success=False, message=str(e))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_queue_grpc.add_OrderQueueServiceServicer_to_server(
        OrderQueueService(), server
    )

    port = "50054"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started. Listening on port {port}.")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
