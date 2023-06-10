from django.shortcuts import render, redirect
from .models import Category, Product, Comment
from main.models import MenuItem


def category_page(request, slug):
    map_sort = {"price descending": "price", "price ascending": "-price", 'creation date descending': "created_at", "creation date ascending": "-created_at"}
    sort_option = request.POST.get('sort_option')
    category = Category.objects.get(slug=slug)
    if sort_option in map_sort:
        products = category.product_set.filter(is_active=True).order_by(map_sort.get(sort_option))
    else:
        products = category.product_set.filter(is_active=True)
    return render(request, "category.html",
                  {
                   "category": category,
                   "products": products}
                  )


def product_page(request, product_id: int):
    product = Product.objects.get(id=product_id)
    comments = Comment.objects.filter(parent_id=None).filter(product_id=product.id)
    context = {'product': product, 'comments': comments}
    return render(request, 'product.html', context=context)


def add_comment(request, product_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment = Comment()
            comment.user = request.user
            comment.product_id = product_id
            comment.text = request.POST.get("comment-text")
            if parent_id := request.POST.get("parent", False):
                comment.parent_id = parent_id
            comment.save()
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')
