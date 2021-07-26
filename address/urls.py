from address.views import AddressViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register(r'', AddressViewSet, basename="address")


urlpatterns = [
    path('', include(router.urls))
]
