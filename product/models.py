from django.db import models
from django.contrib.auth.models import User
from home.models import Product
# Create your models here.


class ReviewModel(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    rating = models.SmallIntegerField()
    added_on = models.DateTimeField(auto_now_add=True)
    review = models.CharField(max_length=255)
    product = models.ForeignKey(Product, models.CASCADE)

    def __str__(self):
        return self.review

    def get_rating(self):
        return (5-self.rating) * '<span class="fa fa-star"></span>' + self.rating*'<span class="fa fa-star checked"></span>'
