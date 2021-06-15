import django
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

from pytest_django.asserts import assertTemplateUsed


# Create your tests here.
def test_home_page_returns_correct_html(client: django.test.Client):
    response = client.get('/')
    assertTemplateUsed(response, 'home.html')