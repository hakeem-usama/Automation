import pytest
from playwright.sync_api import expect, Page, Browser


@pytest.fixture
def page():
    pass


class TestThings:

    def test_one(self, browser: Browser):
        page: Page = browser.new_context(
            viewport={'width': 500, 'height': 400},
            user_agent='xyz',
            locale='es_ES'
            # ...
        ).new_page()

        name_input = page.get_by_label('First name')
        name_input.fill('Sofia')
        expect(name_input).to_have_value('Sofia')

    def test_two(self, browser: Browser):
        page: Page = browser.new_context(
            viewport={'width': 500, 'height': 400},
            user_agent='xyz',
            locale='es_ES'
            # ...
        ).new_page()

        name_input = page.get_by_label('First name')
        name_input.fill('Andrejs')
        expect(name_input).to_have_value('Andrejs')
