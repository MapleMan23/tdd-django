import django
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

import pytest
from pytest_django.asserts import assertTemplateUsed, assertContains

from lists.models import Item

# Create your tests here.

#### HOME PAGE TESTS ####
@pytest.mark.django_db
def test_uses_home_template(client: django.test.Client):
    response = client.get('/')
    assertTemplateUsed(response, 'home.html')

@pytest.mark.django_db
def test_can_save_a_POST_request(client: django.test.Client):
    client.post('/', data={'item_text': 'A new list item'})

    assert Item.objects.count() == 1    # pylint: disable=no-member
    new_item = Item.objects.first()     # pylint: disable=no-member
    assert new_item.text == 'A new list item'


@pytest.mark.django_db
def test_redirects_after_POST(client: django.test.Client):
    response = client.post('/', data={'item_text': 'A new list item'})

    assert response.status_code == 302
    assert response['location'] == '/lists/the-only-list-in-the-world/'

@pytest.mark.django_db
def test_only_saves_items_when_necessary(client):
    client.get('/')
    assert Item.objects.count() == 0 # pylint: disable=no-member


#### ITEM MODEL TEST ####
@pytest.mark.django_db
def test_saving_and_retrieving_items():
    first_item = Item()
    first_item.text = 'The first (ever) list item'
    first_item.save()

    second_item = Item()
    second_item.text = 'Item the second'
    second_item.save()

    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    assert first_saved_item.text == 'The first (ever) list item'
    assert second_saved_item.text == 'Item the second'


#### LIST VIEW TEST ####
@pytest.mark.django_db
def test_uses_list_template(client):
    response = client.get('/lists/the-only-list-in-the-world/')
    assertTemplateUsed(response, 'list.html')

@pytest.mark.django_db
def test_displays_all_items(client: django.test.Client):
    Item.objects.create(text='itemey 1') # pylint: disable=no-member
    Item.objects.create(text='itemey 2') # pylint: disable=no-member

    response = client.get('/lists/the-only-list-in-the-world/')

    assertContains(response, 'itemey 1')
    assertContains(response, 'itemey 2')
