import pytest

from ukr.taggers.cardinal import CardinalFst
from ukr.taggers.decimal import DecimalFst
from ukr.wfst import apply_fst_text, graph


@pytest.mark.parametrize('spoken,expected', [
    ("нуль цілих одна десята", '0.1'),
    ("мінус п'ять цілих одна десята", '-5.1'),
    ("п'ять цілих одна десята", '5.1'),
    ("двадцять п'ять цілих одна десята", '25.1'),
    ("тридцять цілих одна сотих", '30.01'),
    ("тридцять цілих сімдесят п'ять сотих", '30.75'),
    ("сто вісім цілих шість тисячних", '108.006'),
    ("сто вісім цілих тридцять тисячних", '108.030'),
    ("сто вісім цілих тридцять шість тисячних", '108.036'),
    ("сто вісім цілих сто тридцять шість тисячних", '108.136'),
    ("тридцять цілих одна сотих", '30.01'),
])
def test_decimal(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected


@pytest.mark.parametrize('spoken,expected', [
    ("мінус п'ять цілих і одна десята", '-5.1'),
    ("п'ять цілих і одна десята", '5.1'),
    ("двадцять п'ять цілих і одна десята", '25.1'),
])
def test_decimal__delimiter_with_and(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected


@pytest.mark.parametrize('spoken,expected', [
    ("два і сім десятих", '2.7'),
    ("два і сім сотих", '2.07'),
    ("два і сім тисячних", '2.007'),
])
def test_decimal__optional_delimiter_with_and(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected


@pytest.mark.parametrize('spoken,expected', [
    ("сім десятих", '0.7'),
    ("сім сотих", '0.07'),
    ("сім тисячних", '0.007'),
    ("сто двадцять сім тисячних", '0.127'),
    ("сорок одна тисячних", '0.041'),
    ("одинадцять тисячних", '0.011'),
    ("точність приладу рівна двом сотим", 'точність приладу рівна 0.02'),
])
def test_decimal__only_fractional(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected


@pytest.mark.parametrize('spoken,expected', [
    ("мінус п'ять цілих і одна десята мільйона", '-5.1 мільйона'),
    ("п'ять цілих і одна десята мільярдів", '5.1 мільярдів'),
    ("двадцять п'ять цілих і одна десята тисяч", '25.1 тисяч'),
    ("двадцять п'ять тисяч", '25 тисяч'),
])
def test_decimal__delimiter_with_quantity(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected


@pytest.mark.parametrize('spoken,expected', [
    ("мінус п'ять цілих і одна десята мільйона", 'decimal { negative: "true" integer_part: "5" fractional_part: "1"  quantity: "мільйона" }'),
    ("двадцять п'ять тисяч", 'decimal { integer_part: "25" quantity: "тисяч" }'),
    ("два і сім десятих", 'decimal { integer_part: "2" fractional_part: "7" }'),
    ("мінус п'ять цілих і дві десятих", 'decimal { negative: "true" integer_part: "5" fractional_part: "2" }'),
])
def test_decimal__delimiter_with_quantity__only_tagger(spoken, expected):
    tCardinalFst = CardinalFst()
    tDecimalFst = DecimalFst(cardinal=tCardinalFst)

    assert apply_fst_text(spoken, tDecimalFst.fst) == expected
