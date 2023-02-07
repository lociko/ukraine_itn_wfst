import pynini

from ukr.taggers.tokenize_and_classify import ClassifyFst
from ukr.utils import reorder
from ukr.verbalizers.verbalize_final import VerbalizeFinalFst


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


classifyFst = ClassifyFst()
verbalizeFinalFst = VerbalizeFinalFst()

graph = pynini.compose(classifyFst.fst, verbalizeFinalFst.fst).optimize()
json_graph = pynini.compose(classifyFst.fst, verbalizeFinalFst.as_json()).optimize()


def normalize(text, json=False) -> str:
    """
    Apply Inverse Text Normalization (ITN) for the given text

    :param text: given text
    :param json: if True result would be in json
    :return: return normalized text
    """
    classified = apply_fst_text(text, classifyFst.fst)
    classified = reorder(classified)

    if json:
        return apply_fst_text(classified, verbalizeFinalFst.as_json())
    else:
        return apply_fst_text(classified, verbalizeFinalFst.fst)
