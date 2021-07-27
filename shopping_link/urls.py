from rest_framework.routers import DefaultRouter
from django.urls import path, include
from shopping_link.views import ShoppingLinkViewSet


router = DefaultRouter()
router.register(r'shopping-link', ShoppingLinkViewSet, basename="procurement")


urlpatterns = [
    path('', include(router.urls))
]
