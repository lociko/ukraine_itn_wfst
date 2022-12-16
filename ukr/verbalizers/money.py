import pynini
from pynini.lib import pynutil

from ukr.graph_utils import GraphFst, delete_space, NEMO_CHAR
from ukr.verbalizers.decimal import DecimalFst


class MoneyFst(GraphFst):
    """
    Finite state transducer for verbalizing money, e.g.
        money { integer_part: "12" fractional_part: "05" currency: "$" } -> $12.05

    Args:
        decimal: DecimalFst
    """

    def __init__(self, decimal: DecimalFst):
        super().__init__(name="money", kind="verbalize")

        units = pynini.union("$", "₴")

        unit = (
                pynutil.delete("currency:")
                + delete_space
                + pynutil.delete("\"")
                + pynini.closure(units, 1)
                + pynutil.delete("\"")
        )
        graph = unit + delete_space + decimal.numbers
        delete_tokens = self.delete_tokens(graph)
        self.fst = delete_tokens.optimize()
