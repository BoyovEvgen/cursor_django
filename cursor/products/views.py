from django.shortcuts import render
from .models import Category, Product
from main.models import MenuItem


def category_page(request, slug):
    menu_items = MenuItem.objects.all()
    category = Category.objects.get(slug=slug)
    subcategories = category.category_set.all()
    products = category.product_set.filter(is_active=True)
    categories = Category.objects.filter(parent_id=None)
    return render(request, "category.html",
                  {"menu_items": menu_items,
                   "category": category,
                   "subcategories": subcategories,
                   "products": products,
                   "categories": categories
                   }
                  )


def product_page(request, pk: int):
    product = Product.objects.get(id=pk)
    product_imgs = product.productimage_set.all()
    context = {'product': product,
               'product_imgs': product_imgs}
    return render(request, 'product.html', context=context)