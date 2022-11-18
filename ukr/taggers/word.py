import pynini

from ukr.graph_utils import GraphFst, NEMO_NOT_SPACE


class WordFst(GraphFst):

    def __init__(self):
        super().__init__(name="word", kind="classify")
        word = pynini.closure(NEMO_NOT_SPACE, 1)

        self.fst = word.optimize()
