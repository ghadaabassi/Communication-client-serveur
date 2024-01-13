import socket
import threading

def process_request(method, params):
    if method == "ConvertDollar":
        return params.get("a", 0) * 3
    if method == "ConvertEuro":
        return params.get("a", 0) * 3.5

def handle_client(client_socket, addr):
    print("Accepted connection from", addr)

    data = client_socket.recv(1024).decode()
    print("Received data:", data)

    method, params = data.split(";")
    params = int(params)

    result = process_request(method, {"a": params})

    client_socket.send(str(result).encode())
    client_socket.close()

def run_socket_server():
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(("localhost", 5556))
    socket_server.listen(1)
   
    while True:
        client_socket, addr = socket_server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()


