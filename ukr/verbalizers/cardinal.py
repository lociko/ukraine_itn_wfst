import pynini
from pynini.lib import pynutil

from ukr.graph_utils import GraphFst, delete_space, NEMO_NOT_QUOTE


class CardinalFst(GraphFst):
    """
    Finite state transducer for verbalizing cardinal
        e.g. cardinal { integer: "23" negative: "-" } -> -23
    """

    def __init__(self):
        super().__init__(name="cardinal", kind="verbalize")
        # 'cardinal { negative: "true" integer: "70" }'
        optional_sign = pynini.closure(
            pynutil.delete("negative:")
            + delete_space
            + pynutil.delete("\"")
            + pynini.cross("true", "-")
            + pynutil.delete("\"")
            + delete_space,
            0,
            1,
        )
        graph = (
                pynutil.delete("integer:")
                + delete_space
                + pynutil.delete("\"")
                + pynini.closure(NEMO_NOT_QUOTE, 1)
                + pynutil.delete("\"")
        )
        self.numbers = graph
        graph = optional_sign + graph
        delete_tokens = self.delete_tokens(graph)
        self.fst = delete_tokens.optimize()
