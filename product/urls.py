from django.urls import path, include
from .views import add_review


urlpatterns = [
    path('add_review/', add_review, name='add_review'),




]
