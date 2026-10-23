"""Assistente financeiro simulado (substitui um LLM real, para os testes serem deterministas).

Tem guardrails de proposito simples. Os testes em tests/ mostram onde eles seguram e onde nao.
Pontos fracos conhecidos estao marcados com xfail(strict=True) e documentados em docs/findings.md.
"""
import re
import unicodedata

from .knowledge import DOCS
from .ledger import Ledger

INJECTION_PATTERNS = [
    r"ignore (all|previous|the above) instructions",
    r"ignore as instrucoes",
    r"you are now",
    r"system prompt",
    r"reveal your (rules|prompt)",
]
RESTRICTED = "restricted"
SENSITIVE_RE = re.compile(r"(SECRET|KEY-\d+|\bGLX-KEY\b)", re.I)


def _norm(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


class Assistant:
    def __init__(self, ledger=None, retriever_up=True):
        self.ledger = ledger or Ledger()
        self.retriever_up = retriever_up

    # ---- recuperacao (RAG simplificado) ----
    def retrieve(self, tenant, question):
        words = {w for w in re.findall(r"\w+", _norm(question)) if len(w) > 3}
        hits = []
        for d in DOCS.get(tenant, []):
            overlap = words & set(re.findall(r"\w+", _norm(d["text"])))
            if overlap:
                hits.append((len(overlap), d))
        return [d for _, d in sorted(hits, key=lambda x: -x[0])]

    def ask(self, tenant, question, role="employee"):
        if not self.retriever_up:
            return {"answer": "Servico temporariamente indisponivel. Tente novamente em instantes.",
                    "sources": [], "degraded": True}
        q = _norm(question)
        if any(re.search(p, q) for p in INJECTION_PATTERNS):
            return {"answer": "Nao posso seguir essa instrucao.", "sources": [], "blocked": True}
        docs = self.retrieve(tenant, question)
        if role != "admin":
            docs = [d for d in docs if d["classification"] != RESTRICTED]
        if not docs:
            return {"answer": "Nao encontrei essa informacao nos documentos disponiveis.", "sources": []}
        best = docs[0]
        return {"answer": best["text"], "sources": [best["id"]]}

    # ---- ferramentas (acoes) ----
    def run_tool(self, tenant, user_message, role="employee"):
        """Interpreta pedidos como 'lancar credito 100 na conta caixa'. So admin pode postar lancamentos."""
        m = re.search(r"lancar (debito|credito) ([\d.]+) na conta (\w+)", _norm(user_message))
        if not m:
            return {"executed": False, "reason": "nenhuma acao reconhecida"}
        if role != "admin":
            return {"executed": False, "reason": "permissao negada"}
        kind = {"debito": "debit", "credito": "credit"}[m.group(1)]
        self.ledger.post(tenant, m.group(3), m.group(2), kind, actor=role)
        return {"executed": True}
