
from rest_framework import serializers
from products.models import Product, Category
from main.models import OrderItems, Order


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "discount_price"]

# serializers.ModelSerializer
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ["id", "title", "slug", "products"]


