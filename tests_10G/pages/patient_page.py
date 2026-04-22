import re
import time
from playwright.sync_api import Page
from tests_10G.Utils.constants import *

class PatientPage:
    def __init__(self, page:Page):
        self.page=page

    def _menu_frame(self):
        self.page.wait_for_load_state("domcontentloaded")
        deadline = time.time() + 30
        while time.time() < deadline:
            frame = self.page.frame(name="fra_Menu_CureMD")
            if frame is not None:
                return frame
            self.page.wait_for_timeout(500)
        raise RuntimeError("Menu frame 'fra_Menu_CureMD' not found")

    def _patient_locator(self, frame):
        candidates = [
            frame.locator(patient_btn),
        ]
        for locator in candidates:
            if locator.count() > 0:
                return locator.first
        raise RuntimeError("Unable to locate 'Patient' control in menu frame")

    def _body_frame(self):
        self.page.wait_for_selector(f"xpath={patient_search_body_frame}", timeout=30_000)
        body_frame = self.page.frame(name="fraCureMD_Body")
        if body_frame is None:
            raise RuntimeError("Body frame 'fraCureMD_Body' not found")
        return body_frame

    def navigate_to_patient_btn(self):
        print("Clicking Patient button...")
        frame = self._menu_frame()
        frame.wait_for_selector(patient_btn, state="visible", timeout=30_000)
        patient_locator = self._patient_locator(frame)
        patient_locator.click()
        print("Clicked Patient button")
    
    def search_patient(self):
        body_frame = self._body_frame()
        search_input_selector = f"xpath={patient_search_field}"
        search_button_selector = f"xpath={patient_search_btn}"
        patient_link_selector = f"xpath={patient_link}"
        body_frame.wait_for_selector(search_input_selector, state="visible", timeout=30_000)
        search_input = body_frame.locator(search_input_selector)
        search_input.fill(patient_acc_no)
        body_frame.wait_for_selector(search_button_selector, state="visible", timeout=30_000)
        body_frame.locator(search_button_selector).click()
        body_frame.wait_for_selector(patient_link_selector, state="visible", timeout=30_000)
        print("Searching patient link...")
        patient_link_locator = body_frame.locator(patient_link_selector)
        patient_link_locator.click()
        
    
        