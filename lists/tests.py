import django
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

import pytest
from pytest_django.asserts import assertRedirects, assertTemplateUsed, assertContains

from lists.models import Item, List

# Create your tests here.

#### HOME PAGE TESTS ####
def test_uses_home_template(client: django.test.Client):
    response = client.get('/')
    assertTemplateUsed(response, 'home.html')

#### NEW LIST TEST ####
@pytest.mark.django_db
def test_can_save_a_POST_request(client: django.test.Client):
    client.post('/lists/new', data={'item_text': 'A new list item'})

    assert Item.objects.count() == 1    # pylint: disable=no-member
    new_item = Item.objects.first()     # pylint: disable=no-member
    assert new_item.text == 'A new list item'

@pytest.mark.django_db
def test_redirects_after_POST(client: django.test.Client):
    response = client.post('/lists/new', data={'item_text': 'A new list item'})
    assertRedirects(response, '/lists/the-only-list-in-the-world/')


#### ITEM MODEL TEST ####
@pytest.mark.django_db
def test_saving_and_retrieving_items():
    list_ = List()
    list_.save()

    first_item = Item()
    first_item.text = 'The first (ever) list item'
    first_item.list = list_
    first_item.save()

    second_item = Item()
    second_item.text = 'Item the second'
    second_item.list = list_
    second_item.save()

    save_list = List.objects.first()
    assert save_list == list_

    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    assert first_saved_item.text == 'The first (ever) list item'
    assert first_saved_item.list == list_
    assert second_saved_item.text == 'Item the second'
    assert second_saved_item.list == list_


#### LIST VIEW TEST ####
@pytest.mark.django_db
def test_uses_list_template(client):
    response = client.get('/lists/the-only-list-in-the-world/')
    assertTemplateUsed(response, 'list.html')

@pytest.mark.django_db
def test_displays_all_items(client: django.test.Client):
    list_ = List.objects.create()
    Item.objects.create(text='itemey 1', list=list_) # pylint: disable=no-member
    Item.objects.create(text='itemey 2', list=list_) # pylint: disable=no-member

    response = client.get('/lists/the-only-list-in-the-world/')

    assertContains(response, 'itemey 1')
    assertContains(response, 'itemey 2')
