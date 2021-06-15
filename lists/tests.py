import django
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

from pytest_django.asserts import assertTemplateUsed


# Create your tests here.

#### HOME PAGE TESTS ####
def test_uses_home_template(client: django.test.Client):
    response = client.get('/')
    assertTemplateUsed(response, 'home.html')

def test_can_save_a_POST_request(client: django.test.Client):
    response = client.post('/', data={'item_text': 'A new list item'})
    assert 'A new list item' in response.content.decode()
    assertTemplateUsed(response, 'home.html')