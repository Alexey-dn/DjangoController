from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache  # импортируем наш кэш
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .filters import ProductFilter
from .forms import ProductForm
from .models import Category, Subscription
from .models import Product
from .tasks import hello, printer


class ProductsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Product
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    # queryset = Product.objects.filter(price_lt=300).order_by('name')
    # Если хотим, чтобы сортировка шла по товарам ценой меньше
    # 300, то вместо параметра ordering and name указываем этот
    template_name = 'products.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'
    # 'products' должно строго соответствовать {{ products }} в products.html
    paginate_by = 3  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ProductFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        # context['time_now'] = datetime.utcnow() уже не нужна, дата добавлена в теги.
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = "Распродажа в среду!"
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product.html
    template_name = 'product.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'product'
    queryset = Product.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


# Добавляем новое представление для создания товаров.
class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_product',)
    form_class = ProductForm
    # модель товаров
    model = Product
    # и новый шаблон, в котором используется форма.
    template_name = 'product_edit.html'


class ProductSearch(ListView):
    model = Product
    template_name = 'product_search.html'
    context_object_name = 'search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)

        if not self.request.GET:
            return queryset.none()

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #     # К словарю добавим текущую дату в ключ 'time_now'.
        #     context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context

# def create_product(request):
#     form = ProductForm()
#
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/products/')
#     return render(request, 'product_edit.html', {'form': form})

# def multiply(request):
#     number = request.GET.get('number')
#     multiplier = request.GET.get('multiplier')
#
#     try:
#         result = int(number) * int(multiplier)
#         html = f"<html><body>{number}*{multiplier}={result}</body></html>"
#     except (ValueError, TypeError):
#         html = f"<html><body>Invalid input.</body></html>"
#
#     return HttpResponse(html)


# Добавляем представление для изменения товара.
class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_product',)
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


# Представление удаляющее товар.
class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_product',)
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class IndexView(View):
    def get(self, request):
        printer.apply_async([10], eta=datetime.now() + timedelta(seconds=5))
        hello.delay()
        return HttpResponse('Hello!')
