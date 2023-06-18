from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .serializers import ProductSerializer, OrderSerializer, OrderCreateSerializer
from products.models import Product, Category
from products.models import Order
from .permissions import IsAuthorOrReadOnly


class ProductView(APIView):

    def get(self, request, format=None):
        products = Product.objects.all()
        serialized_products = ProductSerializer(products, many=True)
        return Response(serialized_products.data)

# generics.ListAPIView

class ProductSingleView(APIView):

    def get_object(self, id):
        try:
            product = Product.objects.get(id=id)
            return product
        except Product.DoesNotExist:
            return None


    def get(self, request, id):
        product = self.get_object(id)
        serialized_product = ProductSerializer(product)
        return Response(serialized_product.data)


    def put(self, request, id):
        product = self.get_object(id)
        if product is not None:
            serialized_product = ProductSerializer(instance=product, data=request.data)
            if serialized_product.is_valid():
                serialized_product.save()
                return Response(serialized_product.data)
        return Response(None, status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        product = self.get_object(id)
        if product is not None:
            product.delete()
            return Response(None, status.HTTP_204_NO_CONTENT)
        return Response(None, status.HTTP_400_BAD_REQUEST)


class CategoryProductsView(APIView):
    def get_object(self, id):
        try:
            category = Category.objects.get(id=id)
            return category
        except Category.DoesNotExist:
            return None

    def get(self, request, category_id):
        category = self.get_object(category_id)
        if category is not None:
            if category.products:
                products = ProductSerializer(category.products, many=True)
                return Response(products.data)
        return Response(None, status.HTTP_404_NOT_FOUND)



class OrdersView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        products = Order.objects.all()
        serialized_order = OrderSerializer(products, many=True)
        return Response(serialized_order.data)


class OrderSingleView(APIView):
    permission_classes = (IsAuthorOrReadOnly,)
    def get_object(self, id):
        try:
            order = Order.objects.get(id=id)
            return order
        except Order.DoesNotExist:
            return None

    def get(self, request, id):
        order = self.get_object(id)
        serialized_order = OrderSerializer(order)
        return Response(serialized_order.data)

    def put(self, request, id):
        order = self.get_object(id)
        if order is not None:
            serialized_order = OrderSerializer(instance=order, data=request.data)
            if serialized_order.is_valid():
                serialized_order.save()
                return Response(serialized_order.data)
        return Response(None, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        order = self.get_object(id)
        if order is not None:
            order.delete()
            return Response(None, status.HTTP_204_NO_CONTENT)
        return Response(None, status.HTTP_400_BAD_REQUEST)


class OrderCreateView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)
