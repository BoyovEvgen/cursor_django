
from rest_framework import serializers
from products.models import Product, Category
from main.models import OrderItem, Order
from django.db import transaction


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "discount_price"]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ["id", "title", "slug", "products"]


class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    # product = serializers.SlugRelatedField(slug_field="title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "price", "product"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'address',
                  'address2', 'country', 'city', 'postcode', 'total_price', 'items']


class OrderItemsCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = OrderItemsCreateSerializer(many=True)
    class Meta:
        model = Order
        fields = ['user', 'first_name', 'last_name', 'email', 'address', 'address2', 'country', 'city', 'postcode', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        with transaction.atomic():
            order = Order(**validated_data)
            order.total_price = 0
            order.save()

            total_price = 0
            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']

                try:
                    order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity,
                                                           price=product.price)
                    order_item.save()
                    total_price += product.price * quantity

                except Product.DoesNotExist:
                    pass

            order.total_price = total_price
            order.save()
        return order
