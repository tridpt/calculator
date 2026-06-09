# Calculator 🧮

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
2. **Giấy phép hết hạn** – báo cần kích hoạt để dùng dấu `=`
3. 🖥️ **Cập nhật driver máy tính** – quét ra "3 driver lỗi thời" vô lý, bắt cài đặt mới cho dùng
4. 🔐 **Đăng nhập** – mọi mật khẩu đều bị chê; phải bấm "Tiếp tục với tư cách khách"
5. **Chọn gói** – đồng hồ đếm ngược "ưu đãi 90%"; nút "Để sau" chạy trốn con trỏ
6. 📜 **Điều khoản dịch vụ** – phải cuộn xuống tận cuối mới đồng ý được
7. 💳 **Form thẻ** – nút "Kiểm tra số thẻ" chê đủ kiểu; lần đầu "ngân hàng từ chối"; mã giảm giá vô dụng
8. 💰 **Bảng phụ phí** – "VAT của VAT", "Phí hiển thị bảng phí này"...
9. **OTP** – cooldown 30s, bắt buộc sai 1 lần đầu
10. 📷 **Xác minh khuôn mặt** – "camera" giả, lần đầu luôn chê (cười tươi hơn, ánh sáng yếu...)
11. 🎮 **Minigame** (random 1 trong 7, xem bên dưới)
12. **Captcha** – câu hỏi vô lý
13. 🚌 **Captcha chọn ảnh xe buýt** – lưới 3x3 chẳng có xe buýt nào, lần đầu luôn báo sai
14. 📺 **Quảng cáo video** – nút Bỏ qua đếm ngược cứ reset 2 lần
15. ⭐ **Khảo sát** – bắt đánh giá đúng 5 sao
16. 📲 **Chia sẻ mạng xã hội** – bấm gì cũng "chia sẻ thất bại"
17. **Quảng cáo popup + thanh "đang xử lý"**
18. **Kiểm tra quyền gói** (xem bên dưới)
19. **Kết quả** – sai tinh vi (lệch nhỏ, không đổi dấu, đôi khi đúng)
20. ⏰ Sau ~90s, **phiên tự hết hạn** → lần `=` sau phải làm lại từ đầu

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
│   ├── minigames.py     # 6 minigame thử thách
│   └── app.py           # lớp Calculator ghép các mixin
└── tests/               # pytest
    ├── conftest.py
    ├── test_core.py
    ├── test_troll.py
    └── test_config.py
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
pip install pytest
python -m pytest
```

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
