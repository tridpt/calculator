"""Fixtures dùng chung cho test suite.

Tkinter không thích tạo/destroy nhiều tk.Tk() trong cùng một process
(dễ ném TclError ngẫu nhiên). Vì vậy ta tạo MỘT instance Calculator cho
cả phiên test (session-scoped) và reset trạng thái trước mỗi test.
"""

import sys
import os

import pytest

# Cho phép import package calc khi chạy pytest từ thư mục gốc dự án
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _close_toplevels(instance):
    import tkinter as tk
    for w in instance.winfo_children():
        if isinstance(w, tk.Toplevel):
            try:
                w.destroy()
            except Exception:
                pass


@pytest.fixture(scope="session")
def _root():
    """Một Calculator duy nhất dùng chung cho cả phiên test."""
    try:
        import tkinter as tk
    except Exception:
        pytest.skip("tkinter không khả dụng")

    from calc import Calculator
    try:
        instance = Calculator()
    except tk.TclError:
        pytest.skip("không có màn hình (headless), bỏ qua test GUI")

    instance.update_idletasks()
    instance.update()
    _close_toplevels(instance)
    yield instance
    try:
        instance.destroy()
    except Exception:
        pass


@pytest.fixture
def app(_root):
    """Reset trạng thái Calculator về mặc định trước mỗi test."""
    _close_toplevels(_root)
    _root.expression = ""
    _root.memory = 0.0
    _root.history = []
    _root.history_box.delete(0, "end")
    _root.show_history = False
    _root.equals_attempts = 0
    _root.give_ups = 0
    _root.revealed = False
    _root.prank_disabled = False
    _root._exit_attempts = 0
    _root.debt = 0
    _root._update_debt(0)
    _root._refresh()
    return _root
