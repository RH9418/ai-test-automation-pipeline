import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def shared_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        # Pytest will automatically handle the teardown here
        context.close()
        browser.close()
