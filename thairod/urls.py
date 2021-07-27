"""thairod URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Thairod Mall API",
      default_version='v1',
      description="",
      terms_of_service="",
      contact=openapi.Contact(email="k.ronnakrit@thegang.tech"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('procurement.urls')),
    path('api/address/', include('address.urls')),
    path('api/order/', include('order.urls')),
    path('api/product/', include('product.urls')),
    path('api/shipment/', include('shipment.urls')),
    path('api/stock_adjustment/', include('stock_adjustment.urls')),
    path('api/warehouse/', include('warehouse.urls')),
    path('api/user/', include('user.urls')),

    re_path(r'^docs/open_api(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/open_api/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^docs/redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),

]
