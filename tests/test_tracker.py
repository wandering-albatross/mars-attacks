import pytest

from mars_attacks.tracking.trackers.np_tracker import (
    NpTracker,
    NdImage,
)
import numpy as np


@pytest.fixture
def np_tracker():
    return NpTracker()


def test_to_np_array(np_tracker):
    scan = "ooooo\n-o-o-\no-o-o\n-----"
    scan_arr = np_tracker._to_np_array(scan)
    expected = np.array(
        [
            ["o", "o", "o", "o", "o"],
            ["-", "o", "-", "o", "-"],
            ["o", "-", "o", "-", "o"],
            ["-", "-", "-", "-", "-"],
        ]
    )
    assert np.array_equal(scan_arr, expected)


def test_get_padding(np_tracker):
    arrays = [
        # 2x3 array
        NdImage("1", np.arange(6).reshape(2, -1)),
        # 3x2 array
        NdImage("2", np.arange(6).reshape(3, -1)),
    ]
    h, w = np_tracker._get_padding(arrays)
    # height is calculated as max height -1
    assert h == 2
    # width is calculated as max width -1
    assert w == 2


def test_is_match(np_tracker):
    # default expected similarity is 100%
    assert np_tracker._is_match("0123", "0123")
    assert not np_tracker._is_match("1234", "1231")
    # set expected similarity to 50%
    np_tracker.ratio = 0.5
    assert np_tracker._is_match("0123", "0155")
    assert not np_tracker._is_match("0123", "0555")


def test_padding():
    tracker = NpTracker()
    input_array = np.array(
        [
            ["o", "o", "o"],
            ["-", "o", "-"],
            ["o", "-", "o"],
        ]
    )
    expected = np.array(
        [
            ["=", "=", "=", "=", "="],
            ["=", "=", "=", "=", "="],
            ["=", "o", "o", "o", "="],
            ["=", "-", "o", "-", "="],
            ["=", "o", "-", "o", "="],
            ["=", "=", "=", "=", "="],
            ["=", "=", "=", "=", "="],
        ]
    )
    padded_array = tracker._apply_padding(input_array, (2, 1))
    assert np.array_equal(padded_array, expected)


def test_sliding_window_view(np_tracker):
    matrix = np.arange(9).reshape(3, -1)
    expected = np.array(
        [[[[0, 1], [3, 4]], [[1, 2], [4, 5]]], [[[3, 4], [6, 7]], [[4, 5], [7, 8]]]]
    )
    sub_matrices = np_tracker._sliding_window_view(matrix, (2, 2))
    assert np.array_equal(sub_matrices, expected)


def test_np_array_find_pattern(np_tracker):
    padded_array = np.array(
        [
            ["=", "=", "=", "=", "="],
            ["=", "=", "=", "=", "="],
            ["=", "o", "o", "o", "="],
            ["=", "-", "o", "-", "="],
            ["=", "o", "-", "o", "="],
            ["=", "=", "=", "=", "="],
            ["=", "=", "=", "=", "="],
        ]
    )
    invader_array = np.array([["o", "o"], ["o", "-"], ["-", "o"]])
    expected = np.array(
        [
            [False, False, False, False],
            [False, False, False, False],
            [False, False, True, False],
            [False, False, False, False],
            [False, False, False, False],
        ]
    )
    rows = list(np_tracker._find_pattern(padded_array, NdImage("test", invader_array)))
    assert np.array_equal(rows, expected)


def test_build_matches(np_tracker):
    pattern = NdImage("invader1", np.arange(4).reshape(2, -1))
    expected = [dict(name="invader1", start_row=0, end_row=2, start_col=1, end_col=3)]
    matches_row = np_tracker._build_matches_row(
        row_idx=1,
        image_shape=(7, 7),
        row=[False, False, True, False, False],
        pattern=pattern,
        padding=(1, 1),
    )
    assert matches_row == expected


def test_build_matches_out_of_bounds(np_tracker):
    pattern = NdImage("invader1", np.arange(4).reshape(2, -1))
    expected = [
        dict(name="invader1", start_row=4, end_row=5, start_col=0, end_col=1),
        dict(name="invader1", start_row=4, end_row=5, start_col=1, end_col=2)
    ]
    matches_row = np_tracker._build_matches_row(
        row_idx=5,
        image_shape=(5, 2),
        row=[True, False, True, False],  # matches on the padded image
        pattern=pattern,
        padding=(1, 1),
    )
    assert matches_row == expected


def test_search(np_tracker):
    radar_scan = "---o---\n---o---\n-------"
    image = {"name": "image1", "image": radar_scan}
    patterns = [
        {"name": "invader1", "image": "-o\n-o"},
        {"name": "invader2", "image": "o-\no-"},
    ]
    expected = [
        {
            "name": "invader1",
            "start_row": 0,
            "end_row": 2,
            "start_col": 2,
            "end_col": 4,
        },
        {
            "name": "invader2",
            "start_row": 0,
            "end_row": 2,
            "start_col": 3,
            "end_col": 5,
        },
    ]
    assert np_tracker.search(image, patterns) == expected

    radar_scan = "-------\n---o---\n-------"
    image = {"name": "image1", "image": radar_scan}
    assert np_tracker.search(image, patterns) == []
