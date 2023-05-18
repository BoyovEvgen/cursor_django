from django.shortcuts import render
from .models import MenuItem

# Create your views here.

def main(request):
    menu_items = MenuItem.objects.all()
    return render(request, "index.html", {"menu_items": menu_items})
