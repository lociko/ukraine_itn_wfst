import pynini
from pynini.lib import pynutil

from ukr.graph_utils import GraphFst, delete_space, NEMO_CHAR


class MeasureFst(GraphFst):
    """
    Finite state transducer for verbalizing measure, e.g.
        measure { negative: "true" cardinal { integer: "12" } units: "kg" } -> -12 kg

    Args:
        cardinal: CardinalFst
        decimal: DecimalFst
    """

    def __init__(self, cardinal: GraphFst, decimal: GraphFst):
        super().__init__(name="measure", kind="verbalize")
        optional_sign = pynini.closure(pynini.cross("negative: \"true\"", "-"), 0, 1)
        unit = (
                pynutil.delete("units:")
                + delete_space
                + pynutil.delete("\"")
                + pynini.closure(NEMO_CHAR - " ", 1)
                + pynutil.delete("\"")
                + delete_space
        )
        graph_decimal = (
                pynutil.delete("decimal {")
                + delete_space
                + optional_sign
                + delete_space
                + decimal.numbers
                + delete_space
                + pynutil.delete("}")
        )
        graph_cardinal = (
                pynutil.delete("cardinal {")
                + delete_space
                + optional_sign
                + delete_space
                + cardinal.numbers
                + delete_space
                + pynutil.delete("}")
        )
        graph = (graph_cardinal | graph_decimal) + delete_space + pynutil.insert(" ") + unit
        delete_tokens = self.delete_tokens(graph)
        self.fst = delete_tokens.optimize()
