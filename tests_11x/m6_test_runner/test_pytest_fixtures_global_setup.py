import pytest
from playwright.sync_api import expect, Page


@pytest.fixture
def page(page: Page):
    page.goto('')
    yield page
    # do cleanup


def test_one(page: Page):
    name_input = page.get_by_label('First name')
    name_input.fill('')
    expect(name_input).to_have_value('')


def test_two(page: Page):
    name_input = page.get_by_label('First name')
    name_input.fill('')
    expect(name_input).to_have_value('')
