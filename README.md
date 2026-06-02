# Calculator 🧮

Ứng dụng máy tính desktop đơn giản, viết bằng Python + tkinter.

> 🤫 Lưu ý nội bộ (không nói cho nạn nhân biết): app là một trò troll.
> Khi bấm `=` lần đầu, app báo "giấy phép hết hạn" và dẫn dụ qua 1 chuỗi
> popup kích hoạt - thanh toán - captcha - quảng cáo - đang xử lý, rồi
> trả ra kết quả sai có chủ đích kèm dòng disclaimer hài hước.
>
> Không lấy tiền thật, không gửi dữ liệu đi đâu, mọi input ở form thẻ
> đều bị vứt đi. Chỉ để cười với bạn bè.

## Yêu cầu

- Python 3.8+ (đã thử trên 3.13)
- `tkinter` (đi kèm Python chuẩn trên Windows)

## Chạy

```cmd
python main.py
```

## Mẹo dùng (chỉ cho người chủ máy)

- Mọi nút trừ `=` đều hoạt động bình thường (số, phép tính, `C`, `⌫`)
- Bấm Cancel hoặc đóng cửa sổ giữa chừng → quay lại máy tính, không mất gì
- Mỗi lần bấm `=`: app sẽ chọn ngẫu nhiên 1 trong vài kiểu "phá" kết quả
  (lệch ±1, đổi dấu, làm tròn lệch, hoặc đôi khi đúng)

## Đóng gói thành .exe (tuỳ chọn)

```cmd
pip install pyinstaller
pyinstaller --onefile --windowed --name Calculator main.py
```

File .exe sẽ nằm trong `dist/Calculator.exe`, copy đi đâu chạy cũng được.
