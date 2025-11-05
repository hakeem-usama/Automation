from playwright.sync_api import Page, expect


def test_generic_locators(page: Page):
    page.goto('')
