from django.contrib import admin

from .models import Category, Product


# создаём новый класс для представления товаров в админке
class ProductAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Product._meta.get_fields()]
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # генерируем список имён всех полей для более красивого отображения
    list_display = ('name', 'price', 'on_stock')  # если нужны не все поля, оставляем только необходимые


admin.site.register(Category)  # Не забываем зарегистрировать модели, иначе мы не увидим их в админке.
admin.site.register(Product, ProductAdmin)
# admin.site.unregister(Product) # для разрегистрации модели
