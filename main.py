"""
Calculator - Ứng dụng máy tính desktop (tkinter).
"""

import os
import random
import sys
import tkinter as tk
from tkinter import messagebox, ttk

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
        self._session_job = None  # after() id để cancel khi cần

        self._build_ui()
        self._bind_keys()

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

        self.equals_attempts += 1
        beep("warning")

        if not self._step_license_expired():
            return

        plan = self._step_choose_plan()
        if plan is None:
            return

        if not self._step_payment_form():
            return

        if not self._step_otp():
            return

        if not self._step_captcha():
            return

        self._step_random_ads()
        self._step_fake_loading()
        self._deliver_result()
        self._schedule_session_expiry()

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

        tk.Button(win, text="Để sau", bg="#45475a", fg="#cdd6f4",
                  relief="flat", command=win.destroy).pack(pady=8)

        self.wait_window(win)
        return choice["plan"]

    # ---- Bước 3: form thẻ + mã giảm giá ---- #
    def _step_payment_form(self):
        win = self._toplevel("Thanh toán", "400x420")

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
            f"Biểu thức: {self.expression}\n"
            f"Kết quả: {wrong_value}\n\n"
            f"(*) Kết quả tham khảo. Để xem đáp án chính xác, "
            f"vui lòng nâng cấp lên gói cao hơn.\n"
            f"Đáp án thật: {true_value}"
        )
        self._add_history(self.expression, wrong_value)
        self.expression = self._format(wrong_value)
        self._refresh()

    def _sabotage(self, value):
        try:
            v = float(value)
        except (TypeError, ValueError):
            return value

        trick = random.choice(["off_by_one", "swap_sign", "round_weird", "nice"])
        if trick == "off_by_one":
            v += random.choice([-1, 1])
        elif trick == "swap_sign" and v != 0:
            v = -v
        elif trick == "round_weird":
            v = round(v + random.uniform(-0.5, 0.5), 2)

        if float(value).is_integer() and float(v).is_integer():
            return int(v)
        return v

    # ---- Auto re-expire ---- #
    def _schedule_session_expiry(self):
        if self._session_job is not None:
            self.after_cancel(self._session_job)
        self._session_job = self.after(self.SESSION_TTL_MS, self._session_expired)

    def _session_expired(self):
        beep("warning")
        messagebox.showwarning(
            "Calculator",
            "Phiên đăng nhập của bạn đã kết thúc.\n"
            "Vui lòng kích hoạt lại để tiếp tục sử dụng dấu '='."
        )
        # Không reset attempts - lần bấm = sau lại phải qua hết quy trình.

    # ============================ Helpers =========================== #

    def _toplevel(self, title, size, grab=True):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry(size)
        win.configure(bg="#1e1e2e")
        win.transient(self)
        if grab:
            win.grab_set()
        return win


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
