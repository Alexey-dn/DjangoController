from django_filters import FilterSet, ModelChoiceFilter, CharFilter, NumberFilter
from .models import Product, Category


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class ProductFilter(FilterSet):
    name = CharFilter(
        lookup_expr='icontains',
        field_name='name',
        label='Название товара',
    )

    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Любая',
    )

    price = NumberFilter(
        field_name='price',
        label='Цена',
    )

    price__gt = NumberFilter(
        field_name='price',
        lookup_expr='gt',
        label='Цена выше чем',
    )

    price__lt = NumberFilter(
        field_name='price',
        lookup_expr='lt',
        label='Цена ниже чем',
    )



    # class Meta:
    #     # В Meta классе мы должны указать Django модель,
    #     # в которой будем фильтровать записи.
    #     model = Product
    #     # В fields мы описываем по каким полям модели
    #     # будет производиться фильтрация.
    #     fields = {
    #         # поиск по названию
    #         'name': ['icontains'],
    #         # количество товаров должно быть больше или равно
    #         'quantity': ['gt'],
    #         'price': [
    #             'lt',  # цена должна быть меньше или равна указанной
    #             'gt',  # цена должна быть больше или равна указанной
    #         ],
    #     }
