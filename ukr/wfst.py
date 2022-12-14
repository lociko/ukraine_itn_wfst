import pynini
from pynini.lib import pynutil, rewrite

from ukr.graph_utils import delete_extra_space, delete_space
from ukr.taggers.cardinal import CardinalFst as TCardinalFst
from ukr.taggers.decimal import DecimalFst as TDecimalFst
from ukr.taggers.ordinal import OrdinalFst as TOrdinalFst
from ukr.taggers.measure import MeasureFst as TMeasureFst
from ukr.taggers.money import MoneyFst as TMoneyFst
from ukr.taggers.word import WordFst as TWordFst

from ukr.verbalizers.cardinal import CardinalFst as VCardinalFst
from ukr.verbalizers.decimal import DecimalFst as VDecimalFst
from ukr.verbalizers.ordinal import OrdinalFst as VOrdinalFst
from ukr.verbalizers.measure import MeasureFst as VMeasureFst
from ukr.verbalizers.money import MoneyFst as VMoneyFst
from ukr.verbalizers.word import WordFst as VWordFst


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


# ------------------------------------------
# Taggers
# ------------------------------------------
tCardinalFst = TCardinalFst()
tDecimalFst = TDecimalFst(tCardinalFst)
tOrdinalFst = TOrdinalFst(tCardinalFst)
tMeasureFst = TMeasureFst(tCardinalFst, tDecimalFst)
tMoneyFst = TMoneyFst(tCardinalFst, tDecimalFst)
tWordFst = TWordFst()

# ------------------------------------------
# Verbalizers
# ------------------------------------------
vCardinalFst = VCardinalFst()
vDecimalFst = VDecimalFst()
vOrdinalFst = VOrdinalFst()
vMeasureFst = VMeasureFst(vCardinalFst, vDecimalFst)
vMoneyFst = VMoneyFst(vDecimalFst)
vWordFst = VWordFst()

# ------------------------------------------
# Taggers and verbalizers composition
# ------------------------------------------
single_token = (
        pynutil.add_weight(pynini.compose(tCardinalFst.fst, vCardinalFst.fst), 1)
        | pynutil.add_weight(pynini.compose(tDecimalFst.fst, vDecimalFst.fst), 1)
        | pynutil.add_weight(pynini.compose(tOrdinalFst.fst, vOrdinalFst.fst), 1)
        | pynutil.add_weight(pynini.compose(tMeasureFst.fst, vMeasureFst.fst), 1)
        | pynutil.add_weight(pynini.compose(tMoneyFst.fst, vMoneyFst.fst), 1)
        | pynutil.add_weight(pynini.compose(tWordFst.fst, vWordFst.fst), 100)
).optimize()

# Final Inverse Text Normalization WFST graph
# use this to produce written form of numbers, dates, etc.
graph = single_token + pynini.closure(delete_extra_space + single_token)
graph = delete_space + graph + delete_space
