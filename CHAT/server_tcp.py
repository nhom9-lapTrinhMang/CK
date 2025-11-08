# server_tcp.py
import socket
import threading

# Cấu hình server
HOST = '127.0.0.1'
PORT = 5500

# Tạo socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []  # Danh sách client đang online
usernames = {}  # Lưu username theo socket

print(f"Server đang chạy tại {HOST}:{PORT}")

# Gửi tin nhắn đến tất cả client khác
def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

# Xử lý client
def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break
            print("Nhận:", msg.decode('utf-8'))
            broadcast(msg, client)
        except:
            break
    # Khi client thoát
    print("Client đã ngắt kết nối.")
    if client in clients:
        clients.remove(client)
    client.close()

# Chấp nhận client mới
while True:
    client, addr = server.accept()
    print(f"Client {addr} đã kết nối.")
    clients.append(client)
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
