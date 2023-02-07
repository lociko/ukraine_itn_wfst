import pynini

from ukr.graph_utils import (
    GraphFst,
    delete_extra_space,
    delete_space,
    NEMO_DIGIT,
    NEMO_CHAR,
)
from pynini.lib import pynutil

from ukr.taggers.cardinal import CardinalFst
from ukr.taggers.ordinal import OrdinalFst
from ukr.utils import get_abs_path


class TimeFst(GraphFst):
    """
    Finite state transducer for classifying time
        e.g. сьома година п'ять хвилин" -> time { hours: "07" minutes: "05" }
        e.g. о пів на десяту -> time { hours: "09" minutes: "30" }
        e.g. чверть на десяту -> time { hours: "09" minutes: "15" }
        e.g. за чверть одинадцята -> time { hours: "10" minutes: "45" }
        e.g. п'ять хвилин на дванадцяту -> time { hours: "11" minutes: "05" }

        # TODO: add this features
        e.g. twelve past one -> time { minutes: "12" hours: "1" }
        e.g. two o clock a m -> time { hours: "2" suffix: "a.m." }
        e.g. quarter past two -> time { hours: "2" minutes: "15" }
    """

    def __init__(self, cardinal: CardinalFst, ordinal: OrdinalFst):
        super().__init__(name="time", kind="classify")

        hours = pynini.string_file(get_abs_path("data/time/hours.tsv"))
        minutes = pynini.string_file(get_abs_path("data/time/minutes.tsv"))
        to_hour = pynini.string_file(get_abs_path("data/time/to_hour.tsv"))

        hours_ordinal = ordinal.graph_up_to_hundred_component
        hours_ordinal = hours_ordinal @ (pynini.closure(NEMO_DIGIT) + pynutil.delete(pynini.union("-") + pynini.closure(NEMO_CHAR)))
        graph_hours = hours_ordinal + delete_space + pynutil.delete(hours)
        graph_hours = pynutil.insert("hours: \"") + graph_hours + pynutil.insert("\"")

        graph_minutes = cardinal.graph_up_to_hundred_component + delete_space + pynutil.delete(minutes)
        graph_minutes = pynutil.insert("minutes: \"") + graph_minutes + pynutil.insert("\"")

        graph_half_hour = pynutil.delete("о пів на ") + hours_ordinal
        graph_half_hour = graph_half_hour @ to_hour.invert()
        graph_half_hour = pynutil.insert("hours: \"") + graph_half_hour + pynutil.insert("\" minutes: \"30\"")

        to_hour_graph = hours_ordinal @ to_hour
        graph_to_quarter_hour = pynutil.delete("чверть на ") + to_hour_graph
        graph_to_quarter_hour = pynutil.insert("hours: \"") + graph_to_quarter_hour + pynutil.insert("\" minutes: \"15\"")

        graph_from_quarter_hour = pynutil.delete("за чверть ") + to_hour_graph
        graph_from_quarter_hour = pynutil.insert("hours: \"") + graph_from_quarter_hour + pynutil.insert("\" minutes: \"45\"")

        graph_hm = graph_hours + delete_extra_space + graph_minutes

        # п'ять хвилин на дванадцяту -> time { hours: "11" minutes: "05" }
        graph_mh = graph_minutes + pynutil.delete(" на ") + pynutil.insert(" hours: \"") + to_hour_graph + pynutil.insert("\"")

        final_graph = graph_hm | graph_mh | graph_half_hour | graph_to_quarter_hour | graph_from_quarter_hour
        final_graph = self.add_tokens(final_graph.optimize())

        self.fst = final_graph.optimize()
