import pytest

from research.tdm_reservation_check import (
    effective_reservation,
    html_tdm_meta,
    reservation_value,
    robots_disallowed,
    tdmrep_rule_for,
)

RULES = [
    {"location": "/news/*.xml", "tdm-reservation": 0},
    {"location": "/", "tdm-reservation": 1, "tdm-policy": "https://pub.example/tdm-policy.json"},
]


def test_first_matching_rule_wins():
    assert tdmrep_rule_for(RULES, "/news/feed.xml")["tdm-reservation"] == 0
    assert tdmrep_rule_for(RULES, "/sport/rss")["tdm-reservation"] == 1


def test_dollar_anchors_the_end_of_the_path():
    rules = [{"location": "/feed$", "tdm-reservation": 1}]
    assert tdmrep_rule_for(rules, "/feed") is not None
    assert tdmrep_rule_for(rules, "/feed/extra") is None


def test_matching_is_case_sensitive_and_malformed_input_is_ignored():
    assert tdmrep_rule_for([{"location": "/News/", "tdm-reservation": 1}], "/news/x") is None
    assert tdmrep_rule_for({"not": "a list"}, "/") is None
    assert tdmrep_rule_for([{"tdm-reservation": 1}, "junk"], "/") is None


@pytest.mark.parametrize(
    "raw, expected", [(1, 1), (0, 0), ("1", 1), (" 0 ", 0), (2, None), ("yes", None), (True, None)]
)
def test_only_0_and_1_are_valid_reservation_values(raw, expected):
    assert reservation_value(raw) == expected


def test_html_meta_is_read_case_insensitively():
    html = '<html><head><META NAME="TDM-Reservation" CONTENT="1"><meta name="tdm-policy" content="https://p/x"></head>'
    assert html_tdm_meta(html) == {"tdm-reservation": "1", "tdm-policy": "https://p/x"}
    assert html_tdm_meta("<p>no meta here") == {}


def test_precedence_file_then_header_then_meta():
    rule = {"location": "/", "tdm-reservation": 0, "tdm-policy": "https://p/file"}
    assert effective_reservation(rule, {}, {}) == (0, "https://p/file", "tdmrep.json")
    assert effective_reservation(rule, {"tdm-reservation": "1"}, {}) == (1, "https://p/file", "http-header")
    assert effective_reservation(rule, {"tdm-reservation": "1"}, {"tdm-reservation": "0"})[0:3:2] == (0, "html-meta")


def test_absent_or_invalid_later_values_never_reset_earlier_ones():
    rule = {"location": "/", "tdm-reservation": 1}
    assert effective_reservation(rule, {"tdm-reservation": "maybe"}, {})[0] == 1
    assert effective_reservation(None, {}, {}) == (None, None, "none")


def test_robots_rules_per_agent():
    robots = "User-agent: GPTBot\nDisallow: /\n\nUser-agent: *\nDisallow: /private/\n"
    result = robots_disallowed(robots, "https://pub.example/rss.xml", ("*", "GPTBot", "CATS-calibration"))
    assert result == {"*": False, "GPTBot": True, "CATS-calibration": False}
    assert robots_disallowed(robots, "https://pub.example/private/feed", ("*",)) == {"*": True}
