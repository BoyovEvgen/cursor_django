from django.db import models
from django.db.models import Q


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, default="slug")
    parent = models.ForeignKey("Category", null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    # @property
    # def category_tree(self):
    #     tree = {'category': self, 'children': []}
    #     childs = self.category_set.all()
    #     for child in childs:
    #         tree['children'].append(child.category_tree)
    #     return tree


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(null=False)
    discount_price = models.IntegerField(null=True, blank=True)
    show_on_main_page = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    category = models.ManyToManyField(Category)

    @property
    def main_image(self):
        return ProductImage.objects.filter(Q(product_id=self.id) & Q(is_main=True)).first().image

    def __str__(self):
        return str(self.id) + " " + self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/products/")
    is_main = models.BooleanField(default=False)

    class Meta:
        unique_together = ('product', 'is_main')

    def __str__(self):
        return str(self.product.id) + " " + self.product.title + "|" + str(self.id)

