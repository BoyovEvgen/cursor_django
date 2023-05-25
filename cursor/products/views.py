from django.shortcuts import render, redirect
from .models import Category, Product
from main.models import MenuItem


def category_page(request, slug):
    map_sort = {"price descending": "price", "price ascending": "-price", 'creation date descending': "created_at", "creation date ascending": "-created_at"}
    sort_option = request.POST.get('sort_option')
    menu_items = MenuItem.objects.all()
    categories = Category.objects.filter(parent_id=None)
    category = Category.objects.get(slug=slug)
    if sort_option in map_sort:
        products = category.product_set.filter(is_active=True).order_by(map_sort.get(sort_option))
    else:
        products = category.product_set.filter(is_active=True)
    return render(request, "category.html",
                  {"menu_items": menu_items,
                   "categories": categories,
                   "category": category,
                   "products": products}
                  )


def product_page(request, product_id: int):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'product.html', context=context)
