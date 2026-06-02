"""
Calculator - Ứng dụng máy tính desktop (tkinter).
"""

import os
import random
import sys
import tkinter as tk
from tkinter import messagebox, ttk


def _enable_dpi_awareness():
    """Trên Windows, bật DPI awareness để cửa sổ không bị mờ/lệch kích thước
    khi màn hình dùng scaling 125%/150%."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        try:
            # Per-monitor v2 (Windows 10+)
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

try:
    import winsound  # chỉ có trên Windows
    def beep(kind="warning"):
        flag = {
            "warning": winsound.MB_ICONEXCLAMATION,
            "error": winsound.MB_ICONHAND,
            "info": winsound.MB_ICONASTERISK,
        }.get(kind, winsound.MB_ICONEXCLAMATION)
        try:
            winsound.MessageBeep(flag)
        except Exception:
            pass
except ImportError:
    def beep(kind="warning"):
        pass


# ----------------------------- Cấu hình troll ----------------------------- #

PREMIUM_PLANS = [
    ("Gói Cơ Bản",       "29.000đ / phép tính",     "Bao gồm: 1 phép tính. Không hỗ trợ dấu bằng nâng cao."),
    ("Gói Tiêu Chuẩn",   "199.000đ / tháng",        "Mở khoá phép cộng. Phép trừ tính phí thêm."),
    ("Gói Nâng Cao",     "999.000đ / tháng",        "Mở khoá nhân chia. Tặng kèm 1 lỗi sai miễn phí."),
    ("Gói Doanh Nghiệp", "Liên hệ để biết giá",     "Có thể đắt hơn cả cái máy tính Casio thật."),
]

# Mỗi gói chỉ "mở khoá" một số phép tính nhất định -> mô tả gói có tác dụng thật.
# allowed: tập các toán tử được phép. blocked sẽ bị chặn và đòi nâng cấp.
PLAN_PERMISSIONS = {
    "Gói Cơ Bản":       {"allowed": set(),                "next": "Gói Tiêu Chuẩn"},
    "Gói Tiêu Chuẩn":   {"allowed": {"+"},                "next": "Gói Nâng Cao"},
    "Gói Nâng Cao":     {"allowed": {"+", "-", "*", "/"}, "next": "Gói Doanh Nghiệp"},
    "Gói Doanh Nghiệp": {"allowed": {"+", "-", "*", "/"}, "next": None},
}

OP_NAMES = {"+": "phép cộng", "-": "phép trừ", "*": "phép nhân", "/": "phép chia"}

AD_LINES = [
    "🎉 Chúc mừng! Bạn là người dùng thứ 1.000.000 của ứng dụng.",
    "💸 Vay tiền online lãi suất 0% (chỉ trong 3 giây đầu).",
    "🔥 Cô đơn? Tải ngay app hẹn hò với cái máy tính.",
    "📈 Đầu tư coin XYZ - x1000 lần (hoặc về 0).",
    "🧴 Thuốc mọc tóc cho lập trình viên - 100% có gàu.",
]

CAPTCHA_QUESTIONS = [
    ("Bạn có phải con người không?", ["Có", "Không", "Tôi là cái máy tính"]),
    ("2 + 2 = ?  (chứng minh bạn không phải robot)", ["3", "5", "Cá vàng"]),
    ("Chọn đáp án sai:", ["Trời xanh", "Nước ướt", "App này hữu ích"]),
    ("Hôm nay là thứ mấy?", ["Thứ 8", "Thứ Hư Vô", "Không biết, hỏi sếp"]),
]

LOADING_MESSAGES = [
    "Đang kết nối tới máy chủ tính toán...",
    "Đang xác thực thẻ tín dụng của bạn...",
    "Đang hỏi ý kiến của AI...",
    "AI đang suy nghĩ rất lung tung...",
    "Đang tính toán bằng bàn tính tre...",
    "Đang chờ ông bảo vệ bật lại router...",
]

DISCOUNT_CODES = {
    # mã -> (giảm %, message)
    "FREE":   (0.01, "Áp dụng thành công! Giảm 0.01%."),
    "SALE":   (0.10, "Áp dụng thành công! Giảm 0.10%."),
    "BANK":   (None, "Mã chỉ áp dụng cho khách hàng VIP."),
    "VIP":    (None, "Mã đã hết lượt sử dụng (vừa nãy)."),
    "ADMIN":  (None, "Phát hiện gian lận. Giao dịch bị đánh dấu."),
}

# Các ô trên vòng quay may mắn - toàn ô "trượt", chỉ 1 ô hời nhưng kim không bao giờ dừng ở đó
WHEEL_SEGMENTS = [
    "Chúc may mắn lần sau",
    "Trượt rồi 😢",
    "Gần trúng!",
    "Hụt mất tiêu",
    "Thử lại nhé",
    "Sắp trúng tới nơi",
    "🎁 MIỄN PHÍ TRỌN ĐỜI",   # ô xịn - nhưng sẽ không bao giờ trúng
    "Quay lại từ đầu",
]

EXTRA_FEES = [
    ("Phí xử lý giao dịch",       "19.000đ"),
    ("Phí tiện ích nền tảng",     "25.000đ"),
    ("Phí duy trì máy chủ AI",    "49.000đ"),
    ("VAT",                       "10%"),
    ("VAT của VAT",               "10% của 10%"),
    ("Phí làm tròn lên",          "0.99đ"),
    ("Phí hiển thị bảng phí này", "9.000đ"),
]

SURVEY_QUESTIONS = [
    ("Bạn hài lòng với trải nghiệm thanh toán chứ?",
     ["Rất hài lòng", "Cực kỳ hài lòng", "Hài lòng đến phát khóc"]),
    ("Bạn sẽ giới thiệu app này cho kẻ thù chứ?",
     ["Chắc chắn rồi", "Đã giới thiệu sẵn", "Để dành troll sau"]),
    ("Mức giá có hợp lý không?",
     ["Quá rẻ", "Rẻ như cho", "Tôi muốn trả thêm"]),
]

# Điều khoản dịch vụ vô lý - phải cuộn hết mới cho đồng ý
EULA_TEXT = """ĐIỀU KHOẢN SỬ DỤNG DỊCH VỤ MÁY TÍNH

Vui lòng đọc kỹ toàn bộ điều khoản trước khi tiếp tục.
Bạn phải cuộn xuống tận cuối để có thể đồng ý.

Điều 1. Bằng việc sử dụng dấu "=", bạn đồng ý trả phí cho mỗi
kết quả, kể cả kết quả sai.

Điều 2. Mọi kết quả do ứng dụng cung cấp chỉ mang tính tham khảo
và có thể đúng một cách tình cờ.

Điều 3. Bạn không được phép so sánh ứng dụng này với máy tính
Casio, máy tính Windows, hay bất kỳ thiết bị nào tính đúng.

Điều 4. Bạn đồng ý rằng số 7 là một con số nhạy cảm và có thể
bị từ chối mà không cần lý do.

Điều 5. Trong trường hợp kết quả đúng, đó là lỗi của hệ thống
và sẽ được khắc phục trong bản cập nhật tiếp theo.

