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

        day = pynini.union(
            graph_ordinal_digit,
            graph_ordinal_teen,
            pynutil.insert("0") + graph_ordinal_digit,
            graph_ordinal_ties,
            graph_cardinal_ties + delete_space + graph_ordinal_digit,
        )
        day = day @ (pynini.closure(NEMO_DIGIT) + pynutil.delete(pynini.union("-") + pynini.closure(NEMO_CHAR)))
        graph_day = pynutil.insert("day: \"") + day + pynutil.insert("\"")

        graph_month = pynutil.insert("month: \"") + pynini.string_file(get_abs_path("data/month.tsv")) + pynutil.insert("\"")

        year_name = delete_extra_space + pynini.union("року", "рік")
        optional_year_name = pynini.closure(year_name, 0, 1)

        optional_epoch = delete_extra_space + pynini.closure("до ", 0, 1) + pynini.cross("нашої ери", "н. е.")
        optional_epoch = pynini.closure(optional_epoch, 0, 1)

        year = ordinal.graph @ (pynini.closure(NEMO_DIGIT) + pynutil.delete(pynini.union("-") + pynini.closure(NEMO_CHAR)))

        graph_year = pynutil.insert("year: \"") + year + optional_year_name + optional_epoch + pynutil.insert("\"")
        graph_only_year = pynutil.insert("year: \"") + year + year_name + optional_epoch + pynutil.insert("\"")

        graph_dmy = graph_day + delete_extra_space + graph_month + delete_extra_space + graph_year
        graph_my = graph_month + delete_extra_space + graph_year
        graph_dm = graph_day + delete_extra_space + graph_month

        final_graph = graph_dmy | graph_my | graph_dm | graph_only_year

        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
