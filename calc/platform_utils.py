"""Tiện ích phụ thuộc hệ điều hành: DPI awareness và âm thanh cảnh báo."""

import re
import sys


def enable_dpi_awareness():
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

    # Vài "giai điệu" ngắn (tần số Hz, thời lượng ms) cho thêm phần sinh động.
    _TUNES = {
        "win":   [(660, 90), (880, 90), (1175, 160)],   # thắng minigame - đi lên
        "fail":  [(440, 120), (330, 120), (220, 200)],  # thất bại - đi xuống
        "coin":  [(988, 70), (1319, 140)],              # leng keng kiểu game
        "alert": [(700, 80), (700, 80)],                # tít tít cảnh báo
    }

    def play_tune(name="win"):
        """Phát một giai điệu ngắn không chặn luồng (chạy ở thread riêng)."""
        notes = _TUNES.get(name)
        if not notes:
            return

        def _run():
            for freq, dur in notes:
                try:
                    winsound.Beep(int(freq), int(dur))
                except Exception:
                    break

        try:
            import threading
            threading.Thread(target=_run, daemon=True).start()
        except Exception:
            pass

except ImportError:
    def beep(kind="warning"):
        pass

    def play_tune(name="win"):
        pass


_GEO_RE = re.compile(r"(\d+)x(\d+)\+(-?\d+)\+(-?\d+)")


def shake_window(win, intensity=12, times=8, delay=26):
    """Rung cửa sổ qua lại theo chiều ngang (hiệu ứng "lắc đầu" khi báo lỗi)."""
    try:
        if not win.winfo_exists():
            return
        win.update_idletasks()
        m = _GEO_RE.match(win.geometry())
    except Exception:
        return
    if not m:
        return
    w, h, x, y = (int(g) for g in m.groups())
    offsets = [intensity if i % 2 == 0 else -intensity for i in range(times)]
    offsets.append(0)

    def step(i=0):
        try:
            if not win.winfo_exists() or i >= len(offsets):
                if win.winfo_exists():
                    win.geometry(f"{w}x{h}+{x}+{y}")
                return
            win.geometry(f"{w}x{h}+{x + offsets[i]}+{y}")
            win.after(delay, lambda: step(i + 1))
        except Exception:
            pass

    step()


def flash_window(win, color="#f38ba8", times=4, delay=70):
    """Nháy nền cửa sổ vài lần (hiệu ứng cảnh báo nhấp nháy)."""
    try:
        if not win.winfo_exists():
            return
        orig = win.cget("bg")
    except Exception:
        return
    seq = [color if i % 2 == 0 else orig for i in range(times)]
    seq.append(orig)

    def step(i=0):
        try:
            if not win.winfo_exists() or i >= len(seq):
                return
            win.configure(bg=seq[i])
            win.after(delay, lambda: step(i + 1))
        except Exception:
            pass

    step()


def confetti(win, colors=None, count=24, duration=1400):
    """Bắn pháo giấy ăn mừng trên một Canvas phủ kín cửa sổ.

    Tạo một Canvas trong suốt (nền theo win) rồi cho các chấm màu rơi xuống.
    Tự dọn Canvas sau `duration` ms. An toàn nếu cửa sổ bị đóng giữa chừng.
    """
    import random
    try:
        if not win.winfo_exists():
            return
        import tkinter as tk
    except Exception:
        return
    colors = colors or ["#f38ba8", "#f9e2af", "#a6e3a1", "#89b4fa", "#cba6f7", "#fab387"]
    try:
        win.update_idletasks()
        w = max(win.winfo_width(), 200)
        h = max(win.winfo_height(), 200)
        bg = win.cget("bg")
    except Exception:
        return

    canvas = tk.Canvas(win, width=w, height=h, bg=bg, highlightthickness=0)
    canvas.place(x=0, y=0)

    pieces = []
    for _ in range(count):
        x = random.randint(0, w)
        y = random.randint(-h, 0)
        size = random.randint(5, 11)
        color = random.choice(colors)
        vy = random.uniform(4, 9)
        vx = random.uniform(-2, 2)
        item = canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
        pieces.append([item, vx, vy])

    state = {"ticks": 0, "max": max(1, duration // 30)}

    def fall():
        if not win.winfo_exists() or not canvas.winfo_exists():
            return
        if state["ticks"] >= state["max"]:
            try:
                canvas.destroy()
            except Exception:
                pass
            return
        for p in pieces:
            try:
                canvas.move(p[0], p[1], p[2])
            except Exception:
                pass
        state["ticks"] += 1
        canvas.after(30, fall)

    fall()
