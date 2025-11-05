import pytest
from playwright.sync_api import Page


class TestThing:

    def test_one(self, page: Page):
        pass

    def test_two(self, page: Page):
        pass

    def test_three(self, page: Page):
        assert page.evaluate("Intl.DateTimeFormat().resolvedOptions().timeZone") == "Europe/Madrid"
        assert page.evaluate("window.navigator.languages") == ["es-ES"]

    def test_four(self, page: Page):
        assert page.evaluate("Intl.DateTimeFormat().resolvedOptions().timeZone") == "Europe/Madrid"
        assert page.evaluate("window.navigator.languages") == ["es-ES"]
