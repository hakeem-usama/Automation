from playwright.sync_api import expect, Page

home_title = 'Credit Association'
savings_title = 'Save with us'


def test_back_forward_reload(page: Page):
    page.goto('')
    page.goto(f'savings.html')
    expect(page).to_have_title(savings_title)


def test_navigation(page: Page):
    page.goto('', wait_until='load', timeout=100)
    expect(page).to_have_title(home_title)


def test_load_speed_while_navigating(page: Page):
    page.goto('')
    page.goto(f'savings.html', timeout=5000)
    expect(page).to_have_title(savings_title)
