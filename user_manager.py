# user_manager.py - Quản lý danh sách user online
# Tác giả: Nguyễn Minh Trí

from typing import List, Dict
import json

class UserManager:
    def __init__(self):
        self.online_users: List[str] = []
        self.user_info: Dict[str, dict] = {}
        self.current_user: str = None
        
    def set_current_user(self, username: str):
        """Set user hiện tại"""
        self.current_user = username
        
    def update_user_list(self, users: List[str]):
        """Cập nhật danh sách user online"""
        self.online_users = users.copy()
        
    def add_user(self, username: str, user_info: dict = None):
        """Thêm user vào danh sách online"""
        if username not in self.online_users:
            self.online_users.append(username)
            
        if user_info:
            self.user_info[username] = user_info
            
    def remove_user(self, username: str):
        """Xóa user khỏi danh sách online"""
        if username in self.online_users:
            self.online_users.remove(username)
            
        if username in self.user_info:
            del self.user_info[username]
            
    def get_online_users(self) -> List[str]:
        """Lấy danh sách user online"""
        return self.online_users.copy()
    
    def get_user_count(self) -> int:
        """Lấy số lượng user online"""
        return len(self.online_users)
    
    def is_user_online(self, username: str) -> bool:
        """Kiểm tra user có online không"""
        return username in self.online_users
    
    def get_user_info(self, username: str) -> dict:
        """Lấy thông tin user"""
        return self.user_info.get(username, {})
    
    def process_user_update(self, message: dict):
        """Xử lý cập nhật user từ server"""
        if message.get('type') == 'user_joined':
            username = message.get('username')
            if username:
                self.add_user(username, message.get('user_info', {}))
                print(f"User {username} đã tham gia")
                
        elif message.get('type') == 'user_left':
            username = message.get('username')
            if username:
                self.remove_user(username)
                print(f"User {username} đã rời khỏi")
                
        elif message.get('type') == 'user_list':
            users = message.get('users', [])
            self.update_user_list(users)
            print(f"Danh sách user online: {', '.join(users)}")
            
    def create_user_status_message(self, status: str = "online") -> str:
        """Tạo tin nhắn trạng thái user"""
        message = {
            'type': 'user_status',
            'username': self.current_user,
            'status': status,
            'timestamp': None  # sẽ được thêm bởi message_handler
        }
        return json.dumps(message)
    
    def get_formatted_user_list(self) -> str:
        """Lấy danh sách user định dạng để hiển thị"""
        if not self.online_users:
            return "Không có user nào online"
            
        user_list = []
        for user in self.online_users:
            if user == self.current_user:
                user_list.append(f"{user} (bạn)")
            else:
                user_list.append(user)
                
        return f"Users online ({len(self.online_users)}): {', '.join(user_list)}"