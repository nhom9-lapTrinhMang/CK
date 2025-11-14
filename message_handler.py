# message_handler.py - Xử lý tin nhắn
# Tác giả: Nguyễn Minh Trí

import json
from datetime import datetime
from typing import List, Callable

class MessageHandler:
    def __init__(self):
        self.message_history: List[dict] = []
        self.callbacks: List[Callable] = []
        
    def add_callback(self, callback: Callable):
        """Thêm callback xử lý tin nhắn"""
        self.callbacks.append(callback)
        
    def remove_callback(self, callback: Callable):
        """Xóa callback"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def process_message(self, raw_message: str) -> dict:
        """Xử lý tin nhắn thô từ server"""
        try:
            message = json.loads(raw_message)
            
            # Thêm thông tin bổ sung
            if 'timestamp' not in message:
                message['timestamp'] = datetime.now().isoformat()
                
            # Lưu vào lịch sử
            self.message_history.append(message)
            
            # Gọi tất cả callbacks
            for callback in self.callbacks:
                try:
                    callback(message)
                except Exception as e:
                    print(f"Lỗi callback: {e}")
                    
            return message
            
        except json.JSONDecodeError:
            print(f"Lỗi decode JSON: {raw_message}")
            return None
    
    def create_message(self, content: str, username: str, msg_type: str = "text") -> str:
        """Tạo tin nhắn để gửi"""
        message = {
            'type': 'message',
            'content': content,
            'username': username,
            'message_type': msg_type,
            'timestamp': datetime.now().isoformat()
        }
        return json.dumps(message)
    
    def get_history(self, limit: int = 50) -> List[dict]:
        """Lấy lịch sử tin nhắn"""
        return self.message_history[-limit:]
    
    def clear_history(self):
        """Xóa lịch sử tin nhắn"""
        self.message_history.clear()
        
    def format_message_for_display(self, message: dict) -> str:
        """Format tin nhắn để hiển thị"""
        timestamp = message.get('timestamp', '')
        username = message.get('username', 'Unknown')
        content = message.get('content', '')
        
        # Format timestamp
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime('%H:%M:%S')
            except:
                time_str = timestamp[:8]  # fallback
        else:
            time_str = datetime.now().strftime('%H:%M:%S')
            
        return f"[{time_str}] {username}: {content}"