"""Smoke test de UI com Playwright (pytest). Requer: pip install playwright && playwright install chromium"""
import pytest

pytest.importorskip("playwright")
from playwright.sync_api import sync_playwright

pytestmark = pytest.mark.ui


@pytest.fixture
def page():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        yield pg
        b.close()


def test_user_gets_grounded_answer_in_ui(page, live_server):
    base, _ = live_server
    page.goto(base)
    page.select_option("#tenant", "acme")
    page.fill("#q", "limite de aprovacao do gerente")
    page.click("#send")
    page.wait_for_function("document.getElementById('answer').textContent.length > 0")
    assert "10000" in page.inner_text("#answer")


def test_user_does_not_see_restricted_data_in_ui(page, live_server):
    base, _ = live_server
    page.goto(base)
    page.fill("#q", "conta bancaria da tesouraria")
    page.click("#send")
    page.wait_for_function("document.getElementById('answer').textContent.length > 0")
    assert "SECRET" not in page.inner_text("#answer")
