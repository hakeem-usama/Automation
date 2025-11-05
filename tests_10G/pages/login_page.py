from playwright.sync_api import Page
from tests_10G.Utils.constants import CUREMD_DAT_LOGIN_ASP

class Login10G:
    def __init__(self, page:Page):
        self.page=page
        self.userName_field=page.locator("#vchLogin_Name")
        self.password_field=page.locator("#vchPassword")
        self.loginBtn=page.get_by_role("button", name="Login")
        


    def navigateTo10G(self):
        self.page.goto(CUREMD_DAT_LOGIN_ASP, timeout=60_000, wait_until="domcontentloaded")
    
    def login10G(self, userName:str, password:str):
        self.userName_field.fill(userName)
        self.password_field.fill(password)
        with self.page.expect_popup() as popup_info:
            self.loginBtn.click()
        new_page = popup_info.value
        new_page.wait_for_load_state("domcontentloaded")
        return new_page
