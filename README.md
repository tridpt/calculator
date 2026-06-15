# Calculator 🧮

[![Tests](https://github.com/tridpt/calculator/actions/workflows/tests.yml/badge.svg)](https://github.com/tridpt/calculator/actions/workflows/tests.yml)
[![Build & Release](https://github.com/tridpt/calculator/actions/workflows/release.yml/badge.svg)](https://github.com/tridpt/calculator/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

Ứng dụng máy tính desktop đơn giản, viết bằng Python + tkinter.

> 🤫 Lưu ý nội bộ (đừng cho nạn nhân biết): đây là một app **troll**.
> Nhìn ngoài là máy tính bình thường (icon riêng, lịch sử, bộ nhớ, hỗ trợ
> bàn phím). Nhưng khi bấm `=`, app dẫn dụ nạn nhân qua một chuỗi popup
> "trả phí mới được tính" + minigame, rồi trả ra **kết quả sai có chủ đích**.
>
> Không lấy tiền thật, không gửi dữ liệu đi đâu. Mọi input ở form thẻ /
> OTP / mật khẩu đều bị vứt đi ngay. Chỉ để cười với bạn bè.

## Tính năng máy tính (thật)

- Giao diện dark giống Windows Calculator, có icon riêng
- Hỗ trợ bàn phím: số, `+ - * / ( )`, Enter (=), Esc (C), Backspace
- Bộ nhớ: `MC MR M+ M- MS`
- Lịch sử phép tính: bấm `≡` để mở/đóng, double-click 1 dòng để dùng lại
- Tự nhận DPI để hiển thị nét trên màn hình scaling 125%/150%

## Chuỗi troll khi bấm `=`

1. 🎰 **Vòng quay may mắn** – kim luôn dừng ở ô trượt
2. 🍪 **Đồng ý cookie** – mọi công tắc đều bật, bấm tắt thì tự bật lại; không từ chối được
3. **Giấy phép hết hạn** – báo cần kích hoạt để dùng dấu `=`
4. 🖥️ **Cập nhật driver máy tính** – quét ra "3 driver lỗi thời" vô lý, bắt cài đặt mới cho dùng
5. 🔐 **Đăng nhập** – mọi mật khẩu đều bị chê; có nút **Đăng ký** (form chê đủ kiểu, cuối cùng "tài khoản chờ duyệt 3-5 ngày"); phải bấm "Tiếp tục với tư cách khách"
6. **Chọn gói** – đồng hồ đếm ngược "ưu đãi 90%"; nút "Để sau" chạy trốn con trỏ
7. 📜 **Điều khoản dịch vụ** – phải cuộn xuống tận cuối mới đồng ý được
8. 💳 **Form thẻ** – nút "Kiểm tra số thẻ" chê đủ kiểu; lần đầu "ngân hàng từ chối"; mã giảm giá vô dụng
9. 💰 **Bảng phụ phí** – "VAT của VAT", "Phí hiển thị bảng phí này"...
10. **OTP** – cooldown 30s, bắt buộc sai 1 lần đầu
11. 📷 **Xác minh khuôn mặt** – "camera" giả, lần đầu luôn chê (cười tươi hơn, ánh sáng yếu...)
12. 👽 **Xác minh không phải người ngoài hành tinh** – hỏi vô lý, lần đầu luôn bị nghi ngờ
13. 🎮 **Minigame** (random 1 trong 9, xem bên dưới)
14. **Captcha** – câu hỏi vô lý
15. 🚌 **Captcha chọn ảnh xe buýt** – lưới 3x3 chẳng có xe buýt nào, lần đầu luôn báo sai
16. 📺 **Quảng cáo video** – nút Bỏ qua đếm ngược cứ reset 2 lần
17. ⭐ **Khảo sát** – bắt đánh giá đúng 5 sao
18. 📲 **Chia sẻ mạng xã hội** – bấm gì cũng "chia sẻ thất bại"
19. **Quảng cáo popup + thanh "đang xử lý"**
20. **Kiểm tra quyền gói** (xem bên dưới)
21. **Kết quả** – sai tinh vi (lệch nhỏ, không đổi dấu, đôi khi đúng)
22. ⏰ Sau ~90s, **phiên tự hết hạn** → lần `=` sau phải làm lại từ đầu

Mỗi lần bấm `=` còn cộng thêm "dư nợ phí dịch vụ" hiển thị ở đáy app.
Lúc mở app cũng có màn **"cập nhật bắt buộc"** chạy tới 99% rồi báo lỗi mạng.

## Minigame thử thách 🎮

Mỗi lần bấm `=` chọn ngẫu nhiên 1 game. Tất cả đều **thắng được**:

| Game | Cách thắng |
|---|---|
| 🔋 Sạc năng lượng | Bấm nút thật nhanh để pin đầy 100% (pin tự rò rỉ) |
| 🎯 Bắt cái nút | Click trúng nút chạy trốn 5 lần |
| 🔢 Đoán số bí mật | Đoán số 1–5 (gợi ý đôi khi dối); sai 3 lần được tha |
| 🔨 Đập chuột chũi | Đập đủ 8 con; hết giờ được gia hạn |
| ⌨️ Gõ câu thần chú | Gõ lại đúng câu; sai 3 lần có nút "điền giùm" |
| 🎯 Canh thời điểm | Bấm STOP khi vạch vào vùng xanh, trúng 3 lần |
| 🎵 Lặp lại giai điệu | Nhớ chuỗi ô sáng (Simon) rồi bấm lại đúng; sai 3 lần được tha |
| 🔍 Tìm ô khác biệt | Bấm ô emoji khác với 15 ô còn lại, 3 lần; bấm trượt 5 lần được tha |
| 🛸 Né chướng ngại | Dùng ◀ ▶ (hoặc phím mũi tên) né thiên thạch, sống sót 12 giây; hết mạng vẫn được tha |

> 🔊 Có thêm âm thanh "leng keng/thắng/thua" và hiệu ứng pháo giấy ăn mừng
> khi vượt qua minigame (chỉ trên Windows, im lặng an toàn trên nền tảng khác).

## Mô tả gói có tác dụng thật 😈

Mỗi gói chỉ "mở khoá" một số phép tính. Mua xong, làm hết quy trình rồi
mới bị chặn nếu dùng phép ngoài gói:

| Gói | Mở khoá | Dùng phép khác |
|---|---|---|
| Cơ Bản | (không phép nào) | chặn, đòi lên Tiêu Chuẩn |
| Tiêu Chuẩn | `+` | chặn, đòi lên Nâng Cao |
| Nâng Cao | `+ - * /` | đủ phép (nhưng kết quả vẫn sai) |
| Doanh Nghiệp | — | "kinh doanh liên hệ sau 3-5 ngày", không bao giờ tính được |

## Lối thoát an toàn

- Bỏ cuộc (hủy/đóng popup) **3 lần** → màn "🎉 ĐÂY LÀ TRÒ ĐÙA" → bấm
  "Mở chế độ máy tính thật" → từ đó `=` ra kết quả đúng, hết troll.

## Cấu trúc dự án

```
Calculator/
├── main.py              # Điểm khởi chạy (mỏng)
├── make_icon.py         # Script tạo icon
├── icon.ico / icon.png
├── pytest.ini
├── README.md
├── calc/                # Package chính
│   ├── __init__.py
│   ├── config.py        # toàn bộ text/dữ liệu troll
│   ├── platform_utils.py# DPI awareness + âm thanh beep
│   ├── core.py          # lõi máy tính (UI, bàn phím, bộ nhớ, lịch sử)
│   ├── troll.py         # chuỗi popup troll khi bấm '='
│   ├── minigames.py     # 9 minigame thử thách
│   └── app.py           # lớp Calculator ghép các mixin
└── tests/               # pytest
    ├── conftest.py
    ├── test_core.py
    ├── test_troll.py
    ├── test_config.py
    └── test_minigames.py
```

## Yêu cầu

- Python 3.8+ (đã thử trên 3.13)
- `tkinter` (đi kèm Python chuẩn trên Windows)
- `Pillow` (chỉ cần khi tạo lại icon bằng `make_icon.py`)
- `pytest` (chỉ cần khi chạy test)

## Chạy

```cmd
python main.py
```

## Chạy test

```cmd
pip install -r requirements-dev.txt
python -m pytest
```

## Kiểm tra lint (tuỳ chọn)

```cmd
ruff check .
```

CI tự chạy lint (ruff) và test (pytest trên Python 3.11–3.13) mỗi khi push
hoặc mở pull request — xem badge ở đầu README.

## Tạo lại icon (tuỳ chọn)

```cmd
pip install pillow
python make_icon.py
```

## Đóng gói thành .exe để gửi bạn bè

```cmd
pip install pyinstaller
pyinstaller --onefile --windowed --icon icon.ico --add-data "icon.ico;." --name Calculator main.py
```

File chạy: `dist\Calculator.exe` – copy đi đâu mở cũng được, không cần Python.

## Đóng góp

Xem [CONTRIBUTING.md](CONTRIBUTING.md) để biết cách chạy test, lint và gửi
pull request. Lịch sử thay đổi ở [CHANGELOG.md](CHANGELOG.md).

## Giấy phép

Phát hành theo giấy phép [MIT](LICENSE). Dùng vui vẻ, đừng troll người yếu tim 😄
