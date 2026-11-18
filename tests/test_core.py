from noryx.config import Rules
from noryx.rules import AdStat, decide_campaign, results
from noryx.telegram import parse_caption
from noryx.uploader import chunks

R = Rules(target_cost=5.0, max_cost=6.0, validate_min_results=3, kill_spend_no_result=10,
          kill_min_spend=12, pause_others_on_validate=True)


def ad(i, spend, res, active=True):
    return AdStat(str(i), f"ad{i}", spend, res, active)


def actions(ads, rules=R):
    return {a.ad_id: act for a, act, _ in decide_campaign(ads, rules)}


def test_nothing_happens_while_learning():
    assert actions([ad(1, 8, 1), ad(2, 6, 0)]) == {}


def test_pauses_spend_without_result():
    assert actions([ad(1, 12, 0)]) == {"1": "pause"}


def test_pauses_expensive_cost():
    assert actions([ad(1, 14, 2)]) == {"1": "pause"}  # R$7,00 por compra


def test_between_target_and_max_keeps_running():
    assert actions([ad(1, 16.5, 3)]) == {}  # R$5,50: não valida, mas ainda compensa


def test_validated_keeps_and_others_pause():
    got = actions([ad(1, 14.5, 3), ad(2, 4, 1), ad(3, 0, 0, active=False)])
    assert got == {"1": "validate", "2": "pause"}


def test_others_keep_running_when_option_off():
    rules = Rules(**{**R.__dict__, "pause_others_on_validate": False})
    assert actions([ad(1, 14.5, 3), ad(2, 4, 1)], rules) == {"1": "validate"}


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


# ---------- banco de criativos / reposição ----------
import sqlite3  # noqa: E402
from pathlib import Path  # noqa: E402
from types import SimpleNamespace  # noqa: E402

from noryx import db  # noqa: E402
from noryx.config import Product  # noqa: E402
from noryx.uploader import is_alive, pick_creatives  # noqa: E402


def test_is_alive():
    assert is_alive({"status": "ACTIVE", "effective_status": "ACTIVE"})
    assert is_alive({"status": "ACTIVE", "effective_status": "CAMPAIGN_PAUSED"})  # aguardando você ligar
    assert not is_alive({"status": "PAUSED", "effective_status": "PAUSED"})
    assert not is_alive({"status": "ACTIVE", "effective_status": "DISAPPROVED"})


def _bank(tmp_path: Path) -> sqlite3.Connection:
    conn = db.connect(tmp_path)
    for i in range(1, 6):
        conn.execute("INSERT INTO creatives (tg_file_unique_id, product_key, local_path) VALUES (?, 'p', '')",
                     (f"u{i}",))
    # criativo 1 já testado em c1/n1; criativo 4 validou em c2/n1
    conn.execute("INSERT INTO uploads (creative_id, account_key, number_key, status, ad_id) "
                 "VALUES (1, 'c1', 'n1', 'done', 'ad1'), (4, 'c2', 'n1', 'done', 'ad4')")
    conn.execute("INSERT INTO actions (object_id, action, day) VALUES ('ad4', 'validate', '2026-01-01')")
    conn.commit()
    return conn


def test_pick_prioritizes_validated_and_skips_tested(tmp_path):
    conn = _bank(tmp_path)
    settings = SimpleNamespace(products={"p": Product(key="p", message="m")})
    picks = [c["id"] for c in pick_creatives(conn, settings, "c1", "n1", 3)]
    assert picks == [4, 2, 3]


def test_pick_respects_product_accounts(tmp_path):
    conn = _bank(tmp_path)
    settings = SimpleNamespace(products={"p": Product(key="p", message="m", accounts=["c9"])})
    assert pick_creatives(conn, settings, "c1", "n1", 3) == []


# ---------- check ----------
from noryx import check  # noqa: E402
from noryx.config import Account, Number  # noqa: E402
from noryx.meta import Meta, MetaError  # noqa: E402


class _Resp:
    def __init__(self, data):
        self._d = data

    def json(self):
        return self._d


def _check_settings():
    acc = Account("c1", "100", {"n1": Number("n1", "P1", "T1"), "n2": Number("n2", "P2", "T2")}, "tok")
    return SimpleNamespace(telegram_token="t", telegram_chat_id="-1", graph_version="v23.0", dry_run=True,
                           accounts={"c1": acc})


