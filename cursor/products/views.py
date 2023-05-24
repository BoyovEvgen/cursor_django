from django.shortcuts import render
from .models import Category, Product
from main.models import MenuItem


def category_page(request, slug):
    menu_items = MenuItem.objects.all()
    categories = Category.objects.filter(parent_id=None)
    category = Category.objects.get(slug=slug)
    return render(request, "category.html",
                  {"menu_items": menu_items,
                   "categories": categories,
                   "category": category}
                  )


def product_page(request, product_id: int):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'product.html', context=context)