from django.shortcuts import render
from .models import MenuItem, SliderItem
from django.conf import settings
import os

# Create your views here.

def main(request):
    menu_items = MenuItem.objects.all()
    img_urls_list = SliderItem.objects.values_list('link', flat=True)
    context = {"menu_items": menu_items, 'img_urls': img_urls_list}

    return render(request, "index.html", context)
