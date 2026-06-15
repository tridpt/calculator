# Đóng góp cho Calculator

Cảm ơn bạn đã quan tâm! Đây là một app máy tính troll cho vui, mọi đóng góp
(minigame mới, popup troll mới, sửa lỗi) đều được hoan nghênh.

## Thiết lập môi trường

```cmd
git clone https://github.com/tridpt/calculator.git
cd calculator
pip install -r requirements-dev.txt
```

## Chạy app

```cmd
python main.py
```

## Chạy test và lint trước khi gửi PR

```cmd
python -m pytest
python -m ruff check .
```

Cả hai phải xanh (CI cũng kiểm tra y hệt trên mỗi push/PR).

## Quy ước

- **Commit message**: dùng tiền tố kiểu Conventional Commits khi có thể
  (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- **Minigame mới**: thêm method `_minigame_*` vào `calc/minigames.py` và đăng
  ký trong `_step_minigame`. Mọi game phải **thắng được** (có lối thoát khi
  người chơi sai nhiều lần) để không ai bị kẹt.
- **Popup troll mới**: thêm method `_step_*` vào `calc/troll.py`. Dữ liệu
  text/emoji nên đặt ở `calc/config.py` để dễ chỉnh mà không đụng logic.
- **Không thu thập dữ liệu thật**: mọi input thẻ/OTP/mật khẩu phải bị vứt đi
  ngay, không lưu, không gửi đi đâu. Đây là nguyên tắc cốt lõi của app.

## Quy trình

1. Fork và tạo nhánh mới từ `main`.
2. Thực hiện thay đổi, thêm test nếu hợp lý.
3. Đảm bảo `pytest` và `ruff check` đều xanh.
4. Mở Pull Request mô tả rõ thay đổi.
