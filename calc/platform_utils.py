"""Tiện ích phụ thuộc hệ điều hành: DPI awareness và âm thanh cảnh báo."""

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
