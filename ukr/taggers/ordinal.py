import pynini
from pynini.lib import pynutil

from ukr.graph_utils import (
    NEMO_DIGIT,
    GraphFst,
)

from ukr.taggers.cardinal import CardinalFst
from ukr.utils import get_abs_path


class OrdinalFst(GraphFst):

    def __init__(self, cardinal: CardinalFst):
        super().__init__(name="ordinal", kind="classify")

        delete_space = pynutil.delete(" ")
        delete_space_optional = pynini.closure(delete_space, 0, 1)

        graph_cardinal_ties = cardinal.graph_ties
        graph_cardinal_hundred = cardinal.graph_hundred

        graph_ordinal_digit = pynini.invert(pynini.string_file(get_abs_path("data/numbers/ordinal/ordinal_digit.tsv")))
        graph_ordinal_teen = pynini.invert(pynini.string_file(get_abs_path("data/numbers/ordinal/ordinal_teen.tsv")))
        graph_ordinal_ties = pynini.invert(pynini.string_file(get_abs_path("data/numbers/ordinal/ordinal_ties.tsv")))
        graph_ordinal_hundred = pynini.invert(pynini.string_file(get_abs_path("data/numbers/ordinal/ordinal_hundred.tsv")))

        # From 1 to 99
        graph_up_to_hundred_component = pynini.union(
            graph_ordinal_teen,
            pynutil.insert("0") + graph_ordinal_digit,
            graph_ordinal_ties + pynutil.insert("0"),
            graph_cardinal_ties + delete_space + graph_ordinal_digit,
        )

        graph_hundred_component = graph_cardinal_hundred + delete_space_optional + graph_up_to_hundred_component
        graph_hundred_component |= graph_ordinal_hundred + pynutil.insert("00")
        graph_hundred_component |= pynutil.insert("0") + graph_up_to_hundred_component

        thousands = pynini.string_file(get_abs_path("data/numbers/cardinals_thousand.tsv"))

        one_thousand = pynini.cross(thousands, '1') + delete_space + graph_hundred_component
        graph_thousands = (
            pynini.union(
                cardinal.graph_hundred_component + delete_space + pynutil.delete(thousands),
                pynutil.insert("000", weight=0.1),
            )
        )

        graph_millions = (
            pynini.union(
                cardinal.graph_hundred_component + delete_space + pynutil.delete("мільйон"),
                pynutil.insert("000", weight=0.1),
            )
        )

        graph_billions = (
            pynini.union(
                cardinal.graph_hundred_component + delete_space + pynutil.delete("мільярд"),
                pynutil.insert("000", weight=0.1),
            )
        )

        # TODO: add other cardinalities like trillions, etc.
        graph = pynini.union(
            graph_billions
            + delete_space_optional
            + graph_millions
            + delete_space_optional
            + graph_thousands
            + delete_space_optional
            + (graph_hundred_component | pynutil.insert("000")),
            one_thousand,
            graph_up_to_hundred_component,
        )

        self.graph_zeroth = graph
        self.graph = graph @ pynini.union(
            pynini.closure(pynutil.delete(pynini.union("0", ",")))
            + pynini.difference(NEMO_DIGIT, "0")
            + pynini.closure(pynini.union(NEMO_DIGIT, ",")),
            "0",
        )

        final_graph = pynutil.insert("integer: \"") + self.graph + pynutil.insert("\"")
        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph
