import django
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

import pytest
from pytest_django.asserts import assertTemplateUsed

from lists.models import Item

# Create your tests here.

#### HOME PAGE TESTS ####
def test_uses_home_template(client: django.test.Client):
    response = client.get('/')
    assertTemplateUsed(response, 'home.html')

def test_can_save_a_POST_request(client: django.test.Client):
    response = client.post('/', data={'item_text': 'A new list item'})
    assert 'A new list item' in response.content.decode()
    assertTemplateUsed(response, 'home.html')

#### ITEM MODEL TEST ####
@pytest.mark.django_db
def test_saving_and_retrieving_items():
    first_item = Item()
    first_item.text = 'The first (ever) list item'
    first_item.save()

    second_item = Item()
    second_item.text = 'Item the second'
    second_item.save()

    saved_items = Item.objects.all() # pylint: disable=no-member
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    assert first_saved_item.text == 'The first (ever) list item'
    assert second_saved_item.text == 'Item the second'