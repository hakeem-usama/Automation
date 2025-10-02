# tests/conftest.py
import re
import pytest
from playwright.sync_api import Page, expect
from tests.Utils.constants import *
from tests.pages.login_page import Login11x

@pytest.fixture()
def logged_in_application(page: Page) -> Page:
    login_11x=Login11x(page)
    login_11x.navigateTo11x()
    logged_in_application=login_11x.login11x(Username,Password)
    logged_in_application.set_viewport_size({"width": 1920, "height": 1080})
    expect(logged_in_application).to_have_url(re.compile(f"^{Expected_URL_Of_11x}"))
    yield logged_in_application

