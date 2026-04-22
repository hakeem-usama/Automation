import random
import re
from pathlib import Path
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


def read_urls_from_file(file_path: str) -> list[str]:
    path = Path(file_path)
    if not path.exists():
        return []
    urls: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        url = line.strip()
        if url and not url.startswith("#"):
            urls.append(url)
    return urls

def test_run(page: Page) -> None:
    urls = read_urls_from_file("urls.txt")
    print("URLs Found")
    if not urls:
        urls = ["https://c.rt2.me/73a_jwcHo1"]
        print("URL Not Found")
    for url in urls:
        print(f"Processing URL: {url}")
        # If you want headed mode, run pytest with --headed
        page.goto(url)

        # If completion message is present, skip the payment process for this URL
        try:
            page.get_by_text("Payment Request Complete!").first.wait_for(state="visible", timeout=2000)
            print("Payment already complete. Skipping payment process.")
            continue
        except PlaywrightTimeoutError:
            pass

        # Wait for an element containing "$" to be visible
        page.wait_for_selector("text=$")

        # Read the second amount that shows a "$"
        amount_text = page.get_by_text("$").nth(1).inner_text()
        print("Raw Amount Text:", amount_text)

        # Extract numeric value
        decimal = float(amount_text.replace("$", "").replace(",", "").strip())
        print("Extracted Amount:", decimal)

        # If > 10, choose a random amount between 10 and 100
        if decimal > 10:
            decimal = round(random.uniform(10, decimal), 2)
            print(f"Random amount selected: {decimal}")

            # Open the partial payment dialog
            page.get_by_test_id("t-card-statement").locator("button").click()

            # Fill computed amount and confirm
            page.get_by_role("spinbutton").click()
            page.get_by_role("spinbutton").fill(f"{decimal:.2f}")
            page.get_by_test_id("t-partial-payment-ok").click()
            page.wait_for_timeout(3000)
        else:
            print("Amount is less than or equal to 10, skipping partial payment and continuing")

        page.locator("iframe[name=\"card-number\"]").content_frame.get_by_role("textbox", name="•••• •••• •••• ••••").click()
        page.locator("iframe[name=\"card-number\"]").content_frame.get_by_role("textbox", name="•••• •••• •••• ••••").fill("4111 1111 1111 1111")
        page.locator("iframe[name=\"card-number\"]").content_frame.get_by_role("textbox", name="•••• •••• •••• ••••").press("Tab")
        page.locator("iframe[name=\"card-expiration\"]").content_frame.get_by_role("textbox", name="MM / YYYY").fill("11 / 29")
        page.locator("iframe[name=\"card-expiration\"]").content_frame.get_by_role("textbox", name="MM / YYYY").press("Tab")
        page.locator("iframe[name=\"card-cvv\"]").content_frame.get_by_role("textbox", name="•••").fill("589")
        page.locator("iframe[name=\"submit\"]").content_frame.get_by_role("button", name="Pay Now").click()
        page.wait_for_timeout(5000)
        ##assert page.get_by_text(re.compile(r"Payment successful for", re.I)).is_visible()
