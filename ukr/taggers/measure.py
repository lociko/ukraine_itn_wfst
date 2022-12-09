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

        units = pynini.invert(pynini.string_file(get_abs_path("data/measurements.tsv")))
        units = pynutil.insert("units: \"") + units + pynutil.insert("\"")

        graph = cardinal.fst + delete_extra_space + units
        graph |= decimal.fst + delete_extra_space + units

        final_graph = self.add_tokens(graph)
        self.fst = final_graph.optimize()
