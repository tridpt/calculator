"""Lớp ứng dụng chính - ghép phần lõi máy tính và phần troll."""

import tkinter as tk

from .config import COLORS
from .core import CoreCalculatorMixin
from .minigames import MinigameMixin
from .troll import TrollMixin


class Calculator(CoreCalculatorMixin, TrollMixin, MinigameMixin, tk.Tk):
    """Máy tính troll. Lõi máy tính ở CoreCalculatorMixin, troll ở TrollMixin,
    minigame thử thách ở MinigameMixin."""

    SESSION_TTL_MS = 90_000  # 90s sau "kích hoạt" thì phiên hết hạn

    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("660x720")
        self.minsize(480, 600)
        self.configure(bg=COLORS["bg"])
        self._set_icon()

        # Trạng thái
        self.expression = ""
        self.memory = 0.0
        self.history = []
        self.show_history = False
        self.equals_attempts = 0
        self.give_ups = 0
        self.revealed = False
        self.prank_disabled = False
        self._session_job = None
        self._exit_attempts = 0
        self.debt = 0

        self._build_ui()
        self._bind_keys()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        # Cập nhật bắt buộc giả lúc mở app
        self.after(400, self._step_force_update)
