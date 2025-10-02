import pytest
from playwright.sync_api import expect, Page


def test_single_param(page: Page):
    page.goto('')
    name_input = page.get_by_label('First name')
    name_input.fill('Sofia')
    expect(name_input).to_have_value('Sofia')


@pytest.mark.parametrize('name', ['Alice', 'Bob'])
def test_two_params(page: Page, name: str):
    page.goto('')
    name_input = page.get_by_label('First name')
    name_input.fill(name)
    expect(name_input).to_have_value(name)
