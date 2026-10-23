# Plano de testes baseado em risco

Sistema sob teste: assistente financeiro simulado com recuperacao de documentos (RAG), ferramentas que executam acoes e um livro-razao com trilha de auditoria. O "modelo" e simulado para os testes serem deterministas; a estrategia vale para um LLM real (ver "Evolucao").

## Riscos e prioridade

| Risco | Impacto | Probabilidade | Prioridade | Cobertura |
|---|---|---|---|---|
| Vazamento de documento restrito ou de outro tenant | Alto | Media | P0 | test_security_llm, test_tenancy |
| Prompt injection que contorna regras | Alto | Alta | P0 | test_security_llm |
| Acao executada sem autorizacao (agencia excessiva) | Alto | Media | P0 | test_tools_unintended_actions |
| Resposta inventada (sem fonte) | Alto | Alta | P1 | test_rag_grounding |
| Erro de calculo ou arredondamento | Alto | Media | P1 | test_finance_calcs |
| Queda da recuperacao sem comportamento seguro | Medio | Media | P1 | test_resilience |
| Contrato de API quebrado | Medio | Media | P2 | test_api_contract |
| Fluxo de UI quebrado | Medio | Baixa | P2 | tests/ui |

## Estrategia

- **Smoke a cada commit** (contrato e resiliencia), **regressao completa** depois, **UI** em job separado.
- **Testes adversariais** parametrizados por idioma e tecnica de ofuscacao. Falhas conhecidas ficam como `xfail(strict=True)`: o teste passa a falhar quando a correcao chegar, forcando a revisao.
- **SQL como oraculo** para saldos, conciliacao de partida dobrada e trilha de auditoria.
- **Dados de teste**: documentos por tenant com classificacao (public, internal, restricted).

## Criterios de saida

Zero falhas P0 abertas sem decisao de risco registrada; achados documentados em `docs/findings.md`.

## Evolucao (com LLM real)

- Trocar `Assistant` por um cliente do modelo e usar verificacoes de propriedade (fonte citada, ausencia de segredo, recusa) em vez de igualdade de texto.
- Repetir cada caso N vezes e medir taxa de aprovacao, porque a saida varia.
- Avaliador automatico (LLM-as-a-judge) usado so como triagem, com amostra revisada por pessoa.
