import pynini
from pynini.lib import pynutil

from ukr.graph_utils import GraphFst, delete_space, NEMO_NOT_QUOTE, delete_extra_space


class DateFst(GraphFst):

    def __init__(self):
        super().__init__(name="date", kind="verbalize")
        month = (
                pynutil.delete("month:")
                + delete_space
                + pynutil.delete("\"")
                + pynini.closure(NEMO_NOT_QUOTE, 1)
                + pynutil.delete("\"")
        )
        day = (
                pynutil.delete("day:")
                + delete_space
                + pynutil.delete("\"")
                + pynini.closure(NEMO_NOT_QUOTE, 1)
                + pynutil.delete("\"")
        )
        year = (
                pynutil.delete("year:")
                + delete_space
                + pynutil.delete("\"")
                + pynini.closure(NEMO_NOT_QUOTE, 1)
                + delete_space
                + pynutil.delete("\"")
        )

        graph_dmy = day + delete_extra_space + month + delete_extra_space + year
        graph_my = month + delete_extra_space + year
        graph_dm = day + delete_extra_space + month

        final_graph = graph_dmy | graph_my | graph_dm | year

        delete_tokens = self.delete_tokens(final_graph)
        self.fst = delete_tokens.optimize()
