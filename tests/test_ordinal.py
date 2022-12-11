import pytest

from ukr.wfst import apply_fst_text, graph


@pytest.mark.parametrize('spoken,expected', [
    ('перший', '1'),
    ('дванадцятий', '12'),
    ('двадцятий', '20'),
    ('девяносто девяте', '99'),
    ('тридцять другий', '32'),
    ('девятсот дванадцятий', '912'),
    ('дві тисячі девятисотий', '2900'),
    ('дві тисячі перший', '2001'),
    ('дві тисячі двадцять другого', '2022'),
    ('дві тисячі девятнадцятого', '2019'),
])
def test_ordinal(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected


@pytest.mark.parametrize('spoken,expected', [
    ('я пішов двадцять першого числа до монастиря', 'я пішов 21 числа до монастиря'),
    ('ти народилася двадцять першого числа чи двадцять восьмого', 'ти народилася 21 числа чи 28'),
])
def test_ordinal_with_other_words(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected
