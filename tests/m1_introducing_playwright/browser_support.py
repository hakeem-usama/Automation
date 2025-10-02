from playwright.sync_api import sync_playwright
with sync_playwright() as playwright:

    for browserType in [playwright.chromium, playwright.firefox, playwright.webkit]:
        browser=browserType.launch(headless=False , slow_mo=1000)
        page=browser.new_page()
        page.goto('https://www.whatsmybrowser.org/' , timeout=60000, wait_until='domcontentloaded')
        page.screenshot(path=f'example-{browserType.name}.png')
        browser.close()

