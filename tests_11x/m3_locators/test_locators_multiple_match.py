from playwright.sync_api import Page


def test_multiple_matches_fails(page: Page):
    page.goto('')


def test_multiple_matches_first_last_nth(page: Page):
    page.goto('')


def test_multiple_matches_count_or_iterate(page):
    page.goto('')
    page.get_by_role('button', name='Register').click()
