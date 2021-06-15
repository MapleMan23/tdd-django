from selenium import webdriver
import pytest


@pytest.fixture
def browser():
    firefox = webdriver.Firefox()
    firefox.get('http://localhost:8000')

    yield firefox

    firefox.quit()

@pytest.mark.functional_test
def test_can_start_a_list_and_retrieve_it_later(browser: webdriver.Firefox):
    assert 'To-Do' in browser.title