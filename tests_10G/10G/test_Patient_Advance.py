from playwright.sync_api import Page, expect
import re
from tests_10G.Utils.constants import *
from tests_10G.pages.patient_page import PatientPage
from tests_10G.pages.patient_advance import PatientAdvance
from tests_10G.pages.Payment import Payment

def test_Success_Patient_Advance(logged_in_application: Page):
    navigate_patient=PatientPage(logged_in_application)
    navigate_patient.navigate_to_patient_btn()
    patient_search_header = logged_in_application.get_by_text("Patient Search", exact=False)
    expect(patient_search_header).to_be_visible()
    navigate_patient.search_patient()
    advance_actions = PatientAdvance(logged_in_application)
    advance_actions.navigate_to_patient_menu()
    advance_actions.navigate_to_patient_billing()
    advance_actions.navigate_to_patient_advances()
    advance_actions.navigate_to_collect_advances()
    # advance_actions.navigate_to_payment_method()
    payment_actions = Payment(logged_in_application)
    payment_actions.navigate_to_payment_method()
    payment_actions.select_payment_method(payment_option)
    # advance_actions.select_payment_method(payment_option)
    advance_actions.navigate_to_payment_window()
    payment_actions.make_success_manual_payment()
    expect(payment_actions.success_payment_msg).to_have_count(1)

def test_Decline_Patient_Advance(logged_in_application: Page):
    navigate_patient=PatientPage(logged_in_application)
    navigate_patient.navigate_to_patient_btn()
    patient_search_header = logged_in_application.get_by_text("Patient Search", exact=False)
    expect(patient_search_header).to_be_visible()
    navigate_patient.search_patient()
    advance_actions = PatientAdvance(logged_in_application)
    advance_actions.navigate_to_patient_menu()
    advance_actions.navigate_to_patient_billing()
    advance_actions.navigate_to_patient_advances()
    advance_actions.navigate_to_collect_advances()
    # advance_actions.navigate_to_payment_method()
    payment_actions = Payment(logged_in_application)
    payment_actions.navigate_to_payment_method()
    payment_actions.select_payment_method(payment_option)
    # advance_actions.select_payment_method(payment_option)
    advance_actions.navigate_to_payment_window()
    payment_actions.make_decline_manual_payment()
    expect(payment_actions.decline_payment_msg).to_have_count(1)

