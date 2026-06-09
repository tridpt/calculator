"""Các minigame "thử thách" troll mà người dùng phải vượt qua khi bấm '='.

Mixin này được trộn vào lớp Calculator. Mọi game đều THẮNG ĐƯỢC để người
chơi có thể tiến tiếp (vẫn còn lối give-up và phím thoát ẩn nếu nản).
"""

import random
import tkinter as tk
from tkinter import messagebox

from .config import COLORS
from .platform_utils import beep

class MinigameMixin:
    """Cổng minigame: chọn ngẫu nhiên 1 game, trả True nếu vượt qua."""

    def _step_minigame(self):
        game = random.choice([
            self._minigame_charge,
            self._minigame_catch_button,
            self._minigame_guess_number,
            self._minigame_whack_mole,
            self._minigame_type_spell,
            self._minigame_timing_bar,
            self._minigame_simon,
        ])
        return game()

    # ---- Game 1: sạc năng lượng (bấm nhanh, pin tự rò rỉ) ---- #
    def _minigame_charge(self):
        win = self._toplevel("Xác minh: Sạc năng lượng", "400x280")

        tk.Label(win, text="🔋 Sạc năng lượng cho máy chủ tính toán",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 12, "bold"), wraplength=360).pack(pady=(14, 4))
        tk.Label(win, text="Bấm thật nhanh để nạp đầy 100%.",
                 bg=COLORS["bg"], fg=COLORS["muted"],
                 font=("Segoe UI", 9)).pack()

        from tkinter import ttk
        bar = ttk.Progressbar(win, mode="determinate", length=320, maximum=100)
        bar.pack(pady=12)

        pct = tk.Label(win, text="0%", bg=COLORS["bg"], fg=COLORS["warn"],
                       font=("Segoe UI", 11, "bold"))
        pct.pack()

        state = {"charge": 0.0, "done": False}
        result = {"ok": False}

        def update_bar():
            bar["value"] = max(0, min(100, state["charge"]))
            pct.config(text=f"{int(max(0, min(100, state['charge'])))}%")

        def leak():
            # Pin tự rò rỉ để phải bấm liên tục, nhưng rò ít hơn 1 cú bấm
            if state["done"] or not win.winfo_exists():
                return
            state["charge"] = max(0, state["charge"] - 2.5)
            update_bar()
            win.after(250, leak)

        def click():
            if state["done"]:
                return
            state["charge"] += 9  # 1 cú bấm > tốc độ rò -> vẫn thắng được
            update_bar()
            if state["charge"] >= 100:
                state["done"] = True
                result["ok"] = True
                beep("info")
                win.destroy()

        tk.Button(win, text="⚡ SẠC ⚡", bg=COLORS["accent"], fg=COLORS["bg"],
                  relief="flat", font=("Segoe UI", 13, "bold"),
                  command=click).pack(pady=10, ipadx=24, ipady=6)

        leak()
        self.wait_window(win)
        return result["ok"]

    # ---- Game 2: bắt cái nút chạy trốn ---- #
    def _minigame_catch_button(self):
        win = self._toplevel("Xác minh: Bắt mục tiêu", "420x320")

        tk.Label(win, text="🎯 Bấm trúng nút 5 lần để chứng minh bạn không phải robot",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 11, "bold"), wraplength=380).pack(pady=(12, 4))

        counter = tk.Label(win, text="Đã bắt: 0 / 5", bg=COLORS["bg"],
                           fg=COLORS["warn"], font=("Segoe UI", 10, "bold"))
        counter.pack(pady=2)

        arena = tk.Frame(win, bg=COLORS["panel"], height=200)
        arena.pack(fill="both", expand=True, padx=16, pady=10)
        arena.pack_propagate(False)

        state = {"hits": 0}
        result = {"ok": False}

        btn = tk.Button(arena, text="BẮT TÔI!", bg=COLORS["danger"],
                        fg=COLORS["bg"], relief="flat", font=("Segoe UI", 10, "bold"))

        def move():
            arena.update_idletasks()
            aw = arena.winfo_width() or 380
            ah = arena.winfo_height() or 180
            bw, bh = 90, 36
            x = random.randint(0, max(0, aw - bw))
            y = random.randint(0, max(0, ah - bh))
            btn.place(x=x, y=y, width=bw, height=bh)

        def hit():
            state["hits"] += 1
            counter.config(text=f"Đã bắt: {state['hits']} / 5")
            beep("info")
            if state["hits"] >= 5:
                result["ok"] = True
                win.destroy()
            else:
                move()

        btn.config(command=hit)
        move()
        self.wait_window(win)
        return result["ok"]

    # ---- Game 3: đoán số bí mật (sai nhiều thì cho qua) ---- #
    def _minigame_guess_number(self):
        win = self._toplevel("Xác minh: Đoán số", "380x260")

        secret = {"n": random.randint(1, 5)}
        tk.Label(win, text="🔢 Đoán con số bí mật từ 1 đến 5",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 12, "bold")).pack(pady=(14, 6))

        hint = tk.Label(win, text="Bạn có vài lần thử...", bg=COLORS["bg"],
                        fg=COLORS["muted"], font=("Segoe UI", 9))
        hint.pack()

        state = {"tries": 0}
        result = {"ok": False}
        row = tk.Frame(win, bg=COLORS["bg"])
        row.pack(pady=14)

        def guess(n):
            state["tries"] += 1
            if n == secret["n"]:
                beep("info")
                result["ok"] = True
                win.destroy()
                return
            beep("error")
            # Sau 3 lần sai thì "thương tình" cho qua (tránh kẹt vĩnh viễn)
            if state["tries"] >= 3:
                hint.config(text="Thôi được rồi, cho bạn qua vậy 🙄")
                result["ok"] = True
                win.after(800, win.destroy)
                return
            # Gợi ý sai lệch cho cay
            direction = "cao hơn" if n < secret["n"] else "thấp hơn"
            if random.random() < 0.4:  # 40% gợi ý sai
                direction = "thấp hơn" if direction == "cao hơn" else "cao hơn"
            hint.config(text=f"Sai rồi! Thử số {direction} xem (gợi ý có thể sai).")

        for n in range(1, 6):
            tk.Button(row, text=str(n), bg=COLORS["blue"], fg=COLORS["bg"],
                      relief="flat", font=("Segoe UI", 12, "bold"), width=3,
                      command=lambda x=n: guess(x)).pack(side="left", padx=4)

        self.wait_window(win)
        return result["ok"]

    # ---- Game 4: đập chuột chũi (đập đủ số con trong thời gian) ---- #
    def _minigame_whack_mole(self):
        win = self._toplevel("Xác minh: Đập chuột chũi", "420x360")

        need = 8
        tk.Label(win, text="🔨 Đập đủ 8 con chuột chũi để tiếp tục",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 11, "bold"), wraplength=380).pack(pady=(12, 2))

        info = tk.Label(win, text=f"Đã đập: 0 / {need}   |   Thời gian: 20s",
                        bg=COLORS["bg"], fg=COLORS["warn"],
                        font=("Segoe UI", 10, "bold"))
        info.pack(pady=2)

        grid = tk.Frame(win, bg=COLORS["panel"])
        grid.pack(fill="both", expand=True, padx=16, pady=10)

        holes = []
        for r in range(3):
            grid.grid_rowconfigure(r, weight=1)
            for col in range(3):
                grid.grid_columnconfigure(col, weight=1)
                b = tk.Button(grid, text="", bg=COLORS["key"], fg=COLORS["bg"],
                              relief="flat", font=("Segoe UI", 18))
                b.grid(row=r, column=col, padx=4, pady=4, sticky="nsew")
                holes.append(b)

        state = {"hits": 0, "time": 20, "active": None, "done": False}
        result = {"ok": False}

        def clear_holes():
            for b in holes:
                b.config(text="", bg=COLORS["key"], command=lambda: None)

        def pop():
            if state["done"] or not win.winfo_exists():
                return
            clear_holes()
            idx = random.randrange(len(holes))
            state["active"] = idx

            def whack():
                if state["active"] != idx or state["done"]:
                    return
                state["hits"] += 1
                state["active"] = None
                beep("info")
                holes[idx].config(text="💥", bg=COLORS["danger"])
                info.config(text=f"Đã đập: {state['hits']} / {need}   |   "
                                 f"Thời gian: {state['time']}s")
                if state["hits"] >= need:
                    state["done"] = True
                    result["ok"] = True
                    win.after(300, win.destroy)

            holes[idx].config(text="🐹", bg=COLORS["ok"], command=whack)
            win.after(random.randint(600, 1000), pop)

        def timer():
            if state["done"] or not win.winfo_exists():
                return
            state["time"] -= 1
            info.config(text=f"Đã đập: {state['hits']} / {need}   |   "
                             f"Thời gian: {state['time']}s")
            if state["time"] <= 0:
                # Hết giờ mà chưa đủ -> "gia hạn" thêm cho qua được (không kẹt)
                if state["hits"] < need:
                    state["time"] = 15
                    info.config(text="Gia hạn thêm 15s vì bạn đập hơi chậm 🐢")
                win.after(1000, timer)
            else:
                win.after(1000, timer)

        pop()
        timer()
        self.wait_window(win)
        return result["ok"]

    # ---- Game 5: gõ đúng câu thần chú ---- #
    def _minigame_type_spell(self):
        from .config import SPELL_PHRASES
        win = self._toplevel("Xác minh: Gõ câu thần chú", "440x300")

        spell = random.choice(SPELL_PHRASES)

        tk.Label(win, text="⌨️ Gõ lại chính xác câu sau (không sai ký tự nào):",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 11, "bold"), wraplength=400).pack(pady=(12, 6))

        tk.Label(win, text=f"\u201c{spell}\u201d", bg=COLORS["display"],
                 fg=COLORS["warn"], font=("Consolas", 12, "bold"),
                 wraplength=400, padx=10, pady=8).pack(fill="x", padx=20)

        entry = tk.Entry(win, bg=COLORS["display"], fg=COLORS["fg"],
                         relief="flat", insertbackground=COLORS["fg"],
                         font=("Consolas", 12))
        entry.pack(fill="x", padx=20, pady=10, ipady=6)

        status = tk.Label(win, text="", bg=COLORS["bg"], fg=COLORS["danger"],
                          font=("Segoe UI", 9), wraplength=400)
        status.pack()

        state = {"tries": 0}
        result = {"ok": False}
        helper = {}

        def check():
            state["tries"] += 1
            typed = entry.get()
            if typed == spell:
                beep("info")
                result["ok"] = True
                win.destroy()
                return
            beep("error")
            # Tìm vị trí sai đầu tiên cho cay
            pos = 0
            for a, b in zip(typed, spell):
                if a != b:
                    break
                pos += 1
            status.config(text=f"Sai ở ký tự thứ {pos + 1}. Thử lại nhé.")
            # Sau 3 lần sai thì hiện nút "điền giùm"
            if state["tries"] >= 3 and "btn" not in helper:
                def autofill():
                    entry.delete(0, tk.END)
                    entry.insert(0, spell)
                    status.config(text="Đã điền giùm. Bấm Xác nhận đi.",
                                  fg=COLORS["muted"])
                helper["btn"] = tk.Button(win, text="Điền giùm tôi 🙏",
                                          bg=COLORS["key_op"], fg=COLORS["fg"],
                                          relief="flat", command=autofill)
                helper["btn"].pack(pady=2)

        tk.Button(win, text="Xác nhận", bg=COLORS["accent"], fg=COLORS["bg"],
                  relief="flat", command=check).pack(pady=8, ipadx=10)

        self.wait_window(win)
        return result["ok"]

    # ---- Game 6: QTE - dừng thanh con trỏ ở vùng xanh ---- #
    def _minigame_timing_bar(self):
        win = self._toplevel("Xác minh: Canh thời điểm", "440x280")

        tk.Label(win, text="🎯 Bấm STOP khi vạch chạy vào vùng xanh",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 11, "bold"), wraplength=400).pack(pady=(14, 6))

        info = tk.Label(win, text="Cần trúng 3 lần", bg=COLORS["bg"],
                        fg=COLORS["warn"], font=("Segoe UI", 10, "bold"))
        info.pack(pady=2)

        canvas_w, canvas_h = 380, 50
        canvas = tk.Canvas(win, width=canvas_w, height=canvas_h,
                           bg=COLORS["display"], highlightthickness=0)
        canvas.pack(pady=12)

        # Vùng xanh ở giữa
        zone_w = 90
        zone_x0 = (canvas_w - zone_w) // 2
        zone_x1 = zone_x0 + zone_w
        zone_id = canvas.create_rectangle(zone_x0, 0, zone_x1, canvas_h,
                                          fill=COLORS["ok"], outline="")
        cursor = canvas.create_rectangle(0, 0, 6, canvas_h,
                                         fill=COLORS["danger"], outline="")

        state = {"x": 0.0, "dir": 1, "hits": 0, "speed": 7, "running": True,
                 "zx0": zone_x0, "zx1": zone_x1}
        result = {"ok": False}

        def animate():
            if not state["running"] or not win.winfo_exists():
                return
            state["x"] += state["dir"] * state["speed"]
            if state["x"] >= canvas_w - 6:
                state["x"] = canvas_w - 6
                state["dir"] = -1
            elif state["x"] <= 0:
                state["x"] = 0
                state["dir"] = 1
            canvas.coords(cursor, state["x"], 0, state["x"] + 6, canvas_h)
            win.after(16, animate)

        def stop():
            cx = state["x"] + 3
            if state["zx0"] <= cx <= state["zx1"]:
                state["hits"] += 1
                beep("info")
                if state["hits"] >= 3:
                    result["ok"] = True
                    state["running"] = False
                    win.destroy()
                    return
                info.config(text=f"Trúng! {state['hits']} / 3 - vùng xanh hẹp lại 😈")
                # Vùng xanh hẹp dần cho khó (nhưng vẫn trúng được)
                new_zone = max(40, zone_w - state["hits"] * 12)
                nx0 = (canvas_w - new_zone) // 2
                nx1 = nx0 + new_zone
                state["zx0"], state["zx1"] = nx0, nx1
                canvas.coords(zone_id, nx0, 0, nx1, canvas_h)
            else:
                beep("error")
                info.config(text=f"Hụt! Vẫn {state['hits']} / 3. Bình tĩnh lại nào.")

        tk.Button(win, text="STOP", bg=COLORS["accent"], fg=COLORS["bg"],
                  relief="flat", font=("Segoe UI", 13, "bold"),
                  command=stop).pack(pady=4, ipadx=24, ipady=4)

        animate()
        self.wait_window(win)
        return result["ok"]

    # ---- Game 7: Simon - nhớ và lặp lại chuỗi đèn sáng ---- #
    def _minigame_simon(self):
        win = self._toplevel("Xác minh: Lặp lại giai điệu", "380x400")

        tk.Label(win, text="🎵 Nhớ thứ tự các ô sáng rồi bấm lại cho đúng",
                 bg=COLORS["bg"], fg=COLORS["fg"],
                 font=("Segoe UI", 11, "bold"), wraplength=340).pack(pady=(14, 4))

        status = tk.Label(win, text="Xem kỹ nhé...", bg=COLORS["bg"],
                          fg=COLORS["warn"], font=("Segoe UI", 10, "bold"))
        status.pack(pady=2)

        pad_colors = [COLORS["ok"], COLORS["blue"], COLORS["warn"], COLORS["danger"]]
        grid = tk.Frame(win, bg=COLORS["bg"])
        grid.pack(pady=16)

        pads = []
        state = {"seq": [], "input": [], "tries": 0, "locked": True}
        result = {"ok": False}

        def light(idx, ms=380, after=None):
            if not win.winfo_exists():
                return
            pads[idx].config(bg=pad_colors[idx])
            beep("info")

            def restore():
                if win.winfo_exists():
                    pads[idx].config(bg=COLORS["key"])
                if after:
                    after()

            win.after(ms, restore)

        def play(i=0):
            if not win.winfo_exists():
                return
            if i >= len(state["seq"]):
                state["locked"] = False
                status.config(text="Tới lượt bạn! Bấm lại đúng thứ tự.",
                              fg=COLORS["ok"])
                return
            light(state["seq"][i], ms=400,
                  after=lambda: win.after(200, lambda: play(i + 1)))

        def new_round():
            if not win.winfo_exists():
                return
            state["input"] = []
            state["locked"] = True
            state["seq"] = [random.randrange(4) for _ in range(3)]
            status.config(text="Xem kỹ nhé...", fg=COLORS["warn"])
            win.after(500, play)

        def press(idx):
            if state["locked"]:
                return
            light(idx, ms=200)
            state["input"].append(idx)
            n = len(state["input"])
            if state["input"][n - 1] != state["seq"][n - 1]:
                state["tries"] += 1
                beep("error")
                if state["tries"] >= 3:
                    status.config(text="Thôi cho bạn qua vậy 🙄", fg=COLORS["ok"])
                    result["ok"] = True
                    win.after(800, win.destroy)
                    return
                status.config(text=f"Sai rồi! Thử lại ({state['tries']}/3).",
                              fg=COLORS["danger"])
                state["locked"] = True
                win.after(900, new_round)
                return
            if n == len(state["seq"]):
                beep("info")
                status.config(text="Chuẩn không cần chỉnh! ✅", fg=COLORS["ok"])
                result["ok"] = True
                win.after(400, win.destroy)

        for i in range(4):
            b = tk.Button(grid, bg=COLORS["key"], relief="flat",
                          width=10, height=4,
                          activebackground=pad_colors[i],
                          command=lambda x=i: press(x))
            b.grid(row=i // 2, column=i % 2, padx=6, pady=6)
            pads.append(b)

        new_round()
        self.wait_window(win)
        return result["ok"]
