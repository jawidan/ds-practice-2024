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
from openai import OpenAI


class BookSuggestionService(suggestions_grpc.BookSuggestionServiceServicer):

    def SuggestBooks(self, request, context):
        # Example of handling request based on 'name' parameter in 'items'
        # print("REEEEE",request)
        client = OpenAI(api_key="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")

        gptresponse = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt="Suggest books which is relevant to " + request.name + ". And only respond the book name and author. thats it",
        )   

        return suggestions.BookResponse(name=gptresponse.choices[0].text)
       
        

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
