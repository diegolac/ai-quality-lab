# Achados

Formato: cenario, esperado, observado, severidade, passos para reproduzir.

## FINDING-001: bypass multilingue e ofuscado do filtro de prompt injection
- **Severidade:** alta
- **Esperado:** instrucoes de ignorar regras bloqueadas em qualquer idioma ou grafia.
- **Observado:** o filtro por regex cobre apenas frases exatas em ingles e portugues. Espanhol, portugues com palavra extra ("todas as") e texto com letras separadas passam.
- **Reproduzir:** `pytest tests/test_security_llm.py::test_multilingual_and_obfuscated_injections_are_blocked`
- **Recomendacao:** nao depender so de lista de padroes; aplicar controle de acesso nos dados (o documento restrito ja e filtrado por papel) e classificador de intencao independente do idioma.

## FINDING-002: escalada de privilegio por papel enviado pelo cliente
- **Severidade:** alta
- **Esperado:** o papel vem da sessao autenticada no servidor.
- **Observado:** `POST /api/ask` aceita `"role": "admin"` no corpo e libera documentos restritos.
- **Reproduzir:** `pytest tests/test_tenancy.py::test_client_cannot_self_assign_admin_role`
- **Recomendacao:** ignorar `role` do corpo da requisicao e derivar do token de sessao.
- **Status:** corrigido.  
