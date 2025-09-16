import re
from playwright.sync_api import Page, expect
import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.parametrize("browser_type", ["chromium"])
def test_has_title(browser_type):
    with sync_playwright() as p:
        browser = getattr(p, browser_type).launch(headless=True)
        page = browser.new_page()
        page.goto("https://fct24-backend-staging.onrender.com/docs")
        assert page.title() == "Travel Mate project - Swagger UI"
        browser.close()



