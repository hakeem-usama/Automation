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

    def select_payment_location(self, location_name: str):
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

    def make_success_manual_payment(self, location_name: str, save_card: bool, amount: str, card_number: str):
        # Payment location should already be selected by calling select_payment_location() first
        # Wait for the payment window to stabilize after dropdown selection
        self.page.wait_for_timeout(2000)
        
        # Re-initialize payment window frame after dropdown selection
        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        
        # Check for New Card link and click if found
        try:
            new_card_link = payment_window_frame.locator("#NewCardLink a, a:has-text('New Card'), a[onclick*='ShowManualEntry']").first
            if new_card_link.count() > 0:
                new_card_link.wait_for(state="visible", timeout=5_000)
                new_card_link.click()
                print("New Card link clicked")
                self.page.wait_for_timeout(1000)  # Wait for manual entry form to appear
        except Exception:
            print("New Card link not found, continuing with existing card form...")
        
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
        
        # Handle save card option if requested
        if save_card:
            payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
            print("Enabling save card option...")
            
            # Check the "Save card on file" checkbox
            save_card_checkbox = payment_window_frame.get_by_role('checkbox', name=card_on_file_checkbox)
            save_card_checkbox.wait_for(state="visible", timeout=10_000)
            save_card_checkbox.check()
            
            # Fill use till date
            use_till_field = payment_window_frame.locator(use_till_date_fld)
            use_till_field.wait_for(state="visible", timeout=10_000)
            use_till_field.click()
            use_till_field.press("Escape")  # Press ESC to close any date picker
            use_till_field.fill(use_till_date)  # Default use till date
            use_till_field.press("Tab")  # Press Tab to move to next field
            print("Use Till filled...")
            
            # Fill max transaction amount with multiple approaches
            max_amount_filled = False
   
            
                
            max_transaction_field = payment_window_frame.locator(max_transaction_amount_fld)
            max_transaction_field.wait_for(state="visible", timeout=3_000)
            # Clear existing value and fill new value
            max_transaction_field.click()  # Focus the field
            max_transaction_field.press("Control+a")  # Select all existing text
            max_transaction_field.press("Backspace")  # Clear the field
            self.page.wait_for_timeout(500)  # Wait for field to be cleared
            max_transaction_field.fill(max_transaction_amount)  # Fill new value
            max_transaction_field.press("Tab")  # Move to next field to confirm
        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        print("Card Details Filled...")
        submit_frame = self._switch_to_frame(f"xpath={make_payment_btn_frm}", parent_frame=payment_window_frame)
        print("Card Details Filled...")
        submit_frame.locator(f"xpath={make_payment_btn}").click()

        self.page.wait_for_timeout(500)
        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        print("Payment window frame switched...",payment_window_frame)
        self.page.wait_for_timeout(500)
        # Handle signature popup for save card payments
        screenshot_path='payment_success_without_save_card.png'
        if save_card:
            screenshot_path='payment_success_with_save_card.png'
            print("Handling signature popup for save card...")
            try:
                # Search for CardOnFileAgreement iframe in frame tree
                print("Searching for CardOnFileAgreement iframe in frame tree...")
                iframe_locator = payment_window_frame.locator(signature_frm)
                iframe_element = iframe_locator.first.element_handle()

                self.page.wait_for_timeout(500)
                
                # Get the frame content
                signature_frame = iframe_element.content_frame()
                print("Switched to signature frame")
                
                # Wait for frame to load
                signature_frame.wait_for_load_state("domcontentloaded", timeout=30_000)
                
                # First, click the signature image to enable the initials field
                print("Clicking signature image to enable initials field...")
                try:
                    # Try to find and click signature image - this enables the initials field
                    signature_image = signature_frame.locator(signature_img).first
                    signature_image.wait_for(state="visible", timeout=10_000)
                    signature_image.click()
                    print("Signature image clicked")
                    
                    # Wait for the field to become visible after clicking
                    self.page.wait_for_timeout(1000)
                except Exception as img_e:
                    print(f"Could not click signature image: {img_e}")
                    print("Proceeding to fill initials anyway...")
                
                # Now fill the initials field (it should be visible after clicking signature)
                print("Filling initials field...")
                signature_field = signature_frame.locator(signature_fld)
                
                # Wait for field to be visible (may need to wait for it to appear)
                deadline = time.time() + 10
                while time.time() < deadline:
                    try:
                        if signature_field.is_visible():
                            break
                    except:
                        pass
                    self.page.wait_for_timeout(200)
                
                signature_field.click()
                signature_field.fill(card_signature)
                print("Signature filled")
                
                # Click Continue button
                print("Looking for Continue button...")
                continue_btn = signature_frame.locator(continue_btn_locator)
                continue_btn.wait_for(state="visible", timeout=10_000)
                continue_btn.click()
                print("Continue clicked, signature popup closed")
                
                # Wait for popup to close
                self.page.wait_for_timeout(2000)
                signature_handled = True
                    
            except Exception as e:
                print(f"Error handling signature popup: {e}")
                print("Signature popup not handled - test may not be complete")
                # Don't continue - raise the error to make test fail if signature doesn't work
                raise RuntimeError(f"Signature popup handling failed: {e}")
            
        
        # Wait for payment to process
        self.page.wait_for_timeout(3000)
        
        # Try to find payment success message
        try:
            payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
            self._wait_for_payment_locator(success_payment_msg, root_frame=payment_window_frame)
            print("Payment success message found")
            success_locator = payment_window_frame.locator(f"xpath={success_payment_msg}")
            success_locator.wait_for(state="visible", timeout=2_000)
            success_locator.screenshot(path=screenshot_path)
            print("Success message screenshot captured")
        except:
            print("Payment success message not found, taking screenshot anyway...")
            payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        return payment_window_frame

    def make_success_card_on_file_payment(self, location_name: str, amount: str ):

        self.page.wait_for_timeout(2000)

        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
        print("Payment window frame:")
        print(payment_window)
        print("Payment window frame2:")
        print(payment_window_frame)
        try:
            new_card_link = payment_window_frame.locator("#NewCardLink a, a:has-text('New Card'), a[onclick*='ShowManualEntry']").first
            print("New card link count:", new_card_link.count())
            if new_card_link.count() > 0:
                new_card_link.wait_for(state="visible", timeout=5_000)
                #payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")
                amount_fld = payment_window_frame.locator(f"xpath={card_on_file_amount_fld}")
                amount_fld.fill(amount)   

                process_payment_btn=payment_window_frame.locator(f"xpath={process_payment_btn_loc}")
                process_payment_btn.click()

                

                self.page.wait_for_timeout(500)
                success_msg = payment_window_frame.get_by_text("Payment Successful", exact=False)
                success_msg.wait_for(state="visible", timeout=10_000)
                if success_msg.count() > 0:
                    print("Payment successful")
                    screenshot_path='payment_success_with_card_on_file.png'
                    self.page.screenshot(path=screenshot_path)
                    return "Success"
                return None
        except Exception:
            print("Saved Card Screen not shown...")
            return None


    def make_decline_manual_payment(self):
        body_frame = self._body_frame()
        trigger = body_frame.locator(f"xpath={payment_lnk}")
        trigger.wait_for(state="visible", timeout=30_000)
        trigger.click(force=True)
        payment_window_frame = self._switch_to_frame(f"xpath={payment_window}")

        card_number_frame = self._switch_to_frame(f"xpath={payment_card_num_frm}", parent_frame=payment_window_frame)
        card_number_frame.wait_for_selector(f"xpath={payment_card_num_fld}", state="visible", timeout=30_000)
        card_number_frame.locator(f"xpath={payment_card_num_fld}").fill(card_number)

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
        amount_fld.fill(decline_amount)
        
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