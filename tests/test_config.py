"""Test tính toàn vẹn của dữ liệu cấu hình troll."""

from calc import config


def test_plans_have_four_entries():
    assert len(config.PREMIUM_PLANS) == 4
    for name, price, desc in config.PREMIUM_PLANS:
        assert name and price and desc


def test_lists_non_empty():
    assert len(config.AD_LINES) >= 5
    assert len(config.CAPTCHA_QUESTIONS) >= 4
    assert len(config.LOADING_MESSAGES) >= 5
    assert len(config.CARD_REJECTIONS) >= 5
    assert len(config.EXIT_EXCUSES) >= 5
    assert len(config.PASSWORD_COMPLAINTS) >= 5
    assert len(config.SURVEY_QUESTIONS) >= 4
    assert len(config.WHEEL_SEGMENTS) >= 6
    assert len(config.SPELL_PHRASES) >= 4
    assert len(config.VIDEO_AD_TITLES) >= 3
    assert len(config.SHARE_PLATFORMS) >= 3
    assert len(config.UPDATE_STEPS) >= 3


def test_wheel_has_one_winning_segment():
    winners = [s for s in config.WHEEL_SEGMENTS if "MIỄN PHÍ" in s]
    assert len(winners) == 1  # đúng 1 ô xịn (mà kim không bao giờ dừng vào)


def test_captcha_questions_have_options():
    for question, options in config.CAPTCHA_QUESTIONS:
        assert question
        assert len(options) >= 2


def test_survey_questions_have_options():
    for question, options in config.SURVEY_QUESTIONS:
        assert question
        assert len(options) >= 2


def test_discount_codes_structure():
    for code, (pct, msg) in config.DISCOUNT_CODES.items():
        assert isinstance(code, str)
        assert msg
        assert pct is None or isinstance(pct, (int, float))