Điều 6. Bạn đồng ý nhận quảng cáo vào bất kỳ thời điểm nào,
kể cả lúc 3 giờ sáng.

Điều 7. Ứng dụng có quyền hết hạn giấy phép bất cứ lúc nào nó
thấy buồn.

Điều 8. Bạn xác nhận đã đọc hết các điều khoản này, điều mà
chúng tôi biết chắc là không ai làm.

Điều 9. Nếu bạn đọc tới đây, xin chúc mừng, bạn vẫn chưa được
tính toán gì cả.

Điều 10. Mọi tranh chấp sẽ được giải quyết bằng oẳn tù tì.

--- HẾT ĐIỀU KHOẢN ---
Cảm ơn bạn đã giả vờ đọc."""

# Các lỗi vô lý khi "kiểm tra" số thẻ
CARD_REJECTIONS = [
    "Số thẻ không được chứa chữ số 7.",
    "Tổng các chữ số phải chia hết cho 13.",
    "Số thẻ trông giống số thật quá, nghi ngờ gian lận.",
    "Số thẻ phải có đúng 19 chữ số (ô chỉ cho nhập 16).",
    "Chữ số đầu tiên không được là số nguyên tố.",
    "Hệ thống không thích con số này lắm.",
]

# Lý do từ chối khi nạn nhân cố thoát app
EXIT_EXCUSES = [
    "Bạn có chắc muốn thoát? Ưu đãi sẽ không còn nữa đâu.",
    "Khoan đã! Bạn vẫn chưa tính được phép nào mà.",
    "Hệ thống đang lưu... thói quen rời bỏ của bạn.",
    "Thật sự thoát? Cái máy tính sẽ buồn lắm đấy.",
    "Vui lòng xác nhận lần cuối: bạn nỡ bỏ đi sao?",
]

# Mật khẩu nào cũng bị chê - đăng nhập bất khả thi
PASSWORD_COMPLAINTS = [
    "Mật khẩu phải chứa ít nhất 1 chữ Hán.",
    "Mật khẩu không được giống 10.000 mật khẩu phổ biến (kể cả cái bạn vừa nghĩ).",
    "Mật khẩu phải chứa cảm xúc tích cực.",
    "Mật khẩu quá mạnh, làm máy chủ tự ti. Vui lòng yếu hơn.",
    "Tài khoản này có thể tồn tại hoặc không. Vui lòng thử lại.",
]

# Các dòng hiển thị khi "cập nhật bắt buộc" lúc mở app
UPDATE_STEPS = [
    "Đang kiểm tra phiên bản...",
    "Đang tải bản cập nhật quan trọng (0%)...",
    "Đang tải bản cập nhật quan trọng (47%)...",
    "Đang tải bản cập nhật quan trọng (88%)...",
    "Đang cài đặt (99%)...",
]


# --------------------------------- App ----------------------------------- #

class Calculator(tk.Tk):
    SESSION_TTL_MS = 90_000  # 90s sau "kích hoạt" thì phiên hết hạn

    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("520x520")
        self.minsize(380, 480)
        self.configure(bg="#1e1e2e")
        self._set_icon()

        self.expression = ""
        self.memory = 0.0
        self.history = []  # list[str] - "expr = result"
        self.show_history = False
        self.equals_attempts = 0
        self.give_ups = 0          # số lần nạn nhân bỏ cuộc giữa chừng
        self.revealed = False      # đã hiện màn "tự thú" chưa
        self.prank_disabled = False  # sau khi tự thú, cho phép tính thật
        self._session_job = None  # after() id để cancel khi cần
        self._exit_attempts = 0   # số lần cố thoát app
        self.debt = 0             # "nợ phí" tích luỹ (đồng)

        self._build_ui()
        self._bind_keys()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        # Cập nhật bắt buộc giả lúc mở app
        self.after(400, self._step_force_update)

    # ============================== UI ============================== #

    def _set_icon(self):
        """Gắn icon cho cửa sổ. Hoạt động cả khi chạy .py và khi đóng gói .exe."""
        base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        ico = os.path.join(base, "icon.ico")
        try:
            if os.path.exists(ico):
                self.iconbitmap(ico)
                return
        except Exception:
            pass
        # Dự phòng: dùng icon.png qua iconphoto nếu .ico lỗi
        png = os.path.join(base, "icon.png")
        try:
            if os.path.exists(png):
                self._icon_img = tk.PhotoImage(file=png)
                self.iconphoto(True, self._icon_img)
        except Exception:
            pass

    def _build_ui(self):
        # --- Top bar: nút ≡ để toggle history --- #
        topbar = tk.Frame(self, bg="#1e1e2e")
        topbar.pack(fill="x", padx=10, pady=(8, 0))

        self.menu_btn = tk.Button(
            topbar, text="≡", bg="#1e1e2e", fg="#cdd6f4",
            font=("Segoe UI", 12), relief="flat", bd=0,
            activebackground="#313244",
            command=self._toggle_history,
        )
        self.menu_btn.pack(side="left")
        tk.Label(topbar, text="Standard", bg="#1e1e2e", fg="#cdd6f4",
                 font=("Segoe UI", 10)).pack(side="left", padx=8)

        # --- Main container chia làm 2 cột: bàn phím | lịch sử --- #
        main = tk.Frame(self, bg="#1e1e2e")
        main.pack(fill="both", expand=True, padx=10, pady=8)

        self.left = tk.Frame(main, bg="#1e1e2e")
        self.left.pack(side="left", fill="both", expand=True)

        self.right = tk.Frame(main, bg="#181825")  # history panel
        # mặc định ẩn, chỉ pack khi user toggle

        # --- Display --- #
        self.display = tk.Entry(
            self.left, font=("Consolas", 24), justify="right",
            bg="#11111b", fg="#cdd6f4",
            insertbackground="#cdd6f4", relief="flat", bd=10,
            state="readonly", readonlybackground="#11111b",
            disabledforeground="#cdd6f4",
        )
        self.display.pack(fill="x", pady=(2, 8), ipady=12)

        # --- Memory row --- #
        mem = tk.Frame(self.left, bg="#1e1e2e")
        mem.pack(fill="x", pady=(0, 4))
        for i, label in enumerate(["MC", "MR", "M+", "M-", "MS"]):
            tk.Button(
                mem, text=label, bg="#1e1e2e", fg="#a6adc8",
                relief="flat", font=("Segoe UI", 9),
                activebackground="#313244",
                command=lambda l=label: self._on_memory(l),
            ).pack(side="left", expand=True, fill="x", padx=1)

        # --- Bàn phím chính --- #
        keypad = tk.Frame(self.left, bg="#1e1e2e")
        keypad.pack(fill="both", expand=True)

        layout = [
            ["C",  "(",  ")", "/"],
            ["7",  "8",  "9", "*"],
            ["4",  "5",  "6", "-"],
            ["1",  "2",  "3", "+"],
            ["0",  ".",  "⌫", "="],
        ]
        for r, row in enumerate(layout):
            keypad.grid_rowconfigure(r, weight=1)
            for c, label in enumerate(row):
                keypad.grid_columnconfigure(c, weight=1)
                self._make_button(keypad, label, r, c)

        # --- History panel (chuẩn bị nội dung, ẩn cho tới khi toggle) --- #
        tk.Label(self.right, text="Lịch sử", bg="#181825", fg="#cdd6f4",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(8, 4))

        self.history_box = tk.Listbox(
            self.right, bg="#181825", fg="#cdd6f4",
            selectbackground="#45475a", selectforeground="#cdd6f4",
            font=("Consolas", 10), relief="flat", bd=0, width=22,
            activestyle="none",
        )
        self.history_box.pack(fill="both", expand=True, padx=8, pady=4)
        self.history_box.bind("<Double-Button-1>", self._reuse_history)

        tk.Button(
            self.right, text="Xoá lịch sử", bg="#181825", fg="#a6adc8",
            relief="flat", font=("Segoe UI", 9),
            activebackground="#313244",
            command=self._clear_history,
        ).pack(fill="x", padx=8, pady=(0, 8))

        # --- Thanh trạng thái "nợ phí" ở đáy --- #
        self.debt_label = tk.Label(
            self, text="Dư nợ phí dịch vụ: 0đ", bg="#181825", fg="#6c7086",
            font=("Segoe UI", 8), anchor="e",
        )
        self.debt_label.pack(side="bottom", fill="x")

    def _update_debt(self, amount):
        """Tăng 'nợ phí' và cập nhật thanh trạng thái."""
        self.debt += amount
        if hasattr(self, "debt_label"):
            color = "#f38ba8" if self.debt > 0 else "#6c7086"
            self.debt_label.config(
                text=f"Dư nợ phí dịch vụ: {self.debt:,}đ".replace(",", "."),
                fg=color,
            )

    def _make_button(self, parent, label, r, c):
        op_chars = {"+", "-", "*", "/", "(", ")"}
        if label == "=":
            bg, fg = "#74c7ec", "#1e1e2e"
        elif label in ("C", "⌫"):
            bg, fg = "#45475a", "#cdd6f4"
        elif label in op_chars:
            bg, fg = "#45475a", "#cdd6f4"
        else:
            bg, fg = "#313244", "#cdd6f4"

        btn = tk.Button(
            parent, text=label, font=("Segoe UI", 12, "bold"),
            bg=bg, fg=fg, relief="flat",
            activebackground="#585b70",
            command=lambda l=label: self._on_press(l),
        )
        btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

    # ---------- Keyboard bindings ---------- #

    def _bind_keys(self):
        self.bind("<Return>",      self._key_eq)
        self.bind("<KP_Enter>",    self._key_eq)
        self.bind("<Escape>",      self._key_clear)
        self.bind("<BackSpace>",   self._key_back)
        for ch in "0123456789+-*/().":
            self.bind(ch, lambda e, c=ch: self._key_char(c))

    # Các handler kiểm tra focus: nếu đang gõ vào Entry trong popup
    # (form thẻ, OTP, mã giảm giá) thì không can thiệp vào máy tính chính.
    def _focus_in_popup(self):
        try:
            w = self.focus_get()
        except KeyError:
            return False
        if w is None or w is self.display:
            return False
        return isinstance(w, (tk.Entry, tk.Text))

    def _key_eq(self, _e):
        if self._focus_in_popup():
            return
        self._on_press("=")

    def _key_clear(self, _e):
        if self._focus_in_popup():
            return
        self._on_press("C")

    def _key_back(self, _e):
        if self._focus_in_popup():
            return
        self._on_press("⌫")

    def _key_char(self, ch):
        if self._focus_in_popup():
            return
        self._on_press(ch)

    # ============================ History =========================== #

    def _toggle_history(self):
        self.show_history = not self.show_history
        if self.show_history:
            self.right.pack(side="right", fill="y", padx=(8, 0))
        else:
            self.right.pack_forget()

    def _reuse_history(self, _event):
        sel = self.history_box.curselection()
        if not sel:
            return
        item = self.history_box.get(sel[0])
        # item dạng "expr = result", lấy result
        if " = " in item:
            self.expression = item.split(" = ", 1)[1]
            self._refresh()

    def _clear_history(self):
        self.history.clear()
        self.history_box.delete(0, tk.END)

    def _add_history(self, expr, result):
        line = f"{expr} = {result}"
        self.history.append(line)
        self.history_box.insert(0, line)

    # ============================ Memory ============================ #

    def _on_memory(self, label):
        try:
            current = float(self._safe_eval(self.expression)) if self.expression else 0.0
        except Exception:
            current = 0.0

        if label == "MC":
            self.memory = 0.0
        elif label == "MR":
            self.expression = self._format(self.memory)
            self._refresh()
        elif label == "MS":
            self.memory = current
        elif label == "M+":
            self.memory += current
        elif label == "M-":
            self.memory -= current

    # ========================== Phím bấm ============================ #

    def _on_press(self, key):
        if key == "C":
            self.expression = ""
        elif key == "⌫":
            self.expression = self.expression[:-1]
        elif key == "=":
            self._handle_equals()
            return
        else:
            self.expression += key
        self._refresh()

    def _refresh(self):
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
        self.display.config(state="readonly")

    @staticmethod
    def _safe_eval(expr):
        if not expr or not expr.strip():
            return None
        return eval(expr, {"__builtins__": {}}, {})

    @staticmethod
    def _format(value):
        try:
            f = float(value)
            if f.is_integer():
                return str(int(f))
            return f"{f:g}"
        except Exception:
            return str(value)

    # ===================== Cốt truyện troll khi = ===================== #

    def _handle_equals(self):
        if not self.expression.strip():
            messagebox.showinfo("Calculator", "Chưa có biểu thức để tính.")
            return

        # Sau khi đã "tự thú", máy tính hoạt động bình thường (kết quả đúng)
        if self.prank_disabled:
            self._deliver_real_result()
            return

        self.equals_attempts += 1
        beep("warning")
        # Mỗi lần bấm = lại "phát sinh" thêm phí dịch vụ
        self._update_debt(random.choice([9000, 15000, 29000]))

        # Bước 0: vòng quay "may mắn" (luôn trượt)
        self._step_lucky_wheel()

        if not self._step_license_expired():
            self._register_give_up()
            return

        # Đăng nhập tài khoản (mọi mật khẩu đều bị chê, có nút khách cho qua)
        if not self._step_login():
            self._register_give_up()
            return

        plan = self._step_choose_plan()
        if plan is None:
            self._register_give_up()
            return

        # Điều khoản dịch vụ dài lê thê
        if not self._step_eula():
            self._register_give_up()
            return

        if not self._step_payment_form():
            self._register_give_up()
            return

        # Bảng phụ phí lằng nhằng sau khi "thanh toán"
        if not self._step_extra_fees(plan):
            self._register_give_up()
            return

        if not self._step_otp():
            self._register_give_up()
            return

        if not self._step_captcha():
            self._register_give_up()
            return

        # Khảo sát hài lòng bắt buộc
        if not self._step_survey():
            self._register_give_up()
            return

        self._step_random_ads()
        self._step_fake_loading()

        # Gói vừa mua chỉ mở khoá một số phép tính -> kiểm tra quyền
        if not self._step_check_plan_permission(plan):
            return

        self._deliver_result()
        self._schedule_session_expiry()

    # ---- Đếm số lần bỏ cuộc và "tự thú" khi nạn nhân nản ---- #
    def _register_give_up(self):
        self.give_ups += 1
        # Sau 3 lần bỏ cuộc thì hiện màn tự thú (chỉ 1 lần)
        if self.give_ups >= 3 and not self.revealed:
            self._step_reveal_prank()

    def _step_reveal_prank(self):
        self.revealed = True
        win = self._toplevel("🎉🎉🎉", "420x300")

        tk.Label(win, text="ĐÂY LÀ TRÒ ĐÙA! 🎉", bg="#1e1e2e",
                 fg="#a6e3a1", font=("Segoe UI", 18, "bold")).pack(pady=(24, 8))
        tk.Label(
            win,
            text=("Không có phí nào hết, không ai lấy tiền của bạn cả.\n"
                  "Số 'dư nợ' kia là bịa, mọi thông tin thẻ / OTP bạn nhập\n"
                  "đều bị vứt đi ngay.\n\n"
                  "Đây chỉ là một cái máy tính troll thôi 😄\n"
                  "Cảm ơn bạn đã kiên nhẫn (hoặc đã tức điên)."),
            bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 10),
            justify="center", wraplength=370,
        ).pack(pady=4)

        def enable_free():
            self.prank_disabled = True
            # Xoá "nợ phí" - vì đây chỉ là trò đùa
            self.debt = 0
            self._update_debt(0)
            # Hủy job "phiên hết hạn" nếu còn treo, tránh nổ popup sau khi đã tự thú
            if self._session_job is not None:
                try:
                    self.after_cancel(self._session_job)
                except Exception:
                    pass
                self._session_job = None
            win.destroy()
            messagebox.showinfo(
                "Calculator",
                "Đã bật chế độ máy tính bình thường. Giờ bấm = sẽ ra kết quả đúng!"
            )

        tk.Button(win, text="Mở chế độ máy tính thật 🧮", bg="#74c7ec",
                  fg="#1e1e2e", relief="flat", font=("Segoe UI", 10, "bold"),
                  command=enable_free).pack(pady=14, ipadx=10, ipady=2)

        self.wait_window(win)

    # ---- Khởi động: cập nhật bắt buộc giả (chạy 99% rồi lỗi) ---- #
    def _step_force_update(self):
        win = self._toplevel("Cập nhật phần mềm", "400x170")
        # Không cho đóng cửa sổ update bằng nút X
        win.protocol("WM_DELETE_WINDOW", lambda: None)

        tk.Label(win, text="Đang cập nhật ứng dụng", bg="#1e1e2e",
                 fg="#cdd6f4", font=("Segoe UI", 12, "bold")).pack(pady=(16, 6))

        status = tk.Label(win, text="", bg="#1e1e2e", fg="#a6adc8",
                          font=("Segoe UI", 9))
        status.pack()

        bar = ttk.Progressbar(win, mode="determinate", length=320, maximum=100)
        bar.pack(pady=12)

        steps = list(enumerate(UPDATE_STEPS))
        values = [5, 30, 60, 90, 99]

        def run(idx=0):
            if not win.winfo_exists():
                return
            if idx < len(steps):
                status.config(text=steps[idx][1])
                bar["value"] = values[idx]
                win.after(random.randint(500, 900), lambda: run(idx + 1))
            else:
                # Tới 99% thì "lỗi" rồi cho vào dùng
                beep("error")
                status.config(text="Cập nhật thất bại: mất kết nối. Sẽ thử lại sau.",
                              fg="#f38ba8")
                win.after(1200, win.destroy)

        run()
        # Không grab toàn cục để smoke test có thể đóng; vẫn là cửa sổ con
        self.wait_window(win)

    # ---- Bước 0: vòng quay may mắn (rigged - không bao giờ trúng) ---- #
    def _step_lucky_wheel(self):
        win = self._toplevel("Vòng quay may mắn", "360x300")

        tk.Label(win, text="🎰 Quay trúng 1 phép tính MIỄN PHÍ!",
                 bg="#1e1e2e", fg="#f9e2af",
                 font=("Segoe UI", 11, "bold")).pack(pady=(12, 4))

        slot = tk.Label(win, text="—", bg="#11111b", fg="#cdd6f4",
                        font=("Segoe UI", 14, "bold"), width=22, height=2)
        slot.pack(pady=10)

        status = tk.Label(win, text="Nhấn QUAY để thử vận may",
                          bg="#1e1e2e", fg="#a6adc8", font=("Segoe UI", 9))
        status.pack()

        state = {"spinning": False, "done": False}
        # Loại bỏ ô xịn khỏi kết quả cuối: kim luôn dừng ở ô "trượt"
        losing = [s for s in WHEEL_SEGMENTS if "MIỄN PHÍ" not in s]

        def spin():
            if state["spinning"] or state["done"]:
                return
            state["spinning"] = True
            beep("info")
            ticks = {"n": 0}

            def roll():
                if ticks["n"] < 20:
                    # Lúc quay thì hiện cả ô xịn cho hồi hộp
                    slot.config(text=random.choice(WHEEL_SEGMENTS))
                    ticks["n"] += 1
                    win.after(80 + ticks["n"] * 6, roll)
                else:
                    # Dừng: luôn rơi vào ô trượt
                    slot.config(text=random.choice(losing), fg="#f38ba8")
                    status.config(text="Chúc bạn may mắn lần sau! 🍀")
                    beep("error")
                    state["spinning"] = False
                    state["done"] = True
                    win.after(1200, win.destroy)

            roll()

        tk.Button(win, text="QUAY 🎯", bg="#74c7ec", fg="#1e1e2e",
                  relief="flat", font=("Segoe UI", 11, "bold"),
                  command=spin).pack(pady=12, ipadx=20, ipady=4)
        tk.Button(win, text="Bỏ qua", bg="#45475a", fg="#cdd6f4",
                  relief="flat", command=win.destroy).pack()

        self.wait_window(win)

    # ---- Bước 1: license expired ---- #
    def _step_license_expired(self):
        if self.equals_attempts == 1:
            msg = ("Không thể thực hiện phép tính.\n\n"
                   "Giấy phép sử dụng của ứng dụng đã hết hạn.\n"
                   "Vui lòng kích hoạt để tiếp tục sử dụng tính năng này.")
        else:
            msg = ("Tính năng này yêu cầu giấy phép hợp lệ.\n"
                   "Bạn có muốn kích hoạt ngay bây giờ không?")
        return messagebox.askokcancel("Calculator", msg)

    # ---- Bước 1.5: đăng nhập tài khoản (mọi mật khẩu đều bị chê) ---- #
    def _step_login(self):
        win = self._toplevel("Đăng nhập", "380x300")

        tk.Label(win, text="Đăng nhập để tiếp tục", bg="#1e1e2e",
                 fg="#cdd6f4", font=("Segoe UI", 12, "bold")).pack(pady=(14, 8))

        tk.Label(win, text="Tên đăng nhập", bg="#1e1e2e", fg="#a6adc8",
                 font=("Segoe UI", 9)).pack(anchor="w", padx=30)
        user_entry = tk.Entry(win, bg="#11111b", fg="#cdd6f4",
                              relief="flat", insertbackground="#cdd6f4")
        user_entry.pack(fill="x", padx=30, pady=(2, 6), ipady=4)

        tk.Label(win, text="Mật khẩu", bg="#1e1e2e", fg="#a6adc8",
                 font=("Segoe UI", 9)).pack(anchor="w", padx=30)
        pw_entry = tk.Entry(win, bg="#11111b", fg="#cdd6f4", show="•",
                            relief="flat", insertbackground="#cdd6f4")
        pw_entry.pack(fill="x", padx=30, pady=(2, 6), ipady=4)

        complaint = {"i": 0}
        result = {"ok": False}

        def do_login():
            if not pw_entry.get():
                messagebox.showinfo("Đăng nhập", "Vui lòng nhập mật khẩu.", parent=win)
                return
            msg = PASSWORD_COMPLAINTS[complaint["i"] % len(PASSWORD_COMPLAINTS)]
            complaint["i"] += 1
            beep("error")
            messagebox.showwarning("Đăng nhập", msg, parent=win)
            pw_entry.delete(0, tk.END)

        def as_guest():
            result["ok"] = True
            win.destroy()

        tk.Button(win, text="Đăng nhập", bg="#74c7ec", fg="#1e1e2e",
                  relief="flat", command=do_login).pack(pady=(8, 4), ipadx=10)
        tk.Button(win, text="Tiếp tục với tư cách khách", bg="#45475a",
                  fg="#cdd6f4", relief="flat", command=as_guest).pack()

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 2: chọn gói + đếm ngược ---- #
    def _step_choose_plan(self):
        win = self._toplevel("Kích hoạt giấy phép", "440x400")

        tk.Label(win, text="Chọn gói giấy phép phù hợp",
                 bg="#1e1e2e", fg="#cdd6f4",
                 font=("Segoe UI", 12, "bold")).pack(pady=(10, 4))

        # Đồng hồ ưu đãi
        timer_label = tk.Label(
            win, text="🔥 Ưu đãi giảm 90% còn 00:30",
            bg="#1e1e2e", fg="#f9e2af", font=("Segoe UI", 10, "bold"),
        )
        timer_label.pack(pady=(0, 8))

        countdown = {"left": 30, "expired": False}

        def tick():
            if not win.winfo_exists():
                return
            if countdown["left"] <= 0:
                countdown["expired"] = True
                timer_label.config(
                    text="❌ Ưu đãi đã kết thúc - Giá hiện tại x10",
                    fg="#f38ba8",
                )
                return
            timer_label.config(text=f"🔥 Ưu đãi giảm 90% còn 00:{countdown['left']:02d}")
            countdown["left"] -= 1
            win.after(1000, tick)

        tick()

        choice = {"plan": None}

        for name, price, desc in PREMIUM_PLANS:
            frame = tk.Frame(win, bg="#313244", padx=10, pady=6)
            frame.pack(fill="x", padx=15, pady=4)
            tk.Label(frame, text=f"{name}  -  {price}",
                     bg="#313244", fg="#cdd6f4",
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
            tk.Label(frame, text=desc, bg="#313244", fg="#a6adc8",
                     font=("Segoe UI", 8), wraplength=380, justify="left").pack(anchor="w")
            tk.Button(
                frame, text=f"Chọn {name}",
                bg="#74c7ec", fg="#1e1e2e", relief="flat",
                command=lambda n=name: (choice.update(plan=n), win.destroy()),
            ).pack(anchor="e", pady=2)

        # Nút "Để sau" chạy trốn: rê chuột vào là né, phải đuổi vài lần mới bấm được
        runaway_zone = tk.Frame(win, bg="#1e1e2e", height=60)
        runaway_zone.pack(fill="x", pady=8)
        runaway_zone.pack_propagate(False)

        dodge = {"count": 0}
        skip_btn = tk.Button(runaway_zone, text="Để sau", bg="#45475a",
                             fg="#cdd6f4", relief="flat", command=win.destroy)
        skip_btn.place(relx=0.5, rely=0.5, anchor="center")

        def flee(_e):
            # 4 lần đầu thì né, lần 5 đứng yên cho bấm
            if dodge["count"] >= 5:
                return
            dodge["count"] += 1
            zw = runaway_zone.winfo_width() or 400
            bw = skip_btn.winfo_width() or 60
            new_relx = random.uniform(0.1, 0.9)
            # đảm bảo nút không tràn ra ngoài
            max_relx = max(0.1, 1 - (bw / zw) - 0.05)
            new_relx = min(new_relx, max_relx)
            skip_btn.place(relx=new_relx, rely=random.uniform(0.2, 0.8),
                           anchor="center")

        skip_btn.bind("<Enter>", flee)

        self.wait_window(win)
        return choice["plan"]

    # ---- Bước 2.5: điều khoản dịch vụ (phải cuộn hết mới đồng ý) ---- #
    def _step_eula(self):
        win = self._toplevel("Điều khoản dịch vụ", "460x420")

        tk.Label(win, text="Vui lòng đọc và đồng ý điều khoản",
                 bg="#1e1e2e", fg="#cdd6f4",
                 font=("Segoe UI", 12, "bold")).pack(pady=(10, 6))

        text_frame = tk.Frame(win, bg="#1e1e2e")
        text_frame.pack(fill="both", expand=True, padx=12)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text = tk.Text(text_frame, bg="#11111b", fg="#cdd6f4",
                       font=("Segoe UI", 9), relief="flat", wrap="word",
                       yscrollcommand=scrollbar.set, padx=10, pady=8,
                       width=40, height=10)
        text.pack(side="left", fill="both", expand=True)
        text.insert("1.0", EULA_TEXT)
        text.config(state="disabled")
        scrollbar.config(command=text.yview)

        result = {"ok": False}

        agree_btn = tk.Button(
            win, text="Tôi đồng ý (hãy cuộn xuống cuối)",
            bg="#45475a", fg="#6c7086", relief="flat", state="disabled",
            command=lambda: (result.update(ok=True), win.destroy()),
        )
        agree_btn.pack(pady=10, ipadx=10)

        def check_scrolled(_e=None):
            # yview() trả về (top, bottom) theo tỉ lệ 0..1
            if text.yview()[1] >= 0.99:
                agree_btn.config(state="normal", bg="#a6e3a1", fg="#1e1e2e",
                                 text="Tôi đã đọc và đồng ý")

        text.bind("<MouseWheel>", lambda e: win.after(10, check_scrolled))
        scrollbar.bind("<B1-Motion>", lambda e: win.after(10, check_scrolled))
        scrollbar.bind("<ButtonRelease-1>", lambda e: win.after(10, check_scrolled))
        # Trường hợp text ngắn hiện hết sẵn -> cho enable luôn
        win.after(200, check_scrolled)

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 3: form thẻ + mã giảm giá ---- #
    def _step_payment_form(self):
        win = self._toplevel("Thanh toán", "400x480")

        tk.Label(win, text="Nhập thông tin thẻ", bg="#1e1e2e",
                 fg="#cdd6f4", font=("Segoe UI", 12, "bold")).pack(pady=10)

        fields = {}
        for placeholder in ["Số thẻ",
                            "Họ tên chủ thẻ",
                            "Ngày hết hạn (MM/YY)",
                            "CVV (3 số bí mật)"]:
            tk.Label(win, text=placeholder, bg="#1e1e2e", fg="#a6adc8",
                     font=("Segoe UI", 9)).pack(anchor="w", padx=20)
            entry = tk.Entry(win, bg="#11111b", fg="#cdd6f4",
                             relief="flat", insertbackground="#cdd6f4")
            entry.pack(fill="x", padx=20, pady=2, ipady=4)
            fields[placeholder] = entry

        # Nút "kiểm tra" số thẻ - mỗi lần lại chê một kiểu vô lý
        card_check = {"i": 0}

        def verify_card():
            num = fields["Số thẻ"].get().strip()
            if not num:
                messagebox.showinfo("Calculator", "Vui lòng nhập số thẻ.", parent=win)
                return
            # Xoay vòng qua các lý do từ chối vô lý
            reason = CARD_REJECTIONS[card_check["i"] % len(CARD_REJECTIONS)]
            card_check["i"] += 1
            beep("error")
            messagebox.showwarning("Calculator",
                                   f"Số thẻ chưa hợp lệ:\n{reason}", parent=win)

        tk.Button(win, text="Kiểm tra số thẻ", bg="#45475a", fg="#cdd6f4",
                  relief="flat", command=verify_card).pack(padx=20, pady=(4, 0), anchor="e")

        # Mã giảm giá
        tk.Label(win, text="Mã giảm giá (tuỳ chọn)", bg="#1e1e2e",
                 fg="#a6adc8", font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(8, 0))
        code_row = tk.Frame(win, bg="#1e1e2e")
        code_row.pack(fill="x", padx=20)
        code_entry = tk.Entry(code_row, bg="#11111b", fg="#cdd6f4",
                              relief="flat", insertbackground="#cdd6f4")
        code_entry.pack(side="left", fill="x", expand=True, ipady=4)

        def apply_code():
            code = code_entry.get().strip().upper()
            if not code:
                messagebox.showinfo("Mã giảm giá", "Bạn chưa nhập mã.", parent=win)
                return
            info = DISCOUNT_CODES.get(code)
            if info is None:
                messagebox.showwarning("Mã giảm giá",
                                       "Mã không hợp lệ hoặc đã hết hạn.",
                                       parent=win)
            else:
                _, msg = info
                messagebox.showinfo("Mã giảm giá", msg, parent=win)

        tk.Button(code_row, text="Áp dụng", bg="#45475a", fg="#cdd6f4",
                  relief="flat", command=apply_code).pack(side="left", padx=(6, 0))

        result = {"ok": False, "attempted": False}

        def submit():
            if not result["attempted"]:
                result["attempted"] = True
                beep("error")
                messagebox.showwarning(
                    "Calculator",
                    "Giao dịch bị ngân hàng từ chối.\n"
                    "Vui lòng kiểm tra thông tin và thử lại.",
                    parent=win,
                )
                return
            result["ok"] = True
            win.destroy()

        tk.Button(win, text="Thanh toán", bg="#a6e3a1", fg="#1e1e2e",
                  relief="flat", command=submit).pack(pady=14, ipadx=12)

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 3.5: bảng phụ phí lằng nhằng ---- #
    def _step_extra_fees(self, plan=None):
        win = self._toplevel("Chi tiết thanh toán", "400x420")

        tk.Label(win, text="Vui lòng xác nhận các khoản phí",
                 bg="#1e1e2e", fg="#cdd6f4",
                 font=("Segoe UI", 12, "bold")).pack(pady=(12, 6))

        box = tk.Frame(win, bg="#181825")
        box.pack(fill="x", padx=20, pady=4)

        # Lấy đúng giá của gói đã chọn
        plan_price = "—"
        for name, price, _desc in PREMIUM_PLANS:
            if name == plan:
                plan_price = price
                break

        tk.Label(box, text=f"Giá gói ({plan or 'đã chọn'})", bg="#181825", fg="#cdd6f4",
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=3)
        tk.Label(box, text=plan_price, bg="#181825", fg="#cdd6f4",
                 font=("Segoe UI", 9)).grid(row=0, column=1, sticky="e", padx=10, pady=3)

        for i, (name, amount) in enumerate(EXTRA_FEES, start=1):
            tk.Label(box, text=name, bg="#181825", fg="#a6adc8",
                     font=("Segoe UI", 9)).grid(row=i, column=0, sticky="w", padx=10, pady=2)
            tk.Label(box, text=amount, bg="#181825", fg="#f9e2af",
                     font=("Segoe UI", 9)).grid(row=i, column=1, sticky="e", padx=10, pady=2)

        box.grid_columnconfigure(0, weight=1)
        box.grid_columnconfigure(1, weight=0)

        tk.Label(win, text="Tổng cộng: rất nhiều tiền 💸",
                 bg="#1e1e2e", fg="#f38ba8",
                 font=("Segoe UI", 11, "bold")).pack(pady=10)

        result = {"ok": False}

        def accept():
            result["ok"] = True
            win.destroy()

        tk.Button(win, text="Tôi đồng ý với mọi khoản phí",
                  bg="#a6e3a1", fg="#1e1e2e", relief="flat",
                  command=accept).pack(pady=4, ipadx=10)
        tk.Button(win, text="Huỷ (tiếc tiền)", bg="#45475a", fg="#cdd6f4",
                  relief="flat", command=win.destroy).pack(pady=2)

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 4: OTP ---- #
    def _step_otp(self):
        win = self._toplevel("Xác thực OTP", "360x220")

        tk.Label(win, text="Mã OTP đã được gửi tới số điện thoại đăng ký",
                 bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 10),
                 wraplength=320).pack(pady=(12, 4))

        otp_entry = tk.Entry(win, bg="#11111b", fg="#cdd6f4",
                             relief="flat", insertbackground="#cdd6f4",
                             justify="center", font=("Consolas", 14))
        otp_entry.pack(padx=40, pady=8, ipady=6, fill="x")

        cooldown_label = tk.Label(win, text="Gửi lại OTP sau 30s",
                                  bg="#1e1e2e", fg="#a6adc8",
                                  font=("Segoe UI", 9))
        cooldown_label.pack(pady=2)

        cd = {"left": 30}
        resend_btn_holder = {}

        def cd_tick():
            if not win.winfo_exists():
                return
            if cd["left"] <= 0:
                cooldown_label.config(text="Có thể gửi lại OTP")
                if "btn" in resend_btn_holder:
                    resend_btn_holder["btn"].config(state="normal")
                return
            cooldown_label.config(text=f"Gửi lại OTP sau {cd['left']}s")
            cd["left"] -= 1
            win.after(1000, cd_tick)

        cd_tick()

        result = {"ok": False, "tried": 0}

        def confirm():
            result["tried"] += 1
            if result["tried"] < 2:
                beep("error")
                messagebox.showerror(
                    "Calculator",
                    "Mã OTP không chính xác. Vui lòng thử lại.",
                    parent=win,
                )
                otp_entry.delete(0, tk.END)
                return
            result["ok"] = True
            win.destroy()

        def resend():
            cd["left"] = 30
            resend_btn_holder["btn"].config(state="disabled")
            cd_tick()

        btn_row = tk.Frame(win, bg="#1e1e2e")
        btn_row.pack(pady=10)
        resend_btn = tk.Button(btn_row, text="Gửi lại", bg="#45475a",
                               fg="#cdd6f4", relief="flat", state="disabled",
                               command=resend)
        resend_btn.pack(side="left", padx=4)
        resend_btn_holder["btn"] = resend_btn
        tk.Button(btn_row, text="Xác nhận", bg="#74c7ec", fg="#1e1e2e",
                  relief="flat", command=confirm).pack(side="left", padx=4)

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 5: captcha ---- #
    def _step_captcha(self):
        question, options = random.choice(CAPTCHA_QUESTIONS)
        win = self._toplevel("Xác minh", "380x220")

        tk.Label(win, text=question, bg="#1e1e2e", fg="#cdd6f4",
                 font=("Segoe UI", 11), wraplength=340).pack(pady=15)

        result = {"ok": False}

        def pick(_):
            messagebox.showinfo("Calculator",
                                "Đã xác minh. Tiếp tục...", parent=win)
            result["ok"] = True
            win.destroy()

        for opt in options:
            tk.Button(win, text=opt, bg="#89b4fa", fg="#1e1e2e",
                      relief="flat",
                      command=lambda o=opt: pick(o)).pack(fill="x", padx=40, pady=3)

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 5.5: khảo sát hài lòng bắt buộc ---- #
    def _step_survey(self):
        win = self._toplevel("Khảo sát mức độ hài lòng", "400x340")

        tk.Label(win, text="Trước khi xem kết quả, hãy đánh giá chúng tôi",
                 bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 11, "bold"),
                 wraplength=360).pack(pady=(12, 8))

        # Đánh giá sao - bắt buộc 5 sao mới cho qua
        star_state = {"n": 0}
        stars_frame = tk.Frame(win, bg="#1e1e2e")
        stars_frame.pack(pady=4)
        star_btns = []

        def set_stars(n):
            star_state["n"] = n
            for i, b in enumerate(star_btns):
                b.config(text="★" if i < n else "☆",
                         fg="#f9e2af" if i < n else "#6c7086")

        for i in range(5):
            b = tk.Button(stars_frame, text="☆", bg="#1e1e2e", fg="#6c7086",
                          font=("Segoe UI", 18), relief="flat", bd=0,
                          activebackground="#1e1e2e",
                          command=lambda n=i + 1: set_stars(n))
            b.pack(side="left")
            star_btns.append(b)

        # Câu hỏi vô lý
        question, options = random.choice(SURVEY_QUESTIONS)
        tk.Label(win, text=question, bg="#1e1e2e", fg="#cdd6f4",
                 font=("Segoe UI", 10), wraplength=360).pack(pady=(10, 4))

        answer = tk.StringVar(value="")
        for opt in options:
            tk.Radiobutton(win, text=opt, variable=answer, value=opt,
                           bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244",
                           activebackground="#1e1e2e", activeforeground="#cdd6f4",
                           font=("Segoe UI", 9), anchor="w").pack(fill="x", padx=40)

        result = {"ok": False}

        def submit():
            if star_state["n"] < 5:
                beep("error")
                messagebox.showwarning(
                    "Khảo sát",
                    "Vui lòng đánh giá 5 sao để tiếp tục.\n"
                    "(Đánh giá thấp hơn không được chấp nhận.)",
                    parent=win,
                )
                return
            if not answer.get():
                messagebox.showwarning("Khảo sát",
                                       "Bạn chưa chọn câu trả lời.", parent=win)
                return
            result["ok"] = True
            win.destroy()

        tk.Button(win, text="Gửi đánh giá", bg="#74c7ec", fg="#1e1e2e",
                  relief="flat", command=submit).pack(pady=12, ipadx=10)

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 6: quảng cáo ---- #
    def _step_random_ads(self):
        for _ in range(random.randint(1, 2)):
            beep("info")
            messagebox.showinfo("Thông báo", random.choice(AD_LINES))

    # ---- Bước 7: loading ---- #
    def _step_fake_loading(self):
        win = self._toplevel("Đang xử lý...", "380x140", grab=True)
        label = tk.Label(win, text="", bg="#1e1e2e", fg="#cdd6f4",
                         font=("Segoe UI", 10))
        label.pack(pady=15)
        bar = ttk.Progressbar(win, mode="determinate", length=320, maximum=100)
        bar.pack(pady=5)

        msgs = random.sample(LOADING_MESSAGES, 3)
        steps = [(20, msgs[0]), (55, msgs[1]), (95, msgs[2]), (100, "Hoàn tất.")]

        def schedule(idx=0):
            if idx >= len(steps):
                win.after(300, win.destroy)
                return
            value, text = steps[idx]
            label.config(text=text)
            bar["value"] = value
            win.after(random.randint(400, 900), lambda: schedule(idx + 1))

        win.after(50, schedule)
        self.wait_window(win)

    # ---- Bước 7.5: kiểm tra quyền của gói đã mua ---- #
    def _operators_used(self):
        """Trả về tập toán tử + - * / xuất hiện trong biểu thức.
        Bỏ qua dấu '-' đứng đầu hoặc ngay sau '(' (số âm, không tính là phép trừ).
        """
        ops = set()
        expr = self.expression
        for i, ch in enumerate(expr):
            if ch in "+*/":
                ops.add(ch)
            elif ch == "-":
                prev = ""
                j = i - 1
                while j >= 0 and expr[j] == " ":
                    j -= 1
                if j >= 0:
                    prev = expr[j]
                # '-' là phép trừ nếu trước nó là số hoặc ')'
                if prev.isdigit() or prev == ")" or prev == ".":
                    ops.add("-")
        return ops

    def _step_check_plan_permission(self, plan):
        """Mô tả gói có tác dụng thật: gói chỉ mở khoá một số phép tính.
        Nếu biểu thức dùng phép ngoài quyền -> chặn và đòi nâng cấp.
        Trả về True nếu được phép tính tiếp.
        """
        perm = PLAN_PERMISSIONS.get(plan)
        if perm is None:
            return True

        # Gói Doanh Nghiệp: "liên hệ bộ phận kinh doanh" -> không bao giờ tính được
        if plan == "Gói Doanh Nghiệp":
            beep("warning")
            messagebox.showinfo(
                "Calculator",
                "Cảm ơn bạn đã quan tâm Gói Doanh Nghiệp.\n"
                "Bộ phận kinh doanh sẽ liên hệ trong vòng 3-5 ngày làm việc "
                "để kích hoạt tính năng tính toán cho bạn.\n\n"
                "Trong thời gian chờ, vui lòng tính tay."
            )
            return False

        allowed = perm["allowed"]
        used = self._operators_used()
        forbidden = used - allowed

        if not forbidden:
            return True

        # Có phép ngoài gói -> chặn, gợi ý nâng cấp lên gói cao hơn
        op = sorted(forbidden)[0]
        op_name = OP_NAMES.get(op, f"phép '{op}'")
        nxt = perm["next"]
        upgrade = f"\n\nVui lòng nâng cấp lên {nxt} để mở khoá {op_name}." if nxt else ""
        beep("error")

        if not allowed:
            unlocked = "Gói này không bao gồm bất kỳ phép tính nào."
        else:
            names = ", ".join(OP_NAMES[o] for o in sorted(allowed))
            unlocked = f"Gói của bạn chỉ mở khoá: {names}."

        messagebox.showwarning(
            "Calculator",
            f"Biểu thức của bạn có sử dụng {op_name}.\n"
            f"{unlocked}{upgrade}"
        )
        return False

    # ---- Chế độ thật: tính đúng, không phá (sau khi tự thú) ---- #
    def _deliver_real_result(self):
        try:
            value = self._safe_eval(self.expression)
        except Exception:
            beep("error")
            messagebox.showerror("Calculator",
                                 "Biểu thức không hợp lệ. Vui lòng kiểm tra lại.")
            return
        result = self._format(value)
        self._add_history(self.expression, result)
        self.expression = result
        self._refresh()

    # ---- Bước 8: trả kết quả sai có chủ đích ---- #
    def _deliver_result(self):
        try:
            true_value = self._safe_eval(self.expression)
        except Exception:
            beep("error")
            messagebox.showerror(
                "Calculator",
                "Biểu thức không hợp lệ. Vui lòng kiểm tra lại."
            )
            return

        wrong_value = self._sabotage(true_value)
        beep("info")
        messagebox.showinfo(
            "Calculator",
            f"{self.expression} = {wrong_value}"
        )
        self._add_history(self.expression, wrong_value)
        self.expression = self._format(wrong_value)
        self._refresh()

    def _sabotage(self, value):
        """Làm sai kết quả một cách tinh vi, khó nghi ngờ.
        - Sai lệch nhỏ, tỉ lệ theo độ lớn của số.
        - Không bao giờ đổi dấu hay biến thành 0 (những thứ dễ bị phát hiện).
        - Đôi khi để đúng để nạn nhân không đoán ra quy luật.
        """
        try:
            v = float(value)
        except (TypeError, ValueError):
            return value

        if v == 0:
            # 0 mà sai thành số khác thì lộ ngay -> để nguyên
            return 0

        is_int = float(value).is_integer()
        sign = 1 if v > 0 else -1
        mag = abs(v)

        trick = random.choice(["off_small", "off_small", "tiny_percent", "nice"])

        if trick == "off_small":
            # Lệch 1-3 đơn vị, nhưng không vượt quá ~30% độ lớn (tránh lố với số nhỏ)
            step = random.randint(1, 3)
            delta = min(step, max(1, int(mag * 0.3))) if mag >= 2 else 0
            new_mag = mag + delta * random.choice([-1, 1])
        elif trick == "tiny_percent":
            # Lệch 1-5%
            new_mag = mag * (1 + random.uniform(0.01, 0.05) * random.choice([-1, 1]))
            if is_int:
                new_mag = round(new_mag)
        else:  # nice -> giữ nguyên
            new_mag = mag

        # Không cho rơi về 0 hoặc âm (giữ cùng dấu, tối thiểu là 1 nếu vốn là số nguyên)
        if new_mag <= 0:
            new_mag = mag
        v = sign * new_mag

        if is_int and float(v).is_integer():
            return int(v)
        return round(v, 4)

    # ---- Auto re-expire ---- #
    def _schedule_session_expiry(self):
        if self._session_job is not None:
            self.after_cancel(self._session_job)
        self._session_job = self.after(self.SESSION_TTL_MS, self._session_expired)

    def _session_expired(self):
        self._session_job = None
        if self.prank_disabled:
            return  # đã tự thú -> không làm phiền nữa
        beep("warning")
        messagebox.showwarning(
            "Calculator",
            "Phiên đăng nhập của bạn đã kết thúc.\n"
            "Vui lòng kích hoạt lại để tiếp tục sử dụng dấu '='."
        )
        # Không reset attempts - lần bấm = sau lại phải qua hết quy trình.

    # ============================ Helpers =========================== #

    def _on_close(self):
        # Đã tự thú -> cho thoát ngay, không troll nữa
        if self.prank_disabled:
            self.destroy()
            return

        self._exit_attempts += 1
        if self._exit_attempts <= len(EXIT_EXCUSES):
            beep("warning")
            excuse = EXIT_EXCUSES[self._exit_attempts - 1]
            stay = messagebox.askretrycancel(
                "Calculator",
                f"{excuse}\n\n(Retry = ở lại, Cancel = vẫn thoát)"
            )
            # askretrycancel: Retry=True (ở lại), Cancel=False (thoát)
            if stay:
                return
            # Nạn nhân chọn thoát: vẫn níu thêm cho tới khi hết câu
            if self._exit_attempts < len(EXIT_EXCUSES):
                return
        # Hết câu níu kéo -> đành cho thoát
        self.destroy()

    def _toplevel(self, title, size, grab=True):
        win = tk.Toplevel(self)
        win.title(title)
        win.configure(bg="#1e1e2e")
        win.transient(self)

        # size "WxH" được dùng làm kích thước TỐI THIỂU.
        try:
            min_w, min_h = (int(x) for x in size.lower().split("x"))
        except Exception:
            min_w, min_h = 360, 240
        win.geometry(f"{min_w}x{min_h}")

        if grab:
            win.grab_set()

        # Tự co giãn cửa sổ vừa khít nội dung rồi canh giữa.
        # Khắc phục việc nội dung bị cắt khi màn hình bật DPI scaling.
        def _fit():
            if not win.winfo_exists():
                return
            win.update_idletasks()
            req_w = win.winfo_reqwidth()
            req_h = win.winfo_reqheight()
            w = max(min_w, req_w)
            h = max(min_h, req_h)
            sw = win.winfo_screenwidth()
            sh = win.winfo_screenheight()
            w = min(w, sw - 40)
            h = min(h, sh - 80)
            x = (sw - w) // 2
            y = max(20, (sh - h) // 3)
            win.geometry(f"{w}x{h}+{x}+{y}")
            win.minsize(w, h)

        win.after(60, _fit)
        return win


if __name__ == "__main__":
    _enable_dpi_awareness()
    app = Calculator()
    app.mainloop()
