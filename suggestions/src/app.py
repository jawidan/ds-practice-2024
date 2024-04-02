import sys
import os

FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb/suggestions"))
sys.path.insert(0, utils_path)
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

import grpc
from concurrent import futures

class BookSuggestionService(suggestions_grpc.BookSuggestionServiceServicer):
    def SuggestBooks(self, request, context):
        # Assuming you're just echoing back the vector clock without modification
        # In a real scenario, you might update it based on some internal logic
        vector_clock = request.vector_clock
        
        # Construct the response, including the same vector clock received in the request
        response = suggestions.BookResponse(
            name="Introduction to Advanced Book Programming, by Jonathan Haddon",
            vector_clock=vector_clock
        )
        
        return response
       
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    suggestions_grpc.add_BookSuggestionServiceServicer_to_server(BookSuggestionService(), server)

    port = "50053"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started. Listening on port {port}.")

    server.wait_for_termination()

if __name__ == "__main__":
    serve()
