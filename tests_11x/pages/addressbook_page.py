import re
from playwright.sync_api import Page
from tests_11x.Utils.constants import *

class Addressbook:
    def __init__(self, page:Page):
        self.page=page
        self.InboxIcon=page.get_by_label("Inbox")
        self.click_addressbook=page.get_by_role("button", name="Address Book")
        self.add_new_contact_btn=page.get_by_role("button", name=re.compile("New Contact", re.I))
        self.save_btn=page.get_by_role("button", name="Save")
        self.type_practice_user=page.get_by_role("button", name="Practice User")
        self.field_first_name=page.get_by_role("textbox", name="First Name")
        self.field_last_name=page.get_by_role("textbox", name="Last Name")
        self.field_contact=page.get_by_label("Phone Contacts").first
        self.all_filter=page.locator('button.mat-mdc-menu-trigger.dropdown-underlined:has-text("All")').first
        self.menu_item_practice_user=page.get_by_role("menuitem", name="Practice User")
        self.first_tile=page.locator(".address-book-listing").first.locator(".cmd-provider-name")
        

    def navigate_to_addressbook(self):
        self.InboxIcon.click()
        self.click_addressbook.click()

    def add_new_contact(self):
        self.add_new_contact_btn.click()
        self.save_btn.click()
        
    def add_new_contact(self, fisrtName:str, lastName:str, contact:str):
        self.add_new_contact_btn.click()
        self.type_practice_user.click()
        self.field_first_name.click()
        self.field_first_name.fill(fisrtName)
        self.field_last_name.click()
        self.field_last_name.fill(lastName)
        self.field_contact.click()
        self.field_contact.fill(contact)
        self.save_btn.click()

    def apply_contact_filter(self):
        self.all_filter.click()
        self.menu_item_practice_user.click()
        self.first_tile.click()
         
    def get_next_tile(self,n):
        return self.page.locator(f'(//div[@class="cmd-provider-name"])[{n+1}]')
