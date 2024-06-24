from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone
from django.utils import timezone
from home.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qunatity = models.PositiveIntegerField(default=0)
    isClear = models.BooleanField(default=False)

    def total_price(self):
        return self.qunatity * self.product.price

    def increment(self):
        self.qunatity += 1
        self.save()

    def decrement(self):
        if self.qunatity > 2:
            self.qunatity -= 1
            self.save()

    def clear_cart(self):
        self.isClear = True
        self.save()


# Order tracking system
METHOD = (
    ('cash on delivery', 'cash on delivery'),
    ('esewa', 'esewa'),
)
ORDER_STATUS = [
    ('PL', 'Placed'),
    ('SH', 'Shipped'),
    ('DL', 'Delivered'),
]


class Order(models.Model):
    # cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    total = models.PositiveIntegerField(default=True)
    order_status = models.CharField(
        max_length=50, choices=ORDER_STATUS, default=True)
    created_at = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="esewa")
    payment_completed = models.BooleanField(default=False)

    def __str__(self):
        return "Order: " + str(self.id)


class contact(models.Model):
    name = models.CharField(max_length=32)
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True)
    subject = models.CharField(max_length=500)

    def __str__(self):
        return self.name
