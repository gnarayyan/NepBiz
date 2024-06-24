from django.urls import path, include
from .views import product, product_list, filter_products
urlpatterns = [
    path('products/', product_list, name='products'),
    path('product/<int:id>', product, name='product'),

    path('products/filter/', filter_products, name='filter_products'),




]
