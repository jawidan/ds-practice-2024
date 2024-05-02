import sys
import os

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment_system'))
sys.path.insert(0, utils_path)
import payment_system_pb2 as payment_system
import payment_system_pb2_grpc as payment_system_grpc


import grpc
from concurrent import futures


class PaymentService(payment_system_grpc.PaymentServiceServicer):
    def CheckBalance(self, request, context):
        balance_exists = True

        return payment_system.CheckBalanceResponse(success=balance_exists)
    
    def ConfirmPayment(self, request, context):

        payment_result = True

        return payment_system.CheckBalanceResponse(success=payment_result)
    
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payment_system_grpc.add_PaymentServiceServicer_to_server(PaymentService(), server)
    server.add_insecure_port('[::]:50060')
    server.start()
    print("Payment Service started. Listening on port 50060.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
