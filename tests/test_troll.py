"""Test logic phần troll: sabotage, phát hiện toán tử, phân quyền gói."""


def test_operators_used_basic(app):
    cases = {
        "1+2": {"+"},
        "5-3": {"-"},
        "2*3": {"*"},
        "8/4": {"/"},
        "1+2*3-4/2": {"+", "-", "*", "/"},
    }
    for expr, expected in cases.items():
        app.expression = expr
        assert app._operators_used() == expected, expr


def test_operators_used_negative_numbers(app):
    # Số âm đứng đầu hoặc sau '(' KHÔNG tính là phép trừ
    app.expression = "-5"
    assert app._operators_used() == set()
    app.expression = "-5+3"
    assert app._operators_used() == {"+"}
    app.expression = "3*(-2)"
    assert app._operators_used() == {"*"}
    # Trừ thật sự
    app.expression = "10-3"
    assert app._operators_used() == {"-"}
    app.expression = "(5)-2"
    assert app._operators_used() == {"-"}


def test_sabotage_never_flips_sign_or_zero(app):
    for _ in range(500):
        for true_val in [2, 42, 100, 7, 1000, 3.5, -8]:
            w = float(app._sabotage(true_val))
            if true_val > 0:
                assert w > 0, f"{true_val} -> {w} (đổi dấu/về 0)"
            elif true_val < 0:
                assert w < 0, f"{true_val} -> {w} (đổi dấu)"


def test_sabotage_small_error(app):
    for _ in range(500):
        for true_val in [2, 42, 100, 1000]:
            w = float(app._sabotage(true_val))
            assert abs(w - true_val) <= abs(true_val) * 0.10 + 2.01, \
                f"{true_val} -> {w} (lệch quá xa)"


def test_sabotage_zero_stays_zero(app):
    assert app._sabotage(0) == 0


def test_plan_permissions_config():
    from calc import config
    assert config.PLAN_PERMISSIONS["Gói Cơ Bản"]["allowed"] == set()
    assert config.PLAN_PERMISSIONS["Gói Tiêu Chuẩn"]["allowed"] == {"+"}
    assert config.PLAN_PERMISSIONS["Gói Nâng Cao"]["allowed"] == {"+", "-", "*", "/"}
