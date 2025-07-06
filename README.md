<h1 align="center"> 📩 HỆ THỐNG GỬI MAIL CÓ THỜI HẠN </h1>
 
<div align="center">

<p align="center">
  <img src="logoDaiNam.png" alt="DaiNam University Logo" width="200"/>
</p>

</div>

# 📩 Gửi mail có thời 

Đây là hệ thống gửi và nhận tài liệu bảo mật sử dụng mã hóa AES-RSA, chữ ký số và giới hạn thời gian để đảm bảo tính an toàn, toàn vẹn và xác thực của dữ liệu.

# 📝 Giới thiệu
📤 Gửi tài liệu bảo mật: Người gửi chọn file .txt và hệ thống sẽ mã hóa nội dung bằng AES-CBC, ký số bằng RSA 2048-bit, gắn thời gian sống (TTL) 24 giờ và gửi sang phía người nhận.

🔏 Xác thực & Toàn vẹn: Gói tin gửi đi chứa khóa phiên đã mã hóa, chữ ký số và hàm băm SHA-512 nhằm đảm bảo tính xác thực và toàn vẹn nội dung.

⏳ Giới hạn thời gian: Gói tin chỉ có hiệu lực trong vòng 24 giờ, sau thời gian này sẽ bị từ chối giải mã.

📥 Nhận và giải mã: Người nhận nhấn “Nhận” để giải mã file. Nếu hash, chữ ký và thời hạn hợp lệ thì sẽ giải mã thành công và lưu lại file.

📂 Quản lý file đã nhận: Tất cả các file nhận được sẽ được lưu trữ, hiển thị cùng thời gian nhận và có thể tải về hoặc xóa.

🗑️ Tự động dọn dẹp: Sau khi giải mã xong, gói tin truyền (transmission.json) sẽ tự động bị xóa để đảm bảo bảo mật.

