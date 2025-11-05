from time import sleep

from playwright.sync_api import Page, BrowserType


# Code > CLI > config
def test_override_example(page: Page, browser_type: BrowserType):
    page.goto('')
