import pytest

from ukr.wfst import apply_fst_text, graph


@pytest.mark.parametrize('spoken,expected', [
    ('пeрший', '1'),
    ('дванадцятий', '12'),
    ('двадцятий', '20'),
    ('девяносто девяте', '99'),
    ('тридцять другий', '32'),
    ('девятсот дванадцятий', '912'),
    ('дві тисячі девятисотий', '2900'),
    ('дві тисячі пeрший', '2001'),
    ('дві тисячі двадцять другого', '2022'),
    ('дві тисячі девятнадцятого', '2019'),
])
def test_cardinal(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected
