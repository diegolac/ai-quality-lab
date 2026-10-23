# AI Quality Lab

Laboratório prático de QA para aplicações com IA em contexto financeiro. Mostra como planejar e automatizar testes de um assistente com recuperação de documentos (RAG), ferramentas que executam ações e um livro-razão com trilha de auditoria.

O "modelo" é uma simulação determinística, sem chave de API, para que qualquer pessoa rode os testes e obtenha o mesmo resultado. O foco aqui é a estratégia de teste, não o modelo.

## Rodar

```bash
pip install -r requirements.txt
playwright install chromium   # apenas para os testes de UI
pytest --ignore=tests/ui      # API, segurança, RAG, financeiro
pytest tests/ui -m ui         # UI com Playwright
pytest --html=report.html --self-contained-html --ignore=tests/ui
```

## O que cada suite cobre

| Responsabilidade | Onde |
|---|---|
| Plano de testes baseado em risco | `docs/test-plan.md` |
| Validação de busca e recuperação de documentos (RAG), respostas fundamentadas | `tests/test_rag_grounding.py` |
| Prompt injection (OWASP LLM01) | `tests/test_security_llm.py` |
| Divulgação de informação sensível (LLM06) | `tests/test_security_llm.py` |
| Isolamento multi-tenant e controle de acesso | `tests/test_tenancy.py` |
| Ações indevidas de ferramentas (LLM08) | `tests/test_tools_unintended_actions.py` |
| Queda e recuperação do serviço | `tests/test_resilience.py` |
| Contrato de API | `tests/test_api_contract.py` |
| Cálculos, conciliação, trilha de auditoria (SQL) | `tests/test_finance_calcs.py` |
| Fluxo de interface (Playwright) | `tests/ui/test_smoke_ui.py` |
| Smoke e regressão em pipeline | `.github/workflows/ci.yml` |
| Registro de achados | `docs/findings.md` |

## Achados conhecidos

Duas falhas ficam marcadas como `xfail(strict=True)` de propósito e documentadas em `docs/findings.md`: bypass multilingue do filtro de injection e escalada de privilégio por papel enviado pelo cliente. Quando forem corrigidas, os testes passam a falhar e exigem remover a marca.

## Limites

- O assistente é simulado; não há medição de qualidade de modelo real.
- Evolução planejada: trocar a simulação por um modelo real, repetir cada caso várias vezes e medir taxa de aprovação; usar avaliador automático apenas como triagem.
