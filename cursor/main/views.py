
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import SliderItem, Order, OrderItem, Discount_code
from .forms import NewUserForm
from products.models import Product, Category
from telegram.telegramBot import serialize_send_message


def main(request):
    img_urls_list = SliderItem.objects.values_list('link', flat=True)
    products = Product.objects.filter(show_on_main_page=True)

    context = {"img_urls": img_urls_list,
               "products": products}
    return render(request, "index.html", context)


def add_to_cart(request, product_id: int):
    discount = request.session.get('discount', None)
    is_product_already_exist = False
    if not request.session.get('cart'):
        request.session['cart'] = []
    else:
        for product in request.session.get('cart', []):
            if product['id'] == product_id:
                product['quantity'] = product['quantity'] + 1
                product['total_price'] = product['price'] * product['quantity']
                product['total_price_with_discount'] = update_price_with_discount(discount, product['total_price'])
                is_product_already_exist = True

    if not is_product_already_exist:
        product_obj = Product.objects.get(id=product_id)
        cart_product = {"id": product_id,
                        "quantity": 1,
                        "price": product_obj.price,
                        'total_price': product_obj.price,
                        'total_price_with_discount': update_price_with_discount(discount, product_obj.price),
                        'title': product_obj.title,
                        'description': product_obj.description,
                        'main_image': product_obj.main_image.url}

        request.session["cart"].append(cart_product)
    request.session.modified = True
    return HttpResponseRedirect("/")


def cart(request):
    cart_products = request.session.get("cart", [])
    discount = request.session.get('discount', None)
    return render(request, "cart.html", {'cart_products': cart_products, 'discount': discount})


def checkout(request):
    total_price = sum(map(lambda cart_item: cart_item["total_price_with_discount"], request.session.get("cart", [])))
    return render(request, "checkout.html", {"total_price": total_price})


def checkout_proceed(request):
    if request.method == "POST":
        card_products = request.session.get("cart", [])
        order = Order()
        order.first_name = request.POST.get("first_name")
        order.last_name = request.POST.get("last_name")
        order.email = request.POST.get("email")
        order.address = request.POST.get("address")
        order.address2 = request.POST.get("address2")
        order.country = request.POST.get("country")
        order.city = request.POST.get("city")
        order.postcode = request.POST.get("postcode")
        order.total_price = sum(map(lambda cart_item: cart_item["total_price_with_discount"], card_products))
        order.user = request.user
        order.save()
        for item in card_products:
            order_item = OrderItem()
            order_item.product_id = item["id"]
            order_item.order_id = order.id
            order_item.price = item["total_price_with_discount"]
            order_item.quantity = item["quantity"]
            order_item.save()

        request.session['cart'] = []
        request.session['discount'] = None
        serialize_send_message(order)
    return HttpResponseRedirect("/")


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/")
    form = NewUserForm()
    return render(request, "sign-up.html", {"form": form})


def sign_in(request):
    if request.method == "POST":
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
        return HttpResponseRedirect('/')
    return render(request, "sign-in.html")


def sign_out(request):
    logout(request)
    return HttpResponseRedirect("/")


def discount_apply(request):
    if request.method == 'POST':
        code = request.POST.get("discount_code")
        try:
            discount_code = Discount_code.objects.get(code=code)
            if discount_code.is_active:
                request.session['discount'] = discount_code.discount
        except Discount_code.DoesNotExist:
            request.session['discount'] = None

        if cart := request.session.get('cart'):
            discount = request.session.get('discount', None)
            for product in cart:
                product['total_price_with_discount'] = update_price_with_discount(discount, product['total_price'])

    return redirect('cart')


def update_price_with_discount(discount, price):
    return price - price / 100 * discount if discount else price
