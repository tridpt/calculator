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
        win = self._toplevel("Xác minh: Gõ câu thần chú", "440x300")

        spells = [
            "toi khong phai robot",
            "may tinh nay tinh dung",
            "xin hay cho toi tinh toan",
            "9 cong 10 bang 21",
        ]
        spell = random.choice(spells)

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
