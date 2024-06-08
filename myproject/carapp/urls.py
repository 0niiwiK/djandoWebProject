from django.urls import path
from .views import add_car_api

urlpatterns = [
    path('api/add_car/', add_car_api, name='add_car_api'),
]
