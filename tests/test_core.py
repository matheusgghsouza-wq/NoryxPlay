from noryx.config import Rules
from noryx.rules import AdStat, decide_campaign, results
from noryx.telegram import parse_caption
from noryx.uploader import chunks

R = Rules(target_cost=1.41, validate_min_results=10, kill_spend_no_result=10,
          kill_min_spend=10, kill_cost_multiplier=1.5, pause_others_on_validate=True)


def ad(i, spend, res, active=True):
    return AdStat(str(i), f"ad{i}", spend, res, active)


def actions(ads, rules=R):
    return {a.ad_id: act for a, act, _ in decide_campaign(ads, rules)}


def test_nothing_happens_while_learning():
    assert actions([ad(1, 3, 1), ad(2, 2, 0)]) == {}


def test_pauses_spend_without_result():
    assert actions([ad(1, 12, 0)]) == {"1": "pause"}


def test_pauses_expensive_cost():
    assert actions([ad(1, 30, 10)]) == {"1": "pause"}  # R$3,00 por resultado


def test_validated_keeps_and_others_pause():
    got = actions([ad(1, 13, 10), ad(2, 4, 2), ad(3, 0, 0, active=False)])
    assert got == {"1": "validate", "2": "pause"}


def test_others_keep_running_when_option_off():
    rules = Rules(**{**R.__dict__, "pause_others_on_validate": False})
    assert actions([ad(1, 13, 10), ad(2, 4, 2)], rules) == {"1": "validate"}


def test_results_sum():
    row = {"actions": [{"action_type": R.result_action, "value": "7"},
                       {"action_type": "link_click", "value": "40"}]}
    assert results(row, R.result_action) == 7


def test_chunks():
    assert chunks([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_parse_caption():
    products = {"ProdutoX": None, "outro": None}
    assert parse_caption("#produtox gancho 2", products, "outro") == ("ProdutoX", "gancho 2")
    assert parse_caption("sem tag", products, "outro") == ("outro", "sem tag")
    assert parse_caption("#desconhecido", products, "outro") == ("outro", "#desconhecido")
