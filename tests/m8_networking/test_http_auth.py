import pytest
from playwright.sync_api import expect, APIRequestContext, Playwright, Page

# Constants
REPO = 'Playwright-Test-Repo'
USERNAME = 'andrejs-ps'  # Replace with your GitHub username
TOKEN = 'your_token_here'  # Replace with your actual GitHub token


@pytest.fixture(autouse=True)
def setup_and_teardown(playwright: Playwright):
    pass


def test_work_with_newly_created_repo(page: Page):
    pass
