import pytest
import asyncio
from matrix_lib.core import parse_matrix, traverse_spiral_ccw

def test_parse_matrix():
    sample = "+-----+-----+\n| 1 | 2 |\n+-----+-----+\n| 3 | 4 |\n+-----+-----+"
    expected = [[1, 2], [3, 4]]
    assert parse_matrix(sample) == expected

def test_traverse_spiral_4x4():
    # Матрица из задания Авито
    matrix = [
        [10, 20, 30, 40],
        [50, 60, 70, 80],
        [90, 100, 110, 120],
        [130, 140, 150, 160]
    ]
    expected = [10, 50, 90, 130, 140, 150, 160, 120, 80, 40, 30, 20, 60, 100, 110, 70]
    assert traverse_spiral_ccw(matrix) == expected

def test_traverse_empty():
    assert traverse_spiral_ccw([]) == []