import pynini
from pynini.lib import pynutil

from ukr.graph_utils import (
    GraphFst,
)

from ukr.taggers.cardinal import CardinalFst
from ukr.taggers.decimals import DecimalFst
from ukr.utils import get_abs_path


class MeasureFst(GraphFst):

    def __init__(self, cardinal: CardinalFst, decimal: DecimalFst):
        super().__init__(name="ordinal", kind="classify")

        delete_space = pynutil.delete(" ")

        measurements = pynini.invert(pynini.string_file(get_abs_path("data/measurements.tsv")))

        graph = cardinal.fst + delete_space + measurements
        graph |= decimal.fst + delete_space + measurements

        self.fst = graph.optimize()
