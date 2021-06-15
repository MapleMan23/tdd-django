from selenium import webdriver
import pytest
import time
from selenium.webdriver.common.keys import Keys
import django
import pytest_django
from selenium.common.exceptions import WebDriverException


@pytest.fixture
def browser():
    firefox = webdriver.Firefox()

    yield firefox

    firefox.quit()

MAX_WAIT = 10
def wait_for_row_in_list_tabel(browser: webdriver.Firefox, row_text: str):
    start_time = time.time()
    while True:
        try:
            table = browser.find_element_by_id('id_list_table')
            rows = table.find_elements_by_tag_name('tr')
            assert row_text in [row.text for row in rows]
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)

@pytest.mark.functional_test
@pytest.mark.django_db
def test_can_start_a_list_and_retrieve_it_later(browser: webdriver.Firefox, live_server):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser.get(live_server.url)

    # She notices the page title and header mention to-do lists
    assert 'To-Do' in browser.title
    header_text = browser.find_element_by_tag_name('h1').text
    assert 'To-Do' in header_text

    # She is invited to enter a to-do item straight away
    inputbox = browser.find_element_by_id('id_new_item')
    assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

    # She types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fly-fishing lures)
    inputbox.send_keys('Buy peacock feathers')

    # When she hits enter, the page updates, and now the page lists
    # "1: Buy peacock feathers" as an item in a to-do list table
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_tabel(browser, '1: Buy peacock feathers')

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very
    # methodical)
    inputbox = browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Use peacock feathers to make a fly')
    inputbox.send_keys(Keys.ENTER)

    # The page updates again, and now shows both items on her list
    wait_for_row_in_list_tabel(browser, '1: Buy peacock feathers')
    wait_for_row_in_list_tabel(browser, '2: Use peacock feathers to make a fly')

    # Edith wonders whether the site will remember her list. Then she sees
    # that the site has generated a unique URL for her -- there is some
    # explanatory text to that effect.
    pytest.xfail('FINISHED THE TEST')

    # She visits that URL - her to-do list is still there.