def _fake_get(bad: bool):
    def get(self, path, **params):
        if path == "act_100":
            return {"name": "Conta 1", "account_status": 1, "currency": "BRL"}
        if path in ("P1", "P2"):
            return {"name": f"Página {path}"}
        if path == "T1":
            return {"name": "Modelo 1", "account_id": "100", "bid_strategy": "LOWEST_COST_WITH_BID_CAP",
                    "daily_budget": "10000"}
        if path == "T2":
            if bad:
                raise MetaError("(#100) objeto não existe")
            return {"name": "Modelo 2", "account_id": "100", "daily_budget": "10000"}
        if path.endswith("/adsets"):
            return {"data": [{"id": "a"}]}
        if path.endswith("/ads"):
            return {"data": [{"id": "x"}] if bad and path.startswith("T1") else []}
        raise AssertionError(path)
    return get


def _fake_tg(url, params=None, timeout=None):
    if url.endswith("/getMe"):
        return _Resp({"ok": True, "result": {"username": "noryx_bot"}})
    return _Resp({"ok": True, "result": {"title": "Criativos"}})


def test_check_all_good(monkeypatch, capsys):
    monkeypatch.setattr(Meta, "get", _fake_get(bad=False))
    monkeypatch.setattr(check.requests, "get", _fake_tg)
    assert check.run(_check_settings()) is True
    assert "Tudo certo" in capsys.readouterr().out


def test_check_finds_problems(monkeypatch, capsys):
    monkeypatch.setattr(Meta, "get", _fake_get(bad=True))
    monkeypatch.setattr(check.requests, "get", _fake_tg)
    assert check.run(_check_settings()) is False
    out = capsys.readouterr().out
    assert "1 anúncio(s) (precisa ter 0)" in out
    assert "sem acesso à campanha modelo T2" in out


# ---------- painel web ----------
import io  # noqa: E402

from noryx.web import create_app  # noqa: E402


def _web(tmp_path):
    acc = Account("conta1", "1", {"n1": Number("n1", "P", "T"), "n2": Number("n2", "P2", "T2")}, "tok")
    s = SimpleNamespace(data_dir=tmp_path, dry_run=True, accounts={"conta1": acc},
                        products={"dorama": Product("dorama", "m")}, default_product="dorama")
    app = create_app(s, password="segredo")
    app.config["TESTING"] = True
    return app.test_client(), s


def test_web_requires_login(tmp_path):
    client, _ = _web(tmp_path)
    assert client.get("/").status_code == 302
    assert client.post("/api/enviar").status_code == 401
    assert "Senha errada" in client.post("/login", data={"password": "x"}, follow_redirects=True).text


def test_web_upload_goes_to_bank(tmp_path):
    client, s = _web(tmp_path)
    client.post("/login", data={"password": "segredo"})
    r = client.post("/api/enviar", data={"product": "dorama", "variant": "gancho 1",
                                         "video": (io.BytesIO(b"fake"), "video.mp4")},
                    content_type="multipart/form-data")
    assert r.json == {"ok": True, "id": 1, "name": "gancho 1"}
    bad = client.post("/api/enviar", data={"video": (io.BytesIO(b"x"), "foto.jpg")},
                      content_type="multipart/form-data")
    assert bad.status_code == 400
    home = client.get("/").text
    assert "#1 gancho 1" in home and "No banco" in home and "0/2" in home
    conn = db.connect(tmp_path)
    row = conn.execute("SELECT * FROM creatives").fetchone()
    assert row["product_key"] == "dorama" and Path(row["local_path"]).read_bytes() == b"fake"


def test_web_shows_brasilia_time(tmp_path):
    client, _ = _web(tmp_path)
    app = client.application
    assert app.jinja_env.filters["quando"]("2026-11-18 03:34:00") == "18/11 00:34"
    assert app.jinja_env.filters["quando"]("2026-11-18 03:34:00", True) == "00:34"
    assert app.jinja_env.filters["quando"]("2026-11-18T03:34") == "18/11 00:34"
    assert app.jinja_env.filters["quando"]("lixo") == "lixo"
