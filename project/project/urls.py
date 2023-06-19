from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers
from simpleapp import views

"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


router = routers.DefaultRouter()
router.register(r'products', views.ProductViewset)
router.register(r'category', views.CategoryViewset)



urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # подключаем встроенные эндопинты для работы с локализацией
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/", include("allauth.urls")),  # Важен порядок с предыдущим путем
    # path('pages/', include('django.contrib.flatpages.urls')),
   # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
   # подключались к главному приложению с префиксом products/.
    path('products/', include('simpleapp.urls')),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    # path('', include(router.urls)),
    path('api/', include(router.urls), name='api'),
]
