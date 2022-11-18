import pynini
from pynini.lib import rewrite, pynutil

from ukr.graph_utils import delete_extra_space, delete_space
from ukr.taggers.cardinal import CardinalFst
from ukr.taggers.decimals import DecimalFst
from ukr.taggers.measure import MeasureFst
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


def apply_fst(text, fst):
    """ Given a string input, returns the output string
    produced by traversing the path with lowest weight.
    If no valid path accepts input string, returns an
    error.
    """
    try:
        print(text, '---->', rewrite.rewrites(text, fst))
    except Exception as ex:
        print(f"'{text}' ----> Error: No valid output with given input: {ex}")


cardinal = CardinalFst()
decimal = DecimalFst(cardinal)
ordinal = OrdinalFst(cardinal)
measure = MeasureFst(cardinal, decimal)
word = WordFst()

classify = (
        pynutil.add_weight(cardinal.fst, 1)
        | pynutil.add_weight(decimal.fst, 1)
        | pynutil.add_weight(ordinal.fst, 1)
        | pynutil.add_weight(measure.fst, 1)
        | pynutil.add_weight(word.fst, 100)
)

token = classify

graph = token + pynini.closure(delete_extra_space + token)
graph = delete_space + graph + delete_space
