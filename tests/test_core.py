"""Test phần lõi máy tính: eval, format, nhập liệu, bộ nhớ, lịch sử, nợ phí."""

from calc.app import Calculator


# ----- Các hàm tĩnh: không cần GUI ----- #

def test_safe_eval_basic():
    assert Calculator._safe_eval("1+2") == 3
    assert Calculator._safe_eval("2*3-4") == 2
    assert Calculator._safe_eval("(1+2)*3") == 9


def test_safe_eval_empty():
    assert Calculator._safe_eval("") is None
    assert Calculator._safe_eval("   ") is None


def test_safe_eval_blocks_builtins():
    # __builtins__ bị chặn -> không gọi được hàm nguy hiểm
    import pytest
    with pytest.raises(Exception):
        Calculator._safe_eval("__import__('os').getcwd()")


def test_format_integer_and_float():
    assert Calculator._format(42.0) == "42"
    assert Calculator._format(3.14) == "3.14"
    assert Calculator._format(10) == "10"


# ----- Cần GUI (dùng fixture app) ----- #

def test_input_and_clear(app):
    for ch in "12+3":
        app._on_press(ch)
    assert app.expression == "12+3"
    app._on_press("⌫")
    assert app.expression == "12+"
    app._on_press("C")
    assert app.expression == ""


def test_memory(app):
    app.expression = "5"
    app._on_memory("MS")
    assert app.memory == 5.0
    app._on_memory("M+")
    assert app.memory == 10.0
    app._on_memory("M-")
    assert app.memory == 5.0
    app._on_memory("MR")
    assert app.expression == "5"
    app._on_memory("MC")
    assert app.memory == 0.0


def test_debt_counter(app):
    assert app.debt == 0
    app._update_debt(9000)
    assert app.debt == 9000
    app._update_debt(15000)
    assert app.debt == 24000
    assert "24.000" in app.debt_label.cget("text")


def test_history(app):
    app._add_history("1+1", 3)
    assert any("1+1 = 3" in h for h in app.history)


def test_real_result_is_correct(app):
    app.prank_disabled = True
    app.expression = "8*9-2"
    app._deliver_real_result()
    assert app.expression == "70"


def test_secret_quit_calls_destroy(app, monkeypatch):
    # Không destroy root dùng chung; chỉ kiểm tra _secret_quit gọi destroy()
    called = {"n": 0}
    monkeypatch.setattr(app, "destroy", lambda: called.__setitem__("n", called["n"] + 1))
    app._secret_quit()
    assert called["n"] == 1
