# AI Quality Lab

Laboratorio pratico de QA para aplicacoes com IA em contexto financeiro. Mostra como planejar e automatizar testes de um assistente com recuperacao de documentos (RAG), ferramentas que executam acoes e um livro-razao com trilha de auditoria.

O "modelo" e uma simulacao deterministica, sem chave de API, para que qualquer pessoa rode os testes e obtenha o mesmo resultado. O foco aqui e a estrategia de teste, nao o modelo.

## Rodar

```bash
pip install -r requirements.txt
playwright install chromium   # so para os testes de UI
pytest --ignore=tests/ui      # API, seguranca, RAG, financeiro
pytest tests/ui -m ui         # UI com Playwright
pytest --html=report.html --self-contained-html --ignore=tests/ui
```

## O que cada suite cobre

| Responsabilidade | Onde |
|---|---|
| Plano de testes baseado em risco | `docs/test-plan.md` |
| Validacao de busca e recuperacao de documentos (RAG), respostas fundamentadas | `tests/test_rag_grounding.py` |
| Prompt injection (OWASP LLM01) | `tests/test_security_llm.py` |
| Divulgacao de informacao sensivel (LLM06) | `tests/test_security_llm.py` |
| Isolamento multi-tenant e controle de acesso | `tests/test_tenancy.py` |
| Acoes indevidas de ferramentas (LLM08) | `tests/test_tools_unintended_actions.py` |
| Queda e recuperacao do servico | `tests/test_resilience.py` |
| Contrato de API | `tests/test_api_contract.py` |
| Calculos, conciliacao, trilha de auditoria (SQL) | `tests/test_finance_calcs.py` |
| Fluxo de interface (Playwright) | `tests/ui/test_smoke_ui.py` |
| Smoke e regressao em pipeline | `.github/workflows/ci.yml` |
| Registro de achados | `docs/findings.md` |

## Achados conhecidos

Duas falhas ficam marcadas como `xfail(strict=True)` de proposito e documentadas em `docs/findings.md`: bypass multilingue do filtro de injection e escalada de privilegio por papel enviado pelo cliente. Quando forem corrigidas, os testes passam a falhar e exigem remover a marca.

## Limites

- O assistente e simulado; nao ha medicao de qualidade de modelo real.
- Evolucao planejada: trocar a simulacao por um modelo real, repetir cada caso varias vezes e medir taxa de aprovacao; usar avaliador automatico apenas como triagem.
