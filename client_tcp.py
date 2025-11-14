# client_tcp.py - Kết nối TCP Client
# Tác giả: Nguyễn Minh Trí

import socket
import threading
import json
from datetime import datetime

class ClientTCP:
    def __init__(self, host='127.0.0.1', port=5500):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.username = None
        self.message_callbacks = []
        
    def connect(self, username):
        """Kết nối tới server TCP"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.username = username
            self.connected = True
            
            # Gửi thông tin đăng nhập
            login_data = {
                'type': 'login',
                'username': username,
                'timestamp': datetime.now().isoformat()
            }
            self.send_message(json.dumps(login_data))
            
            # Bắt đầu thread lắng nghe tin nhắn
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Lỗi kết nối: {e}")
            return False
    
    def send_message(self, message):
        """Gửi tin nhắn tới server"""
        if self.connected and self.socket:
            try:
                message_data = {
                    'type': 'message',
                    'username': self.username,
                    'content': message,
                    'timestamp': datetime.now().isoformat()
                }
                self.socket.send(json.dumps(message_data).encode('utf-8'))
                return True
            except Exception as e:
                print(f"Lỗi gửi tin nhắn: {e}")
                return False
        return False
    
    def receive_messages(self):
        """Lắng nghe tin nhắn từ server"""
        while self.connected:
            try:
                data = self.socket.recv(1024)
                if data:
                    message = json.loads(data.decode('utf-8'))
                    self.handle_received_message(message)
                else:
                    break
            except Exception as e:
                print(f"Lỗi nhận tin nhắn: {e}")
                break
        
        self.disconnect()
    
    def handle_received_message(self, message):
        """Xử lý tin nhắn nhận được"""
        for callback in self.message_callbacks:
            callback(message)
    
    def add_message_callback(self, callback):
        """Thêm callback xử lý tin nhắn"""
        self.message_callbacks.append(callback)
    
    def disconnect(self):
        """Ngắt kết nối"""
        self.connected = False
        if self.socket:
            self.socket.close()
            self.socket = None

# Example usage:
if __name__ == "__main__":
    client = ClientTCP()
    
    def on_message_received(message):
        if message['type'] == 'message':
            print(f"[{message['timestamp']}] {message['username']}: {message['content']}")
        elif message['type'] == 'user_list':
            print(f"Users online: {', '.join(message['users'])}")
    
    client.add_message_callback(on_message_received)
    
    if client.connect("test_user"):
        print("Kết nối thành công!")
        
        # Test gửi tin nhắn
        import time
        time.sleep(1)
        client.send_message("Hello from client!")
        
        # Giữ kết nối
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            client.disconnect()
    else:
        print("Kết nối thất bại!")