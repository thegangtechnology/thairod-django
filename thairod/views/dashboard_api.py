from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from thairod.services.dashboard.dashboard_service import DashboardService, DashboardSummary
from thairod.utils import tzaware
from thairod.utils.auto_serialize import swagger_auto_serialize_get_schema


class DashboardAPI(APIView):

    @swagger_auto_serialize_get_schema(
        None, DashboardSummary
    )
    def get(self, request: Request):
        anchor = tzaware.now()
        return DashboardService().get_dashboard_summary(anchor).to_response()
