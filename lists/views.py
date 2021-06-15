import django
from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item

# Create your views here.
def home_page(request: django.http.HttpRequest):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text']) # pylint: disable=no-member
        return redirect('/')

    items = Item.objects.all() # pylint: disable=no-member
    return render(request, 'home.html', {'items': items})
