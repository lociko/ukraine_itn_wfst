import pynini
from pynini.lib import pynutil

from ukr.graph_utils import GraphFst, delete_space, NEMO_DIGIT


class TimeFst(GraphFst):
    """
    Finite state transducer for verbalizing time, e.g.
        time { hours: "12" minutes: "30" } -> 12:30
        time { hours: "1" minutes: "12" } -> 01:12
    """

    def __init__(self):
        super().__init__(name="time", kind="verbalize")
        add_leading_zero_to_double_digit = (NEMO_DIGIT + NEMO_DIGIT) | (pynutil.insert("0") + NEMO_DIGIT)
        hour = (
                pynutil.delete("hours:")
                + delete_space
                + pynutil.delete("\"")
                + pynini.closure(NEMO_DIGIT, 1)
                + pynutil.delete("\"")
        )
        minute = (
                pynutil.delete("minutes:")
                + delete_space
                + pynutil.delete("\"")
                + pynini.closure(NEMO_DIGIT, 1)
                + pynutil.delete("\"")
        )
        graph = (
                hour @ add_leading_zero_to_double_digit
                + delete_space
                + pynutil.insert(":")
                + (minute @ add_leading_zero_to_double_digit)
        )
        delete_tokens = self.delete_tokens(graph)
        self.fst = delete_tokens.optimize()
