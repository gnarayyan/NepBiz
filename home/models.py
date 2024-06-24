from django.db import models
from django.utils.translation import gettext_lazy as _
from .validator import validate_positive
import decimal


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="brand/", null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category/", null=True, blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="activity/", null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class GenderChoice(models.IntegerChoices):
        MEN = 0, _("Men")
        WOMEN = 1, _("Women")
        BOTH = 2, _("Both")
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1024, null=True, blank=True)
    category = models.CharField(max_length=50,  null=True, blank=True)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[validate_positive])
    gender = models.PositiveSmallIntegerField(
        choices=GenderChoice, default=GenderChoice.BOTH)  # 'men' or 'women'
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[validate_positive])
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to="product/", default='fallback.jpg')
    image2 = models.ImageField(upload_to="product/", null=True, blank=True)
    image3 = models.ImageField(upload_to="product/", null=True, blank=True)

    def __str__(self):
        return self.name

    def discountedPrice(self):
        return self.price - (self.price*self.discount/decimal.Decimal(100.0))


class FeatureProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.product.name
