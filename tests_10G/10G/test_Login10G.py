from playwright.sync_api import Page, expect
import re
from tests_10G.Utils.constants import *

def test_LoginPage(logged_in_application: Page):
    expect(logged_in_application).to_have_url(Expected_URL_Of_10G)