from playwright.sync_api import Page


def test_fill(page: Page):
    page.goto('')


def test_click_demo(page: Page):
    page.goto('')
    btn = page.get_by_role('button', name='Register')
