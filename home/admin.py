from django.contrib import admin
from .models import Brand, Category, Activity, Product, FeatureProduct


# Register your models here.
admin.site.register(Activity)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(FeatureProduct)
admin.site.register(Product)
