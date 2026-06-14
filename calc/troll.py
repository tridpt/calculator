"""Phần troll: chuỗi popup khi bấm '=', vòng quay, đăng nhập, thanh toán...

Mixin này được trộn vào lớp Calculator. Dùng các method/thuộc tính từ
CoreCalculatorMixin (self.expression, self._toplevel, self._refresh...).
"""

import random
import tkinter as tk
from tkinter import messagebox, ttk

from .config import (
    AD_LINES, BUS_CAPTCHA_COMPLAINTS, BUS_CAPTCHA_TILES, CAPTCHA_QUESTIONS,
    CARD_REJECTIONS, COLORS, COOKIE_TYPES, DISCOUNT_CODES, DRIVER_NAMES,
    DRIVER_SCAN_STEPS, EULA_TEXT, EXIT_EXCUSES, EXTRA_FEES, FACE_SCAN_COMPLAINTS,
    LOADING_MESSAGES, OP_NAMES, PASSWORD_COMPLAINTS, PLAN_PERMISSIONS,
    PREMIUM_PLANS, REGISTER_COMPLAINTS, SHARE_PLATFORMS, SURVEY_QUESTIONS,
    UPDATE_STEPS, VIDEO_AD_TITLES, WHEEL_SEGMENTS,
)
from .platform_utils import beep, flash_window, shake_window, confetti, play_tune


