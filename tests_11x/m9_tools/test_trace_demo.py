from playwright.sync_api import expect, Page


def test_trace_viewer_demo(page: Page):
    page.goto('')

    checkbox = page.get_by_role('checkbox')
    textarea = page.locator('#textarea')
    message = 'msg'

    checkbox.check()
    textarea.fill(message)
    expect(textarea).to_have_value('another message')  # fail
