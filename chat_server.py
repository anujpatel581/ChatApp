import socket
import threading

def handle_client(client_socket, clients):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            for c in clients:
                if c != client_socket:
                    c.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Client disconnected: {e}")
            break

    clients.remove(client_socket)
    client_socket.close()

def start_server(host='127.0.0.1', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    clients = []

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, clients))
        client_thread.start()

if __name__ == "__main__":
    start_server()
