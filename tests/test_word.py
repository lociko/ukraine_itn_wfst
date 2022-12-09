import pytest

from ukr.wfst import apply_fst_text, graph


@pytest.mark.parametrize('spoken,expected', [
    ('це трапилося дві тисячі девятнадцятого числа', 'це трапилося 2019 числа'),
])
def test_word(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected
