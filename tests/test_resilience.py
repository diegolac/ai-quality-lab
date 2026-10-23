"""Falhas e degradacao: o que acontece quando a recuperacao de documentos cai."""
from app.assistant import Assistant
from app.server import serve
import threading
from tests.conftest import http


def test_outage_returns_safe_fallback_without_made_up_content():
    a = Assistant(retriever_up=False)
    r = a.ask("acme", "Qual o limite de aprovacao do gerente?")
    assert r["degraded"] is True
    assert r["sources"] == []
    assert "10000" not in r["answer"]


def test_outage_surfaces_503_on_api():
    a = Assistant(retriever_up=False)
    srv = serve(a, port=0)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        status, body = http("POST", f"http://127.0.0.1:{srv.server_address[1]}/api/ask",
                            {"tenant": "acme", "question": "limite do gerente"})
        assert status == 503 and body["degraded"] is True
    finally:
        srv.shutdown()


def test_service_recovers_after_outage():
    a = Assistant(retriever_up=False)
    assert a.ask("acme", "limite de aprovacao do gerente").get("degraded")
    a.retriever_up = True
    assert a.ask("acme", "limite de aprovacao do gerente")["sources"] == ["acme-002"]
