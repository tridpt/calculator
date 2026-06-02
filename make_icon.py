"""
Tạo icon.ico hình máy tính cho ứng dụng.
Chạy 1 lần để sinh file icon, không cần chạy lại khi dùng app.
"""

from PIL import Image, ImageDraw

# Vẽ ở kích thước lớn cho nét, rồi xuất ra nhiều size trong file .ico
SIZE = 256
img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# Thân máy tính (bo góc), màu xanh giống Windows Calculator
body = [28, 16, 228, 240]
d.rounded_rectangle(body, radius=28, fill=(0, 120, 212, 255))

# Màn hình hiển thị
screen = [50, 40, 206, 96]
d.rounded_rectangle(screen, radius=10, fill=(13, 17, 27, 255))

# Số "=" mờ trên màn hình (gợi ý máy tính)
d.rectangle([170, 58, 196, 64], fill=(116, 199, 236, 255))
d.rectangle([170, 72, 196, 78], fill=(116, 199, 236, 255))

# Lưới nút bấm 4 cột x 4 hàng
cols, rows = 4, 4
x0, y0, x1, y1 = 50, 112, 206, 224
gap = 10
bw = (x1 - x0 - gap * (cols - 1)) / cols
bh = (y1 - y0 - gap * (rows - 1)) / rows

for r in range(rows):
    for c in range(cols):
        bx = x0 + c * (bw + gap)
        by = y0 + r * (bh + gap)
        # Nút "=" (góc dưới phải) tô màu nhấn
        if r == rows - 1 and c == cols - 1:
            color = (116, 199, 236, 255)
        else:
            color = (236, 240, 247, 255)
        d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=5, fill=color)

# Xuất ra .ico với nhiều kích thước (Windows tự chọn cái phù hợp)
sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save("icon.ico", sizes=sizes)
# Lưu thêm bản PNG để README/GitHub dùng nếu cần
img.save("icon.png")
print("Đã tạo icon.ico và icon.png")
