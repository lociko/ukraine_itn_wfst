import pynini
from pynini.lib import rewrite, pynutil

from ukr.graph_utils import delete_extra_space, delete_space
from ukr.taggers.cardinal import CardinalFst as TCardinalFst
from ukr.verbalizers.cardinal import CardinalFst as VCardinalFst
from ukr.taggers.decimal import DecimalFst as TDecimalFst
from ukr.verbalizers.decimal import DecimalFst as VDecimalFst
from ukr.taggers.measure import MeasureFst
from ukr.taggers.money import MoneyFst
from ukr.taggers.ordinal import OrdinalFst
from ukr.taggers.word import WordFst


def find_tags(text: str, tagger) -> 'pynini.FstLike':
    """
    Given text use tagger Fst to tag text

    Args:
        text: sentence

    Returns: tagged lattice
    """
    lattice = text @ tagger
    return lattice


def select_tag(lattice: 'pynini.FstLike') -> str:
    """
    Given tagged lattice return shortest path

    Args:
        tagged_text: tagged text

    Returns: shortest path
    """
    tagged_text = pynini.shortestpath(lattice, nshortest=1, unique=True).string()
    return tagged_text


def apply_fst_text(text, fst):
    text = pynini.escape(text)
    tagged_lattice = find_tags(text, fst)
    tagged_text = select_tag(tagged_lattice)

    return tagged_text


tCardinalFst = TCardinalFst()
tDecimalFst = TDecimalFst(tCardinalFst)
ordinal = OrdinalFst(tCardinalFst)
measure = MeasureFst(tCardinalFst, tDecimalFst)
money = MoneyFst(tCardinalFst, tDecimalFst)
word = WordFst()

vCardinalFst = VCardinalFst()
vDecimalFst = VDecimalFst()

classify_and_verbalize = (
        pynutil.add_weight(pynini.compose(tCardinalFst.fst, vCardinalFst.fst), 1)
        | pynutil.add_weight(pynini.compose(tDecimalFst.fst, vDecimalFst.fst), 1)
).optimize()

token = classify_and_verbalize

graph = token + pynini.closure(delete_extra_space + token)
graph = delete_space + graph + delete_space
