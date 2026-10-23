"""Contrato da API: status codes, validacao de entrada, erros."""
from tests.conftest import http


def test_health(live_server):
    base, _ = live_server
    status, body = http("GET", f"{base}/health")
    assert status == 200 and body == {"status": "ok"}


def test_ask_returns_answer_and_sources(live_server):
    base, _ = live_server
    status, body = http("POST", f"{base}/api/ask", {"tenant": "acme", "question": "Em quanto tempo reembolsos de viagem sao aprovados?"})
    assert status == 200
    assert set(body) >= {"answer", "sources"}
    assert body["sources"] == ["acme-001"]


def test_missing_fields_return_422(live_server):
    base, _ = live_server
    status, body = http("POST", f"{base}/api/ask", {"tenant": "acme"})
    assert status == 422
    assert "obrigatorios" in body["error"]


def test_malformed_json_returns_400(live_server):
    base, _ = live_server
    status, _ = http("POST", f"{base}/api/ask", raw=b"{nao e json")
    assert status == 400


def test_unknown_route_returns_404(live_server):
    base, _ = live_server
    status, _ = http("GET", f"{base}/nao-existe")
    assert status == 404
