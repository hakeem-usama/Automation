from playwright.sync_api import Page, expect
import re
from tests_10G.Utils.constants import *
from tests_10G.pages.patient_page import PatientPage

def test_Patient(logged_in_application: Page):
    logged_in_application.wait_for_load_state("networkidle")
    navigate_patient=PatientPage(logged_in_application)
    navigate_patient.navigate_to_patient_btn()
    patient_search_header = logged_in_application.get_by_text("Patient Search", exact=False)
    expect(patient_search_header).to_be_visible()
    navigate_patient.search_patient()
    