# server.py
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
import threading

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/xmlrpc',)

def convert_dollar(a):
    return a * 3

def convert_euro(a):
    return a * 3.5

def run_server():
    server = SimpleXMLRPCServer(("localhost", 5001), requestHandler=RequestHandler)
    server.register_introspection_functions()
    server.register_function(convert_dollar, 'ConvertDollar')
    server.register_function(convert_euro, 'ConvertEuro')

    print("XML-RPC server is running on port 5001")

    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
