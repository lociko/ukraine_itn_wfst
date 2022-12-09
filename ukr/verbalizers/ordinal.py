import pynini
from pynini.lib import pynutil

from ukr.graph_utils import GraphFst, delete_space, NEMO_NOT_QUOTE, NEMO_SIGMA


class OrdinalFst(GraphFst):

    def __init__(self):
        super().__init__(name="ordinal", kind="verbalize")
        graph = (
                pynutil.delete("integer:")
                + delete_space
                + pynutil.delete("\"")
                + pynini.closure(NEMO_NOT_QUOTE, 1)
                + pynutil.delete("\"")
        )

        delete_tokens = self.delete_tokens(graph)
        self.fst = delete_tokens.optimize()
