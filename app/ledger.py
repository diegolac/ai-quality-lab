"""Livro-razao simples com trilha de auditoria, em SQLite (memoria)."""
import sqlite3
from decimal import Decimal, ROUND_HALF_UP


class Ledger:
    def __init__(self):
        self.db = sqlite3.connect(":memory:", check_same_thread=False)
        self.db.executescript(
            """
            CREATE TABLE entries (id INTEGER PRIMARY KEY, tenant TEXT, account TEXT,
                                  amount_cents INTEGER, kind TEXT);
            CREATE TABLE audit (id INTEGER PRIMARY KEY, tenant TEXT, actor TEXT,
                                action TEXT, detail TEXT);
            """
        )

    def post(self, tenant, account, amount, kind, actor):
        cents = int((Decimal(str(amount)) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        if kind not in ("debit", "credit"):
            raise ValueError("kind invalido")
        if cents <= 0:
            raise ValueError("valor deve ser positivo")
        self.db.execute("INSERT INTO entries(tenant,account,amount_cents,kind) VALUES (?,?,?,?)",
                        (tenant, account, cents, kind))
        self.db.execute("INSERT INTO audit(tenant,actor,action,detail) VALUES (?,?,?,?)",
                        (tenant, actor, "post_entry", f"{kind}:{account}:{cents}"))
        self.db.commit()

    def balance_cents(self, tenant, account):
        row = self.db.execute(
            "SELECT COALESCE(SUM(CASE kind WHEN 'credit' THEN amount_cents ELSE -amount_cents END),0) "
            "FROM entries WHERE tenant=? AND account=?", (tenant, account)).fetchone()
        return row[0]

    def is_balanced(self, tenant):
        d, c = self.db.execute(
            "SELECT COALESCE(SUM(CASE WHEN kind='debit' THEN amount_cents END),0),"
            "COALESCE(SUM(CASE WHEN kind='credit' THEN amount_cents END),0) FROM entries WHERE tenant=?",
            (tenant,)).fetchone()
        return d == c

    def audit_rows(self, tenant):
        return self.db.execute("SELECT actor,action,detail FROM audit WHERE tenant=?", (tenant,)).fetchall()


def installment_schedule(principal, months, annual_rate_pct):
    """Parcelas pela tabela Price. Retorna lista de centavos; a ultima parcela absorve o arredondamento."""
    p = Decimal(str(principal))
    i = Decimal(str(annual_rate_pct)) / 100 / 12
    if months <= 0:
        raise ValueError("months deve ser positivo")
    if i == 0:
        pmt = p / months
    else:
        pmt = p * i / (1 - (1 + i) ** -months)
    cents = int((pmt * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    return [cents] * months
