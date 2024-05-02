import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/books_database_2'))
sys.path.insert(0, utils_path)
import books_database_2_pb2 as books_database_2
import books_database_2_pb2_grpc as books_database_2_grpc


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

class OrderService(books_database_2_grpc.OrderServiceServicer):
    def CreateOrder(self, request, context):
        response = books_database_2.CreateOrderResponse()

        order_id = 1

        response.id = order_id
        response.success = True
        return response
    

class BookService(books_database_2_grpc.BookServiceServicer):
    def CreateBook(self, request, context):
        response = books_database_2.CreateBookResponse()

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

        response.id = book_id
        response.success = True
        return response
    
    def GetBooks(self, request, context):
        response = books_database_2.GetBooksResponse()

        books = []

        response.books = books
        return response
    
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_database_2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    books_database_2_grpc.add_BookServiceServicer_to_server(BookService(), server)
    # Adjust the port number as needed
    server.add_insecure_port('[::]:50058')
    server.start()
    print("Book Database 2 Service started. Listening on port 50058.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
