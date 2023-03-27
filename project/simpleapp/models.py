from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


# Товар для нашей витрины
class Product(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,  # названия товаров не должны повторяться
        verbose_name='Название',
    )
    description = models.TextField(verbose_name='Описание')
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Количество',
    )
    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='products',  # все продукты в категории будут доступны через поле products
        verbose_name='Категория'
    )
    price = models.FloatField(
        validators=[MinValueValidator(0.0)],
        verbose_name='Цена',
    )

    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'  #title() метод делающий первую букву заглавной

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    class Meta:  #  Возвращает название категории во множественном или единственном числе в админпанеле
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True, verbose_name='Категория')

    def __str__(self):
        return f'{self.name.title()}'

    class Meta:  #  Возвращает название категории во множественном или единственном числе в админпанеле
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
