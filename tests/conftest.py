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




    
    # # Go to login page
    # page.goto(CUREMD_DAT_LOGIN_ASP, timeout=60_000, wait_until="domcontentloaded")
    # page.locator("#vchLogin_Name").fill(Username)
    # page.locator("#vchPassword").fill(Password)

    # with page.expect_popup() as popup_info:
    #     page.get_by_role("button", name="Login").click()
    # logged_in_application = popup_info.value
    # logged_in_application.set_viewport_size({"width": 1920, "height": 1080})
    # # Sanity assertion on the new window URL prefix
    # expect(logged_in_application).to_have_url(re.compile(f"^{Expected_URL_Of_11x}"))

    # Yield the authenticated app page to the test
    

    # no explicit close needed—pytest-playwright cleans up the context
