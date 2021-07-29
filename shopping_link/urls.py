from rest_framework.routers import DefaultRouter
from django.urls import path, include
from shopping_link.views import ShoppingLinkViewSet


router = DefaultRouter()
router.register(r'shopping_links', ShoppingLinkViewSet, basename="shopping-link")


urlpatterns = [
    path('', include(router.urls))
]
