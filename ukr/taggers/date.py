import pynini
from pynini.lib import pynutil

from ukr.graph_utils import GraphFst, delete_space, delete_extra_space, NEMO_CHAR, NEMO_DIGIT
from ukr.taggers.cardinal import CardinalFst
from ukr.taggers.ordinal import OrdinalFst
from ukr.utils import get_abs_path


class DateFst(GraphFst):
    """
    Finite state transducer for classifying date,
        e.g. january fifth twenty twelve -> date { month: "january" day: "5" year: "2012" }

    Args:
        cardinal: CardinalFst
        ordinal: OrdinalFst
    """

    def __init__(self, cardinal: CardinalFst, ordinal: OrdinalFst):
        super().__init__(name="date", kind="classify")

        graph_cardinal_ties = cardinal.graph_ties

        graph_ordinal_digit = pynini.invert(pynini.string_file(get_abs_path("data/numbers/ordinal/ordinal_digit.tsv")))
        graph_ordinal_teen = pynini.invert(pynini.string_file(get_abs_path("data/numbers/ordinal/ordinal_teen.tsv")))
        graph_ordinal_ties = pynini.invert(pynini.string_file(get_abs_path("data/numbers/ordinal/ordinal_ties.tsv")))

        graph_day = pynini.union(
            graph_ordinal_digit,
            graph_ordinal_teen,
            pynutil.insert("0") + graph_ordinal_digit,
            graph_ordinal_ties,
            graph_cardinal_ties + delete_space + graph_ordinal_digit,
        )

        graph_day = pynutil.insert("day: \"") + graph_day + pynutil.insert("\"")
        graph_month = pynutil.insert("month: \"") + pynini.string_file(get_abs_path("data/month.tsv")) + pynutil.insert("\"")

        graph_year = ordinal.graph @ (pynini.closure(NEMO_DIGIT) + pynutil.delete(pynini.union("-") + pynini.closure(NEMO_CHAR)))
        graph_year = pynutil.insert("year: \"") + graph_year + delete_extra_space + pynini.union("року") + pynutil.insert("\"")

        graph_dmy = graph_day + delete_extra_space + graph_month + delete_extra_space + graph_year

        final_graph = graph_dmy

        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
