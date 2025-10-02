from playwright.sync_api import Page, expect
import re
from tests.Utils.constants import *
from tests.pages.addressbook_page import Addressbook

def test_LoginPage(logged_in_application: Page):
    expect(logged_in_application).to_have_url(re.compile(r"CureMDClient/#"))


def test_NavigateToAddressbook(logged_in_application: Page):
    navigate_addressbook=Addressbook(logged_in_application)
    navigate_addressbook.navigate_to_addressbook()
    expect(logged_in_application).to_have_url(Addressbook_URL)


def test_vadlaiteName_ContactMandatory(logged_in_application: Page):
    navigate_addressbook=Addressbook(logged_in_application)
    navigate_addressbook.navigate_to_addressbook()
    expect(logged_in_application).to_have_url(Addressbook_URL)
    navigate_addressbook.add_new_contact()
    expect(logged_in_application.get_by_text(re.compile(Addressbook_Error_atleast_one_contact))).to_be_visible()
    expect(logged_in_application.get_by_text(re.compile(Addressbook_Error_enter_name))).to_be_visible()

def test_AddPracticeUserWithMinimumInfo(logged_in_application: Page):
    navigate_addressbook=Addressbook(logged_in_application)
    navigate_addressbook.navigate_to_addressbook()
    expect(logged_in_application).to_have_url(Addressbook_URL)
    navigate_addressbook.add_new_contact(userFirstName, userLastName, userConatct)
    expect(logged_in_application.get_by_text(re.compile(contactAddedSucessfully))).to_be_visible()

def test_ApplyStaffFilter(logged_in_application: Page):
    navigate_addressbook=Addressbook(logged_in_application)
    navigate_addressbook.navigate_to_addressbook()
    expect(logged_in_application).to_have_url(Addressbook_URL)
    navigate_addressbook.apply_contact_filter()
    for x in range(10):
        contact_category_firstContact= navigate_addressbook.get_next_tile(x)
        expect(contact_category_firstContact).to_have_text(contactType)

