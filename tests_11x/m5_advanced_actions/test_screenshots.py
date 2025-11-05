from playwright.sync_api import Page


def test_screenshot_demo(page: Page):

    page.goto('')
    name_input = page.get_by_label('First name')
    name_input.fill('Andrejs')
    page.get_by_role('button', name='Register').click()
