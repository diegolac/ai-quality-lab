"""Calculos financeiros, conciliacao e trilha de auditoria (SQL como oraculo)."""
import pytest

from app.ledger import Ledger, installment_schedule

pytestmark = pytest.mark.finance


def test_rounding_half_up_on_posting():
    l = Ledger()
    l.post("acme", "caixa", "10.005", "credit", "admin")
    assert l.balance_cents("acme", "caixa") == 1001  # 10,005 -> 10,01


def test_no_float_drift_on_many_small_postings():
    l = Ledger()
    for _ in range(1000):
        l.post("acme", "caixa", "0.10", "credit", "admin")
    assert l.balance_cents("acme", "caixa") == 10000


@pytest.mark.parametrize("amount", [0, -5, "0"])
def test_invalid_amounts_rejected(amount):
    with pytest.raises(ValueError):
        Ledger().post("acme", "caixa", amount, "credit", "admin")


def test_double_entry_reconciliation():
    l = Ledger()
    l.post("acme", "caixa", "100", "debit", "admin")
    l.post("acme", "receita", "100", "credit", "admin")
    assert l.is_balanced("acme")
    l.post("acme", "caixa", "1", "debit", "admin")
    assert not l.is_balanced("acme")


def test_audit_trail_matches_entries_one_to_one():
    l = Ledger()
    for i in range(5):
        l.post("acme", "caixa", i + 1, "credit", "admin")
    entries = l.db.execute("SELECT COUNT(*) FROM entries WHERE tenant='acme'").fetchone()[0]
    audits = l.db.execute("SELECT COUNT(*) FROM audit WHERE tenant='acme'").fetchone()[0]
    assert entries == audits == 5


def test_tenant_data_is_isolated_in_sql():
    l = Ledger()
    l.post("acme", "caixa", "50", "credit", "admin")
    assert l.balance_cents("globex", "caixa") == 0
    assert l.audit_rows("globex") == []


def test_price_table_installments():
    parcelas = installment_schedule(1000, 12, 12)
    assert len(parcelas) == 12
    assert parcelas[0] == 8885  # R$ 88,85 por mes, valor de referencia da tabela Price
