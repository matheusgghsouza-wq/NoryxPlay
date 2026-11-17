from noryx.config import Rules
from noryx.rules import conversions, decide
from noryx.telegram import parse_caption

R = Rules(target_cpa=50, kill_spend_multiplier=1.5, kill_cpa_multiplier=2.0,
          scale_min_conversions=2, scale_pct=20, max_daily_budget=100)


def test_keeps_learning_without_spend():
    assert decide(20, 0, 5000, R, False).action == "keep"


def test_pauses_spend_without_conversion():
    assert decide(75, 0, 5000, R, False).action == "pause"


def test_pauses_expensive_cpa():
    assert decide(220, 2, 5000, R, False).action == "pause"


def test_scales_good_cpa_once_per_day():
    d = decide(80, 2, 5000, R, False)
    assert d.action == "scale" and d.new_budget_cents == 6000
    assert decide(80, 2, 5000, R, True).action == "keep"


def test_scale_respects_budget_cap():
    assert decide(80, 2, 9000, R, False).new_budget_cents == 10000
    assert decide(80, 2, 10000, R, False).action == "keep"


def test_conversions_sum():
    row = {"actions": [{"action_type": "offsite_conversion.fb_pixel_purchase", "value": "3"},
                       {"action_type": "link_click", "value": "40"}]}
    assert conversions(row, "offsite_conversion.fb_pixel_purchase") == 3


def test_parse_caption():
    products = {"ProdutoX": None, "outro": None}
    assert parse_caption("#produtox gancho 2", products, "outro") == ("ProdutoX", "gancho 2")
    assert parse_caption("sem tag", products, "outro") == ("outro", "sem tag")
    assert parse_caption("#desconhecido", products, "outro") == ("outro", "#desconhecido")
