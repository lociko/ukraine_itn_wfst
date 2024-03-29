import pytest

from ukr.wfst import normalize


@pytest.mark.parametrize('spoken,expected', [
    ("перший", 'перший'),
    ("дванадцятий", '12-й'),
    ("двадцятий", '20-й'),
    ("дев'яносто дев'яте", '99-те'),
    ("тридцять другий", '32-й'),
    ("дев'ятсот дванадцятий", '912-й'),
    ("дві тисячі дев'ятисотий", '2900-й'),
    ("дві тисячі перший", '2001-й'),
    ("дві тисячі двадцять другого", '2022-го'),
    ("дві тисячі дев'ятнадцятого", '2019-го'),
    # ("один мільйон сто тридцять тисячний рік", '130000-й рік'),
    ("тисячу дванадцятий", '1012-й'),
])
def test_ordinal(spoken, expected):
    assert normalize(spoken) == expected


@pytest.mark.parametrize('spoken,expected', [
    ('я пішов двадцять першого числа до монастиря', 'я пішов 21-го числа до монастиря'),
    ('ти народилася двадцять першого числа чи двадцять восьмого', 'ти народилася 21-го числа чи 28-го'),
])
def test_ordinal_with_other_words(spoken, expected):
    assert normalize(spoken) == expected
