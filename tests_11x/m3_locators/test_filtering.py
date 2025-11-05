from playwright.sync_api import Page


def test_filtering_demo(page: Page):
    page.goto(f'savings.html')
