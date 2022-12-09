import pytest

from ukr.wfst import apply_fst_text, graph


@pytest.mark.parametrize('spoken,expected', [
    ('нуль цілих одна десята відсотка', '0.1 %'),
    ('мінус пять цілих одна десята відсотка', '-5.1 %'),
    ('пять відсотків', '5 %'),
    ('сто пять відсотків', '105 %'),
    ('сто відсотків', '100 %'),
])
def test_percent(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected
