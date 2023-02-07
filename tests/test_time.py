import pytest

from ukr.wfst import apply_fst_text, graph


@pytest.mark.parametrize("spoken,expected", [
    ("сьома година двадцять п'ять хвилин", '07:25'),
    ("сьома година п'ять хвилин", '07:05'),
    ("дванадцята година п'ять хвилин", '12:05'),
    ("о пів на десяту", '09:30'),
    ("о пів на першу", '00:30'),
    ("о пів на двадцять четверту", '23:30'),
    ("чверть на одинадцяту", '10:15'),
    ("за чверть одинадцята", '10:45'),
    ("п'ять хвилин на дванадцяту", '11:05'),
])
def test_time(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected
