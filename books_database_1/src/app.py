import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
books_database_1_path = os.path.abspath(
    os.path.join(FILE, "../../../utils/pb/books_database_1")
)
books_database_2_path = os.path.abspath(
    os.path.join(FILE, "../../../utils/pb/books_database_2")
)
books_database_3_path = os.path.abspath(
    os.path.join(FILE, "../../../utils/pb/books_database_3")
)


sys.path.insert(0, books_database_1_path)
sys.path.insert(1, books_database_2_path)
sys.path.insert(2, books_database_3_path)

import books_database_1_pb2 as books_database_1
import books_database_2_pb2 as books_database_2
import books_database_3_pb2 as books_database_3
import books_database_1_pb2_grpc as books_database_1_grpc
import books_database_2_pb2_grpc as books_database_2_grpc
import books_database_3_pb2_grpc as books_database_3_grpc


import grpc
from concurrent import futures

books = [
    {
        "id": 1,
        "author": "sed",
        "category": "con",
        "copies": "culpa",
        "copiesAvailable": "inc",
        "description": "mo",
        "img": "veniam ",
        "price": 12,
        "title": "do",
    },
    {
        "id": 2,
        "author": "sed",
        "category": "con",
        "copies": "culpa",
        "copiesAvailable": "inc",
        "description": "mo",
        "img": "veniam ",
        "price": 12,
        "title": "do",
    },
]


class OrderService(books_database_1_grpc.OrderServiceServicer):
    def CreateOrder(self, request, context):
        response = books_database_1.CreateOrderResponse()
        replicate_create_order(request)

        
        print(request)
        order_id = 1 # TODO REPLACE THIS WITH DATABASE CALL
        response.id = order_id
        response.success = True
        return response

    def PrepareOrder(self, request, context):
        response = books_database_1.PrepareOrderResponse()

        result = True

        response.success = result
        return response


class BookService(books_database_1_grpc.BookServiceServicer):
    def CreateBook(self, request, context):
        response = books_database_1.CreateBookResponse()

        book_id = len(books) + 1

        books.append(
            {
                "id": book_id,
                "author": request.author,
                "category": request.category,
                "copies": request.copies,
                "copiesAvailable": request.copiesAvailable,
                "description": request.description,
                "img": request.img,
                "price": request.price,
                "title": request.title,
            }
        )

        replicate_create_book(request)

        response.id = book_id
        response.success = True
        return response

    def GetBooks(self, request, context):
        response = books_database_1.GetBooksResponse(
            books=[
                books_database_1.Book(
                    id=book.get("id"),
                    title=book.get("title"),
                    author=book.get("author"),
                    description=book.get("description"),
                    copies=book.get("copies"),
                    copiesAvailable=book.get("copiesAvailable"),
                    category=book.get("category"),
                    img=book.get("img"),
                    price=book.get("price"),
                )
                for book in books
            ]
        )
        return response


def replicate_create_order(order):
    request1 = books_database_2.CreateOrderRequest(
        user=books_database_2.User(name=order.user.name, contact=order.user.contact),
        billingAddress=books_database_2.BillingAddress(
            street=order.billingAddress.street,
            city=order.billingAddress.city,
            state=order.billingAddress.state,
            zip=order.billingAddress.zip,
            country=order.billingAddress.country,
        ),
        items=[
            books_database_2.Item(name=item.name, quantity=item.quantity)
            for item in order.items
        ],
    )
    request2 = books_database_3.CreateOrderRequest(
        user=books_database_3.User(name=order.user.name, contact=order.user.contact),
        billingAddress=books_database_3.BillingAddress(
            street=order.billingAddress.street,
            city=order.billingAddress.city,
            state=order.billingAddress.state,
            zip=order.billingAddress.zip,
            country=order.billingAddress.country,
        ),
        items=[
            books_database_3.Item(name=item.name, quantity=item.quantity)
            for item in order.items
        ],
    )
    with grpc.insecure_channel("books_database_2:50058") as channel:
        stub = books_database_2_grpc.OrderServiceStub(channel)
        stub.CreateOrder(request1)
    with grpc.insecure_channel("books_database_3:50059") as channel:
        stub = books_database_3_grpc.OrderServiceStub(channel)
        stub.CreateOrder(request2)


def replicate_create_book(order):
    request1 = books_database_2.CreateBookRequest(
        title=order.title,
        author=order.author,
        description=order.description,
        copies=order.copies,
        copiesAvailable=order.copiesAvailable,
        category=order.category,
        img=order.img,
        price=order.price,
    )
    request2 = books_database_3.CreateBookRequest(
        title=order.title,
        author=order.author,
        description=order.description,
        copies=order.copies,
        copiesAvailable=order.copiesAvailable,
        category=order.category,
        img=order.img,
        price=order.price,
    )
    with grpc.insecure_channel("books_database_2:50058") as channel:
        stub = books_database_2_grpc.BookServiceStub(channel)
        stub.CreateBook(request1)
    with grpc.insecure_channel("books_database_3:50059") as channel:
        stub = books_database_3_grpc.BookServiceStub(channel)
        stub.CreateBook(request2)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_database_1_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    books_database_1_grpc.add_BookServiceServicer_to_server(BookService(), server)
    # Adjust the port number as needed
    server.add_insecure_port("[::]:50057")
    server.start()
    print("Book Database 1 Service started. Listening on port 50057.")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
