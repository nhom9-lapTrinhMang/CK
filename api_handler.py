# api_handler.py - API cho GUI (login/chat)  
# Tác giả: Nguyễn Minh Trí

import threading
import time
from typing import Optional, Callable
from client_tcp import ClientTCP
from message_handler import MessageHandler
from user_manager import UserManager

class APIHandler:
    def __init__(self):
        self.client = ClientTCP()
        self.message_handler = MessageHandler()
        self.user_manager = UserManager()
        
        # Callbacks cho GUI
        self.on_message_received: Optional[Callable] = None
        self.on_user_list_updated: Optional[Callable] = None
        self.on_connection_status_changed: Optional[Callable] = None
        
        # Kết nối message handler với client
        self.client.add_message_callback(self._handle_server_message)
        
        # Kết nối message handler với user manager
        self.message_handler.add_callback(self.user_manager.process_user_update)
        
    def set_message_callback(self, callback: Callable):
        """Set callback cho tin nhắn mới"""
        self.on_message_received = callback
        
    def set_user_list_callback(self, callback: Callable):
        """Set callback cho cập nhật danh sách user"""
        self.on_user_list_updated = callback
        
    def set_connection_callback(self, callback: Callable):
        """Set callback cho thay đổi trạng thái kết nối"""
        self.on_connection_status_changed = callback
    
    def login(self, username: str, host: str = '127.0.0.1', port: int = 5500) -> bool:
        """Đăng nhập và kết nối server"""
        try:
            # Cập nhật thông tin kết nối
            self.client.host = host
            self.client.port = port
            self.user_manager.set_current_user(username)
            
            # Thử kết nối
            success = self.client.connect(username)
            
            if success:
                if self.on_connection_status_changed:
                    self.on_connection_status_changed("connected")
                return True
            else:
                if self.on_connection_status_changed:
                    self.on_connection_status_changed("failed")
                return False
                
        except Exception as e:
            print(f"Lỗi đăng nhập: {e}")
            if self.on_connection_status_changed:
                self.on_connection_status_changed("error")
            return False
    
    def send_message(self, content: str) -> bool:
        """Gửi tin nhắn"""
        if not self.client.connected:
            return False
            
        # Tạo tin nhắn định dạng
        message = self.message_handler.create_message(
            content, 
            self.user_manager.current_user
        )
        
        return self.client.send_message(message)
    
    def get_message_history(self, limit: int = 50) -> list:
        """Lấy lịch sử tin nhắn"""
        return self.message_handler.get_history(limit)
    
    def get_online_users(self) -> list:
        """Lấy danh sách user online"""
        return self.user_manager.get_online_users()
    
    def get_user_count(self) -> int:
        """Lấy số lượng user online"""
        return self.user_manager.get_user_count()
    
    def disconnect(self):
        """Ngắt kết nối"""
        if self.client.connected:
            # Gửi thông báo offline trước khi ngắt kết nối
            offline_message = self.user_manager.create_user_status_message("offline")
            self.client.send_message(offline_message)
            
            time.sleep(0.1)  # Đợi tin nhắn được gửi
            
        self.client.disconnect()
        
        if self.on_connection_status_changed:
            self.on_connection_status_changed("disconnected")
    
    def _handle_server_message(self, raw_message: str):
        """Xử lý tin nhắn từ server (callback internal)"""
        message = self.message_handler.process_message(raw_message)
        
        if message:
            # Xử lý tin nhắn chat
            if message.get('type') == 'message' and self.on_message_received:
                self.on_message_received(message)
            
            # Xử lý cập nhật danh sách user
            elif message.get('type') in ['user_joined', 'user_left', 'user_list']:
                if self.on_user_list_updated:
                    self.on_user_list_updated(self.user_manager.get_online_users())
    
    def is_connected(self) -> bool:
        """Kiểm tra trạng thái kết nối"""
        return self.client.connected
    
    def get_current_user(self) -> str:
        """Lấy username hiện tại"""
        return self.user_manager.current_user

# Example usage cho GUI:
if __name__ == "__main__":
    api = APIHandler()
    
    def on_new_message(message):
        formatted = api.message_handler.format_message_for_display(message)
        print(formatted)
    
    def on_users_updated(users):
        print(f"Users online: {', '.join(users)}")
    
    def on_status_changed(status):
        print(f"Connection status: {status}")
    
    # Đăng ký callbacks
    api.set_message_callback(on_new_message)
    api.set_user_list_callback(on_users_updated)
    api.set_connection_callback(on_status_changed)
    
    # Test đăng nhập
    if api.login("test_user"):
        print("Đăng nhập thành công!")
        
        # Test gửi tin nhắn
        time.sleep(1)
        api.send_message("Hello from API!")
        
        # Giữ chương trình chạy
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            api.disconnect()
            print("Đã ngắt kết nối!")
    else:
        print("Đăng nhập thất bại!")