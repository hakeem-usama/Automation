import re
import time
from playwright.sync_api import Page
from tests_10G.Utils.constants import *
from tests_10G.pages.Payment import Payment

class PatientAdvance:
    def __init__(self, page:Page):
        self.page=page

    def _menu_frame(self):
        self.page.wait_for_load_state("domcontentloaded")
        deadline = time.time() + 30
        while time.time() < deadline:
            frame = self.page.frame(name="fraCureMD_Patient_Menu")
            if frame is not None:
                return frame
            self.page.wait_for_timeout(500)
        raise RuntimeError("Menu frame 'fraCureMD_Patient_Menu' not found")

    def _body_frame(self):
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_selector(f"xpath={patient_search_body_frame}", timeout=30_000)
        frame = self.page.frame(name="fraCureMD_Body")
        if frame is None:
            raise RuntimeError("Body frame 'fraCureMD_Body' not found")
        return frame

    def navigate_to_patient_menu(self):
        return self._menu_frame()

    def navigate_to_patient_billing(self):
        self.page.wait_for_load_state("domcontentloaded")
        menu_frame = self._menu_frame()
        menu_frame.wait_for_selector(f"xpath={patient_blng_btn}", state="visible", timeout=30_000)
        menu_frame.locator(f"xpath={patient_blng_btn}").click()
        return self._body_frame()

    def navigate_to_patient_advances(self):
        self.page.wait_for_load_state("domcontentloaded")
        menu_frame = self._menu_frame()
        menu_frame.wait_for_selector(f"xpath={patient_adv_btn}", state="visible", timeout=30_000)
        menu_frame.locator(f"xpath={patient_adv_btn}").click()
        return self._body_frame()

    def navigate_to_collect_advances(self):
        self.page.wait_for_load_state("domcontentloaded")
        body_frame = self._body_frame()
        body_frame.wait_for_selector(f"xpath={collect_adv_btn}", state="visible", timeout=30_000)
        body_frame.locator(f"xpath={collect_adv_btn}").click()
        return body_frame

    
    def navigate_to_payment_window(self):
        self.page.wait_for_load_state("domcontentloaded")
        body_frame = self._body_frame()
        trigger = body_frame.locator(f"xpath={payment_lnk}")
        trigger.wait_for(state="visible", timeout=30_000)
        trigger.click()
        self.page.wait_for_selector(f"xpath={payment_window}", timeout=30_000)
        payment_frame = self.page.frame_locator(f"xpath={payment_window}")
        
