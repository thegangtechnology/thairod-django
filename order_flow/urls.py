from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from .views import CreateOrderFlowsAPI, OrderFlowsHashAPI, CheckoutDoctorOrderAPI, PatientConfirmationAPI


router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('order-flows/create-flow/', csrf_exempt(CreateOrderFlowsAPI.as_view())),
    path('order-flows/hash/', csrf_exempt(OrderFlowsHashAPI.as_view())),
    path('order-flows/doctor-checkout/', csrf_exempt(CheckoutDoctorOrderAPI.as_view())),
    path('order-flows/patient-checkout/', csrf_exempt(PatientConfirmationAPI.as_view()))
]
