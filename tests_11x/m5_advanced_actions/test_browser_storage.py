from pprint import pprint

from playwright.sync_api import expect, Page

name = 'Sofia'


def test_storage_ui_perspective(page: Page):
    page.goto('')

    name_input = page.get_by_label('First name')
    name_input.fill(name)
    page.reload()
    expect(name_input).to_have_value('')

    name_input.fill(name)
    page.get_by_role('button', name='Save Input').click()
    page.reload()
    expect(name_input).to_have_value(name)


def test_local_storage(page: Page):
    page.goto('')
    page.get_by_label('First name').fill(name)
    page.get_by_role('button', name='Save Input').click()


def test_session_storage(page: Page):
    page.goto('')

    name_input = page.get_by_label('First name')
    name_input.fill(name)
    page.get_by_role('button', name='Save Input').click()
