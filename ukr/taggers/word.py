import pynini
from pynini.lib import pynutil

from ukr.graph_utils import GraphFst, NEMO_NOT_SPACE


class WordFst(GraphFst):

    def __init__(self):
        super().__init__(name="word", kind="classify")
        word = pynutil.insert("name: \"") + pynini.closure(NEMO_NOT_SPACE, 1) + pynutil.insert("\"")
        word = self.add_tokens(word)
        self.fst = word.optimize()
