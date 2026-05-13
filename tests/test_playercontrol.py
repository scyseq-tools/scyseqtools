from codix.encoder.playercontrol import bound_time_to_media


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
