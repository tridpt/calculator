"""Phần lõi của máy tính: giao diện bàn phím, hiển thị, bộ nhớ, lịch sử, eval.

Đây là mixin - được trộn vào lớp Calculator (kế thừa tk.Tk) trong app.py.
Các thuộc tính như self.expression, self.memory... được khởi tạo ở app.py.
"""

import os
import sys
import tkinter as tk

from .config import COLORS


class CoreCalculatorMixin:
    """Chức năng máy tính thật: nhập liệu, bàn phím, bộ nhớ, lịch sử."""

    # ------------------------------ Icon ------------------------------ #

    def _set_icon(self):
        """Gắn icon cho cửa sổ. Hoạt động cả khi chạy .py và khi đóng gói .exe."""
        base = getattr(sys, "_MEIPASS", None)
        if base is None:
            # icon.ico nằm ở thư mục gốc dự án (cha của package calc/)
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ico = os.path.join(base, "icon.ico")
        try:
            if os.path.exists(ico):
                self.iconbitmap(ico)
                return
        except Exception:
            pass
        png = os.path.join(base, "icon.png")
        try:
            if os.path.exists(png):
                self._icon_img = tk.PhotoImage(file=png)
                self.iconphoto(True, self._icon_img)
        except Exception:
            pass

    # ------------------------------ UI ------------------------------- #

    def _build_ui(self):
        c = COLORS
        topbar = tk.Frame(self, bg=c["bg"])
        topbar.pack(fill="x", padx=10, pady=(8, 0))

        self.menu_btn = tk.Button(
            topbar, text="≡", bg=c["bg"], fg=c["fg"],
            font=("Segoe UI", 12), relief="flat", bd=0,
            activebackground=c["key"],
            command=self._toggle_history,
        )
        self.menu_btn.pack(side="left")
        tk.Label(topbar, text="Standard", bg=c["bg"], fg=c["fg"],
                 font=("Segoe UI", 10)).pack(side="left", padx=8)

        main = tk.Frame(self, bg=c["bg"])
        main.pack(fill="both", expand=True, padx=10, pady=8)

        self.left = tk.Frame(main, bg=c["bg"])
        self.left.pack(side="left", fill="both", expand=True)

        self.right = tk.Frame(main, bg=c["panel"])  # history panel, ẩn cho tới khi toggle

        # --- Display --- #
        self.display = tk.Entry(
            self.left, font=("Consolas", 24), justify="right",
            bg=c["display"], fg=c["fg"],
            insertbackground=c["fg"], relief="flat", bd=10,
            state="readonly", readonlybackground=c["display"],
            disabledforeground=c["fg"],
        )
        self.display.pack(fill="x", pady=(2, 8), ipady=12)

        # --- Memory row --- #
        mem = tk.Frame(self.left, bg=c["bg"])
        mem.pack(fill="x", pady=(0, 4))
        for label in ["MC", "MR", "M+", "M-", "MS"]:
            tk.Button(
                mem, text=label, bg=c["bg"], fg=c["muted"],
                relief="flat", font=("Segoe UI", 9),
                activebackground=c["key"],
                command=lambda l=label: self._on_memory(l),
            ).pack(side="left", expand=True, fill="x", padx=1)

        # --- Bàn phím --- #
        keypad = tk.Frame(self.left, bg=c["bg"])
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
            for col, label in enumerate(row):
                keypad.grid_columnconfigure(col, weight=1)
                self._make_button(keypad, label, r, col)

        # --- History panel --- #
        tk.Label(self.right, text="Lịch sử", bg=c["panel"], fg=c["fg"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(8, 4))

        self.history_box = tk.Listbox(
            self.right, bg=c["panel"], fg=c["fg"],
            selectbackground=c["key_op"], selectforeground=c["fg"],
            font=("Consolas", 10), relief="flat", bd=0, width=22,
            activestyle="none",
        )
        self.history_box.pack(fill="both", expand=True, padx=8, pady=4)
        self.history_box.bind("<Double-Button-1>", self._reuse_history)

        tk.Button(
            self.right, text="Xoá lịch sử", bg=c["panel"], fg=c["muted"],
            relief="flat", font=("Segoe UI", 9),
            activebackground=c["key"],
            command=self._clear_history,
        ).pack(fill="x", padx=8, pady=(0, 8))

        # --- Thanh trạng thái "nợ phí" ở đáy --- #
        self.debt_label = tk.Label(
            self, text="Dư nợ phí dịch vụ: 0đ", bg=c["panel"], fg=c["dim"],
            font=("Segoe UI", 8), anchor="e",
        )
        self.debt_label.pack(side="bottom", fill="x")

    def _make_button(self, parent, label, r, col):
        c = COLORS
        op_chars = {"+", "-", "*", "/", "(", ")"}
        if label == "=":
            bg, fg = c["accent"], c["bg"]
        elif label in ("C", "⌫") or label in op_chars:
            bg, fg = c["key_op"], c["fg"]
        else:
            bg, fg = c["key"], c["fg"]

        btn = tk.Button(
            parent, text=label, font=("Segoe UI", 12, "bold"),
            bg=bg, fg=fg, relief="flat",
            activebackground=c["active"],
            command=lambda l=label: self._on_press(l),
        )
        btn.grid(row=r, column=col, padx=3, pady=3, sticky="nsew")

    # ------------------------- Keyboard ------------------------------ #

    def _bind_keys(self):
        self.bind("<Return>",    self._key_eq)
        self.bind("<KP_Enter>",  self._key_eq)
        self.bind("<Escape>",    self._key_clear)
        self.bind("<BackSpace>", self._key_back)
        for ch in "0123456789+-*/().":
            self.bind(ch, lambda e, c=ch: self._key_char(c))

    def _focus_in_popup(self):
        """True nếu con trỏ đang ở Entry/Text của popup -> không can thiệp máy tính chính."""
        try:
            w = self.focus_get()
        except KeyError:
            return False
        if w is None or w is self.display:
            return False
        return isinstance(w, (tk.Entry, tk.Text))

    def _key_eq(self, _e):
        if not self._focus_in_popup():
            self._on_press("=")

    def _key_clear(self, _e):
        if not self._focus_in_popup():
            self._on_press("C")

    def _key_back(self, _e):
        if not self._focus_in_popup():
            self._on_press("⌫")

    def _key_char(self, ch):
        if not self._focus_in_popup():
            self._on_press(ch)

    # -------------------------- History ------------------------------ #

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

    # --------------------------- Memory ------------------------------ #

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

    # ------------------------- Input core ---------------------------- #

    def _on_press(self, key):
        if key == "C":
            self.expression = ""
        elif key == "⌫":
            self.expression = self.expression[:-1]
        elif key == "=":
            self._handle_equals()   # định nghĩa ở TrollMixin
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

    # --------------------- Kết quả chế độ thật ----------------------- #

    def _deliver_real_result(self):
        """Tính đúng, không phá (dùng sau khi đã 'tự thú')."""
        from tkinter import messagebox
        from .platform_utils import beep
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

    # ---------------------- Cửa sổ con (helper) ---------------------- #

    def _toplevel(self, title, size, grab=True):
        win = tk.Toplevel(self)
        win.title(title)
        win.configure(bg=COLORS["bg"])
        win.transient(self)

        # size "WxH" làm kích thước TỐI THIỂU.
        try:
            min_w, min_h = (int(x) for x in size.lower().split("x"))
        except Exception:
            min_w, min_h = 360, 240
        win.geometry(f"{min_w}x{min_h}")

        if grab:
            win.grab_set()

        # Tự co giãn vừa khít nội dung rồi canh giữa (khắc phục cắt nội dung khi DPI scaling).
        def _fit():
            if not win.winfo_exists():
                return
            win.update_idletasks()
            w = max(min_w, win.winfo_reqwidth())
            h = max(min_h, win.winfo_reqheight())
            sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
            w = min(w, sw - 40)
            h = min(h, sh - 80)
            x = (sw - w) // 2
            y = max(20, (sh - h) // 3)
            win.geometry(f"{w}x{h}+{x}+{y}")
            win.minsize(w, h)

        win.after(60, _fit)
        return win

    # ------------------------- Debt counter -------------------------- #

    def _update_debt(self, amount):
        """Tăng 'nợ phí' và cập nhật thanh trạng thái."""
        self.debt += amount
        if hasattr(self, "debt_label"):
            color = COLORS["danger"] if self.debt > 0 else COLORS["dim"]
            self.debt_label.config(
                text=f"Dư nợ phí dịch vụ: {self.debt:,}đ".replace(",", "."),
                fg=color,
            )
