Ứng dụng Bảo mật Tin nhắn Âm thanh với Mã hóa DES và Xác thực RSA
Giới thiệu Trang web
Ứng dụng Bảo mật Tin nhắn Âm thanh là một dự án phát triển trong khuôn khổ học phần Nhập môn An toàn, Bảo mật Thông tin, nhằm xây dựng một hệ thống chat âm thanh an toàn sử dụng kết nối P2P (Peer-to-Peer). Trang web cho phép người dùng ghi âm, gửi và nhận tin nhắn âm thanh với các tính năng bảo mật sau:


Mã hóa dữ liệu: Sử dụng thuật toán DES (chế độ CBC) để mã hóa tin nhắn âm thanh, đảm bảo tính bí mật trong quá trình truyền tải.
Xác thực người dùng: Sử dụng RSA 2048-bit với OAEP và SHA-256 để ký số metadata và mã hóa khóa DES, đảm bảo chỉ người dùng hợp lệ có thể gửi/nhận dữ liệu.
Kiểm tra toàn vẹn: Sử dụng SHA-256 để tạo giá trị băm, giúp phát hiện bất kỳ thay đổi hoặc giả mạo nào trong dữ liệu.
Hệ thống bao gồm:

Giao diện người dùng: Được xây dựng bằng HTML (index.html), cung cấp giao diện thân thiện để ghi âm, gửi tin nhắn, và theo dõi trạng thái kết nối.
Máy chủ tín hiệu: Được viết bằng Python (signaling_server.py), sử dụng thư viện websockets để quản lý kết nối WebSocket và hỗ trợ thiết lập kênh P2P qua WebRTC (giả định).
Kênh P2P: Sử dụng WebRTC để truyền dữ liệu âm thanh trực tiếp giữa các client, giảm thiểu sự phụ thuộc vào máy chủ trung gian.
Trang web được thiết kế để chạy trên môi trường cục bộ (localhost), phù hợp cho mục đích thử nghiệm và học tập. Hệ thống đảm bảo tính bảo mật, xác thực, và toàn vẹn của tin nhắn âm thanh theo các yêu cầu của đề tài.
![image](https://github.com/user-attachments/assets/1b11b0f9-e795-4ed2-bcf5-67932b9c55b7)

Tính năng Chính
Ghi âm và gửi tin nhắn thoại: Người dùng có thể ghi âm thông qua nút “Bắt đầu Ghi âm” và gửi tin nhắn âm thanh mã hóa qua kênh P2P.
Hiển thị trạng thái kết nối: Giao diện hiển thị trạng thái như “Chưa kết nối Server”, “Chưa trao đổi khóa”, hoặc “Chưa có kênh P2P”.
Hộp thư đến: Hiển thị danh sách tin nhắn âm thanh nhận được (hiện tại: “Chưa có tin nhắn nào...”).
Log hệ thống: Cung cấp thông tin chi tiết về trạng thái và lỗi để hỗ trợ gỡ lỗi.

![image](https://github.com/user-attachments/assets/db8248ac-d57a-474f-8ac4-a50263946e0a)

Bảo mật:
Mã hóa tin nhắn bằng DES (CBC mode).
Xác thực người dùng qua chữ ký RSA và trao đổi khóa an toàn.
Kiểm tra toàn vẹn dữ liệu bằng hash SHA-256.
Công nghệ Sử dụng
Frontend: HTML, JavaScript (giả định sử dụng Web Audio API và Web Crypto API).
Backend: Python với thư viện websockets và asyncio.
Giao thức: WebSocket (cho tín hiệu), WebRTC (cho kênh P2P).
Bảo mật: DES (CBC mode), RSA 2048-bit (OAEP + SHA-256), SHA-256.
Cách Sử dụng
Dưới đây là hướng dẫn chi tiết để cài đặt và chạy ứng dụng trên máy tính cục bộ.

1. Yêu cầu Hệ thống
Hệ điều hành: Windows, macOS, hoặc Linux.
Python: Phiên bản 3.8 trở lên.
Trình duyệt: Chrome, Firefox, hoặc bất kỳ trình duyệt hỗ trợ Web Audio API và WebRTC.
Thư viện Python:
websockets: Để chạy máy chủ tín hiệu.
asyncio: Để xử lý kết nối bất đồng bộ.
Công cụ (khuyến nghị):
Visual Studio Code để chỉnh sửa mã nguồn.
Git để clone repository.
2. Cài đặt
Clone Repository:
git clone https://github.com/[your-username]/[your-repo].git
cd [your-repo]
Cài đặt Thư viện Python:
pip install websockets
Cấu trúc thư mục:
index.html: Giao diện người dùng.
signaling_server.py: Máy chủ tín hiệu.
(Giả định) app.js: File JavaScript xử lý logic bảo mật (DES, RSA, SHA-256) và WebRTC.
3. Chạy Ứng dụng
Khởi động Máy chủ Tín hiệu:
python signaling_server.py
Máy chủ sẽ chạy trên ws://localhost:8765.
Log hệ thống sẽ hiển thị các sự kiện như đăng ký client, chuyển tiếp tin nhắn, hoặc lỗi.
Mở Giao diện Người dùng:
Mở file index.html trong trình duyệt (khuyến nghị Chrome).
Hoặc triển khai trên một web server cục bộ:
python -m http.server 8000
Truy cập http://localhost:8000 để sử dụng giao diện.
Sử dụng Ứng dụng:
Kết nối: Nhấn nút “Thiết lập Kênh Bảo mật” để đăng ký client và thiết lập kênh P2P.
Ghi âm: Nhấn “Bắt đầu Ghi âm” để thu âm thanh, sau đó mã hóa và gửi qua kênh P2P.
Nhận tin nhắn: Tin nhắn nhận được sẽ hiển thị trong “Hộp thư đến” (yêu cầu tích hợp JavaScript).
Theo dõi trạng thái: Kiểm tra trạng thái kết nối và log hệ thống để phát hiện lỗi.
4. Quy trình Bảo mật
Bắt tay (Handshake):
Client A gửi “Hello!” qua máy chủ tín hiệu, Client B phản hồi “Ready!”.
Trao đổi khóa công khai RSA qua kênh P2P.
Xác thực và Trao đổi Khóa:
Client A ký số metadata (định danh, thời gian) bằng RSA và gửi khóa DES mã hóa.
Truyền Dữ liệu:
Tin nhắn âm thanh được mã hóa bằng DES (CBC mode), tạo hash SHA-256, và gửi qua kênh P2P.
Kiểm tra Toàn vẹn:
Client B kiểm tra chữ ký RSA và hash SHA-256, giải mã dữ liệu nếu hợp lệ.
5. Lưu ý
Ứng dụng hiện chạy trong môi trường cục bộ, cần thử nghiệm trên mạng diện rộng để đánh giá hiệu suất thực tế.
Mã JavaScript xử lý bảo mật (DES, RSA, SHA-256) chưa được cung cấp, cần tích hợp thêm.
Đảm bảo trình duyệt hỗ trợ WebRTC và Web Audio API.
Cài đặt và Chạy Thử nghiệm
Chạy thử nghiệm:
Gửi file âm thanh nhỏ (1MB) và lớn (10MB) để đo thời gian mã hóa, truyền tải, và giải mã.
Kiểm tra lỗi như timeout đăng ký hoặc không tìm thấy người nhận.
Kết quả dự kiến (giả định):
File 1MB: Mã hóa ~0.5s, truyền tải ~1s, giải mã ~0.4s.
File 10MB: Mã hóa ~4s, truyền tải ~8s, giải mã ~3.5s.
Kiểm tra toàn vẹn:
Dữ liệu giải mã giống dữ liệu gốc.
Hash SHA-256 đảm bảo không có thay đổi trong quá trình truyền tải.
Hạn chế
DES (khóa 56-bit) có độ bảo mật thấp, dễ bị tấn công brute-force.
Giao diện HTML thiếu logic JavaScript để xử lý ghi âm và bảo mật.
Máy chủ tín hiệu chưa có cơ chế xác thực client.
