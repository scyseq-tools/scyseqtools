from scyseqtools.encoder.infoframe import normalize_resume_data


def test_normalize_resume_data_uses_coded_samples_not_time_count():
    record = {
        "times": [0, 5_000, 10_000, 15_000],
        "comments": ["a", "b", "c"],
        "data": {
            "cat": {"sound": [0, 1, 2]},
            "dog": {"movement": [2, 1, 0]},
        },
    }

    state = normalize_resume_data(record)

    assert state["recorded_steps"] == {1, 2, 3}
    assert state["times"] == [0, 5_000, 10_000, 15_000]
    assert state["comments"] == ["a", "b", "c"]


def test_normalize_resume_data_handles_legacy_time_count_equal_to_data_count():
    record = {
        "times": [5_000, 10_000],
        "comments": ["a", "b"],
        "data": {
            "cat": {"sound": [0, 1]},
            "dog": {"movement": [2, 1]},
        },
    }

    state = normalize_resume_data(record)

    assert state["recorded_steps"] == {1, 2}
    assert state["times"] == [5_000, 10_000]
    assert state["comments"] == ["a", "b"]


def test_normalize_resume_data_trims_to_shortest_coded_sequence():
    record = {
        "times": [0, 5_000, 10_000, 15_000],
        "comments": ["a", "b", "c", "extra"],
        "data": {
            "cat": {"sound": [0, 1, 2]},
            "dog": {"movement": [2, 1]},
        },
    }

    state = normalize_resume_data(record)

    assert state["recorded_steps"] == {1, 2}
    assert state["comments"] == ["a", "b"]


def test_normalize_resume_data_pads_missing_comments():
    record = {
        "times": [0, 5_000, 10_000],
        "comments": ["a"],
        "data": {
            "cat": {"sound": [0, 1]},
        },
    }

    state = normalize_resume_data(record)

    assert state["recorded_steps"] == {1, 2}
    assert state["comments"] == ["a", ""]


def test_normalize_resume_data_synthesizes_missing_times_from_period():
    record = {
        "times": [],
        "comments": ["a", "b"],
        "code": {"period": 5.0},
        "data": {
            "cat": {"sound": [0, 1]},
        },
    }

    state = normalize_resume_data(record)

    assert state["recorded_steps"] == {1, 2}
    assert state["times"] == [0, 5_000, 10_000]
