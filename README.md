# Client TCP - Nguyễn Minh Trí

## Phần phụ trách: Client TCP (connect, send, receive)

### Tính năng:

- Kết nối tới server TCP
- Gửi tin nhắn, nhận tin nhắn từ server
- Cập nhật danh sách user online
- Cung cấp API cho GUI (login/chat)

### Cấu trúc:

```
client_tcp/
├── client_tcp.py          # Kết nối TCP chính
├── message_handler.py     # Xử lý tin nhắn
├── user_manager.py        # Quản lý user online
└── api_handler.py         # API cho GUI
```

### Người thực hiện:

**Nguyễn Minh Trí** - Kết nối Client TCP và xử lý giao tiếp với server
