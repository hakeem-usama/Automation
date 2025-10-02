from pprint import pprint

from playwright.sync_api import expect, Page, APIResponse, Playwright, APIRequestContext, Response


def test_api_request_response(page: Page):
    response: Response = page.goto('')


def test_api_request_context(playwright: Playwright):
    pass
