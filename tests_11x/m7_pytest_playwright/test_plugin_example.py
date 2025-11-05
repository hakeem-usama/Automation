from playwright.sync_api import Page, expect


def test_plugin_example(page: Page):

    page.goto('')

    page.get_by_label('First name').fill('Andrejs')
    page.get_by_role('button', name='Register', exact=True).click()

    warning = page.get_by_text('Valid last name is required')
    expect(warning).not_to_be_visible()  # fail, will be visible
