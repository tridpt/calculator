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

except ImportError:
    def beep(kind="warning"):
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
