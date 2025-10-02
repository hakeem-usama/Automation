from playwright.sync_api import expect, Page

name = 'Sofia'


# Default handling is to dismiss
def test_dialog_default_handling(page: Page):
    page.goto('')

    name_input = page.get_by_label('First name')
    name_input.fill(name)
    expect(name_input).to_have_value(name)

    page.get_by_role('button', name='Clear').click()
    expect(name_input).to_have_value(name)


def test_dialog_ok_or_dismiss(page: Page):

    page.goto('')

    input_name = page.get_by_label('First name')
    input_name.fill(name)

    page.get_by_role('button', name='Clear').click()
    expect(input_name).to_have_value('')
