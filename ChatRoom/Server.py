import socket
import threading

clients = []
username_counter = 1  

def handle_client(client_socket, client_address):
    global username_counter
    username = f"user #{username_counter}"
    username_counter += 1  
    
    print(f"New connection: {client_address} with username {username}")
    
    clients.append((client_socket, username))#List the users.
    broadcast(f"{username}:  joined the chat", client_socket)
    while True:
        try:
            message = client_socket.recv(1024).decode()
          
            print(f"{username}: {message}")
            broadcast(f"{username}: {message}", client_socket)

        except:
            broadcast(f"{username}: Left the chat", client_socket)
            clients.remove((client_socket, username))
            client_socket.close()
            break

def broadcast(message, sender_socket):
    for client_socket, _ in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                clients.remove((client_socket, _))
                client_socket.close()
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('xx.xxx.xxx.x', 12345))
    server_socket.listen(5)
    print("Server is listening for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.daemon = True
        thread.start()          

if __name__ == "__main__":
    start_server()
