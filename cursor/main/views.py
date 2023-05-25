from django.http import HttpResponse
from django.shortcuts import render
from .models import MenuItem, SliderItem
from products.models import Product, Category


# Create your views here.

def main(request):
    menu_items = MenuItem.objects.all()
    img_urls_list = SliderItem.objects.values_list('link', flat=True)
    products = Product.objects.filter(show_on_main_page=True)
    categories = Category.objects.filter(parent_id=None)


    context = {"menu_items": menu_items,
               'img_urls': img_urls_list,
               "products": products,
               "categories": categories}

    return render(request, "index.html", context)