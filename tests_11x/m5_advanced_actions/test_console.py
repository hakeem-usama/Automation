from playwright.sync_api import Page


def test_check_console(page: Page):

    page.goto('')

    page.get_by_role('button', name='Register').click()


def test_check_console_error(page: Page):

    page.goto('')
    page.get_by_role('button', name='Register').click()
