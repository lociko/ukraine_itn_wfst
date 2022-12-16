from ukr.graph_utils import GraphFst
from ukr.verbalizers.cardinal import CardinalFst
from ukr.verbalizers.decimal import DecimalFst
from ukr.verbalizers.measure import MeasureFst
from ukr.verbalizers.money import MoneyFst
from ukr.verbalizers.ordinal import OrdinalFst


class VerbalizeFst(GraphFst):

    def __init__(self):
        super().__init__(name="verbalize", kind="verbalize")

        cardinal = CardinalFst()
        cardinal_graph = cardinal.fst
        ordinal_graph = OrdinalFst().fst
        decimal = DecimalFst()
        decimal_graph = decimal.fst
        measure_graph = MeasureFst(decimal=decimal, cardinal=cardinal).fst
        money_graph = MoneyFst(decimal=decimal).fst

        graph = (
                money_graph
                | measure_graph
                | ordinal_graph
                | decimal_graph
                | cardinal_graph
        )

        self.fst = graph
