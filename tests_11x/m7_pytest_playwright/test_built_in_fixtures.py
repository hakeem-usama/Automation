import pytest
from playwright.sync_api import Page, Browser, Playwright


def test_page_fixture(page: Page):
    name_input = page.get_by_label('First name')


def test_different_browsers(playwright: Playwright):
    pass


def test_browser(browser: Browser):
    pass


def test_browser_type(page: Page):
    pass


def test_incomplete_fixture_name(playwright: Playwright, page: Page):
    pass



