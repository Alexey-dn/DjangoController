from django.urls import path

from .views import IndexView
from .views import (
    ProductCreate, ProductDelete, ProductDetail, ProductSearch, ProductsList,
    ProductUpdate, subscriptions
)


urlpatterns = [
    path('', ProductsList.as_view(), name='product_list'),
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('<int:pk>', ProductDetail.as_view(), name='product_detail'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('create/', ProductCreate.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('search/', ProductSearch.as_view(), name='product_search'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('index/', IndexView.as_view()),
]
