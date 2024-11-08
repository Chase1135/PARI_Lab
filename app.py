from socket import *

ip = '0.0.0.0'
port = 5000
server_socket = socket(AF_INET, SOCK_STREAM)

print("Binding to IP and port...", flush=True)
server_socket.bind((ip, port))
print("Bound successfully.", flush=True)

print("Listening for incoming connections...", flush=True)
server_socket.listen(1)
print("Ready to receive connections.", flush=True)
print(f"Listening on {ip}:{port}", flush=True)

print("testing the automated builds", flush=True)

while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024).decode()
    print("Received data from client: " + data, flush=True)

    client_socket.close()

    if (data == 'end'):
        break
