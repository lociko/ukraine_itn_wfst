import pytest

from ukr.wfst import reorder


@pytest.mark.parametrize("given,expected", [
    (
            """tokens { word { name: "збагатила" } }""",
            """tokens { word { name: "збагатила" } }""",
    ), (
            """tokens { word { name: "збагатила" } } tokens { time { minutes: "05">> hours: "11" } }""",
            """tokens { word { name: "збагатила" } } tokens { time { hours: "11" minutes: "05" } }""",
    ), (
            """tokens { time { minutes: "05">> hours: "11" } } tokens { time { minutes: "15">> hours: "22" } }""",
            """tokens { time { hours: "11" minutes: "05" } } tokens { time { hours: "22" minutes: "15" } }""",
    ),
])
def test_reorder(given, expected):
    assert reorder(given) == expected
