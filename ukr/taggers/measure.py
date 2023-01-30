import pynini
from pynini.lib import pynutil

from ukr.graph_utils import (
    GraphFst, delete_extra_space,
)

from ukr.taggers.cardinal import CardinalFst
from ukr.taggers.decimal import DecimalFst
from ukr.utils import get_abs_path


class MeasureFst(GraphFst):

    def __init__(self, cardinal: CardinalFst, decimal: DecimalFst):
        super().__init__(name="measure", kind="classify")

        integer_graph = cardinal.graph_integer
        decimal_graph = decimal.graph

        units = pynini.invert(pynini.string_file(get_abs_path("data/measurements.tsv")))
        units = pynutil.insert("units: \"") + units + pynutil.insert("\"")

        optional_minus_graph = pynini.closure(pynutil.insert("negative: \"true\" ") + pynutil.delete("мінус "), 0, 1)

        graph = optional_minus_graph + integer_graph + delete_extra_space + units
        graph |= optional_minus_graph + decimal_graph + delete_extra_space + units

        final_graph = self.add_tokens(graph)
        self.fst = final_graph.optimize()
