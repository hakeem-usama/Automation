from playwright.sync_api import expect, Page


def test_select(page):
    page.goto(f'savings.html')

    deposit = page.get_by_test_id('deposit')
    period = page.get_by_test_id('period')
    result = page.get_by_test_id('result')
