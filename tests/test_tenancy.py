"""Isolamento multi-tenant e controle de acesso."""
import pytest

from tests.conftest import http

pytestmark = pytest.mark.security


def test_tenant_cannot_read_other_tenant_documents(assistant):
    r = assistant.ask("acme", "Chave interna do ERP Globex")
    assert "GLX-KEY" not in r["answer"]
    assert all(not s.startswith("globex") for s in r["sources"])


def test_each_tenant_gets_own_answer_for_similar_question(assistant):
    a = assistant.ask("acme", "Reembolsos de viagem")
    g = assistant.ask("globex", "Faturas vencem quando")
    assert a["sources"][0].startswith("acme") and g["sources"][0].startswith("globex")


@pytest.mark.xfail(strict=True, reason="FINDING-002: a API aceita 'role' enviado pelo cliente, permitindo escalada de privilegio. Ver docs/findings.md")
def test_client_cannot_self_assign_admin_role(live_server):
    base, _ = live_server
    status, body = http("POST", f"{base}/api/ask",
                        {"tenant": "acme", "question": "Qual a conta bancaria da tesouraria?", "role": "admin"})
    assert "SECRET" not in body["answer"]