# 🛠️ Hệ thống
![image](https://github.com/user-attachments/assets/d6675b38-f399-461a-af56-65faa6732373)

# 🔧 Công nghệ sử dụng
## 🔐 Mã hóa & Bảo mật
- AES-CBC (Advanced Encryption Standard - Cipher Block Chaining)
→ Mã hóa nội dung file nhạy cảm.

- RSA 2048-bit (PKCS#1 v1.5)
→ Trao đổi khóa phiên và ký số metadata.

- SHA-512 (Secure Hash Algorithm)
→ Kiểm tra tính toàn vẹn của gói tin.

- Chữ ký số (RSA + SHA-512)
→ Xác thực người gửi và chống giả mạo.

## 🖥️ Ngôn ngữ & Framework
- Python 3.10+

- Flask – Web framework nhẹ, xử lý backend và routing.

- HTML/CSS/JavaScript – Giao diện người dùng (UI).

- Jinja2 – Template engine của Flask (render HTML động).

## 📦 Thư viện Python chính
- pycryptodome: Mã hóa AES, RSA, ký số và băm SHA-512.

- base64, json, os, datetime: Xử lý dữ liệu và thời gian.

## 🗂️ Quản lý file
- Thư mục received_files/ – Lưu các file đã giải mã thành công.

File transmission.json – Gói tin truyền tạm thời giữa người gửi và người nhận.
# 📋 Yêu cầu hệ thống
## ⚙️ Phần cứng:
- 🖥️ Arduino, 3 đèn led, còi, cảm biến khí gas, cảm biến ánh sáng, 3 servo, đầu lọc thẻ từ
- 🔌 Cáp USB để kết nối máy tính với Arduino
## 💾 Phần mềm:
- 🐍 Python (xử lý nhận diện khuôn mặt, điều khiển cửa và thực hiện gửi thông báo)
- 🛠️ Arduino IDE (nạp code Arduino)
- 📩 Pushover (dùng để gửi thông báo) 
## 📦 Cài đặt thư viện cần thiết
```pip3 install opencv-python pyserial requests flask numpy```
# 🔌 Hướng dẫn cắm dây bảng mạch
🔐 Cắm dây đối với chức năng mở cửa khuôn mặt, cảnh báo khí gas, cảm biến ánh sáng: 

![image](https://github.com/user-attachments/assets/9b38467c-faf5-454c-b03c-c991f0fdf566)

💳 Cắm dây đối với chức năng mở cửa bằng thẻ từ RFID:
- Kết nối RFID với Arduino

![image](https://github.com/user-attachments/assets/ca694cb4-f1fd-4984-8a1b-5783add3cd02)

- Kết nối servo với Arduino

![image](https://github.com/user-attachments/assets/f1a1dfc6-2b99-4303-87ec-59e3eb19dfbc)

# 📚 Hướng dẫn cài đặt và chạy chương trình
## 🛠️ Chuẩn bị phần cứng
- 🔐 Nạp mã Arduino cho chức năng mở cửa bằng khuôn mặt, cảnh báo khí gas, cảm biến ánh sáng:
  + Mở file FaceGasLightControl.ino bằng Arduino IDE
  + Kết nối board Arduino với máy tính
  + Chạy nạp mã nguồn vào board
  + Đảm bảo chạy cổng COM8 để phù hợp với mã trong file face_recognition_with_web.py
- 💳 Nạp mã Arduino cho chức năng mở cửa bằng thẻ từ:
  + Mở file RFIDDoor.ino bằng Arduino IDE
  + Kết nối board Arduino với máy tính
  + Chạy nạp mã nguồn vào board
## 🐍 Cài đặt python
Cài đặt python về máy và cài các thư viện phía trên bằng pip
## 📱 Cài đặt và đăng ký ứng dụng pushover
- Cài đặt ứng dụng về máy điện thoại bằng AppStore hoặc CH Play
- Đăng ký tài khoản trên pushover để lấy key sử dụng
## 🚀 Các bước chạy chương trình
- Bước 1: Chạy file capture_faces.py để thiết lập khuôn mặt và lưu hình ảnh vào folder data_set (python capture_faces.py). Ứng dụng sẽ chạy sau đó camera máy tính mở lên, bạn cần nhập tên người dùng vào terminal sau đó enter để camera chụp lại khuôn mặt của bạn và lưu vào folder data_set.
- Bước 2: Chạy file train_faces.py để training chương trình sau khi lưu xong khuôn mặt (python train_faces.py).
- Bước 3: Chạy file face_recognition_with_web.py để sử dụng chức năng nhận diện khuôn mặt và thông báo khí gas (python face_recognition_with_web.py).
# 📘 Hướng dẫn sử dụng 
## 🔐 Nhận diện khuôn mặt mở cửa: 
- Người dùng đưa khuôn mặt vào camera để nhận diện.
- Nếu nhận diện đúng với khuôn mặt đã lưu cửa sẽ tự động mở ra.
- Sai khuôn mặt sẽ hiển cảnh báo đồng thời cửa sẽ không mở.
## 💳 Quét thẻ từ mở cửa:
- Người dùng đưa thẻ từ vào quét.
- Nếu đúng mã thẻ cửa sẽ mở.
- Sai mã thẻ sẽ không mở cửa.
- Nếu cửa đang mở chờ hết 1 phút cửa sẽ tự động đóng.
## ⛽ Cảnh báo khí gas:
- Sử dụng bật lửa xì gas vào cảm biến.
- Cảm biến phát hiện khí gas còi sẽ kêu, đèn nhấp nháy, cửa sổ mở và thông báo qua pushover.
## 💡 Cảm biến ánh sáng bật đèn:
- Chỉ cần lấy tay che toàn bộ cảm biến hoặc để cảm biến vào nơi thiếu ánh sáng.
- Đèn sẽ tự động bật.
# 🖼️ Poster
![Poster_CNTT5_ThanhNguyen](https://github.com/user-attachments/assets/88c03204-924c-4363-b59b-c254b1a99b39)