class TrollMixin:
    """Toàn bộ cốt truyện troll."""

    # ===================== Orchestrator khi bấm = ===================== #

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

        self._step_lucky_wheel()

        if not self._step_cookie_consent():
            self._register_give_up()
            return

        if not self._step_license_expired():
            self._register_give_up()
            return

        if not self._step_driver_update():
            self._register_give_up()
            return

        if not self._step_login():
            self._register_give_up()
            return

        plan = self._step_choose_plan()
        if plan is None:
            self._register_give_up()
            return

        if not self._step_eula():
            self._register_give_up()
            return

        if not self._step_payment_form():
            self._register_give_up()
            return

        if not self._step_extra_fees(plan):
            self._register_give_up()
            return

        if not self._step_otp():
            self._register_give_up()
            return

        if not self._step_face_verify():
            self._register_give_up()
            return

        # Minigame thử thách (sạc pin / bắt nút / đoán số - chọn ngẫu nhiên)
        if not self._step_minigame():
            self._register_give_up()
            return

        if not self._step_captcha():
            self._register_give_up()
            return

        if not self._step_bus_captcha():
            self._register_give_up()
            return

        # Xem hết quảng cáo video mới được tính
        if not self._step_video_ad():
            self._register_give_up()
            return

        if not self._step_survey():
            self._register_give_up()
            return

        # Chia sẻ mạng xã hội để "mở khoá"
        if not self._step_social_share():
            self._register_give_up()
            return

        self._step_random_ads()
        self._step_fake_loading()

        # Gói vừa mua chỉ mở khoá một số phép tính -> kiểm tra quyền
        if not self._step_check_plan_permission(plan):
            return

        self._deliver_result()
        self._schedule_session_expiry()

    # ---- Đếm bỏ cuộc + tự thú ---- #
    def _register_give_up(self):
        self.give_ups += 1
        if self.give_ups >= 3 and not self.revealed:
            self._step_reveal_prank()

    def _step_reveal_prank(self):
        self.revealed = True
        win = self._toplevel("🎉🎉🎉", "420x300")

        tk.Label(win, text="ĐÂY LÀ TRÒ ĐÙA! 🎉", bg=COLORS["bg"],
                 fg=COLORS["ok"], font=("Segoe UI", 18, "bold")).pack(pady=(24, 8))
        tk.Label(
            win,
            text=("Không có phí nào hết, không ai lấy tiền của bạn cả.\n"
                  "Số 'dư nợ' kia là bịa, mọi thông tin thẻ / OTP bạn nhập\n"
                  "đều bị vứt đi ngay.\n\n"
                  "Đây chỉ là một cái máy tính troll thôi 😄\n"
                  "Cảm ơn bạn đã kiên nhẫn (hoặc đã tức điên)."),
            bg=COLORS["bg"], fg=COLORS["fg"], font=("Segoe UI", 10),
            justify="center", wraplength=370,
        ).pack(pady=4)

        def enable_free():
            self.prank_disabled = True
            self.debt = 0
            self._update_debt(0)
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

        tk.Button(win, text="Mở chế độ máy tính thật 🧮", bg=COLORS["accent"],
                  fg=COLORS["bg"], relief="flat", font=("Segoe UI", 10, "bold"),
                  command=enable_free).pack(pady=14, ipadx=10, ipady=2)

        # Ăn mừng: nhạc thắng + pháo giấy cho cái kết vui vẻ
        win.after(120, lambda: (play_tune("win"), confetti(win, count=36, duration=2200)))

        self.wait_window(win)

    # ---- Khởi động: cập nhật bắt buộc giả ---- #
    def _step_force_update(self):
        win = self._toplevel("Cập nhật phần mềm", "400x170")
        win.protocol("WM_DELETE_WINDOW", lambda: None)  # chặn nút X

        tk.Label(win, text="Đang cập nhật ứng dụng", bg=COLORS["bg"],
                 fg=COLORS["fg"], font=("Segoe UI", 12, "bold")).pack(pady=(16, 6))

        status = tk.Label(win, text="", bg=COLORS["bg"], fg=COLORS["muted"],
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
                beep("error")
                status.config(text="Cập nhật thất bại: mất kết nối. Sẽ thử lại sau.",
                              fg=COLORS["danger"])
                win.after(1200, win.destroy)

        run()
        self.wait_window(win)

    # ---- Bước 0: vòng quay may mắn (rigged) ---- #
    def _step_lucky_wheel(self):
        win = self._toplevel("Vòng quay may mắn", "360x300")

        tk.Label(win, text="🎰 Quay trúng 1 phép tính MIỄN PHÍ!",
                 bg=COLORS["bg"], fg=COLORS["warn"],
                 font=("Segoe UI", 11, "bold")).pack(pady=(12, 4))

        slot = tk.Label(win, text="—", bg=COLORS["display"], fg=COLORS["fg"],
                        font=("Segoe UI", 14, "bold"), width=22, height=2)
        slot.pack(pady=10)

        status = tk.Label(win, text="Nhấn QUAY để thử vận may",
                          bg=COLORS["bg"], fg=COLORS["muted"], font=("Segoe UI", 9))
        status.pack()

        state = {"spinning": False, "done": False}
        losing = [s for s in WHEEL_SEGMENTS if "MIỄN PHÍ" not in s]

        def spin():
            if state["spinning"] or state["done"]:
                return
            state["spinning"] = True
            beep("info")
            ticks = {"n": 0}

            def roll():
                if ticks["n"] < 20:
                    slot.config(text=random.choice(WHEEL_SEGMENTS))
                    ticks["n"] += 1
                    win.after(80 + ticks["n"] * 6, roll)
                else:
                    slot.config(text=random.choice(losing), fg=COLORS["danger"])
                    status.config(text="Chúc bạn may mắn lần sau! 🍀")
                    beep("error")
                    state["spinning"] = False
                    state["done"] = True
                    win.after(1200, win.destroy)

            roll()

        tk.Button(win, text="QUAY 🎯", bg=COLORS["accent"], fg=COLORS["bg"],
                  relief="flat", font=("Segoe UI", 11, "bold"),
                  command=spin).pack(pady=12, ipadx=20, ipady=4)
        tk.Button(win, text="Bỏ qua", bg=COLORS["key_op"], fg=COLORS["fg"],
                  relief="flat", command=win.destroy).pack()

        self.wait_window(win)

    # ---- Bước 0.5: đồng ý cookie (toggle nào cũng bật lại) ---- #
    def _step_cookie_consent(self):
        win = self._toplevel("Chính sách Cookie 🍪", "420x440")

        tk.Label(win, text="🍪 Trang web này dùng cookie",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 13, "bold")).pack(pady=(14, 2))
        tk.Label(win, text="(Đây là app desktop, nhưng kệ đi.) "
                           "Bạn có thể 'tuỳ chỉnh' bên dưới.",
                 bg=COLORS["bg"], fg=COLORS["muted"],
                 font=("Segoe UI", 9), wraplength=380).pack(pady=(0, 8))

        box = tk.Frame(win, bg=COLORS["panel"])
        box.pack(fill="both", expand=True, padx=18, pady=4)

        # Mọi công tắc đều bật, và bấm tắt thì nó tự bật lại.
        toggles = []
        for name, desc in COOKIE_TYPES:
            row = tk.Frame(box, bg=COLORS["panel"])
            row.pack(fill="x", padx=10, pady=4)

            var = tk.BooleanVar(value=True)

            def make_resist(v=var):
                def resist():
                    if not v.get():
                        beep("error")
                        v.set(True)  # cứng đầu: tự bật lại
                return resist

            chk = tk.Checkbutton(
                row, variable=var, command=make_resist(var),
                bg=COLORS["panel"], fg=COLORS["fg"],
                selectcolor=COLORS["key"], activebackground=COLORS["panel"],
                activeforeground=COLORS["fg"], text=name,
                font=("Segoe UI", 9, "bold"), anchor="w")
            chk.pack(anchor="w")
            tk.Label(row, text=desc, bg=COLORS["panel"], fg=COLORS["muted"],
                     font=("Segoe UI", 8), wraplength=350,
                     justify="left").pack(anchor="w", padx=24)
            toggles.append(var)

        result = {"ok": False}

        def accept_all():
            for v in toggles:
                v.set(True)
            beep("info")
            result["ok"] = True
            win.destroy()

        def reject_all():
            # "Từ chối" nhưng thật ra vẫn bật hết rồi mới cho qua
            beep("error")
            shake_window(win)
            for v in toggles:
                v.set(True)
            messagebox.showinfo(
                "Cookie",
                "Rất tiếc, không thể từ chối cookie cần thiết, "
                "cookie không cần thiết, và cookie không tồn tại.\n"
                "Đã bật lại tất cả giúp bạn. Không có gì.", parent=win)

        btn_row = tk.Frame(win, bg=COLORS["bg"])
        btn_row.pack(pady=12)
        tk.Button(btn_row, text="Chấp nhận tất cả", bg=COLORS["ok"],
                  fg=COLORS["bg"], relief="flat", font=("Segoe UI", 10, "bold"),
                  command=accept_all).pack(side="left", padx=4, ipadx=8)
        tk.Button(btn_row, text="Từ chối (không được đâu)", bg=COLORS["key_op"],
                  fg=COLORS["fg"], relief="flat",
                  command=reject_all).pack(side="left", padx=4)

        self.wait_window(win)
        return result["ok"]

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

    # ---- Bước 1.2: cập nhật driver máy tính (giả) ---- #
    def _step_driver_update(self):
        win = self._toplevel("Cập nhật driver", "440x280")

        tk.Label(win, text="🖥️ Trình điều khiển máy tính đã lỗi thời",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 12, "bold"), wraplength=400).pack(pady=(14, 4))

        status = tk.Label(win, text="", bg=COLORS["bg"], fg=COLORS["muted"],
                          font=("Segoe UI", 9), wraplength=400)
        status.pack()

        bar = ttk.Progressbar(win, mode="determinate", length=360, maximum=100)
        bar.pack(pady=10)

        listing = tk.Label(win, text="", bg=COLORS["display"], fg=COLORS["warn"],
                           font=("Consolas", 9), wraplength=380, justify="left",
                           padx=10, pady=6)
        listing.pack(fill="x", padx=20)

        result = {"ok": False}
        state = {"phase": "scan"}

        btn_row = tk.Frame(win, bg=COLORS["bg"])
        btn_row.pack(pady=12)
        install_btn = tk.Button(btn_row, text="Đang quét...", bg=COLORS["key_op"],
                                fg=COLORS["dim"], relief="flat", state="disabled")
        install_btn.pack(side="left", padx=4)
        tk.Button(btn_row, text="Để sau", bg=COLORS["key_op"], fg=COLORS["fg"],
                  relief="flat", command=win.destroy).pack(side="left", padx=4)

        def do_install():
            if state["phase"] != "found":
                return
            state["phase"] = "install"
            install_btn.config(state="disabled", text="Đang cài đặt...",
                               bg=COLORS["key_op"], fg=COLORS["dim"])

            def run(v=0):
                if not win.winfo_exists():
                    return
                if v <= 100:
                    bar["value"] = v
                    status.config(text=f"Đang cài đặt driver... {v}%")
                    win.after(120, lambda: run(v + random.randint(7, 18)))
                else:
                    beep("info")
                    result["ok"] = True
                    win.destroy()

            run()

        def scan(idx=0, vals=None):
            if not win.winfo_exists():
                return
            vals = vals or [20, 45, 70, 95]
            if idx < len(DRIVER_SCAN_STEPS):
                status.config(text=DRIVER_SCAN_STEPS[idx])
                bar["value"] = vals[idx % len(vals)]
                win.after(random.randint(500, 800), lambda: scan(idx + 1, vals))
            else:
                state["phase"] = "found"
                bad = random.sample(DRIVER_NAMES, 3)
                listing.config(text="⚠ Phát hiện 3 driver lỗi thời:\n• "
                                    + "\n• ".join(bad))
                status.config(text="Cần cập nhật ngay để dùng được dấu '='.",
                              fg=COLORS["danger"])
                bar["value"] = 0
                beep("warning")
                flash_window(win, COLORS["danger"])
                install_btn.config(state="normal", text="Cài đặt driver ngay",
                                   bg=COLORS["accent"], fg=COLORS["bg"],
                                   command=do_install)
                win.refit()

        scan()
        self.wait_window(win)
        return result["ok"]

    # ---- Bước 1.5: đăng nhập (mọi mật khẩu đều bị chê) ---- #
    def _step_login(self):
        win = self._toplevel("Đăng nhập", "380x300")

        tk.Label(win, text="Đăng nhập để tiếp tục", bg=COLORS["bg"],
                 fg=COLORS["fg"], font=("Segoe UI", 12, "bold")).pack(pady=(14, 8))

        tk.Label(win, text="Tên đăng nhập", bg=COLORS["bg"], fg=COLORS["muted"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=30)
        tk.Entry(win, bg=COLORS["display"], fg=COLORS["fg"],
                 relief="flat", insertbackground=COLORS["fg"]).pack(
                     fill="x", padx=30, pady=(2, 6), ipady=4)

        tk.Label(win, text="Mật khẩu", bg=COLORS["bg"], fg=COLORS["muted"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=30)
        pw_entry = tk.Entry(win, bg=COLORS["display"], fg=COLORS["fg"], show="•",
                            relief="flat", insertbackground=COLORS["fg"])
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

        tk.Button(win, text="Đăng nhập", bg=COLORS["accent"], fg=COLORS["bg"],
                  relief="flat", command=do_login).pack(pady=(8, 4), ipadx=10)
        tk.Button(win, text="Đăng ký tài khoản mới", bg=COLORS["blue"],
                  fg=COLORS["bg"], relief="flat",
                  command=lambda: self._open_register(win)).pack(pady=(0, 4), ipadx=10)
        tk.Button(win, text="Tiếp tục với tư cách khách", bg=COLORS["key_op"],
                  fg=COLORS["fg"], relief="flat", command=as_guest).pack()

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 1.6: đăng ký tài khoản (mở từ màn đăng nhập, luôn thất bại) ---- #
    def _open_register(self, parent_win):
        win = self._toplevel("Đăng ký tài khoản", "400x420")

        tk.Label(win, text="Tạo tài khoản mới", bg=COLORS["bg"],
                 fg=COLORS["fg"], font=("Segoe UI", 12, "bold")).pack(pady=(14, 8))

        fields = {}
        specs = [
            ("Tên đăng nhập", False),
            ("Email", False),
            ("Mật khẩu", True),
            ("Xác nhận mật khẩu", True),
        ]
        for placeholder, secret in specs:
            tk.Label(win, text=placeholder, bg=COLORS["bg"], fg=COLORS["muted"],
                     font=("Segoe UI", 9)).pack(anchor="w", padx=30)
            entry = tk.Entry(win, bg=COLORS["display"], fg=COLORS["fg"],
                             relief="flat", insertbackground=COLORS["fg"],
                             show="•" if secret else "")
            entry.pack(fill="x", padx=30, pady=(2, 6), ipady=4)
            fields[placeholder] = entry

        status = tk.Label(win, text="", bg=COLORS["bg"], fg=COLORS["danger"],
                          font=("Segoe UI", 9), wraplength=340, justify="center")
        status.pack(pady=2)

        state = {"tries": 0}

        def submit():
            # Bắt buộc điền hết cho có vẻ nghiêm túc
            if any(not e.get().strip() for e in fields.values()):
                messagebox.showinfo("Đăng ký",
                                    "Vui lòng điền đầy đủ thông tin.", parent=win)
                return
            state["tries"] += 1
            if state["tries"] < 3:
                beep("error")
                shake_window(win)
                status.config(text=random.choice(REGISTER_COMPLAINTS))
                fields["Mật khẩu"].delete(0, tk.END)
                fields["Xác nhận mật khẩu"].delete(0, tk.END)
                win.refit()
                return
            # Lần 3: "thành công" nhưng tài khoản phải chờ duyệt -> vô dụng
            beep("info")
            messagebox.showinfo(
                "Đăng ký",
                "🎉 Đăng ký thành công!\n\n"
                "Tài khoản của bạn đang chờ phê duyệt thủ công trong vòng "
                "3-5 ngày làm việc (không tính ngày bạn cần tính toán).\n\n"
                "Trong thời gian chờ, vui lòng tiếp tục với tư cách khách.",
                parent=win)
            win.destroy()

        tk.Button(win, text="Đăng ký", bg=COLORS["accent"], fg=COLORS["bg"],
                  relief="flat", command=submit).pack(pady=(8, 4), ipadx=12)
        tk.Button(win, text="Quay lại đăng nhập", bg=COLORS["key_op"],
                  fg=COLORS["fg"], relief="flat", command=win.destroy).pack()

        self.wait_window(win)
        # Khôi phục grab cho cửa sổ đăng nhập sau khi đóng form đăng ký
        try:
            if parent_win.winfo_exists():
                parent_win.grab_set()
        except Exception:
            pass

    # ---- Bước 2: chọn gói + đếm ngược + nút chạy trốn ---- #
    def _step_choose_plan(self):
        win = self._toplevel("Kích hoạt giấy phép", "440x400")

        tk.Label(win, text="Chọn gói giấy phép phù hợp",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 12, "bold")).pack(pady=(10, 4))

        timer_label = tk.Label(
            win, text="🔥 Ưu đãi giảm 90% còn 00:30",
            bg=COLORS["bg"], fg=COLORS["warn"], font=("Segoe UI", 10, "bold"),
        )
        timer_label.pack(pady=(0, 8))

        countdown = {"left": 30}

        def tick():
            if not win.winfo_exists():
                return
            if countdown["left"] <= 0:
                timer_label.config(text="❌ Ưu đãi đã kết thúc - Giá hiện tại x10",
                                   fg=COLORS["danger"])
                return
            timer_label.config(text=f"🔥 Ưu đãi giảm 90% còn 00:{countdown['left']:02d}")
            countdown["left"] -= 1
            win.after(1000, tick)

        tick()

        choice = {"plan": None}

        for name, price, desc in PREMIUM_PLANS:
            frame = tk.Frame(win, bg=COLORS["key"], padx=10, pady=6)
            frame.pack(fill="x", padx=15, pady=4)
            tk.Label(frame, text=f"{name}  -  {price}",
                     bg=COLORS["key"], fg=COLORS["fg"],
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")
            tk.Label(frame, text=desc, bg=COLORS["key"], fg=COLORS["muted"],
                     font=("Segoe UI", 8), wraplength=380, justify="left").pack(anchor="w")
            tk.Button(
                frame, text=f"Chọn {name}",
                bg=COLORS["accent"], fg=COLORS["bg"], relief="flat",
                command=lambda n=name: (choice.update(plan=n), win.destroy()),
            ).pack(anchor="e", pady=2)

        # Nút "Để sau" chạy trốn
        runaway_zone = tk.Frame(win, bg=COLORS["bg"], height=60)
        runaway_zone.pack(fill="x", pady=8)
        runaway_zone.pack_propagate(False)

        dodge = {"count": 0}
        skip_btn = tk.Button(runaway_zone, text="Để sau", bg=COLORS["key_op"],
                             fg=COLORS["fg"], relief="flat", command=win.destroy)
        skip_btn.place(relx=0.5, rely=0.5, anchor="center")

        def flee(_e):
            if dodge["count"] >= 5:
                return
            dodge["count"] += 1
            zw = runaway_zone.winfo_width() or 400
            bw = skip_btn.winfo_width() or 60
            new_relx = random.uniform(0.1, 0.9)
            max_relx = max(0.1, 1 - (bw / zw) - 0.05)
            new_relx = min(new_relx, max_relx)
            skip_btn.place(relx=new_relx, rely=random.uniform(0.2, 0.8), anchor="center")

        skip_btn.bind("<Enter>", flee)

        self.wait_window(win)
        return choice["plan"]

    # ---- Bước 2.5: điều khoản (phải cuộn hết mới đồng ý) ---- #
    def _step_eula(self):
        win = self._toplevel("Điều khoản dịch vụ", "460x420")

        tk.Label(win, text="Vui lòng đọc và đồng ý điều khoản",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 12, "bold")).pack(pady=(10, 6))

        text_frame = tk.Frame(win, bg=COLORS["bg"])
        text_frame.pack(fill="both", expand=True, padx=12)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text = tk.Text(text_frame, bg=COLORS["display"], fg=COLORS["fg"],
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
            bg=COLORS["key_op"], fg=COLORS["dim"], relief="flat", state="disabled",
            command=lambda: (result.update(ok=True), win.destroy()),
        )
        agree_btn.pack(pady=10, ipadx=10)

        def check_scrolled(_e=None):
            if text.yview()[1] >= 0.99:
                agree_btn.config(state="normal", bg=COLORS["ok"], fg=COLORS["bg"],
                                 text="Tôi đã đọc và đồng ý")

        text.bind("<MouseWheel>", lambda e: win.after(10, check_scrolled))
        scrollbar.bind("<B1-Motion>", lambda e: win.after(10, check_scrolled))
        scrollbar.bind("<ButtonRelease-1>", lambda e: win.after(10, check_scrolled))
        win.after(200, check_scrolled)

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 3: form thẻ + mã giảm giá + kiểm tra thẻ ---- #
    def _step_payment_form(self):
        win = self._toplevel("Thanh toán", "400x480")

        tk.Label(win, text="Nhập thông tin thẻ", bg=COLORS["bg"],
                 fg=COLORS["fg"], font=("Segoe UI", 12, "bold")).pack(pady=10)

        fields = {}
        for placeholder in ["Số thẻ", "Họ tên chủ thẻ",
                            "Ngày hết hạn (MM/YY)", "CVV (3 số bí mật)"]:
            tk.Label(win, text=placeholder, bg=COLORS["bg"], fg=COLORS["muted"],
                     font=("Segoe UI", 9)).pack(anchor="w", padx=20)
            entry = tk.Entry(win, bg=COLORS["display"], fg=COLORS["fg"],
                             relief="flat", insertbackground=COLORS["fg"])
            entry.pack(fill="x", padx=20, pady=2, ipady=4)
            fields[placeholder] = entry

        card_check = {"i": 0}

        def verify_card():
            num = fields["Số thẻ"].get().strip()
            if not num:
                messagebox.showinfo("Calculator", "Vui lòng nhập số thẻ.", parent=win)
                return
            reason = CARD_REJECTIONS[card_check["i"] % len(CARD_REJECTIONS)]
            card_check["i"] += 1
            beep("error")
            messagebox.showwarning("Calculator",
                                   f"Số thẻ chưa hợp lệ:\n{reason}", parent=win)

        tk.Button(win, text="Kiểm tra số thẻ", bg=COLORS["key_op"], fg=COLORS["fg"],
                  relief="flat", command=verify_card).pack(padx=20, pady=(4, 0), anchor="e")

        tk.Label(win, text="Mã giảm giá (tuỳ chọn)", bg=COLORS["bg"],
                 fg=COLORS["muted"], font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(8, 0))
        code_row = tk.Frame(win, bg=COLORS["bg"])
        code_row.pack(fill="x", padx=20)
        code_entry = tk.Entry(code_row, bg=COLORS["display"], fg=COLORS["fg"],
                              relief="flat", insertbackground=COLORS["fg"])
        code_entry.pack(side="left", fill="x", expand=True, ipady=4)

        def apply_code():
            code = code_entry.get().strip().upper()
            if not code:
                messagebox.showinfo("Mã giảm giá", "Bạn chưa nhập mã.", parent=win)
                return
            info = DISCOUNT_CODES.get(code)
            if info is None:
                messagebox.showwarning("Mã giảm giá",
                                       "Mã không hợp lệ hoặc đã hết hạn.", parent=win)
            else:
                _, msg = info
                messagebox.showinfo("Mã giảm giá", msg, parent=win)

        tk.Button(code_row, text="Áp dụng", bg=COLORS["key_op"], fg=COLORS["fg"],
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

        tk.Button(win, text="Thanh toán", bg=COLORS["ok"], fg=COLORS["bg"],
                  relief="flat", command=submit).pack(pady=14, ipadx=12)

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 3.5: bảng phụ phí ---- #
    def _step_extra_fees(self, plan=None):
        win = self._toplevel("Chi tiết thanh toán", "400x420")

        tk.Label(win, text="Vui lòng xác nhận các khoản phí",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 12, "bold")).pack(pady=(12, 6))

        box = tk.Frame(win, bg=COLORS["panel"])
        box.pack(fill="x", padx=20, pady=4)

        plan_price = "—"
        for name, price, _desc in PREMIUM_PLANS:
            if name == plan:
                plan_price = price
                break

        tk.Label(box, text=f"Giá gói ({plan or 'đã chọn'})", bg=COLORS["panel"],
                 fg=COLORS["fg"], font=("Segoe UI", 9, "bold")).grid(
                     row=0, column=0, sticky="w", padx=10, pady=3)
        tk.Label(box, text=plan_price, bg=COLORS["panel"], fg=COLORS["fg"],
                 font=("Segoe UI", 9)).grid(row=0, column=1, sticky="e", padx=10, pady=3)

        for i, (name, amount) in enumerate(EXTRA_FEES, start=1):
            tk.Label(box, text=name, bg=COLORS["panel"], fg=COLORS["muted"],
                     font=("Segoe UI", 9)).grid(row=i, column=0, sticky="w", padx=10, pady=2)
            tk.Label(box, text=amount, bg=COLORS["panel"], fg=COLORS["warn"],
                     font=("Segoe UI", 9)).grid(row=i, column=1, sticky="e", padx=10, pady=2)

        box.grid_columnconfigure(0, weight=1)

        tk.Label(win, text="Tổng cộng: rất nhiều tiền 💸",
                 bg=COLORS["bg"], fg=COLORS["danger"],
                 font=("Segoe UI", 11, "bold")).pack(pady=10)

        result = {"ok": False}

        def accept():
            result["ok"] = True
            win.destroy()

        tk.Button(win, text="Tôi đồng ý với mọi khoản phí",
                  bg=COLORS["ok"], fg=COLORS["bg"], relief="flat",
                  command=accept).pack(pady=4, ipadx=10)
        tk.Button(win, text="Huỷ (tiếc tiền)", bg=COLORS["key_op"], fg=COLORS["fg"],
                  relief="flat", command=win.destroy).pack(pady=2)

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 4: OTP ---- #
    def _step_otp(self):
        win = self._toplevel("Xác thực OTP", "360x220")

        tk.Label(win, text="Mã OTP đã được gửi tới số điện thoại đăng ký",
                 bg=COLORS["bg"], fg=COLORS["fg"], font=("Segoe UI", 10),
                 wraplength=320).pack(pady=(12, 4))

        otp_entry = tk.Entry(win, bg=COLORS["display"], fg=COLORS["fg"],
                             relief="flat", insertbackground=COLORS["fg"],
                             justify="center", font=("Consolas", 14))
        otp_entry.pack(padx=40, pady=8, ipady=6, fill="x")

        cooldown_label = tk.Label(win, text="Gửi lại OTP sau 30s",
                                  bg=COLORS["bg"], fg=COLORS["muted"],
                                  font=("Segoe UI", 9))
        cooldown_label.pack(pady=2)

        cd = {"left": 30}
        holder = {}

        def cd_tick():
            if not win.winfo_exists():
                return
            if cd["left"] <= 0:
                cooldown_label.config(text="Có thể gửi lại OTP")
                if "btn" in holder:
                    holder["btn"].config(state="normal")
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
                messagebox.showerror("Calculator",
                                     "Mã OTP không chính xác. Vui lòng thử lại.",
                                     parent=win)
                otp_entry.delete(0, tk.END)
                return
            result["ok"] = True
            win.destroy()

        def resend():
            cd["left"] = 30
            holder["btn"].config(state="disabled")
            cd_tick()

        btn_row = tk.Frame(win, bg=COLORS["bg"])
        btn_row.pack(pady=10)
        resend_btn = tk.Button(btn_row, text="Gửi lại", bg=COLORS["key_op"],
                               fg=COLORS["fg"], relief="flat", state="disabled",
                               command=resend)
        resend_btn.pack(side="left", padx=4)
        holder["btn"] = resend_btn
        tk.Button(btn_row, text="Xác nhận", bg=COLORS["accent"], fg=COLORS["bg"],
                  relief="flat", command=confirm).pack(side="left", padx=4)

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 4.5: xác minh khuôn mặt (giả) ---- #
    def _step_face_verify(self):
        win = self._toplevel("Xác minh khuôn mặt", "400x380")

        tk.Label(win, text="📷 Xác minh khuôn mặt để chống gian lận",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 12, "bold"), wraplength=360).pack(pady=(12, 4))

        # "Khung camera" giả
        cam = tk.Frame(win, bg="#000000", height=170)
        cam.pack(fill="x", padx=30, pady=8)
        cam.pack_propagate(False)
        face = tk.Label(cam, text="🙂", bg="#000000", font=("Segoe UI", 60))
        face.pack(expand=True)

        status = tk.Label(win, text="Đặt khuôn mặt vào giữa khung hình.",
                          bg=COLORS["bg"], fg=COLORS["muted"],
                          font=("Segoe UI", 9), wraplength=360)
        status.pack(pady=2)

        bar = ttk.Progressbar(win, mode="determinate", length=320, maximum=100)
        bar.pack(pady=8)

        state = {"tries": 0, "scanning": False}
        result = {"ok": False}

        scan_btn = tk.Button(win, text="Quét khuôn mặt", bg=COLORS["accent"],
                             fg=COLORS["bg"], relief="flat",
                             font=("Segoe UI", 10, "bold"))
        scan_btn.pack(pady=4, ipadx=10)
        tk.Button(win, text="Bỏ qua xác minh", bg=COLORS["key_op"],
                  fg=COLORS["fg"], relief="flat", command=win.destroy).pack(pady=2)

        faces = ["🙂", "😐", "😑", "🤨", "😬", "😶"]

        def scan():
            if state["scanning"]:
                return
            state["scanning"] = True
            scan_btn.config(state="disabled", bg=COLORS["key_op"], fg=COLORS["dim"])

            def run(v=0):
                if not win.winfo_exists():
                    return
                if v <= 100:
                    bar["value"] = v
                    face.config(text=random.choice(faces))
                    status.config(text=f"Đang quét khuôn mặt... {v}%",
                                  fg=COLORS["muted"])
                    win.after(110, lambda: run(v + random.randint(8, 16)))
                else:
                    finish()

            run()

        def finish():
            state["tries"] += 1
            state["scanning"] = False
            if state["tries"] < 2:
                beep("error")
                shake_window(win)
                face.config(text="😵")
                status.config(text=random.choice(FACE_SCAN_COMPLAINTS),
                              fg=COLORS["danger"])
                bar["value"] = 0
                scan_btn.config(state="normal", text="Quét lại",
                                bg=COLORS["accent"], fg=COLORS["bg"])
                win.refit()
            else:
                beep("info")
                face.config(text="😎")
                status.config(text="Xác minh thành công! Cũng đẹp trai/xinh gái đấy.",
                              fg=COLORS["ok"])
                result["ok"] = True
                win.after(700, win.destroy)

        scan_btn.config(command=scan)
        self.wait_window(win)
        return result["ok"]

    # ---- Bước 5: captcha ---- #
    def _step_captcha(self):
        question, options = random.choice(CAPTCHA_QUESTIONS)
        win = self._toplevel("Xác minh", "380x220")

        tk.Label(win, text=question, bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 11), wraplength=340).pack(pady=15)

        result = {"ok": False}

        def pick(_):
            messagebox.showinfo("Calculator", "Đã xác minh. Tiếp tục...", parent=win)
            result["ok"] = True
            win.destroy()

        for opt in options:
            tk.Button(win, text=opt, bg=COLORS["blue"], fg=COLORS["bg"],
                      relief="flat",
                      command=lambda o=opt: pick(o)).pack(fill="x", padx=40, pady=3)

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 5.3: captcha chọn ảnh xe buýt (vô lý) ---- #
    def _step_bus_captcha(self):
        win = self._toplevel("Xác minh hình ảnh", "380x440")

        tk.Label(win, text="Chọn tất cả ô có XE BUÝT 🚌",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 12, "bold")).pack(pady=(12, 2))
        tk.Label(win, text="(Bấm vào ô để chọn, bấm lại để bỏ chọn)",
                 bg=COLORS["bg"], fg=COLORS["muted"],
                 font=("Segoe UI", 8)).pack()

        grid = tk.Frame(win, bg=COLORS["panel"])
        grid.pack(padx=20, pady=10)

        selected = set()
        tiles = []
        result = {"ok": False, "tries": 0}

        def shuffle_tiles():
            new = random.sample(BUS_CAPTCHA_TILES, 9)
            for i, b in enumerate(tiles):
                b.config(text=new[i], bg=COLORS["display"])
            selected.clear()

        def toggle(i):
            if i in selected:
                selected.discard(i)
                tiles[i].config(bg=COLORS["display"])
            else:
                selected.add(i)
                tiles[i].config(bg=COLORS["accent"])
            beep("info")

        for r in range(3):
            for c in range(3):
                idx = r * 3 + c
                b = tk.Button(grid, text="", bg=COLORS["display"],
                              relief="flat", font=("Segoe UI", 22),
                              width=3, height=1,
                              command=lambda x=idx: toggle(x))
                b.grid(row=r, column=c, padx=3, pady=3)
                tiles.append(b)

        status = tk.Label(win, text="", bg=COLORS["bg"], fg=COLORS["danger"],
                          font=("Segoe UI", 9), wraplength=340)
        status.pack(pady=(2, 0))

        def verify():
            result["tries"] += 1
            # Lần đầu luôn báo sai (làm gì có xe buýt thật), lần sau cho qua
            if result["tries"] < 2:
                beep("error")
                shake_window(win)
                status.config(text=random.choice(BUS_CAPTCHA_COMPLAINTS))
                shuffle_tiles()
                win.refit()
                return
            beep("info")
            result["ok"] = True
            win.destroy()

        btn_row = tk.Frame(win, bg=COLORS["bg"])
        btn_row.pack(pady=12)
        tk.Button(btn_row, text="Xác minh", bg=COLORS["accent"], fg=COLORS["bg"],
                  relief="flat", command=verify).pack(side="left", padx=4)

        def deny():
            beep("error")
            shake_window(win)
            status.config(text="Có xe buýt mà, nhìn kỹ lại đi 🚌 (bấm Xác minh nhé)")
            win.refit()

        tk.Button(btn_row, text="Không thấy xe buýt nào", bg=COLORS["key_op"],
                  fg=COLORS["fg"], relief="flat",
                  command=deny).pack(side="left", padx=4)

        shuffle_tiles()
        self.wait_window(win)
        return result["ok"]

    # ---- Bước 5.5: khảo sát (bắt 5 sao) ---- #
    def _step_survey(self):
        win = self._toplevel("Khảo sát mức độ hài lòng", "400x340")

        tk.Label(win, text="Trước khi xem kết quả, hãy đánh giá chúng tôi",
                 bg=COLORS["bg"], fg=COLORS["fg"], font=("Segoe UI", 11, "bold"),
                 wraplength=360).pack(pady=(12, 8))

        star_state = {"n": 0}
        stars_frame = tk.Frame(win, bg=COLORS["bg"])
        stars_frame.pack(pady=4)
        star_btns = []

        def set_stars(n):
            star_state["n"] = n
            for i, b in enumerate(star_btns):
                b.config(text="★" if i < n else "☆",
                         fg=COLORS["warn"] if i < n else COLORS["dim"])

        for i in range(5):
            b = tk.Button(stars_frame, text="☆", bg=COLORS["bg"], fg=COLORS["dim"],
                          font=("Segoe UI", 18), relief="flat", bd=0,
                          activebackground=COLORS["bg"],
                          command=lambda n=i + 1: set_stars(n))
            b.pack(side="left")
            star_btns.append(b)

        question, options = random.choice(SURVEY_QUESTIONS)
        tk.Label(win, text=question, bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 10), wraplength=360).pack(pady=(10, 4))

        answer = tk.StringVar(value="")
        for opt in options:
            tk.Radiobutton(win, text=opt, variable=answer, value=opt,
                           bg=COLORS["bg"], fg=COLORS["fg"], selectcolor=COLORS["key"],
                           activebackground=COLORS["bg"], activeforeground=COLORS["fg"],
                           font=("Segoe UI", 9), anchor="w").pack(fill="x", padx=40)

        result = {"ok": False}

        def submit():
            if star_state["n"] < 5:
                beep("error")
                messagebox.showwarning(
                    "Khảo sát",
                    "Vui lòng đánh giá 5 sao để tiếp tục.\n"
                    "(Đánh giá thấp hơn không được chấp nhận.)", parent=win)
                return
            if not answer.get():
                messagebox.showwarning("Khảo sát",
                                       "Bạn chưa chọn câu trả lời.", parent=win)
                return
            result["ok"] = True
            win.destroy()

        tk.Button(win, text="Gửi đánh giá", bg=COLORS["accent"], fg=COLORS["bg"],
                  relief="flat", command=submit).pack(pady=12, ipadx=10)

        self.wait_window(win)
        return result["ok"]

    # ---- Bước 5.7: quảng cáo video bắt xem hết ---- #
    def _step_video_ad(self):
        win = self._toplevel("Quảng cáo", "420x300")

        title = random.choice(VIDEO_AD_TITLES)
        # "Khung video" giả
        screen = tk.Frame(win, bg="#000000", height=150)
        screen.pack(fill="x", padx=20, pady=(16, 6))
        screen.pack_propagate(False)
        tk.Label(screen, text="▶", bg="#000000", fg=COLORS["fg"],
                 font=("Segoe UI", 30)).pack(expand=True)

        tk.Label(win, text=title, bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 10, "bold")).pack()

        # Nút "Bỏ qua" có đếm ngược, nhưng cứ gần hết lại bị reset vài lần
        skip_state = {"left": 5, "resets": 0}
        result = {"ok": False}

        skip_btn = tk.Button(win, text="", bg=COLORS["key_op"], fg=COLORS["fg"],
                             relief="flat", state="disabled")
        skip_btn.pack(pady=12, ipadx=8)

        def enable_skip():
            skip_btn.config(state="normal", bg=COLORS["accent"], fg=COLORS["bg"],
                            text="Bỏ qua quảng cáo  ✕",
                            command=lambda: (result.update(ok=True), win.destroy()))

        def countdown():
            if not win.winfo_exists():
                return
            if skip_state["left"] > 0:
                skip_btn.config(text=f"Có thể bỏ qua sau {skip_state['left']}s")
                skip_state["left"] -= 1
                win.after(1000, countdown)
            else:
                # Tới 0 thì... reset 2 lần đầu cho cay, lần 3 mới cho bỏ qua
                if skip_state["resets"] < 2:
                    skip_state["resets"] += 1
                    skip_state["left"] = 5
                    beep("warning")
                    skip_btn.config(text="Quảng cáo khác đang tải...")
                    win.after(900, countdown)
                else:
                    enable_skip()

        countdown()
        self.wait_window(win)
        return result["ok"]

    # ---- Bước 5.9: chia sẻ mạng xã hội để mở khoá ---- #
    def _step_social_share(self):
        win = self._toplevel("Chia sẻ để mở khoá", "400x320")

        tk.Label(win, text="Chia sẻ ứng dụng để mở khoá kết quả",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 12, "bold"), wraplength=360).pack(pady=(14, 4))
        tk.Label(win, text="Cần chia sẻ lên ít nhất 1 nền tảng (mà có chia sẻ được đâu).",
                 bg=COLORS["bg"], fg=COLORS["muted"],
                 font=("Segoe UI", 9), wraplength=360).pack(pady=(0, 8))

        result = {"ok": False, "tries": 0}

        def share(msg):
            result["tries"] += 1
            beep("info")
            messagebox.showinfo("Chia sẻ", msg, parent=win)
            # Sau 2 lần thử chia sẻ (đều thất bại) thì cho qua bằng nút bên dưới
            if result["tries"] >= 2:
                cont_btn.config(state="normal", bg=COLORS["ok"], fg=COLORS["bg"],
                                text="Tiếp tục (thôi tha cho bạn)")

        for label, msg in SHARE_PLATFORMS:
            tk.Button(win, text=label, bg=COLORS["blue"], fg=COLORS["bg"],
                      relief="flat", font=("Segoe UI", 10),
                      command=lambda m=msg: share(m)).pack(fill="x", padx=50, pady=3)

        cont_btn = tk.Button(
            win, text="Cần chia sẻ trước đã...", bg=COLORS["key_op"],
            fg=COLORS["dim"], relief="flat", state="disabled",
            command=lambda: (result.update(ok=True), win.destroy()),
        )
        cont_btn.pack(pady=(12, 4), ipadx=8)

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
        label = tk.Label(win, text="", bg=COLORS["bg"], fg=COLORS["fg"],
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

    # ---- Bước 7.5: kiểm tra quyền gói ---- #
    def _operators_used(self):
        """Tập toán tử + - * / trong biểu thức. Bỏ qua dấu '-' của số âm."""
        ops = set()
        expr = self.expression
        for i, ch in enumerate(expr):
            if ch in "+*/":
                ops.add(ch)
            elif ch == "-":
                j = i - 1
                while j >= 0 and expr[j] == " ":
                    j -= 1
                prev = expr[j] if j >= 0 else ""
                if prev.isdigit() or prev == ")" or prev == ".":
                    ops.add("-")
        return ops

    def _step_check_plan_permission(self, plan):
        perm = PLAN_PERMISSIONS.get(plan)
        if perm is None:
            return True

        if plan == "Gói Doanh Nghiệp":
            beep("warning")
            messagebox.showinfo(
                "Calculator",
                "Cảm ơn bạn đã quan tâm Gói Doanh Nghiệp.\n"
                "Bộ phận kinh doanh sẽ liên hệ trong vòng 3-5 ngày làm việc "
                "để kích hoạt tính năng tính toán cho bạn.\n\n"
                "Trong thời gian chờ, vui lòng tính tay.")
            return False

        allowed = perm["allowed"]
        forbidden = self._operators_used() - allowed
        if not forbidden:
            return True

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
            f"Biểu thức của bạn có sử dụng {op_name}.\n{unlocked}{upgrade}")
        return False

    # ---- Bước 8: kết quả sai có chủ đích ---- #
    def _deliver_result(self):
        try:
            true_value = self._safe_eval(self.expression)
        except Exception:
            beep("error")
            messagebox.showerror("Calculator",
                                 "Biểu thức không hợp lệ. Vui lòng kiểm tra lại.")
            return

        wrong_value = self._sabotage(true_value)
        beep("info")
        messagebox.showinfo("Calculator", f"{self.expression} = {wrong_value}")
        self._add_history(self.expression, wrong_value)
        self.expression = self._format(wrong_value)
        self._refresh()

    def _sabotage(self, value):
        """Làm sai tinh vi: lệch nhỏ, không đổi dấu, không về 0, đôi khi đúng."""
        try:
            v = float(value)
        except (TypeError, ValueError):
            return value

        if v == 0:
            return 0

        is_int = float(value).is_integer()
        sign = 1 if v > 0 else -1
        mag = abs(v)
        trick = random.choice(["off_small", "off_small", "tiny_percent", "nice"])

        if trick == "off_small":
            step = random.randint(1, 3)
            delta = min(step, max(1, int(mag * 0.3))) if mag >= 2 else 0
            new_mag = mag + delta * random.choice([-1, 1])
        elif trick == "tiny_percent":
            new_mag = mag * (1 + random.uniform(0.01, 0.05) * random.choice([-1, 1]))
            if is_int:
                new_mag = round(new_mag)
        else:
            new_mag = mag

        if new_mag <= 0:
            new_mag = mag
        v = sign * new_mag

        if is_int and float(v).is_integer():
            return int(v)
        return round(v, 4)

    # ---- Auto re-expire phiên ---- #
    def _schedule_session_expiry(self):
        if self._session_job is not None:
            self.after_cancel(self._session_job)
        self._session_job = self.after(self.SESSION_TTL_MS, self._session_expired)

    def _session_expired(self):
        self._session_job = None
        if self.prank_disabled:
            return
        beep("warning")
        messagebox.showwarning(
            "Calculator",
            "Phiên đăng nhập của bạn đã kết thúc.\n"
            "Vui lòng kích hoạt lại để tiếp tục sử dụng dấu '='.")

    # ---- Thoát app khó ---- #
    def _on_close(self):
        if self.prank_disabled:
            self.destroy()
            return

        self._exit_attempts += 1
        if self._exit_attempts <= len(EXIT_EXCUSES):
            beep("warning")
            excuse = EXIT_EXCUSES[self._exit_attempts - 1]
            stay = messagebox.askretrycancel(
                "Calculator",
                f"{excuse}\n\n(Retry = ở lại, Cancel = vẫn thoát)")
            if stay:
                return
            if self._exit_attempts < len(EXIT_EXCUSES):
                return
        self.destroy()
