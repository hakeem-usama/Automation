from playwright.sync_api import Page, expect
import re
from tests.Utils.constants import CUREMD_DAT_LOGIN_ASP

def test_LoginPage(logged_in_application: Page):

    expect(logged_in_application).to_have_url(re.compile(r"CureMDClient/#"))


def test_NavigateToAddressbook(logged_in_application: Page):
    # Use the same fixture; each test gets a fresh logged-in window
    logged_in_application.get_by_label("Inbox").click()
    logged_in_application.get_by_role("button", name="Address Book").click()
    expect(logged_in_application).to_have_url(
        "https://baseline11x.curemd.com/CureMDClient/#/home/personal/(mainContent:address-book)"
    )

def test_vadlaiteName_ContactMandatory(logged_in_application: Page):
    logged_in_application.get_by_label("Inbox").click()
    logged_in_application.get_by_role("button", name="Address Book").click()
    expect(logged_in_application).to_have_url(
        "https://baseline11x.curemd.com/CureMDClient/#/home/personal/(mainContent:address-book)")
    logged_in_application.get_by_role("button", name=re.compile("New Contact", re.I)).click()
    logged_in_application.get_by_role("button", name="Save").click()
    expect(logged_in_application.get_by_text(re.compile("Please enter at least one contact detail"))).to_be_visible()
    expect(logged_in_application.get_by_text(re.compile("Please enter either First Name or Last Name"))).to_be_visible()

def test_AddPracticeUserWithMinimumInfo(logged_in_application: Page):
    logged_in_application.get_by_label("Inbox").click()
    logged_in_application.get_by_role("button", name="Address Book").click()
    expect(logged_in_application).to_have_url(
        "https://baseline11x.curemd.com/CureMDClient/#/home/personal/(mainContent:address-book)")
    logged_in_application.keyboard.press("Escape")
    logged_in_application.get_by_role("button", name=re.compile("New Contact", re.I)).click()
    logged_in_application.get_by_role("button", name="Practice User").click()
    logged_in_application.get_by_role("textbox", name="First Name").click()
    logged_in_application.get_by_role("textbox", name="First Name").fill("Automation")
    logged_in_application.get_by_role("textbox", name="First Name").press("Tab")
    logged_in_application.get_by_role("textbox", name="Last Name").fill("EDIPM")
    logged_in_application.get_by_label("Phone Contacts").first.fill("(222) 222 2222 Ext 222222")
    logged_in_application.get_by_role("button", name="Save").click()
    expect(logged_in_application.get_by_text(re.compile("Contact Added Successfully"))).to_be_visible()

def test_ApplyStaffFilter(logged_in_application: Page):
    logged_in_application.get_by_label("Inbox").click()
    logged_in_application.get_by_role("button", name="Address Book").click()
    expect(logged_in_application).to_have_url(
        "https://baseline11x.curemd.com/CureMDClient/#/home/personal/(mainContent:address-book)")
    logged_in_application.keyboard.press("Escape")
    logged_in_application.locator(
        'button.mat-mdc-menu-trigger.dropdown-underlined:has-text("All")'
    ).first.click()
    logged_in_application.get_by_role("menuitem", name="Practice User").click()
    first_tile_provider = logged_in_application.locator(
        ".address-book-listing"
    ).first.locator(".cmd-provider-name")
    first_tile_provider.click()
    for x in range(10):
        contact_category_firstContact= logged_in_application.locator(f'(//div[@class="cmd-provider-name"])[{x+1}]')
        expect(contact_category_firstContact).to_have_text("Practice User")

