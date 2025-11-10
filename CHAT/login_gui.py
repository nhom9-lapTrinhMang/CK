# login_gui.py
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App - Đăng nhập")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Căn giữa cửa sổ
        self.center_window()
        
        # Tạo giao diện
        self.create_widgets()
    
    def center_window(self):
        # Căn giữa cửa sổ trên màn hình
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        # Frame chính
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Tiêu đề
        title_label = tk.Label(main_frame, text="CHAT APPLICATION", 
                              font=('Arial', 18, 'bold'), 
                              bg='white', fg='#2E86AB')
        title_label.pack(pady=(0, 30))
        
        # Frame đăng nhập
        login_frame = tk.Frame(main_frame, bg='white')
        login_frame.pack(pady=20)
        
        # Username
        username_label = tk.Label(login_frame, text="Username:", 
                                 font=('Arial', 12), 
                                 bg='white', fg='#333')
        username_label.pack(pady=(0, 5))
        
        self.username_entry = tk.Entry(login_frame, 
                                      font=('Arial', 12), 
                                      width=25, 
                                      relief=tk.RAISED,
                                      bd=1)
        self.username_entry.pack(pady=(0, 20))
        
        # Nút đăng nhập
        login_button = tk.Button(login_frame, 
                                text="Đăng nhập", 
                                font=('Arial', 12, 'bold'),
                                bg='#2E86AB', 
                                fg='white',
                                width=20,
                                height=2,
                                cursor='hand2',
                                command=self.login)
        login_button.pack(pady=10)
        
        # Bind Enter key
        self.username_entry.bind('<Return>', lambda event: self.login())
        
        # Focus vào ô username
        self.username_entry.focus()
    
    def login(self):
        username = self.username_entry.get().strip()
        
        if not username:
            messagebox.showerror("Lỗi", "Vui lòng nhập username!")
            return
        
        if len(username) < 3:
            messagebox.showerror("Lỗi", "Username phải có ít nhất 3 ký tự!")
            return
        
        # Kiểm tra ký tự đặc biệt
        if not username.replace('_', '').isalnum():
            messagebox.showerror("Lỗi", "Username chỉ được chứa chữ, số và dấu gạch dưới!")
            return
        
        # Lưu username và mở chat GUI
        try:
            # Đóng cửa sổ đăng nhập
            self.root.destroy()
            
            # Khởi động chat GUI với username
            subprocess.run([sys.executable, 'chat_gui.py', username])
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể khởi động chat: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginGUI(root)
    root.mainloop()