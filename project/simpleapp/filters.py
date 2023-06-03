from django_filters import FilterSet, ModelChoiceFilter, CharFilter, NumberFilter
from .models import Category
from django.utils.translation import gettext_lazy


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class ProductFilter(FilterSet):
    name = CharFilter(
        lookup_expr='icontains',
        field_name='name',
        label=gettext_lazy('Product name'),
    )

    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label=gettext_lazy('Category'),
        empty_label=gettext_lazy('Any'),
    )

    price = NumberFilter(
        field_name='price',
        label=gettext_lazy('Price'),
    )

    price__gt = NumberFilter(
        field_name='price',
        lookup_expr='gt',
        label=gettext_lazy('Price bigger then'),
    )

    price__lt = NumberFilter(
        field_name='price',
        lookup_expr='lt',
        label=gettext_lazy('Price lower then'),
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
