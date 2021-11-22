from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Tuple

import numpy as np

import Levenshtein
from mars_attacks.tracking.trackers.base import Tracker


@dataclass
class NdImage:
    name: str
    image: np.ndarray


class NpTracker(Tracker):
    def __init__(self, ratio: float = 1.0):
        self.ratio = ratio

    def search(
        self, image: Dict[str, Any], patterns: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Search for a pattern in an 'image'."""
        # convert patterns and image to NdImages
        patterns_as_arrays = [
            NdImage(pattern.get("name"), self._to_np_array(pattern.get("image")))
            for pattern in patterns
        ]
        image_as_array = self._to_np_array(image.get("image"))

        # get max padding
        padding = self._get_padding(patterns_as_arrays)
        # apply padding
        image_as_padded_array = self._apply_padding(image_as_array, padding)

        matches = []
        for pattern in patterns_as_arrays:
            for row_idx, row in enumerate(
                self._find_pattern(image_as_padded_array, pattern)
            ):
                matches.extend(
                    self._build_matches_row(
                        row_idx, row, image_as_array.shape, pattern, padding
                    )
                )
        return matches

    def _build_matches_row(
        self,
        row_idx: int,
        row: List[bool],
        image_shape: Tuple[int, int],
        pattern: NdImage,
        padding: Tuple[int, int],
    ) -> List[Dict[str, any]]:
        """Recalculate match position from padded matrix to the original one."""
        image_height, image_width = image_shape
        h_pad, w_pad = padding
        return [
            {
                "name": pattern.name,
                "start_row": max(row_idx - h_pad, 0),
                "end_row": min(row_idx + pattern.image.shape[0] - h_pad, image_height),
                "start_col": max(col_idx - w_pad, 0),
                "end_col": min(col_idx + pattern.image.shape[1] - w_pad, image_width),
            }
            for col_idx in np.where(row)[0]
        ]

    def _sliding_window_view(self, matrix, window_shape):
        """Provide sub-matrices to be compared with patterns."""
        return np.lib.stride_tricks.sliding_window_view(matrix, window_shape)

    def _find_pattern(
        self, matrix: np.ndarray, pattern: NdImage
    ) -> Iterator[List[bool]]:
        """Find patterns in the matrix."""
        sub_matrices_matrix = self._sliding_window_view(matrix, pattern.image.shape)
        flat_pattern = "".join(pattern.image.flatten())

        for sub_matrices_row in sub_matrices_matrix:
            yield [
                self._is_match("".join(sub_matrix.flatten()), flat_pattern)
                for sub_matrix in sub_matrices_row
            ]

    def _get_padding(self, patterns: List[NdImage]) -> Tuple:
        """Calculate horizontal and vertical paddings.

        The h and w paddings are calculated so that at least one row or column
        of the pattern still fits into the original image. For example:

        For a pattern shaped (3x2) we want padding of 2x1 (2 rows and 1 col for each side).
        """
        h_pad, w_pad = 0, 0
        for pattern in patterns:
            h, w = pattern.image.shape
            h_pad = h if h > h_pad else h_pad
            w_pad = w if w > w_pad else w_pad
        return h_pad - 1, w_pad - 1

    def _apply_padding(self, matrix: np.ndarray, padding: Tuple[int, int]) -> np.ndarray:
        """Apply padding to the matrix."""
        return np.pad(
            matrix, ((padding[0], padding[0]), (padding[1], padding[1])), "constant", constant_values="="
        )

    def _is_match(self, sub_matrix: str, pattern: str) -> float:
        """Compare sub matrix with the pattern window."""
        return Levenshtein.ratio(sub_matrix, pattern) >= self.ratio

    def _to_np_array(self, image: str) -> np.ndarray:
        """Convert string image to np array."""
        return np.vstack([np.array(list(row), dtype=str) for row in image.splitlines()])
