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
    logged_in_application=login_10G.login10G(Username,Password)
    
    # Try to get current screen size with fallback to default dimensions
    try:
        # Wait a bit for the page to stabilize before evaluating
        logged_in_application.wait_for_timeout(1000)
        
        # Get screen dimensions
        screen_info = logged_in_application.evaluate("""
            () => {
                return {
                    width: window.screen.availWidth || 1366,
                    height: window.screen.availHeight || 768
                };
            }
        """)
        
        # Use 80% of available screen size to leave some margin
        viewport_width = max(1024, int(screen_info['width'] * 0.8))
        viewport_height = max(768, int(screen_info['height'] * 0.8))
        
        # Ensure minimum dimensions for usability
        viewport_width = min(viewport_width, 1920)
        viewport_height = min(viewport_height, 1080)
        
        print(f"Setting viewport to: {viewport_width}x{viewport_height}")
        logged_in_application.set_viewport_size({"width": viewport_width, "height": viewport_height})
        
    except Exception as e:
        print(f"Failed to get screen size, using default dimensions: {e}")
        # Fallback to reasonable default dimensions
        logged_in_application.set_viewport_size({"width": 1366, "height": 768})
    
    expected_url_base = Expected_URL_Of_10G.rstrip("#/")
    expected_url_pattern = re.compile(rf"^{re.escape(expected_url_base)}(?:#/)?$")
    expect(logged_in_application).to_have_url(expected_url_pattern, timeout=60_000)
    _wait_for_application_ready(logged_in_application)
    yield logged_in_application
