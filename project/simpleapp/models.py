from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy   # импортируем «ленивый» геттекст с подсказкой


class Product(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,  # названия товаров не должны повторяться
        verbose_name=gettext_lazy('Product name'),
        help_text=gettext_lazy('Enter a name of the product'),
    )
    description = models.TextField(
        verbose_name=gettext_lazy('Description'),
        help_text=gettext_lazy('Describe the product'),
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0, gettext_lazy('Quantity should be >= 0'))],
        verbose_name=gettext_lazy('Quantity'),
        help_text=gettext_lazy('Quantity should be >= 0'),
    )
    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='products',  # все продукты в категории будут доступны через поле products
        verbose_name=gettext_lazy('Category'),
        help_text=gettext_lazy('Choose a category name'),
    )
    price = models.FloatField(
        validators=[MinValueValidator(0.0, gettext_lazy('Price should be >= 0.0'))],
        # verbose_name='Цена',
        verbose_name=gettext_lazy('Price'),
        help_text=gettext_lazy('Price should be >= 0.0'),
    )

    # допишем свойство, которое будет отображать есть ли товар на складе
    @property
    def on_stock(self):
        return self.quantity > 0

    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}: {self.quantity}'  # title() метод делающий первую букву заглавной

    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с товаром
        return reverse('product_detail', args=[str(self.id)])  # f'/products/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    class Meta:  # Возвращает название категории во множественном или единственном числе в админпанеле
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(
        max_length=100,
        unique=True,
        # verbose_name='Категория'
        verbose_name=gettext_lazy('Category'),
        help_text=gettext_lazy('Category name'),
    )

    def __str__(self):
        return f'{self.name.title()}'

    class Meta:  # Возвращает название категории во множественном или единственном числе в админпанеле
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
