from playwright.sync_api import expect, Page, Browser


def test_route_abort(page: Page):

    # ...

    page.goto(f'')

    page.get_by_test_id('deposit').fill('10')

    expect(page.get_by_test_id('result')).not_to_be_visible()


def test_route_with_condition(page: Page):
    pass

    # Your test code here
    # page.goto(...) and other actions


def test_route_fulfill(page: Page):

    page.goto(f'')

    page.get_by_text('Download Our Offer').click()
