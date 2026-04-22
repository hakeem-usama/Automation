import re
import time
from playwright.sync_api import Page, TimeoutError, Error
from tests_10G.Utils.constants import *


class Payment:
    def __init__(self, page: Page):
        self.page = page

    @property
    def success_payment_msg(self):
        payment_window_locator = self.page.frame_locator(f"xpath={payment_window}")
        return payment_window_locator.locator(f"xpath={success_payment_msg}")

    @property
    def decline_payment_msg(self):
        payment_window_locator = self.page.frame_locator(f"xpath={payment_window}")
        return payment_window_locator.locator(f"xpath={decline_payment_msg}")

    def _find_locator_in_frame_tree(self, frame, selector: str):
        try:
            locator = frame.locator(selector)
        except Error:
            return None
        try:
            count = locator.count()
        except Error:
            count = 0
        if count and count > 0:
            return locator.first
        for child in frame.child_frames:
            candidate = self._find_locator_in_frame_tree(child, selector)
            if candidate is not None:
                return candidate
        return None

    def _wait_for_payment_locator(self, xpath: str, *, root_frame=None, timeout_ms: int = 30_000):
        selector = f"xpath={xpath}"
        deadline = time.time() + timeout_ms / 1000
        while time.time() < deadline:
            payment_frame = root_frame or self._switch_to_frame(f"xpath={payment_window}")
            candidate = self._find_locator_in_frame_tree(payment_frame, selector)
            if candidate is not None:
                try:
                    candidate.wait_for(state="attached", timeout=1_000)
                except TimeoutError:
                    pass
                try:
                    candidate.wait_for(state="visible", timeout=1_000)
                except TimeoutError:
                    pass
                try:
                    if candidate.is_visible():
                        return candidate
                except Error:
                    pass
            self.page.wait_for_timeout(200)
        raise RuntimeError(f"Unable to locate visible element for selector '{selector}' within payment iframe")

    def _switch_to_frame(self, frame_xpath: str, *, parent_frame=None, timeout_ms: int = 30_000):
        context = parent_frame if parent_frame is not None else self.page
        frame_element = context.wait_for_selector(frame_xpath, state="attached", timeout=timeout_ms)
        frame = frame_element.content_frame()
        if frame is None:
            raise RuntimeError(f"Frame '{frame_xpath}' is present but content frame is unavailable")
        return frame

    def _body_frame(self):
        self.page.wait_for_selector(f"xpath={patient_search_body_frame}", timeout=30_000)
        frame = self.page.frame(name="fraCureMD_Body")
        if frame is None:
            raise RuntimeError("Body frame 'fraCureMD_Body' not found")
        return frame 

    def navigate_to_payment_method(self):
        body_frame = self._body_frame()
        body_frame.wait_for_selector(f"xpath={paymethod_select}", state="visible", timeout=30_000)
        return body_frame

    def select_payment_method(self, option: str):
        body_frame = self.navigate_to_payment_method()
        dropdown = body_frame.locator(f"xpath={paymethod_select}")
        normalized = option.strip().lower()
        options = dropdown.locator("option")
        deadline = time.time() + 10
        count = options.count()
        while count == 0 and time.time() < deadline:
            self.page.wait_for_timeout(200)
            count = options.count()
        if count == 0:
            raise RuntimeError("Payment dropdown options did not populate in time")
        matching_option = None
        for index in range(count):
            candidate = options.nth(index)
            text = candidate.text_content() or ""
            if text.strip().lower() == normalized:
                matching_option = candidate
                break
        if matching_option is None:
            raise RuntimeError(f"Payment option '{option}' not found in dropdown")
        value = matching_option.get_attribute("value")
        if value:
            dropdown.select_option(value=value)
        else:
            dropdown.select_option(label=matching_option.text_content())

    def select_payment_location(self, location_name: str = ".Payfields"):
        body_frame = self._body_frame()
        trigger = body_frame.locator(f"xpath={payment_lnk}")
        trigger.wait_for(state="visible", timeout=30_000)
        trigger.click(force=True)
        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        
        # Find and click the Genius dropdown
        genius_dropdown = payment_window_frame.locator('[title=".Genius"]')
        genius_dropdown.wait_for(state="visible", timeout=30_000)
        genius_dropdown.click()
        
        # Find and fill the search input
        search_input = payment_window_frame.locator('input[type="search"]')
        search_input.wait_for(state="visible", timeout=30_000)
        search_input.click()
        search_input.fill(location_name)
        
        # Click the specified tree item
        location_item = payment_window_frame.get_by_role('treeitem', name=location_name, exact=True)
        location_item.wait_for(state="visible", timeout=30_000)
        location_item.click()

    def make_success_manual_payment(self, location_name: str = ".Payfields"):
        # Payment location should already be selected by calling select_payment_location() first
        # Wait for the payment window to stabilize after dropdown selection
        self.page.wait_for_timeout(2000)
        
        # Re-initialize payment window frame after dropdown selection
        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        
        # Wait for card number frame to be available
        self.page.wait_for_timeout(1000)
        card_number_frame = self._switch_to_frame(f"xpath={payment_card_num_frm}", parent_frame=payment_window_frame)
        card_number_frame.wait_for_selector(f"xpath={payment_card_num_fld}", state="visible", timeout=30_000)
        card_number_frame.locator(f"xpath={payment_card_num_fld}").fill(card_number)

        # Re-get payment window frame before each card field
        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        card_expiry_frame = self._switch_to_frame(f"xpath={payment_card_expiry_frm}", parent_frame=payment_window_frame)
        card_expiry_frame.wait_for_selector(f"xpath={payment_card_expiry_fld}", state="visible", timeout=30_000)
        card_expiry_frame.locator(f"xpath={payment_card_expiry_fld}").fill(card_expiry)

        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        card_cvv_frame = self._switch_to_frame(f"xpath={payment_card_cvv_frm}", parent_frame=payment_window_frame)
        card_cvv_frame.wait_for_selector(f"xpath={payment_card_cvv_fld}", state="visible", timeout=30_000)
        card_cvv_frame.locator(f"xpath={payment_card_cvv_fld}").fill(card_cvv)

        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        amount_fld = self._wait_for_payment_locator(payment_amount_fld, root_frame=payment_window_frame)
        amount_fld.fill(amount)
        
        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        print("Card Details Filled...")
        submit_frame = self._switch_to_frame(f"xpath={make_payment_btn_frm}", parent_frame=payment_window_frame)
        print("Card Details Filled...")
        submit_frame.locator(f"xpath={make_payment_btn}").click()

        self.page.wait_for_timeout(500)
        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        # body_frame.wait_for_selector(f"xpath={success_payment_msg}", timeout=30_000)
        self._wait_for_payment_locator(success_payment_msg, root_frame=payment_window_frame)
        payment_window_locator = self.page.frame_locator(f"xpath={payment_window}")
        screenshot_path = "success_payment.png"
        success_text_xpath = "xpath=.//*[contains(translate(normalize-space(.), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'Payment Successful!')]"
        for attempt in range(3):
            success_locator = payment_window_locator.locator(f"xpath={success_payment_msg}")
            try:
                success_locator.wait_for(state="visible", timeout=1_000)
                try:
                    message_candidate = success_locator.locator(success_text_xpath)
                    target = message_candidate.first if message_candidate.count() else success_locator
                except Error:
                    target = success_locator
                target.screenshot(path=screenshot_path)
                break
            except Error as exc:
                if "Element is not attached" not in str(exc):
                    raise
                self.page.wait_for_timeout(200)
        else:
            raise RuntimeError("Unable to capture success message screenshot before element detached")
        return payment_window_frame

    def make_decline_manual_payment(self):
        body_frame = self._body_frame()
        trigger = body_frame.locator(f"xpath={payment_lnk}")
        trigger.wait_for(state="visible", timeout=30_000)
        trigger.click(force=True)
        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")

        card_number_frame = self._switch_to_frame(f"xpath={payment_card_num_frm}", parent_frame=payment_window_frame)
        card_number_frame.wait_for_selector(f"xpath={payment_card_num_fld}", state="visible", timeout=30_000)
        card_number_frame.locator(f"xpath={payment_card_num_fld}").fill("4012000098765439")

        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        card_expiry_frame = self._switch_to_frame(f"xpath={payment_card_expiry_frm}", parent_frame=payment_window_frame)
        card_expiry_frame.wait_for_selector(f"xpath={payment_card_expiry_fld}", state="visible", timeout=30_000)
        card_expiry_frame.locator(f"xpath={payment_card_expiry_fld}").fill("12/25")

        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        card_cvv_frame = self._switch_to_frame(f"xpath={payment_card_cvv_frm}", parent_frame=payment_window_frame)
        card_cvv_frame.wait_for_selector(f"xpath={payment_card_cvv_fld}", state="visible", timeout=30_000)
        card_cvv_frame.locator(f"xpath={payment_card_cvv_fld}").fill("123")

        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        amount_fld = self._wait_for_payment_locator(payment_amount_fld, root_frame=payment_window_frame)
        amount_fld.fill("13.14")
        
        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        submit_frame = self._switch_to_frame(f"xpath={make_payment_btn_frm}", parent_frame=payment_window_frame)
        submit_frame.locator(f"xpath={make_payment_btn}").click()

        self._wait_for_payment_locator(decline_payment_msg, root_frame=payment_window_frame)
        screenshot_path = "decline_payment.png"
        deadline = time.time() + 20
        while time.time() < deadline:
            payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
            decline_locator = payment_window_frame.locator(f"xpath={decline_payment_msg}")
            try:
                decline_locator.wait_for(state="attached", timeout=2_000)
                text_content = decline_locator.evaluate("el => (el.textContent || '').trim()")
                is_visible = decline_locator.evaluate(
                    "el => { const style = window.getComputedStyle(el);"
                    " return style && style.display !== 'none' && style.visibility !== 'hidden' &&"
                    " (el.offsetWidth > 0 || el.offsetHeight > 0); }"
                )
            except Error as exc:
                if "Element is not attached" in str(exc):
                    self.page.wait_for_timeout(200)
                    continue
                raise

            normalized_text = re.sub(r"\s+", " ", text_content or "").strip()
            if normalized_text and is_visible:
                payment_window_frame.locator("body").screenshot(path=screenshot_path)
                break

            self.page.wait_for_timeout(200)
        else:
            raise RuntimeError("Decline message text did not populate for screenshot")
        return payment_window_frame