# tests/conftest.py
import re
import time
import pytest
from playwright.sync_api import Page, expect, Error, TimeoutError as PlaywrightTimeoutError
from tests_10G.Utils.constants import *
from tests_10G.pages.login_page import Login10G

def _wait_for_application_ready(app_page: Page, timeout_ms: int = 60_000) -> None:
    deadline = time.time() + timeout_ms / 1000
    poll_interval_ms = 200
    while time.time() < deadline:
        menu_ready = False
        body_ready = False

        menu_frame = app_page.frame(name="fra_Menu_CureMD")
        if menu_frame is not None:
            try:
                menu_frame.wait_for_selector(f"xpath={patient_btn}", state="visible", timeout=1_000)
                if menu_frame.evaluate("document.readyState") == "complete":
                    menu_ready = True
            except (PlaywrightTimeoutError, Error):
                pass

        body_frame = app_page.frame(name="fraCureMD_Body")
        if body_frame is not None:
            try:
                if body_frame.evaluate("document.readyState") == "complete" and body_frame.url != "about:blank":
                    body_ready = True
            except Error:
                pass

        if menu_ready and body_ready:
            return

        app_page.wait_for_timeout(poll_interval_ms)

    raise RuntimeError("Application shell did not finish loading within allotted time")

@pytest.fixture()
def logged_in_application(page: Page) -> Page:
    page.wait_for_load_state("domcontentloaded")
    login_10G=Login10G(page)
    login_10G.navigateTo10G()
    viewport_dimensions = page.evaluate(
        "() => ({ width: window.screen.availWidth, height: window.screen.availHeight })"
    )
    logged_in_application=login_10G.login10G(Username,Password)
    logged_in_application.set_viewport_size(viewport_dimensions)
    expected_url_base = Expected_URL_Of_10G.rstrip("#/")
    expected_url_pattern = re.compile(rf"^{re.escape(expected_url_base)}(?:#/)?$")
    expect(logged_in_application).to_have_url(expected_url_pattern, timeout=60_000)
    _wait_for_application_ready(logged_in_application)
    yield logged_in_application
