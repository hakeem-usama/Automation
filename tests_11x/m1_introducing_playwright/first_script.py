from playwright.sync_api import sync_playwright
with sync_playwright() as playwright:
    browser=playwright.chromium.launch(headless=False , slow_mo=1000)
    page=browser.new_page()
    try:
        page.goto('https://www.google.com', timeout=60000, wait_until='domcontentloaded')
        print(page.title())
    except PlaywrightTimeoutError as e:
        print("Navigation timed out:", e)
    finally:
        browser.close()
browser.close
