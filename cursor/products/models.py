from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, default="slug")
    parent = models.ForeignKey("Category", null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    @property
    def subcategories(self):
        return self.category_set.all()

    @property
    def products(self):
        return self.product_set.filter(is_active=True)


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(null=False)
    discount_price = models.IntegerField(null=True, blank=True)
    show_on_main_page = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    category = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def main_image(self):
        return ProductImage.objects.filter(Q(product_id=self.id) & Q(is_main=True)).first().image
    @property
    def all_images(self):
        return ProductImage.objects.filter(product_id=self.id).values_list('image', flat=True).order_by('-is_main')

    def __str__(self):
        return str(self.id) + " " + self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="uploads/products/")
    is_main = models.BooleanField(default=False)

    class Meta:
        unique_together = ('product', 'is_main')  # можливо створити тільки 2 зображення.

    # class Meta:
    #     constraints = [
    #         UniqueConstraint(fields=['product', 'is_main'], condition=models.Q(is_main=True), name='unique_main_image'),
    #     ]

    def __str__(self):
        return str(self.product.id) + " " + self.product.title + "|" + str(self.id)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE, related_name="childs")
    text = models.TextField()

    @property
    def child_comments(self):
        return self.childs.all()

    def __str__(self):
        return self.text


class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    total_price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return str(self.id) + " " + self.address


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return str(self.order.id) + " " + self.product.title
