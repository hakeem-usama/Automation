import pytest
from playwright.sync_api import expect, Page


# Before Parameterization
def test_single_param_with_bob(page: Page):
    page.goto('')

    name_input = page.get_by_label('First name')
    name_input.fill('Bob')
    expect(name_input).to_have_value('Bob')

    # ...


def test_single_param_with_alexandrina(page: Page):
    page.goto('')

    name_input = page.get_by_label('First name')
    name_input.fill('Alexandrina')
    expect(name_input).to_have_value('Alexandrina')

    # ...


# After: to parameterize
def test_single_param(page: Page):
    page.goto('')

    name_input = page.get_by_label('First name')
    name_input.fill('')
    expect(name_input).to_have_value('')

    # ...


# After: to parameterize with tuples
def test_two_params(page: Page):
    page.goto('')

    first_name_input = page.get_by_label('First name')
    first_name_input.fill('')
    expect(first_name_input).to_have_value('')

    last_name_input = page.get_by_label('Last name')
    last_name_input.fill('')
    expect(last_name_input).to_have_value('')
