import pytest

from ukr.wfst import apply_fst_text, graph


@pytest.mark.parametrize("spoken,expected", [
    ("першого січня дві тисячі першого року", '1-го січня 2001 року'),
    ("першого січня", '1-го січня'),
    ("перше травня", '1 травня'),
    ("двадцять перше лютого", '21-го лютого'),

])
def test_month(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected
