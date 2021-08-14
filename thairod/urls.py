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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from thairod.settings import DEBUG
from thairod.views.async_test import AsyncView
from thairod.views.dashboard_api import DashboardAPI
from thairod.views.ipcheck import IPCheckView
from thairod.views.ordered_non_repeatable import DidOrderNonRepeatableAPI
from thairod.views.quick_snapshot_api import QuickSnapshotView
from thairod.views.stock_api import StockAPI

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
    path('api/', include('order_flow.urls')),
    path('api/', include('address.urls')),
    path('api/', include('order.urls')),
    path('api/', include('product.urls')),
    path('api/', include('shipment.urls')),
    path('api/', include('stock_adjustment.urls')),
    path('api/', include('warehouse.urls')),
    path('api/', include('user.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ping/', IPCheckView.as_view(), name='ip-check'),
    path('async/', AsyncView.as_view(), name='async'),
    path('api/stock/', StockAPI.as_view(), name='get-stock'),
    path('api/dashboard/', DashboardAPI.as_view(), name='dashboard'),
    path('api/did-order-non-repeatable/', DidOrderNonRepeatableAPI.as_view(), name='did-order-non-repeatable'),
    path('api/quick-snapshot/', QuickSnapshotView.as_view(), name='quick-snapshot')
]

if DEBUG:
    urlpatterns += [
        re_path(r'^docs/open_api(?P<format>\.json|\.yaml)$',
                schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^docs/open_api/$', schema_view.with_ui('swagger',
                                                         cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^docs/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
