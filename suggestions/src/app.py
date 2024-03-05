import sys
import os

FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(
    os.path.join(FILE, "../../../utils/pb/suggestions")
)
sys.path.insert(0, utils_path)
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

import grpc
from concurrent import futures


class BookSuggestionService(suggestions_grpc.BookSuggestionServiceServicer):

    def SuggestBooks(self, request, context):
        # Example of handling request based on 'name' parameter in 'items'
        # print("REEEEE",request)
        
        if 'python' in request.name.lower():
            response = suggestions.BookResponse(name="Automate the Boring Stuff with Python")
            return response
        elif 'javascript' in request.name.lower():
            response = suggestions.BookResponse(name="Eloquent JavaScript")
            return response

        # Default response if no specific language found in request items
        response = suggestions.BookResponse(name="No specific book suggestion found")
        return response
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    suggestions_grpc.add_BookSuggestionServiceServicer_to_server(
        BookSuggestionService(), server
    )

    port = "50053"
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started. Listening on port 50053.")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
