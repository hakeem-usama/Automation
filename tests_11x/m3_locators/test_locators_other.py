from playwright.sync_api import Page


def test_multiple_matches_fails(page: Page):

    page.goto('')
    page.check('#heard-about')
    page.fill('#textarea', 'So I was thinking the other day...')
