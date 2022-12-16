import json
import pytest

from ukr.wfst import apply_fst_text, graph, json_graph


@pytest.mark.parametrize('spoken,expected', [
    ('це трапилося дві тисячі девятнадцятого числа', 'це трапилося 2019 числа'),
    ('коливання в межах трьох копійок експерт оцінив як прийнятні', 'коливання в межах ₴0.03 експерт оцінив як прийнятні'),
    ('збагатила аферистів на три тисячі гривень', 'збагатила аферистів на ₴3000'),
    ('близько двох мільйонів гривень', 'близько ₴2 мільйонів'),
])
def test_word(spoken, expected):
    assert apply_fst_text(spoken, graph) == expected


@pytest.mark.parametrize('spoken,expected', [
    ('це трапилося дві тисячі девятнадцятого числа', 'це трапилося 2019 числа'),
    ('коливання в межах трьох копійок експерт оцінив як прийнятні', 'коливання в межах ₴0.03 експерт оцінив як прийнятні'),
    ('збагатила аферистів на три тисячі гривень', 'збагатила аферистів на ₴3000'),
    ('близько двох мільйонів гривень', 'близько ₴2 мільйонів'),
])
def test_word__json_graph(spoken, expected):
    json_text = apply_fst_text(spoken, json_graph)
    words = json.loads(json_text)
    text = ' '.join([list(word.values())[0] for word in words])

    assert text == expected
