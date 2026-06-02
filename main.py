"""
Calculator - Ứng dụng máy tính desktop (tkinter).

Điểm khởi chạy. Toàn bộ logic nằm trong package `calc/`:
  - calc/config.py         : dữ liệu/nội dung troll
  - calc/platform_utils.py : DPI awareness + âm thanh
  - calc/core.py           : lõi máy tính (UI, bàn phím, bộ nhớ, lịch sử)
  - calc/troll.py          : chuỗi popup troll khi bấm '='
  - calc/app.py            : lớp Calculator ghép các phần lại
"""

from calc import Calculator
from calc.platform_utils import enable_dpi_awareness


def main():
    enable_dpi_awareness()
    app = Calculator()
    app.mainloop()


if __name__ == "__main__":
    main()
