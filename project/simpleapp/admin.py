from django.contrib import admin
from .models import Category, Product


admin.site.register(Category)  # Не забываем зарегистрировать модели, иначе мы не увидим их в админке.
admin.site.register(Product)
