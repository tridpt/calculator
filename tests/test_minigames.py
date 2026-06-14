"""Test phần minigame và hiệu ứng (âm thanh/pháo giấy).

Các minigame chạy bằng wait_window (chặn luồng) nên không test trực tiếp
vòng chơi được. Thay vào đó test các "mối nối" có thể kiểm chứng:
- danh sách game được chọn ngẫu nhiên (roster)
- helper _celebrate không gây lỗi
- các hiệu ứng trong platform_utils chạy an toàn trên cửa sổ thật và
  cả khi cửa sổ đã bị đóng.
"""

import tkinter as tk

from calc import platform_utils


def _capture_roster(app, monkeypatch):
    """Bắt lấy danh sách game mà _step_minigame truyền cho random.choice."""
    captured = {}

    def fake_choice(seq):
        captured["games"] = list(seq)
        # Trả về 1 stub không mở cửa sổ để _step_minigame kết thúc ngay
        return lambda: True

    monkeypatch.setattr("calc.minigames.random.choice", fake_choice)
    result = app._step_minigame()
    return captured.get("games", []), result


def test_minigame_roster_has_nine_unique_games(app, monkeypatch):
    games, result = _capture_roster(app, monkeypatch)
    assert len(games) == 9
    # Mỗi game là một callable (bound method) và không trùng nhau
    assert all(callable(g) for g in games)
    assert len({g.__name__ for g in games}) == 9
    # Stub trả True -> _step_minigame trả True
    assert result is True


def test_spot_difference_method_exists(app):
    # Game thứ 8 phải tồn tại và gọi được
    assert hasattr(app, "_minigame_spot_difference")
    assert callable(app._minigame_spot_difference)


def test_dodge_method_exists(app):
    # Game thứ 9 phải tồn tại và gọi được
    assert hasattr(app, "_minigame_dodge")
    assert callable(app._minigame_dodge)


def test_celebrate_no_crash(app):
    win = tk.Toplevel(app)
    win.geometry("300x200")
    app.update_idletasks()
    # Không được ném lỗi dù chạy nhạc + pháo giấy
    app._celebrate(win)
    app.update_idletasks()
    win.destroy()


# ----- platform_utils: hiệu ứng phải an toàn ----- #

def test_play_tune_no_crash():
    # Tên hợp lệ và tên rác đều không được ném lỗi
    platform_utils.play_tune("win")
    platform_utils.play_tune("khong_ton_tai")


def test_beep_no_crash():
    for kind in ["warning", "error", "info", "linh_tinh"]:
        platform_utils.beep(kind)


def test_confetti_no_crash_on_live_window(app):
    win = tk.Toplevel(app)
    win.geometry("320x240")
    app.update_idletasks()
    platform_utils.confetti(win, count=10, duration=120)
    app.update_idletasks()
    win.destroy()


def test_confetti_safe_on_destroyed_window(app):
    win = tk.Toplevel(app)
    win.destroy()
    # Cửa sổ đã đóng -> phải thoát êm, không ném lỗi
    platform_utils.confetti(win)


def test_shake_and_flash_no_crash(app):
    win = tk.Toplevel(app)
    win.geometry("320x240")
    app.update_idletasks()
    platform_utils.shake_window(win, times=2, delay=1)
    platform_utils.flash_window(win, times=2, delay=1)
    app.update_idletasks()
    win.destroy()


def test_effects_safe_on_destroyed_window(app):
    win = tk.Toplevel(app)
    win.destroy()
    platform_utils.shake_window(win)
    platform_utils.flash_window(win)
