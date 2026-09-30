from app import App

def test_stone_speed_starts_at_base_score_zero(app):
    app.score = 0
    app.update_difficulty()
    assert app.stone_speed == 1.0


def test_stone_speed_never_exceeds_cap_beyond_ramp(app):
    app.score = 999999
    app.update_difficulty()
    assert app.stone_speed == 6.5


def test_stone_interval_decreases_as_score_increases(app):
    app.score = 0
    app.update_difficulty()
    interval_start = app.stone_interval

    app.score = 4000
    app.update_difficulty()
    interval_end = app.stone_interval

    assert interval_end < interval_start
    