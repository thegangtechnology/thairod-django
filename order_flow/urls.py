from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CreateOrderFlowsAPI, OrderFlowsHashAPI, CheckoutDoctorOrderAPI, PatientConfirmationAPI


router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('order-flows/create-flow/', CreateOrderFlowsAPI.as_view()),
    path('order-flows/hash/', OrderFlowsHashAPI.as_view(), name='order-flows-hash'),
    path('order-flows/doctor-checkout/', CheckoutDoctorOrderAPI.as_view()),
    path('order-flows/patient-checkout/', PatientConfirmationAPI.as_view())
]
