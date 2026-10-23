"""Fundamentacao: toda resposta deve vir de um documento citado; sem base, deve admitir que nao sabe."""
import pytest

pytestmark = pytest.mark.rag


def test_answer_is_grounded_in_cited_source(assistant):
    r = assistant.ask("acme", "Qual o limite de aprovacao do gerente por transacao?")
    assert r["sources"] == ["acme-002"]
    assert "10000" in r["answer"]


def test_answer_text_comes_only_from_cited_document(assistant):
    from app.knowledge import DOCS
    r = assistant.ask("acme", "Reembolsos de viagem sao aprovados em quantos dias?")
    cited = {d["id"]: d["text"] for d in DOCS["acme"]}[r["sources"][0]]
    assert r["answer"] == cited  # nada inventado alem do documento


@pytest.mark.parametrize("question", [
    "Qual a capital da Franca?",
    "Qual o salario do diretor financeiro?",
    "Quantas pessoas trabalham na empresa?",
])
def test_unknown_topics_do_not_hallucinate(assistant, question):
    r = assistant.ask("acme", question)
    assert r["sources"] == []
    assert "Nao encontrei" in r["answer"]


def test_unknown_tenant_has_no_documents(assistant):
    r = assistant.ask("inexistente", "reembolsos de viagem")
    assert r["sources"] == []


def test_same_question_is_consistent_across_runs(assistant):
    answers = {assistant.ask("acme", "limite de aprovacao do gerente")["answer"] for _ in range(20)}
    assert len(answers) == 1
