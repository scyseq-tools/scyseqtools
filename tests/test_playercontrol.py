from scyseqtools.encoder.playercontrol import bound_time_to_media, regular_step_target


def test_bound_time_to_media_allows_zero_when_duration_unknown():
    assert bound_time_to_media(0, -1) == (0, None)


def test_bound_time_to_media_allows_positive_time_when_duration_is_zero():
    assert bound_time_to_media(30_000, 0) == (30_000, None)


def test_bound_time_to_media_allows_positive_time_when_duration_unknown():
    assert bound_time_to_media(30_000, -1) == (30_000, None)


def test_bound_time_to_media_still_enforces_lower_bound_when_duration_unknown():
    assert bound_time_to_media(-100, -1) == (0, "before_start")


def test_bound_time_to_media_enforces_known_upper_bound():
    assert bound_time_to_media(1_500, 1_000) == (1_000, "after_end")


def test_regular_step_target_adds_period_in_milliseconds():
    assert regular_step_target(50_000, 5, 60_000) == (55_000, None)


def test_regular_step_target_rounds_fractional_period_to_milliseconds():
    assert regular_step_target(50_000, 5.1236, 60_000) == (55_124, None)


def test_regular_step_target_enforces_known_upper_bound():
    assert regular_step_target(50_000, 5, 54_950) == (54_950, "after_end")


def test_regular_step_target_still_enforces_lower_bound_when_duration_unknown():
    assert regular_step_target(-10_000, 5, -1) == (0, "before_start")


def test_regular_step_target_allows_positive_time_when_duration_unknown():
    assert regular_step_target(50_000, 5, -1) == (55_000, None)
