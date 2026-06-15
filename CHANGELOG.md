# Changelog

Mọi thay đổi đáng chú ý của dự án sẽ được ghi lại ở đây.

Định dạng dựa theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/),
và dự án tuân theo [Semantic Versioning](https://semver.org/lang/vi/).

## [Chưa phát hành]

## [1.0.2]

### Thêm
- 🛸 Minigame thứ 9 "Né chướng ngại": điều khiển bằng nút ◀ ▶ hoặc phím mũi
  tên, né thiên thạch rơi trong 12 giây (3 mạng, hết mạng vẫn được tha).
- 👽 Popup "Xác minh không phải người ngoài hành tinh" với câu hỏi vô lý,
  lần đầu luôn bị nghi ngờ.
- Job `lint` (ruff) chạy song song với test trong CI.
- File cấu hình `ruff.toml`.
- Badge Tests và Build & Release ở đầu README.

### Sửa
- Dọn các cảnh báo lint: import thừa, biến mơ hồ `l`, sắp xếp lại import.

## [1.0.1]

### Thêm
- 🍪 Popup "Đồng ý cookie": mọi công tắc đều bật, tắt thì tự bật lại.
- 🔍 Minigame thứ 8 "Tìm ô khác biệt": lưới 4x4, tìm ô khác với phần còn lại.
- Âm thanh giai điệu ngắn (thắng/thua/leng keng) và hiệu ứng pháo giấy khi
  vượt qua minigame (chỉ trên Windows, im lặng an toàn trên nền tảng khác).
- Bộ test cho minigame và dữ liệu cấu hình mới.
- Workflow CI chạy pytest trên mỗi push/PR.

### Sửa
- Đồng bộ số lượng minigame trong README.

## [1.0.0]

### Thêm
- Máy tính desktop tkinter giao diện dark, hỗ trợ bàn phím, bộ nhớ
  (MC/MR/M+/M-/MS) và lịch sử phép tính.
- Tự nhận DPI để hiển thị nét trên màn hình scaling 125%/150%.
- Chuỗi troll khi bấm `=`: vòng quay may mắn, giấy phép hết hạn, cập nhật
  driver giả, đăng nhập/đăng ký bất khả thi, chọn gói, điều khoản dịch vụ,
  form thẻ, bảng phụ phí, OTP, xác minh khuôn mặt, captcha, quảng cáo video,
  khảo sát, chia sẻ mạng xã hội, và kết quả sai có chủ đích.
- 7 minigame thử thách (sạc pin, bắt nút, đoán số, đập chuột chũi, gõ câu
  thần chú, canh thời điểm, Simon).
- Hệ thống gói có tác dụng thật (mỗi gói mở khoá một số phép tính).
- Lối thoát an toàn: bỏ cuộc 3 lần để mở chế độ máy tính thật.
- GitHub Actions tự build `Calculator.exe` và phát hành release khi push tag.
- Bộ test pytest.

[Chưa phát hành]: https://github.com/tridpt/calculator/compare/v1.0.2...HEAD
[1.0.2]: https://github.com/tridpt/calculator/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/tridpt/calculator/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/tridpt/calculator/releases/tag/v1.0.0
