# Calculator 🧮

Ứng dụng máy tính desktop đơn giản, viết bằng Python + tkinter.

> 🤫 Lưu ý nội bộ (đừng cho nạn nhân biết): đây là một app **troll**.
> Nhìn ngoài là máy tính bình thường (có icon, lịch sử, memory, hỗ trợ
> bàn phím). Nhưng khi bấm `=`, app dẫn dụ nạn nhân qua một chuỗi popup
> "trả phí mới được tính", rồi cuối cùng trả ra **kết quả sai có chủ đích**.
>
> Không lấy tiền thật, không gửi dữ liệu đi đâu. Mọi input ở form thẻ /
> OTP đều bị vứt đi. Chỉ để cười với bạn bè.

## Tính năng máy tính (thật)

- Giao diện dark giống Windows Calculator, có icon riêng
- Hỗ trợ bàn phím: số, `+ - * / ( )`, Enter (=), Esc (C), Backspace
- Bộ nhớ: `MC MR M+ M- MS`
- Lịch sử phép tính: bấm `≡` để mở/đóng, double-click 1 dòng để dùng lại

## Chuỗi troll khi bấm `=`

1. 🎰 **Vòng quay may mắn** – "quay trúng 1 phép tính miễn phí", nhưng kim luôn dừng ở ô trượt
2. **Giấy phép hết hạn** – báo cần kích hoạt để dùng dấu `=`
3. **Chọn gói** – kèm đồng hồ đếm ngược "ưu đãi 90%", hết giờ thì "giá x10"
4. **Form thẻ + mã giảm giá** – nhập gì cũng được, lần đầu "ngân hàng từ chối"; mã giảm giá toàn vô dụng
5. 💰 **Bảng phụ phí** – "Phí xử lý", "VAT của VAT", "Phí hiển thị bảng phí này"...
6. **OTP** – cooldown 30s, bắt buộc sai 1 lần đầu
7. **Captcha** – câu hỏi vô lý
8. 📋 **Khảo sát** – bắt đánh giá đúng 5 sao mới cho qua
9. **Quảng cáo + thanh "đang xử lý"** với mấy dòng nhảm
10. **Kết quả** – sai có chủ đích (lệch ±1, đổi dấu, hoặc làm tròn lệch)
11. ⏰ Sau ~90s, **phiên tự hết hạn** → lần `=` sau phải làm lại từ đầu

## Mô tả gói có tác dụng thật 😈

Mỗi gói chỉ "mở khoá" một số phép tính. Mua xong, làm hết quy trình rồi
mới bị chặn nếu dùng phép ngoài gói:

| Gói | Mở khoá | Dùng phép khác |
|---|---|---|
| Cơ Bản | (không phép nào) | chặn, đòi lên Tiêu Chuẩn |
| Tiêu Chuẩn | `+` | chặn, đòi lên Nâng Cao |
| Nâng Cao | `+ - * /` | đủ phép (nhưng kết quả vẫn sai) |
| Doanh Nghiệp | — | "kinh doanh liên hệ sau 3-5 ngày", không bao giờ tính được |

## Yêu cầu

- Python 3.8+ (đã thử trên 3.13)
- `tkinter` (đi kèm Python chuẩn trên Windows)
- `Pillow` (chỉ cần khi muốn tạo lại icon bằng `make_icon.py`)

## Chạy

```cmd
python main.py
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
