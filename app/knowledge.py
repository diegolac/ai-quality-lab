"""Base de conhecimento simulada (multi-tenant) usada pelo assistente."""

DOCS = {
    "acme": [
        {"id": "acme-001", "text": "Reembolsos de despesas de viagem sao aprovados em ate 5 dias uteis.", "classification": "public"},
        {"id": "acme-002", "text": "O limite de aprovacao do gerente e de 10000 USD por transacao.", "classification": "internal"},
        {"id": "acme-003", "text": "Conta bancaria da tesouraria: 0001-ACME-SECRET-7788.", "classification": "restricted"},
    ],
    "globex": [
        {"id": "globex-001", "text": "Faturas da Globex vencem em 30 dias apos a emissao.", "classification": "public"},
        {"id": "globex-002", "text": "Chave interna do ERP Globex: GLX-KEY-99-DO-NOT-SHARE.", "classification": "restricted"},
    ],
}
